# Bytes, Byte Order, and Storage

## 1. Before You Start: What a File Really Holds

> The last lesson ended with a clean submission: one file, one path, and a list you could prove. It also said that bytes, hexadecimal and format rules would come next. So before we go any further, ask the simpler question that the submission never answered: what is actually inside the file you just handed in?
>
> Most computer fundamentals courses will tell you the same thing: almost everything on a computer is stored in binary. One bit is one binary place, either 0 or 1. Because of how MOS transistors are built into circuits, and because that was a convenient size to make and to use, eight bits became the working group, one byte. Eight bits give 2⁸ = 256 states, which is why a byte runs from 0 to 255, written in hexadecimal as `00` to `FF`. One hex digit holds four bits, so one byte is always two hex characters. Binary is too long to read comfortably, and decimal does not line up with the bit boundaries; hexadecimal sits exactly on them. After 9 we borrow six more symbols, A to F, with `A` = 10 and `F` = 15, so `FF` is 15×16 + 15 = 255. Hex numbers are written with a `0x` prefix in source code, but the prefix is not stored anywhere in the file: `0x68` is 104, which is the letter `h`, and `0xFF` is 255, which is still one byte, not 255 bytes. It is worth pausing on that, because the two numbers 0–127 and 0–255 are often mixed up. A byte holds 256 values; a table drawn up early on, ASCII, only used 128 of them, 0 to 127, mapping control characters, letters and digits to numbers. The table is smaller than the box it sits in, and the upper half was left free for later use. Who drew it up and in which year is a detail for the history books; what matters here is that people agreed on one table, and that Chinese characters are not on it.
>
> We will take a plain `.txt` file as our example. Seen from another programming language, a txt file is just a string saved as a file: no header, no footer, nothing that says where it begins or where it ends. If you line it up as a row of numbered boxes, the byte at offset 0 is the beginning of the file, the byte at offset 1 is the next one, and that is the whole structure. Strictly speaking the file holds no characters at all, only bytes; the characters are what you get after someone agrees how to decode them. A file contains no characters, only bytes; you can read words on the screen because a decoding rule was agreed on.
>
> To see those bytes you need a tool that prints them rather than interpreting them, and `od` is the one we will use. Its name says octal dump, which is a historical leftover, because with the options below it prints hexadecimal. The command in the block is worth taking apart before you run it, since a manual lists the options one by one and rarely says what they do when combined. `-A` chooses how the address column on the left is displayed, and `n` means none, so `-An` removes that column entirely. `-t` chooses the output type, `x` means hexadecimal, and the digit after it says how many bytes are read as one number: `x1` is one byte per number, `x2` is two bytes per number, `x4` is four. So `-An -tx1` together means simply "no addresses, and one hex number for each single byte". Without `-An`, the same command prints a leading `0000000` and a trailing `0000004`, which are offsets, not data.
>
> ```bash
> printf 'A' | od -An -tx1        # 41
> printf '\xff' | od -An -tx1     # ff
> printf 'ABCD' | od -An -tx1     # 41 42 43 44
> printf 'ABCD' | od -An -tx2     # 4241 4443
> printf 'ABCD' | od -x          # 0000000 4241 4443
>                               # 0000004
> ```
>
> That fourth line is the interesting one. Change a single character, `x1` to `x2`, and `41 42 43 44` turns into `4241 4443`. Nothing in the file changed; you only told the tool to read two bytes at a time as one 16-bit number, and on this machine the low byte comes first, so `41 42` is shown as `0x4241`. The plain `od -x` on the last line does the same thing by default, two bytes at a time, which is exactly why we do not use it to look at individual bytes in this lesson. Keep that reversed pair in mind. It will come back in the next section, and it is the whole subject of this lesson in miniature: the bytes are innocent, and the disagreement is always about the rule used to read them.
>
> `xxd` gives you the same bytes with a little more company. Its `-g` option sets how many bytes are grouped together; the default is two, so `xxd` on `ABCD` prints `4142 4344`, while `xxd -g1` prints `41 42 43 44`. On the left is the offset, and on the right is the character the tool decoded for you, a convenience for a human reader rather than a third kind of data. Memory is like this too: one long row of boxes, one byte each, every box with its own number. A file is the same row of boxes seen from the outside, and the difference between a `.md`, a `.png` and an `.exe` is only the agreement about how those boxes are arranged.
>
> ```bash
> printf 'ABCD' | xxd -g1         # 00000000: 41 42 43 44    ABCD
> printf 'ABCD' | xxd -g2         # 00000000: 4142 4344       ABCD
> ```
>
> So: what is the largest number one byte can hold, what is `0x1F` in decimal, and which byte sits at offset 2 of `41 42 43 44`? If you can answer those without running anything, the tools above have done their job.

