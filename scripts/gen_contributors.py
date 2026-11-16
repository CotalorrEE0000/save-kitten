#!/usr/bin/env python3
"""从 AtomGit 贡献者 API 生成 CONTRIBUTORS.md 的自动区块。

仅用标准库，方便在任何 runner 上跑，也方便 P1–P4 各仓库直接复用。

接口：GET https://api.atomgit.com/api/v5/repos/{owner}/{repo}/contributors
      query: type=committers|authors（可选）、access_token=<token>（可选，匿名可省）
      返回: [{"name": "...", "contributions": 3, "email": "..."}]

令牌怎么传
----------
平台把这个接口的用户令牌定义在 *query* 的 access_token 上（不是 Bearer header）。
脚本从环境变量 ATOMGIT_TOKEN 读取，绝不把拼好的 URL 打印出来——URL 里含令牌。

本地等价的 curl 写法（-G + --data-urlencode 让令牌不出现在命令行/日志里）：

  # 匿名（公开仓库够用）
  curl -fsS -G 'https://api.atomgit.com/api/v5/repos/<owner>/<repo>/contributors' \
       -H 'Accept: application/json'

  # 带令牌（私有仓库 / 需要认证时）
  curl -fsS -G 'https://api.atomgit.com/api/v5/repos/<owner>/<repo>/contributors' \
       -H 'Accept: application/json' \
       --data-urlencode 'type=committers' \
       --data-urlencode "access_token=$ATOMGIT_TOKEN"

限流
----
接口文档只声明 429 = 请求过于频繁，**没有给额度，也没有说令牌能提额**。
所以遇到 429 的正解是退避重试，不是赶紧加 token。
脚本对 429 / 5xx 自动重试（默认 3 次，指数退避 2/4/8s，尊重 Retry-After），
可用 --retries 调整；CI 里没人手动点重试，这一步尤其必要。

三种模式
--------
  无参数          打印生成的区块到 stdout，不改文件
  --write         把区块写回 CONTRIBUTORS.md（人工维护的部分原样保留）
  --check         与文件现状比对，不一致就 exit 2 并打印 diff（给 CI 用）

环境变量：ATOMGIT_OWNER / ATOMGIT_REPO / CONTRIBUTOR_TYPE / ATOMGIT_TOKEN
"""

import argparse
import difflib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.atomgit.com/api/v5/repos/{owner}/{repo}/contributors"
BEGIN = "<!-- BEGIN:auto-contributors -->"
END = "<!-- END:auto-contributors -->"
RETRYABLE = {429, 500, 502, 503, 504}
RETRY_BASE = 2
HINTS = {401: "令牌无效或缺少凭证", 403: "禁止访问，检查仓库可见性与令牌权限",
         404: "owner/repo 路径不存在", 429: "触发限流", 500: "服务端错误"}


def retry_after_seconds(exc, attempt):
    """优先读 Retry-After（整数秒），否则指数退避；上限 60s 防止 CI 挂太久。"""
    headers = getattr(exc, "headers", None)
    raw = headers.get("Retry-After") if headers else None
    if raw:
        try:
            return max(0, min(int(raw.strip()), 60))
        except (TypeError, ValueError):
            pass  # HTTP-date 形式就退回指数退避
    return min(RETRY_BASE * (2 ** attempt), 60)


def fetch(owner, repo, ctype, token, timeout=15, retries=3):
    params = {}
    if ctype:
        params["type"] = ctype
    if token:
        params["access_token"] = token

    url = API.format(owner=urllib.parse.quote(owner, safe=""),
                     repo=urllib.parse.quote(repo, safe=""))
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json",
                 "User-Agent": "save-kitten-contributors/1.0"},
    )

    raw = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
            break
        except urllib.error.HTTPError as exc:
            # 只报状态码，绝不回显 URL（里面可能有 access_token）
            hint = HINTS.get(exc.code, "请求失败")
            if exc.code in RETRYABLE and attempt < retries:
                wait = retry_after_seconds(exc, attempt)
                print(f"[gen_contributors] HTTP {exc.code}（{hint}），"
                      f"{wait}s 后重试 {attempt + 1}/{retries}", file=sys.stderr)
                time.sleep(wait)
                continue
            print(f"[gen_contributors] HTTP {exc.code}: {hint}", file=sys.stderr)
            if exc.code == 429:
                print("[gen_contributors] 限流未退，等几分钟再跑；"
                      "也可以 --retries 5 拉长退避", file=sys.stderr)
            sys.exit(3)
        except urllib.error.URLError as exc:
            if attempt < retries:
                wait = min(RETRY_BASE * (2 ** attempt), 60)
                print(f"[gen_contributors] 网络错误（{exc.reason}），"
                      f"{wait}s 后重试 {attempt + 1}/{retries}", file=sys.stderr)
                time.sleep(wait)
                continue
            print(f"[gen_contributors] 网络错误: {exc.reason}", file=sys.stderr)
            sys.exit(3)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("[gen_contributors] 响应不是合法 JSON", file=sys.stderr)
        sys.exit(3)
    if not isinstance(data, list):
        print("[gen_contributors] 响应不是数组，可能是错误响应体", file=sys.stderr)
        sys.exit(3)
    return data


