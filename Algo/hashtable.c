/*
 * hashmap_str_int.c —— string key -> int value 专用哈希表（非泛型）
 * 编译：gcc -std=c11 -Wall -Wextra -Wpedantic -o hashmap_str_int hashmap_str_int.c
 * 不含任何具体题目逻辑；末尾 main() 仅用于自测，可整段删除。
 */
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>

typedef enum {
    HM_ERR_NOMEM = -1,   /* put：分配失败 */
    HM_MISS      =  0,   /* get/remove：键不存在 */
    HM_HIT       =  1,   /* get 命中 / remove 删到 / put 覆盖了旧值 */
    HM_NEW       =  2    /* put：新建了节点 */
} HmStatus;

typedef struct HashNode {
    char *key;                 /* 表自己复制一份并拥有，调用方不必保留原串 */
    int value;                 /* 值直接存 int，不是 void* */
    struct HashNode *next;
} HashNode;

typedef struct HashMap {
    HashNode **buckets;        /* 桶数组，链地址法 */
    size_t cap;                /* 桶数，create 时保证 > 0 */
    size_t size;               /* 当前键值对数；本版不扩容 */
} HashMap;

HashMap *hashmap_create(size_t cap);
HmStatus hashmap_put(HashMap *m, const char *key, int value);
HmStatus hashmap_get(const HashMap *m, const char *key, int *out);
HmStatus hashmap_remove(HashMap *m, const char *key);
size_t   hashmap_size(const HashMap *m);
void     hashmap_free(HashMap *m);

static char *dup_key(const char *s) {
    size_t n = strlen(s) + 1;
    char *p = (char *)malloc(n);
    if (p) memcpy(p, s, n);
    return p;
}

static size_t str_hash(const char *key) {
    const unsigned char *p = (const unsigned char *)key;
    size_t h = 5381;
    while (*p) h = h * 33 + *p++;
    return h;                       /* 返回完整哈希值，取模交给表内 */
}

static size_t bucket_of(const HashMap *m, const char *key) {
    return str_hash(key) % m->cap;
}

/* 一次查找：put 查重、get、remove 共用；prev_out 供 remove 断链 */
static HashNode *find_node(const HashMap *m, const char *key, HashNode **prev_out) {
    HashNode *prev = NULL;
    HashNode *cur  = m->buckets[bucket_of(m, key)];
    while (cur) {
        if (strcmp(cur->key, key) == 0) {   /* 内容判等，不用单独写 eq 函数 */
            if (prev_out) *prev_out = prev;
            return cur;
        }
        prev = cur;
        cur  = cur->next;
    }
    return NULL;
}

/* ---- 实现 ---- */
HashMap *hashmap_create(size_t cap) {
    if (cap == 0) return NULL;
    HashMap *m = (HashMap *)malloc(sizeof *m);
    if (!m) return NULL;
    m->buckets = (HashNode **)calloc(cap, sizeof *m->buckets);
    if (!m->buckets) { free(m); return NULL; }
    m->cap  = cap;
    m->size = 0;
    return m;
}

HmStatus hashmap_put(HashMap *m, const char *key, int value) {
    HashNode *node = find_node(m, key, NULL);   /* 先查重：唯一键语义 */
    if (node) {
        node->value = value;                    /* 覆盖；表内原有的 key 副本继续用 */
        return HM_HIT;                          /* 没有复制新 key，因此没有任何东西要释放 */
    }

    char *copy = dup_key(key);                  /* 表复制键，接管所有权 */
    if (!copy) return HM_ERR_NOMEM;
    node = (HashNode *)malloc(sizeof *node);
    if (!node) { free(copy); return HM_ERR_NOMEM; }
    node->key   = copy;
    node->value = value;

    size_t i = bucket_of(m, key);
    node->next = m->buckets[i];                 /* 头插：O(1)，不遍历 */
    m->buckets[i] = node;
    m->size++;
    return HM_NEW;
}

HmStatus hashmap_get(const HashMap *m, const char *key, int *out) {
    HashNode *node = find_node(m, key, NULL);
    if (!node) return HM_MISS;                  /* 未找到时 *out 保持原值 */
    if (out) *out = node->value;                /* out 传 NULL 即「只问存在性」 */
    return HM_HIT;
}

HmStatus hashmap_remove(HashMap *m, const char *key) {
    size_t i = bucket_of(m, key);
    HashNode *prev = NULL;
    HashNode *node = find_node(m, key, &prev);
    if (!node) return HM_MISS;
    if (prev) prev->next = node->next;
    else      m->buckets[i] = node->next;
    free(node->key);                            /* 释放表自己那份副本 */
    free(node);
    m->size--;
    return HM_HIT;
}

size_t hashmap_size(const HashMap *m) {
    return m ? m->size : 0;
}

void hashmap_free(HashMap *m) {
    if (!m) return;
    for (size_t i = 0; i < m->cap; i++) {
        HashNode *cur = m->buckets[i];
        while (cur) {
            HashNode *next = cur->next;
            free(cur->key);
            free(cur);
            cur = next;
        }
    }
    free(m->buckets);
    free(m);
}

/* ============================================================
 * 极短自测，接入自己的代码时可整段删除
 * ============================================================ */
int main(void) {
    HashMap *m = hashmap_create(8);
    if (!m) return 1;

    printf("put alice -> %d (2=新建)\n", hashmap_put(m, "alice", 18));
    printf("put bob   -> %d (2=新建)\n", hashmap_put(m, "bob", 25));

    /* 栈上的键：插入后立刻改写缓冲区，验证表确实复制了键 */
    char buf[16] = "carol";
    hashmap_put(m, buf, 32);
    strcpy(buf, "XXXXX");
    int v = -1;
    HmStatus s = hashmap_get(m, "carol", &v);   /* 分开写，别塞进 printf 参数 */
    printf("get carol -> status=%d value=%d (原缓冲区已被改写)\n", s, v);

    v = 777;                                    /* 故意给个非零初值 */
    s = hashmap_get(m, "nobody", &v);
    printf("get nobody -> status=%d, v 仍为 %d (未找到不改 out)\n", s, v);

    printf("contains bob (out=NULL) -> %d\n", hashmap_get(m, "bob", NULL));
    printf("put alice again -> %d (1=覆盖)\n", hashmap_put(m, "alice", 99));
    printf("remove alice -> %d (1=删到)\n", hashmap_remove(m, "alice"));
    printf("remove alice -> %d (0=已无)\n", hashmap_remove(m, "alice"));
    printf("size -> %zu\n", hashmap_size(m));

    hashmap_free(m);                            /* 剩余节点的 key 副本在这里释放 */
    puts("hashmap_free done");
    return 0;
}