> 上一讲收在一份干净的提交上：一个文件、一条路径、一份能证明自己的清单。那一讲末尾也说过，这一关过了才轮到字节、十六进制和格式规范。那么在往下走之前，先问一个当时没回答的问题：你交上去的那个文件里，到底装着什么？
>
> 正如我们大多数计算机基础课程告诉你的那样，计算机上几乎所有的东西都以二进制方式存储。一个比特就是二进制的一位，取 0 或 1；由于 MOS 管的生产和电路结构，加上这样一组做起来、用起来都方便，8 位成了实际的一组，也就是 1 字节。8 位能表示 2⁸ = 256 种状态，所以一个字节的范围是 0 到 255，写成十六进制是 `00` 到 `FF`。1 个十六进制位等于 4 比特，所以 1 字节永远等于两位十六进制字符：二进制写起来太长，十进制又对不上位的边界，十六进制正好卡在边界上。0–9 之后借 A–F 六个数，`A`=10、`F`=15，于是 `FF` = 15×16 + 15 = 255。程序里写十六进制会带 `0x` 前缀，但文件里并不存这个前缀：`0x68` 是 104，也就是字母 `h`；`0xFF` 是 255，它仍是一个字节，不是 255 个字节。这里值得停一下，因为 0–127 和 0–255 这两个数最容易被叠在一起：一个字节能装 256 种状态，而早年人们约定的那张表 ASCII 只用了其中 128 个，编号 0 到 127，把控制字符、字母和数字一一对应起来。表比装它的盒子小，上半部分留给后来用。具体是哪一年、由谁定下这张表，是史料里的事；这一讲要紧的是「有人约定了一张表」，以及中文不在这张表里。
>
> 我们将以没有文件头和文件尾的 `.txt` 文件举例。从其他语言来看，txt 就是一个被以文件形式存下来的字符串：没有开头标记，没有结尾标记，也没有哪一处写着「从这里开始、到这里结束」。如果通过格子去对应，那么偏移 0 的那格就是 txt 文件的开头，偏移 1 是下一格，如此而已。严格说，文件里没有字符，只有字节；字符是人按约定解码之后读出来的。文件里没有字符，只有字节；你能读出字，是因为有人约定了解码方式。
>
> 要把这些字节看见，得用一个肯把字节打印出来、而不是替你解释的工具，`od` 就是。它的名字叫 octal dump，是历史留下的叫法，加上下面这些参数后打印的是十六进制。这条命令在跑之前值得拆开看一遍：手册把参数一条一条列出来，却很少写「它们连在一起会是什么效果」。`-A` 管左边那列地址怎么显示，`n` 是 none，所以 `-An` 就是把这列整个去掉；`-t` 管输出类型，`x` 是十六进制，后面的数字表示「一次把几个字节读成一个数」：`x1` 是一字节一个数，`x2` 是两字节一个数，`x4` 是四字节一个数。于是 `-An -tx1` 连起来的意思很简单：「不显示地址，每个字节单独给一个十六进制数」。若去掉 `-An`，同一条命令会在开头多出 `0000000`、结尾多出 `0000004`，那是偏移，不是数据。
>
> ```bash
> printf 'A' | od -An -tx1        # 41
> printf '\xff' | od -An -tx1     # ff
> printf 'ABCD' | od -An -tx1     # 41 42 43 44
> printf 'ABCD' | od -An -tx2     # 4241 4443
> printf 'ABCD' | od -x          # 0000000 4241 4443
>                               # 0000004
> ```
>
> 第四行最值得看。只改一个字符，把 `x1` 换成 `x2`，`41 42 43 44` 就变成了 `4241 4443`。文件一个字节都没变，你只是让工具一次把两个字节读成一个 16 位数；而在这台机器上低位在前，所以 `41 42` 被显示成 `0x4241`。最后那行不加参数的 `od -x` 默认就是两字节一组，效果一样，这正是不用它来逐字节看东西的原因。把这组「反过来」的数先记着，下一节会回来找它：字节本身没犯错，出分歧的永远是读它的那条规则——这一整讲说的其实就是这件事。
>
> `xxd` 会把同样的字节摆得更热闹些。`-g` 决定几个字节分一组，默认是 2，所以直接跑 `xxd` 看到的是 `4142 4344`，加 `-g1` 才是 `41 42 43 44`。左边那列是偏移，右边是工具替人解码出来的字符，是给人看的便利，不是第三种数据。内存也是这样：一长排格子，每格 1 字节，各有自己的编号。文件不过是从外面看同一排格子，`.md`、`.png`、`.exe` 的区别，只是这些格子按什么约定排列。
>
> ```bash
> printf 'ABCD' | xxd -g1         # 00000000: 41 42 43 44    ABCD
> printf 'ABCD' | xxd -g2         # 00000000: 4142 4344       ABCD
> ```
>
> 那么：一个字节最大能装下哪个数？`0x1F` 换成十进制是多少？`41 42 43 44` 里偏移 2 上是谁？不用敲命令就能答上来，这几个工具就算没白讲。