def mask_email(email):
    """默认脱敏：API 会返回邮箱，但公开名单里不宜直接摊开。"""
    email = (email or "").strip()
    if "@" not in email:
        return "—"
    local, domain = email.rsplit("@", 1)
    if not local:
        return f"***@{domain}"
    return f"{local[0]}***@{domain}"


def render(data, show_email=False):
    rows = sorted(
        data,
        key=lambda d: (-int(d.get("contributions") or 0),
                       str(d.get("name") or "").lower()),
    )
    lines = [
        BEGIN,
        "",
        "| 贡献者 | 提交数 | 邮箱 |",
        "|:---|---:|:---|",
    ]
    if not rows:
        lines.append("| _暂无 API 记录_ | — | — |")
    for item in rows:
        name = str(item.get("name") or "(unknown)").replace("|", "\\|")
        count = int(item.get("contributions") or 0)
        email = str(item.get("email") or "")
        shown = email if show_email else mask_email(email)
        lines.append(f"| `{name}` | {count} | {shown} |")
    lines += ["", END]
    return "\n".join(lines)


def replace_block(text, block):
    if BEGIN not in text or END not in text:
        return None
    prefix, rest = text.split(BEGIN, 1)
    _, suffix = rest.split(END, 1)
    return prefix + block + suffix


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--owner", default=os.environ.get("ATOMGIT_OWNER", ""))
    ap.add_argument("--repo", default=os.environ.get("ATOMGIT_REPO", ""))
    ap.add_argument("--type", dest="ctype",
                    default=os.environ.get("CONTRIBUTOR_TYPE", "committers"),
                    choices=["committers", "authors", ""])
    ap.add_argument("--token", default=os.environ.get("ATOMGIT_TOKEN", ""))
    ap.add_argument("--file", default="CONTRIBUTORS.md")
    ap.add_argument("--show-email", action="store_true", help="关闭邮箱脱敏")
    ap.add_argument("--check", action="store_true", help="只校验，不写文件")
    ap.add_argument("--write", action="store_true", help="写回文件")
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--retries", type=int, default=int(os.environ.get("ATOMGIT_RETRIES", "3")),
                    help="429 / 5xx 的重试次数，默认 3")
    args = ap.parse_args()

    if not args.owner or not args.repo:
        print("[gen_contributors] 缺 --owner/--repo（或 ATOMGIT_OWNER/ATOMGIT_REPO）",
              file=sys.stderr)
        sys.exit(1)

    data = fetch(args.owner, args.repo, args.ctype, args.token,
                 args.timeout, max(0, args.retries))
    block = render(data, args.show_email)

    if not (args.check or args.write):
        print(block)
        return

    try:
        with open(args.file, encoding="utf-8") as fh:
            current = fh.read()
    except FileNotFoundError:
        print(f"[gen_contributors] 找不到 {args.file}", file=sys.stderr)
        sys.exit(2)

    updated = replace_block(current, block)
    if updated is None:
        print(f"[gen_contributors] {args.file} 缺少 {BEGIN} / {END} 标记",
              file=sys.stderr)
        sys.exit(2)

    if args.check:
        if updated == current:
            print(f"[gen_contributors] OK · {len(data)} 位贡献者，名单已是最新")
            return
        diff = difflib.unified_diff(
            current.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile=f"{args.file} (current)",
            tofile=f"{args.file} (API)",
        )
        sys.stdout.writelines(diff)
        print("[gen_contributors] 名单与 API 不一致；本地跑 "
              "`python3 scripts/gen_contributors.py --write` 后提交", file=sys.stderr)
        sys.exit(2)

    with open(args.file, "w", encoding="utf-8") as fh:
        fh.write(updated)
    print(f"[gen_contributors] 已更新 {args.file} · {len(data)} 位贡献者")


if __name__ == "__main__":
    main()