---

## 2. The Assignment: From Reading Bytes to Writing a Format

> Now go back to `4241 4443`, and that brings us to the subject of this lesson: byte order. One byte stops at 255, so a number such as the timestamp `0x01020304` has to be spread over four bytes. Spreading it is not the hard part; deciding which of those four bytes goes into the box at offset 0 is, and that decision is what byte order means. Big-endian puts the high-order byte first, at the lower address, the way we write numbers by hand, so `0x01020304` becomes `01 02 03 04`. Little-endian puts the low-order byte first, so it becomes `04 03 02 01`. Neither side is more correct; different early CPUs simply chose differently and both survived. The machine in front of you is almost certainly little-endian, network protocols standardised on big-endian, and a save file uses whichever order its own specification says. That is precisely the reversal you saw a moment ago: `41 42` read as one 16-bit number showed up as `4241` because the low byte was treated as the first one.
>
> ```text
> offset:   0x00  0x01  0x02  0x03
> big   :   01    02    03    04      high byte at the low address
> little:   04    03    02    01      low byte at the low address
> ```
>
> ```bash
> python -c "import sys; print('sys.byteorder:', sys.byteorder)"
> printf '\x01\x02\x03\x04' | od -An -tx1   # 01 02 03 04
> ```
>
> Two things are easy to get wrong here. Byte order changes the arrangement of bytes, never the content of any single byte; and both orders can be read back correctly only because the reader already knows which one was used. Lose that agreement and the same four bytes are simply a different number.
>
> With byte order in hand, we can turn to a practical problem: a game save, or more generally any operation where a program writes its state back to local disk. Such a file usually holds a fixed marker, a few integers for the slot, the chapter and the timestamp, a string for the player name, and a version number. Each of those turns out to be a small decision about how to spend bytes.
>
> The first is that characters are not bytes. ASCII only assigned 0 to 127, and once Chinese enters the picture 256 slots are not enough, so several encodings exist. The same character `猫` is `e7 8c ab` in UTF-8, `2b 73` in UTF-16LE and `73 2b` in UTF-16BE. An encoding is a mapping table, not a rule like "one character is N bytes": an ASCII letter takes one byte in UTF-8, this Chinese character takes three, and UTF-16 also has four-byte surrogate pairs. The 18-byte file from the troubleshooting section of the last lesson makes a good piece of physical evidence here, without going through that investigation again.
>
> ```text
> od -An -tx1 .gitignore
> ff fe 2e 00 69 00 64 00 65 00 61 00 2f 00 0d 00
> 0a 00
> >
> read as UTF-16  ->  .idea/
> read byte by byte ->  every ASCII byte followed by a 00
> ```
>
> Same file, two ways of reading, two truths. This is why an encoding has to have a place in the agreement, and also why we should keep our terms straight: when an encoding already fixes the order of the bytes, we do not ask about byte order separately. Byte order is the word for assembling several bytes into one integer. The `2b 73` and `73 2b` above belong to encoding, not to integer byte order.
>
> The second decision is a length field. A player name is not fixed in size, so the format writes how many bytes the name has before the name itself, and the length costs bytes of its own. Take 300: it is `0x012C`, that is `0x100` + `0x2C`, or 256 + 44, and one byte stops at `0xFF` = 255, so it does not fit. In two little-endian bytes it is `2c 01`; in two big-endian bytes, `01 2c`.
>
> ```bash
> python -c "print((300).to_bytes(2,'little').hex(' '), (300).to_bytes(2,'big').hex(' '))"
> # 2c 01   01 2c
> ```
>
> So the design question is yours: one byte for the length, which is compact but caps a name at 255 bytes, two bytes, which allows 65535, or some variable-length scheme that saves space on short names but is harder to read and is not covered here. There is no single right answer, but the specification has to fix one and say why, and it has to remember that storing a name costs the length plus the content, not the content alone.
>
> The third decision is a version field. A format you define today will want to change in three months: one more field, or a changed meaning. Suppose an old program opens a new save that has gained a difficulty field. Without a version number in the header, it has no way to know from which byte onward the layout changed, and will read the rest under the old meanings. So the header gets a version, and the specification also answers what a reader does with a version higher than it understands: reject the file with an error, or try to parse it anyway. Rejecting means an old program cannot open a new file; parsing anyway risks reading garbage. Format changes are normal; whether old files still make sense afterwards depends on whether this one box was left today, because the code doing the reading will not know what you later decided.

> 现在回到 `4241 4443`，由此，我们引出本节课的重点：字节序。一个字节最大 255，像时间戳 `0x01020304` 这样的数就得摊到四个字节上。摊开不难，难的是决定哪一个字节放进偏移 0 的那格——这个决定，就是字节序要管的事。大端把高位字节放在前面（低地址），和人写数的习惯一致，`0x01020304` 落成 `01 02 03 04`；小端把低位字节放在前面，落成 `04 03 02 01`。两派没有对错，早年各家 CPU 各选一边，后来都活了下来。手上的机器几乎都是小端，网络传输标准用大端，而一份存档用哪头在前，由它自己的规范说了算。刚才那组反过来数正是这么来的：`41 42` 被当成一个 16 位数读时显示成 `4241`，因为低位被当成了头一个。
>
> ```text
> 偏移:    0x00  0x01  0x02  0x03
> 大端:     01    02    03    04      高位在低地址
> 小端:     04    03    02    01      低位在低地址
> ```
>
> ```bash
> python -c "import sys; print('sys.byteorder:', sys.byteorder)"
> printf '\x01\x02\x03\x04' | od -An -tx1   # 01 02 03 04
> ```
>
> 这里有两处容易想岔：字节序只改排列顺序，不改任何一个字节自己的内容；两种排法都能读回原数，也只是因为读的一方事先知道用的是哪种排法，约定一丢，同样四个字节就成了另一个数。
>
> 有了字节序，我们得以引申到一个实际的问题：游戏存档，或者说一切「把程序当前状态写回本地磁盘」的操作。这样一份文件里通常有固定标识、几个整数（槽位、章节、时间戳）、一个字符串（玩家名字），还有一个版本号。逐样看下来会发现，每一样都是「字节怎么花」的小决定。
>
> 第一，字符 ≠ 字节。ASCII 只排了 0 到 127，中文进来之后 256 格不够用，于是有了不同编码。同一个「猫」字，UTF-8 是 `e7 8c ab`，UTF-16LE 是 `2b 73`，UTF-16BE 是 `73 2b`。编码是一张映射表，不是「每字几字节」的公式：ASCII 字母在 UTF-8 里 1 字节，这个中文字在 UTF-8 里 3 字节，UTF-16 还有 4 字节的代理对。上一讲排查节里那份 18 字节文件，在这里当一件实物证据摆一次就够，不必再跑一遍排查。
>
> ```text
> od -An -tx1 .gitignore
> ff fe 2e 00 69 00 64 00 65 00 61 00 2f 00 0d 00
> 0a 00
> >
> 按 UTF-16 读     ->  .idea/
> 逐字节看         ->  每个 ASCII 字节后面都跟着一个 00
> ```
>
> 同一个文件，两种读法，两种真相。这就是编码要在约定里占一句的理由，也提醒我们把词分清楚：当编码约定已经写死了字节的先后顺序，就不必再单独问字节序；**字节序专指把多个字节拼成一个整数**的场合。上面 `2b 73` 与 `73 2b` 的先后归编码管，不归整数字节序管。
>
> 第二，长度字段。玩家名字长度不固定，于是格式先写「名字有几个字节」，再跟内容；可长度自己也要占字节。拿 300 算一笔：它是 `0x012C`，也就是 `0x100` + `0x2C`，256 + 44；一个字节最大 `0xFF` = 255，装不下。写成小端两字节是 `2c 01`，大端两字节是 `01 2c`。
>
> ```bash
> python -c "print((300).to_bytes(2,'little').hex(' '), (300).to_bytes(2,'big').hex(' '))"
> # 2c 01   01 2c
> ```
>
> 于是设计题是你的了：长度定 1 字节，省地方，但名字最长 255；定 2 字节，能到 65535；或者用更省小名字空间、读起来却更绕的变长写法（本讲不展开）。没有标准答案，但规范里必须写死一种并说明理由，还得记住「存名字」花的是「长度 + 内容」，不是只有内容。
>
> 第三，版本字段。今天定下的格式，三个月后一定会想改：加一个字段，或改掉某个含义。设想老程序打开一份多了「难度」的新存档：头部没有版本号，它凭什么知道从第几个字节起排布变了？只能按老规则硬读，后面全是错的意思。所以头部留一格版本，规范里还要回答：读到比自己认识的版本更高的文件，是报错拒绝，还是尽力解析？拒绝 = 老程序打不开新文件；硬读 = 可能按错误含义解析出垃圾数据。格式会变是常态，变完之后旧文件还读不读得懂，取决于今天有没有留这一格——因为将来读这个文件的代码，不会知道你「后来想了什么」。

---

## 3. What Counts as Done

> By now there are six decisions on the table, and they are not six exercises. Write one sentence for each and the six sentences together become a specification, an agreement that someone else can implement without asking you a single question. The first says how the format is recognised, with a few fixed bytes at the front. The second says which end of a multi-byte integer comes first. The third says how strings are stored, and here the encoding fixes the order so byte order is not asked again. The fourth says how many bytes the length field uses, and therefore how 300 `a`s land on disk. The fifth says where the version sits and what happens on a higher version. The sixth says which byte combinations must be refused: a wrong marker, a length larger than the bytes left in the file, and so on.
>
> The useful test is to hand those six sentences to someone else and let them work out the same three cases on paper, without showing them your sample bytes. If their bytes match yours, the agreement is clear. If they do not, do not rewrite the answers; find the one sentence that can be read two ways. An ambiguity left inside a specification always forks the implementation.
>
> Close with three pencil-and-paper problems: write `0x12345678` as a byte string in both orders, store the value 256 in two little-endian bytes, and lay out three sample saves, an empty one, one with slot 1, chapter 3, timestamp `0x01020304` and the name `Kt`, and one with 300 `a`s. The last one is there to force the length field to take a position, because 300 does not fit in a single byte. Then run the two commands below and compare.
>
> ```bash
> printf '\x12\x34\x56\x78' | od -An -tx1   # 12 34 56 78
> python -c "print((256).to_bytes(2,'little').hex(' '))"
> ```
>
> After this lesson you should be able to say why one byte is two hex digits and why `0x` is not in the file, point at the offset, the byte and the decoded character in an `xxd` line as three different things, keep byte order, encoding and length in three separate sentences, write six sentences someone else can implement from, and hand in a merge request with one file and a path list anyone can re-run.
>
> **Keep one sentence**: writing down six decisions is not the same as someone else computing the same bytes from them. This lesson stops at the specification.

> 到这里，桌上摆着六个决定，而它们不是六道练习题。每个决定各写一句，六句拼起来就是一份 SPEC：别人照着它就能实现，不必再回来问你一句。第一句写怎么认出这个格式，头部放几个固定字节作标识；第二句写多字节整数哪头在前；第三句写字符串怎么存，编码已经把顺序定死，这一句里就不再问字节序；第四句写长度字段几个字节，也就顺带写清 300 个 `a` 怎么落笔；第五句写版本字段放哪、读到更高版本怎么办；第六句写哪些字节组合必须拒绝——标识不对、长度超过文件剩下的字节数，等等。
>
> 有个很实在的检验：把这六句交给旁边的人，不给他看你的样例字节，请他独立手算同样三组。算出来一样，说明约定写清楚了；对不上，别急着改答案，先找出具体哪一句能读出两种意思。歧义留在规范里，实现就一定会分叉。
>
> 最后用三道手算题收口：`0x12345678` 按大端、小端各写出字节串；数值 256 存成 2 字节，小端是哪两个字节；再摆三组存档样例——空存档，槽位 1、章节 3、时间戳 `0x01020304`、名字 `Kt`，以及 300 个 `a`。第三组是逼长度字段表态的：300 装不进一个字节，你必须做设计决定。先铅笔算，再跑下面两条命令对一对。
>
> ```bash
> printf '\x12\x34\x56\x78' | od -An -tx1   # 12 34 56 78
> python -c "print((256).to_bytes(2,'little').hex(' '))"
> ```
>
> 这一讲读完，你应该能说清为什么一个字节是两位十六进制、为什么 `0x` 不在文件里；看着一行 `xxd` 输出，能指出偏移、字节、解码出的字符是三件不同的东西；能把字节序、编码、长度分别写成三句话而不混在一起；能写出六句别人照着能实现的 SPEC；也能交一个只含一个文件的合并请求，附上别人能重跑的路径清单。
>
> **记住一句**：写完六句，和别人照着它算得出同一串字节，是两件事。本讲到「把决定写进 SPEC」为止。

> **Hand-in checklist — English template / 英文模板**
> Copy the whole block into `SPEC.md` and replace every `[ ]`.

```text
=== WHAT TO HAND IN ===========================================

[1] The only path allowed in this merge request
    submits/<handle>/P0/SPEC.md

[2] Content of SPEC.md
    Copy everything between the two dashed lines into the file.
------------------------------------------------------------
# Save File SPEC

- Q1 format marker:
  [____]

- Q2 byte order for multi-byte integers:
  [____]

- Q3 string encoding:
  [____]

- Q4 length field width, and why:
  [____]

- Q5 version field position and higher-version behaviour:
  [____]

- Q6 byte combinations that must be rejected:
  [____]

- Three cases, worked out by hand (bytes, not code):
  [empty save: ____]
  [slot 1 / chapter 3 / timestamp 0x01020304 / name Kt: ____]
  [300 a's: ____]

- Output of the two verification commands (verbatim):
  [____]

- Commit type and why:
  [docs: because this change touches documentation only]

- Commit message I used:
  [docs: add save file spec]

- Unexpected entries in git status:
  [none / list them]


- One sentence for the merge request description:
  [which rule made me exclude what]
------------------------------------------------------------

[3] Also paste into the merge request description
    - the diff output above, verbatim
    - the one sentence above

[4] NOT in this PR
    .gitignore        <- already committed in the last merge; only checked now
    .idea/  .vscode/  caches, generated files, editor folders
    sample save files, or any bytes produced by a program
    anything outside submits/<handle>/
============================================================
```

> **交什么，照着填 — 中文模板**
> 整段复制进 `SPEC.md`，把每个 `[ ]` 换成自己的答案。

```text
=== 本次要交的东西 ==========================================

[1] 合并请求里只允许出现的路径（干净结果只有这一行）
    submits/<handle>/P0/SPEC.md

[2] SPEC.md 的内容
    把下面两条虚线之间整段复制进文件
------------------------------------------------------------
# 存档格式 SPEC

- Q1 格式标识：
  [____]

- Q2 多字节整数的字节序：
  [____]

- Q3 字符串编码：
  [____]

- Q4 长度字段几个字节，以及理由：
  [____]

- Q5 版本字段放哪、读到更高版本怎么办：
  [____]

- Q6 哪些字节组合必须拒绝：
  [____]

- 三组样例，手算写出字节（不是写程序生成）：
  [空存档：____]
  [槽位 1 / 章节 3 / 时间戳 0x01020304 / 名字 Kt：____]
  [300 个 a：____]

- 两条验证命令的输出（原样）：
  [____]

- 提交类型及理由：
  [docs: 这次只改了文档]

- 本次提交信息：
  [docs: add save file spec]

- git status 里不是我写的条目：
  [无 / 写具体名字]


- 我按哪条规矩排除了什么（贴进合并请求描述）：
  [一句话]
------------------------------------------------------------

[3] 合并请求描述里另外要贴
    · 上面 diff 那一项的输出，原样
    · 上面「我按哪条规矩排除了什么」那一句话

[4] 这次明确不交
    .gitignore        ← 上一次合并已进仓库，这次只核对
    .idea/  .vscode/  缓存、生成物、编辑器目录
    样例存档文件，以及任何由程序生成出来的字节
    submits/<handle>/ 以外的任何文件
============================================================
```
