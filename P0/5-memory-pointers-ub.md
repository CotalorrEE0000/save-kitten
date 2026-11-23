# Memory, Pointers, and Undefined Behavior

## 1. Before You Start: Where a Byte Lives

> The last lesson stopped at the specification. Six sentences said how a save file is recognised, which end of an integer comes first, how strings are stored, how long the length field is, where the version sits, and which bytes must be refused. The file, we decided, holds nothing but bytes; everything you can read on the screen comes from an agreement about how those bytes are arranged. So the natural next question is not what the bytes mean, but where they live while a program is using them.
>
> Some languages and libraries look after this space for you, and some do not; nothing in this lesson depends on which ones you have met, or on whether you have written any C before. We start from the C case because it leaves the two questions in the open: who gave you this piece of memory, and who gives it back. Memory, like a file, is only a long row of bytes. What it adds is that every byte has an address, and that somebody is responsible for releasing the space when it is no longer needed.
>
> Start with one ordinary variable, `int x = 0x01020304;`. It occupies four consecutive bytes, and `&x` is the address of the first of them. Read those four bytes one at a time through an `unsigned char *` and they come out as `04 03 02 01`, not `01 02 03 04`. If that looks familiar, it should: it is the byte order from the last lesson, only now the bytes are in memory rather than in a file. The same machine keeps the same little-endian habit in both places, which is a quiet reason for choosing little-endian in a save format — the numbers do not have to be turned around on their way in or out. It is worth saying one more time that there is no `int` sitting in memory. There are four bytes, and `int` is the interpretation the compiler lends them; read the same four bytes as a `float` and you get a different number entirely.
>
> That raises a larger question: what is a type, then? A variable is a name given to a few bytes together with a promise about how to read them. `int` promises four bytes read as a signed whole number, with the top bit standing for the sign; `unsigned int` promises the very same four bytes read as an unsigned whole number, where that top bit is just another digit. The type never changes the raw bytes. Take `ff ff ff ff`: read as `int` it is -1, read as `unsigned int` it is 4294967295, and written in hexadecimal it is `ff ff ff ff` either way — which is why the dump tools of the last lesson can show you the truth without knowing a single one of your declarations. Underneath both lies one string of switches, `11111111 11111111 11111111 11111111`, and a run like `1010101010` means nothing at all until somebody fixes where it starts, how long it is, and which table to apply. Divide four bytes into a sign, an exponent and a mantissa and the same switches become a `float`: the bit pattern written as `0x3F800000` reads as 1.0 under that agreement, though in this little-endian memory those four bytes lie as `00 00 80 3f`. Take one byte and look it up in ASCII and `41` is the character `A`, or the number 65, depending on which column of the table you read. Lay a run of such bytes down in order, agree an encoding, and agree where the run stops, and you have a string — the length field from the last lesson and the `\0` in this one are simply two answers to that same "where does it stop" question.
>
> Once you see it this way, the rest of a program is made of the same stuff. A `struct` is several such fields placed at agreed offsets, with padding the compiler may slip between them; a `class` in C++ is no different at the bottom, being a storage layout plus the rules for reading it. A file is the same idea stretched out on disk: a header at the front holding the marker and the version, a body of fields in a fixed order, sometimes a footer or a checksum at the end, and a file offset — a pointer to "which byte we are at" — that moves along as you read. The plain `.txt` of the last lesson had neither header nor footer because it needed neither; the moment a format has to hold a slot, a timestamp and a name, somebody has to write down where each begins. That written agreement is what we are calling `savefmt`. We are not reading a ready-made file; we are building a specification, and a specification, once written down, corresponds to exactly one file. The six sentences were the specification, and the skeleton at the end of this lesson is the program that agrees to read by it.
>
> If you have only ever written code inside an editor such as Dev C++ or VS Code, pressing Run hides a step worth naming. The text in a `.c` file is not something a machine can execute; a program called a compiler reads that text and translates it into an executable file. `gcc` and `clang` are two such compilers, and the line below is simply that translation done out loud in a terminal instead of behind a button. An IDE is an editor with the same call wired into its menus, so whichever one you use changes nothing about the bytes under discussion. The outputs here came from a Windows toolchain, but the behaviour below belongs to the language, not to the brand of compiler or the folder it happens to live in.
>
> ```bash
> gcc -Wall -Wextra -o d1 d1.c && ./d1
> ```
>
> Before running it, take the command apart. We did this once already with `od` and `xxd` in the last lesson; the method is the same, but the tool here is a compiler, so the switches are a different set. `gcc` compiles C source, and `g++` is its C++ counterpart in the same compiler family (`clang` is a separate family alongside them): the two share nearly all their switches, and differ in which language they assume and which standard library they link. If the files you have built so far ended in `.cpp`, the name on your build line was `g++`; a `.c` file goes through `gcc`. What follows the name is a stack of small decisions. `d1.c` is the source file to read. `-Wall` turns on one family of compile-time warnings and `-Wextra` a second, partly overlapping one; neither is a general check that the program is correct. `-o d1` names the executable the compiler writes. `&&` means `./d1` runs that executable only if the compile succeeded, instead of running an older copy left behind by a failed build. Manuals list each switch on its own line and rarely say what several of them do together, which is worth remembering for the switches that appear later: `-c` stops after compiling, `-g` keeps debug information, `-O2` selects an optimisation level, `-std=` fixes which language standard is being used, `-fwrapv` and `-Wshift-overflow=2` change how overflow and shifts are treated, and `-fsanitize=address` or `-fsanitize=undefined` instrument the program at run time. Some of them only mean something in combination: `-fsanitize=address` with `-g` is what lets a report name a file and a line, and `-O2` with `-fwrapv` gives a different answer from `-O2` alone. What the opening combination does **not** do is check whether an array index is inside the array, and that silence is the most important thing this lesson has to show you.
>
> ```text
> x = 0x01020304
> sizeof x = 4
> byte[0] = 04
> byte[1] = 03
> byte[2] = 02
> byte[3] = 01
> ```
>
> An address is a number, and a number can be stored, so the next step is small but easy to miss. After `int *p = &x;`, what `p` holds is the address of `x`. Yet `p` is itself a variable, so it also lives in memory, also has an address of its own, `&p`, and on a 64-bit machine takes eight bytes. `*p` means: take the address stored in `p` and read the bytes there as an `int`. The `*` in a declaration is only a mark saying "this is a pointer"; the `*` in an expression is an action. And the type is not decoration either: an `int *` and a `char *` pointed at the very same address read different numbers of bytes, which is why we used `unsigned char *` a moment ago to see `x` one byte at a time.
>
> ```text
> value  *p        = 0x01020304
> where  p  (addr) = 000000a3481ffd1c
> where &p (addr of the pointer itself) = 000000a3481ffd10
> sizeof p = 8 bytes, sizeof *p = 4 bytes
> ```
>
> Those two long addresses will be different every time you run the program; what stays on this run is the gap of twelve bytes between them, because the pointer itself takes eight and something else is lying next to it. If `p` is an address, whose address is `&p`? Once that question has an answer, you are ready to ask what happens when a program walks one step past the bytes it was given.

> 上一讲收在一份 SPEC 上：六句话写清了存档怎么认、整数哪头在前、字符串怎么存、长度字段几个字节、版本放哪、哪些字节必须拒绝。我们当时认定，文件里只有字节；屏幕上能读出字，全靠有人约定了这些字节怎么排。那么接下来该问的就不是字节是什么意思，而是：程序用着它们的时候，它们住在哪里。
>
> 有些语言、有些库会替你把这块空间照看好，有些不会；这一讲不依赖你此前碰过哪一种，也不要求你先写过 C。我们从 C 的情形讲起，只因为它把两个问题明摆着留在桌面上：谁给你的这块内存，以及谁把它还回去。内存和文件一样，也只是长长一排字节；它多出来的是两件事——每个字节都有地址，以及不再用的时候，得有人负责把这块地方释放掉。
>
> 先看一个最普通的变量，`int x = 0x01020304;`。它占四个连续的字节，`&x` 是其中第一个字节的地址。用 `unsigned char *` 一个字节一个字节去读，拿到的是 `04 03 02 01`，不是 `01 02 03 04`。看着眼熟就对了：这正是上一讲的字节序，只不过这次字节不在文件里，在内存里。同一台机器在两处都守着小端的习惯，这也正是存档格式选小端的一个不声不响的理由——数字进出内存不必来回掉头。还有一句值得再说一遍：内存里并没有一个叫 `int` 的东西躺在那儿，只有四个字节；`int` 是编译器借给它们的解释方式，同样四个字节按 `float` 去读，就是另一个数。
>
> 那就要多问一句：类型到底是什么？变量无非是给几个字节起个名字，再附上一份「怎么读」的约定。`int` 约定四个字节按有符号整数读，最高位当符号位；`unsigned int` 约定同样这四个字节按无符号整数读，最高位只是又一位数字。类型从不改动原始字节。拿 `ff ff ff ff` 来说：按 `int` 读是 -1，按 `unsigned int` 读是 4294967295，而写成十六进制两边都是 `ff ff ff ff`——这正是上一讲那些 dump 工具不需要知道你声明过什么、也能把真相摆出来的原因。两者底下是同一串开关 `11111111 11111111 11111111 11111111`；像 `1010101010` 这样一串位，在有人定下「从哪开始、一共几位、查哪张表」之前，什么意思都没有。把 4 字节拆成符号位、指数位和尾数位，同一串开关就成了 `float`：位模式写成 `0x3F800000` 时按这个约定读是 1.0，尽管在这台小端机器的内存里，这四个字节躺成 `00 00 80 3f`。只取 1 字节去 ASCII 表里查，`41` 是字符 `A`，也是数字 65，看你读表里的哪一列。把这样一串字节按顺序排好、约定编码、再约定到哪为止，就有了字符串——上一讲的长度字段和这一讲的 `\0`，不过是「到哪为止」这同一个问题的两种答法。
>
> 这样看下来，程序里其余的东西也都是同一套材料做的。`struct` 是几个这样的字段按约定好的偏移摆在一起，编译器还可能在中间塞进对齐填充；C++ 里的 `class` 剥到底也一样，一份存储布局加上怎么读它的规矩。文件不过是把同一个想法摊到磁盘上：前面一段文件头放标识和版本，中间是按固定顺序排好的字段，末尾有时还有文件尾或校验，另有一个「现在读到第几个字节」的文件偏移指针，一边读一边往前走。上一讲那个普通 `.txt` 既没有文件头也没有文件尾，因为它不需要；可一旦格式要装槽位、时间戳和名字，就得有人把每一块从哪开始写下来。这份写下来的约定，我们叫它 `savefmt`。我们不是在读一个现成的文件，我们是在构建一份规范；而规范一旦落笔，正好对应着一份文件。那六句话是规范，本讲末尾的骨架，就是答应照它来读的程序。
>
> 如果你一直是在 Dev C++、VS Code 这类编辑器里写代码，点一下「运行」其实藏起了一步该说清的事。`.c` 文件里的文字机器并不能直接执行，要有一个叫**编译器**的程序把它读进去、翻译出一个可执行文件。`gcc` 和 `clang` 就是两个这样的编译器，下面那一行，无非是把这次翻译搬到终端里、当着你的面做一遍，而不是藏在按钮背后。IDE 就是把同一条调用接进菜单的编辑器，所以你用哪一个，都不影响我们讨论的这些字节。本讲的输出来自一套 Windows 工具链，但下面的行为属于语言本身，不归某个编译器品牌，也不归它装在哪个文件夹里。
>
> ```bash
> gcc -Wall -Wextra -o d1 d1.c && ./d1
> ```
>
> 先别急着跑，把这条命令拆开看。上一讲我们已经把 `od`、`xxd` 那串开关逐个拆过，办法一样，只是这次的工具换成了编译器，开关也就换了另一套。`gcc` 编的是 C 源文件，`g++` 是同一家族里编 C++ 的那个（`clang` 是并列的另一套）：两者共用绝大部分开关，差别只在默认按哪种语言读、以及链接哪套标准库。如果你此前构建的都是 `.cpp`，那行命令上写的就是 `g++`；`.c` 文件交给 `gcc`。名字后面是一叠小决定：`d1.c` 是要读的源文件；`-Wall` 打开一族编译期警告，`-Wextra` 再打开另一族与它部分重叠的警告，两者都不是「检查程序对不对」的开关；`-o d1` 给编译器写出的可执行文件起名字；`&&` 表示编译成功才由 `./d1` 去运行它，免得编译失败时跑的还是上一回留下的旧程序。手册把每个开关单列一行，很少写「几个连用会是什么效果」，这一点在后面几组开关上尤其要记住：`-c` 只编译不链接，`-g` 保留调试信息，`-O2` 选优化档位，`-std=` 定下按哪一版语言标准来读，`-fwrapv` 与 `-Wshift-overflow=2` 改变溢出和移位的处理方式，`-fsanitize=address`、`-fsanitize=undefined` 则在运行时给程序插桩。有些开关本来就得连着用才有意义：`-fsanitize=address` 配上 `-g`，报告才说得出是哪个文件哪一行；`-O2` 单独用和再加 `-fwrapv`，同一个表达式会给出两个答案。而开头这一串组合**不做**的一件事，是检查数组下标有没有出界——本讲最要紧的，恰恰是它在这件事上的沉默。
>
> ```text
> x = 0x01020304
> sizeof x = 4
> byte[0] = 04
> byte[1] = 03
> byte[2] = 02
> byte[3] = 01
> ```
>
> 地址是一个数，而数是可以被存起来的，下一步很少，却最容易漏掉。写完 `int *p = &x;`，`p` 里装的是 `x` 的地址；可 `p` 自己也是变量，所以它也住在内存里，也有自己的地址 `&p`，在 64 位机器上占 8 个字节。`*p` 做的事是：取出 `p` 里存着的地址，把那片字节按 `int` 来读。声明里的 `*` 只是「这是个指针」的记号，表达式里的 `*` 才是一个动作。类型也不是摆设：`int *` 和 `char *` 指向同一个地址，读出来的字节数完全不同——刚才正是靠 `unsigned char *` 才把 `x` 一眼一眼看成了四个字节。
>
> ```text
> value  *p        = 0x01020304
> where  p  (addr) = 000000a3481ffd1c
> where &p (addr of the pointer itself) = 000000a3481ffd10
> sizeof p = 8 bytes, sizeof *p = 4 bytes
> ```
>
> 这两个长地址每次运行都会变；这一次不变的是它们相差 12 字节，因为指针自己占 8 字节，旁边还躺着别的东西。如果 `p` 是地址，那 `&p` 是谁的地址？这个问题能答上来，就可以往下问了：程序要是往给它的字节之外多走一步，会怎样。

---

## 2. The Assignment: What the Compiler Does Not Check

> An array is only some bytes standing next to each other. `int arr[2]` is eight bytes in a row, and `arr[2]` is nothing more mysterious than the address `arr + 2*4`: the compiler computes the offset and does not ask whether it is legal. Put that array inside a struct with an `int guard` beside it, write `s.arr[2] = 999`, and the neighbouring `guard` changes from 12345 to 999. Both `-Wall` and `-Wextra` stay completely silent.
>
> ```text
> before: arr[0]=1 arr[1]=2 guard=12345
> after : arr[0]=1 arr[1]=2 guard=999
> ```
>
> This is the moment to slow down, because the program did not crash, it printed exactly what you would expect if everything were fine, and it is still wrong. Being careful is not a defence: which neighbour gets overwritten, whether it crashes afterwards, and whether the answer changes when you move `guard`, turn on `-O2`, or build on another machine are all outside what the language promises. **"It ran" is not the same as "it is right"; it only means it was not caught this time.** Undefined behaviour is not a kind of bug that crashes; it is a stretch of code about which the standard says nothing at all, and the compiler is free to assume it never happens.
>
> A C string has the same weakness with a different face. There is no length field; the last byte is a zero, `\0`, and that is the only thing telling `strlen` where to stop. Give it `{'a','b','c'}` with no terminating zero and it keeps counting into whatever happens to lie beyond. On this run it stopped at 3, because the next byte happened to be zero — the most dangerous version of the same problem, since nothing looks broken. `sizeof` counts bytes, `strlen` counts characters until it meets `\0`; `char t[] = "ab"` is therefore 3 by `sizeof` and 2 by `strlen`, the extra byte being the terminator.
>
> ```text
> sizeof s   = 3
> strlen(s)  = 3   <- already past the end of s
> char t[]="ab": sizeof = 3, strlen = 2
> ```
>
> That also answers a question left over from the last lesson: why did our save format write its own length field instead of doing what C strings do? Because the contents of a save may perfectly well contain a zero byte, and because a length field can be read in one step, whereas a terminator makes every reader walk the whole string first. The format we specified is, among other things, a refusal to depend on a lucky zero.
>
> So far the bytes have all been local, and local bytes have a short life: when the function returns, they are gone. To hold something longer — an entire save file, say — you ask the system for a block with `malloc`. It hands you an address and does not tell you the size; the size is yours to remember. `realloc` grows the block and may move it, which makes the old address invalid the moment it returns. `free` gives the block back to the allocator and does **not** wipe its contents; the bytes are still there, and reading them afterwards is exactly the undefined behaviour we have been describing. And `p = q` only gives the same block another name, it does not copy anything.
>
> ```text
> malloc 4 ints  -> 000001cf84ec8ce0
> realloc to 4000 ints -> 000001cf850180c0  (old 000001cf84ec8ce0, moved: yes)
> q[0..3] still there: 0 1 2 3
> ```
>
> The six problems in the first problem set under `algo` were each shown in Go, Rust, C and C++, so one sentence is enough here, and not having done them changes nothing below: Vector --A container that grows by itself quietly does four things for you: it works out how much larger a block it needs, allocates one, copies the old data across, and releases the old block. In C those four things are simply yours to write, and the compiler helps with exactly one of them. On this run `gcc` also printed `warning: pointer 'p' used after 'realloc' [-Wuse-after-free]` — even printing the old address after `realloc` counts as using a pointer whose block is gone. It is one of the few undefined behaviours `-Wall` does catch, and it is worth reading carefully rather than silencing.
>
> The clearest demonstration that undefined behaviour is about meaning rather than crashing needs two builds of one program. Read an integer from the command line and print `x + 1 > x`. With `-O2` and `x = 2147483647`, the answer is 1; add `-fwrapv` and the answer is 0. Here `-O2` selects an optimisation level, and `-fwrapv` tells the compiler to treat signed overflow as binary wraparound instead of something that cannot happen. The compiler is entitled to answer "always true" in the first build because the standard declares signed overflow undefined: it may simply assume it never occurs. If it does occur, nothing the program concludes afterwards counts. The second build is not a fixed program, it is a different agreement with the compiler. Not a compiler bug — the line of code itself has no defined meaning at that value.
>
> ```text
> x=2147483647  x+1>x -> 1        # -O2
> x=2147483647  x+1>x -> 0        # -O2 -fwrapv
> ```
>
> Shifts have the same split. `1 << 31` needs 33 bits to represent but `int` has only 32, so it is undefined; `1u << 31` is unsigned and perfectly legal, giving 2147483648. On this machine the `int` version happens to print -2147483648, which is another one of those lucky-looking results and not a guarantee. Notice too that `-Wall` does not report `1 << 31` on its own: you have to add `-Wshift-overflow=2` before the compile says `warning: result of '1 << 31' requires 33 bits to represent, but 'int' only has 32 bits [-Wshift-overflow=]`. Warning switches have a division of labour just as the `x1` and `x2` of the last lesson did; knowing which one is on is part of reading the output.
>
> Hand-checking is not enough, so there are tools that turn an accident into a definite report. `-fsanitize=address` builds a version of the program that registers every address as it is read or written; `-g` keeps the debug information that lets the report name a file and a line. Together they do not wait for a crash — an out-of-bounds access is reported at once, with how far past the block it went and who allocated it. Run the two-`int` allocation that writes `p[2]` this way and the report says `heap-buffer-overflow` and `0 bytes after 8-byte region`, which means the access landed exactly at the end of that eight-byte block, on the first byte of `p[2]`. `-fsanitize=undefined` covers the arithmetic and shift side instead. It needs one extra runtime library at link time, and a toolchain that does not ship it stops at `cannot find -lubsan`; a toolchain that does ship it runs the same command without complaint. That is a missing library, not a command written wrongly, so the arithmetic half is simply built where that library exists. Neither tool is a net over everything: AddressSanitizer watches memory, UBSan watches arithmetic and shifts, and data races or a plain mistake in your logic are outside both.
>
> ```text
> ERROR: AddressSanitizer: heap-buffer-overflow on address 0x123c0c620298 ...
> WRITE of size 4 at 0x123c0c620298 thread T0
>     #0 ... in main d6.c:6
> 0x123c0c620298 is located 0 bytes after 8-byte region [0x123c0c620290,0x123c0c620298)
> ```
>
> Now the six sentences from the last lesson can become code. The first thing the skeleton does is read the file: `fopen`, then `fseek` to learn its size, then `malloc(size)` and `fread`, and that first `malloc` already has a matching `free` waiting at the end. The second is to take the header apart byte by byte, reading the magic, the version and each length field with an `unsigned char *` in the byte order the SPEC fixed, rather than `memcpy` the bytes into a struct — a struct has alignment padding between its members, and the fields come out wrong. The third is the line this whole lesson has been walking towards: before anything is copied out, compare every length with the bytes still left in the file, `if (name_len > remaining) return ERROR;`. That one comparison is Q6 from the SPEC made real, and it is the first gate against reading past the end. The last is to give the memory back, on the success path and on every error path alike, which is easiest if the function is written with a single exit from the start.

> 数组不过是挨着站的一排字节。`int arr[2]` 就是连续的 8 个字节，`arr[2]` 也没什么神秘的，不过是 `arr + 2*4` 这个地址：编译器把偏移算出来，并不问这个偏移合不合法。把它和一个 `int guard` 一起放进结构体，写一句 `s.arr[2] = 999`，隔壁的 `guard` 就从 12345 变成了 999。`-Wall` 和 `-Wextra` 全程一声不吭。
>
> ```text
> before: arr[0]=1 arr[1]=2 guard=12345
> after : arr[0]=1 arr[1]=2 guard=999
> ```
>
> 这里该慢下来看：程序没崩，屏幕上的结果也和「一切正常」时一模一样，可它仍然是错的。「我小心点就行」挡不住这件事——究竟踩到谁、踩完崩不崩、把 `guard` 挪个位置或开个 `-O2`、换台机器之后结果会不会变，语言一概不保证。**跑通了不算对，只是这一次没被抓住（catch）。** 未定义行为不是「一种会崩的 bug」，而是一段标准什么都没说的代码；编译器因此可以干脆假设它不会发生。
>
> C 字符串是同一个弱点换了张皮。它没有长度字段，最后一个字节是 `\0`，全靠这个零告诉 `strlen` 到此为止。给它一个没有结尾零的 `{'a','b','c'}`，它就一路往后数；这一次数到 3 停了，只因为后面那格恰好是 0——这恰恰是最危险的一种，因为看上去毫无破绽。`sizeof` 数字节，`strlen` 数字符直到遇见 `\0`；所以 `char t[] = "ab"` 的 `sizeof` 是 3、`strlen` 是 2，多出来的那一格就是结尾的零。
>
> ```text
> sizeof s   = 3
> strlen(s)  = 3   <- 已经越过 s 的末尾了
> char t[]="ab": sizeof = 3, strlen = 2
> ```
>
> 这也顺手回答了上一讲留下的一个问题：我们的存档格式为什么自己写长度字段，不学 C 字符串？因为存档内容里完全可能出现零字节（二进制数据本来就是），也因为长度字段一步就能读到，而靠结尾零就得每次把整条内容先走一遍。我们定下的那份格式，某种意义上就是不肯把正确性押在一个恰巧为零的字节上。
>
> 到目前为止，字节都是局部的，而局部字节命不长：函数一返回，它们就没了。想让东西活得比函数久——比如把整份存档读进来——就得用 `malloc` 向系统要一块。它给你地址，却不告诉你大小，大小得你自己记着；`realloc` 扩容时可能搬家，返回的那一刻旧地址立刻作废；`free` 只是把这块还给分配器，**并不清零**，字节还在那里，之后再读就是我们一路讲下来的未定义行为。还有 `p = q`，它只是给同一块内存换了个名字，并没有拷贝内容。
>
> ```text
> malloc 4 ints  -> 000001cf84ec8ce0
> realloc to 4000 ints -> 000001cf850180c0  (old 000001cf84ec8ce0, moved: yes)
> q[0..3] still there: 0 1 2 3
> ```
>
> algo 下第一个题单的六道题，每一道都按 Go、Rust、C、C++ 分别讲过；这里只提一句，没做过也不影响往下读：vector是一个会自己长大的容器，悄悄替你做的是四件事：算出需要多大的新块、分配、把旧数据拷过去、释放旧块。在 C 里它们就落回你手上，而编译器只在其中一步上帮得上忙。这一次 `gcc` 还打了 `warning: pointer 'p' used after 'realloc' [-Wuse-after-free]`——连 `realloc` 之后把旧地址打印出来，都算用了一个块已经不在的指针。这是 `-Wall` 少数能抓到的未定义行为之一，值得看清楚，别急着把它关掉。
>
> 要说明未定义行为关乎「有没有意义」而不是「会不会崩」，最清楚的办法是把同一份程序编两次。从命令行读一个整数，打印 `x + 1 > x`：只加 `-O2`、`x = 2147483647` 时答 1；再加一个 `-fwrapv` 就答 0。这里 `-O2` 是优化档位，`-fwrapv` 是告诉编译器「有符号溢出就按二进制回绕算」，别再当成不会发生的事。第一个版本敢直接回答「恒真」，是因为标准把有符号溢出判成未定义，编译器便可以假设它不发生；真发生了，这行之后程序得出的一切结论都不作数。第二个版本不是把程序修好了，只是和编译器换了份约定。这不是编译器的 bug——那行代码在这个取值上本就没有定义。
>
> ```text
> x=2147483647  x+1>x -> 1        # -O2
> x=2147483647  x+1>x -> 0        # -O2 -fwrapv
> ```
>
> 移位也分成两边。`1 << 31` 需要 33 位才装得下，可 `int` 只有 32 位，所以它是未定义；写成 `1u << 31` 是无符号，合法，得到 2147483648。这台机器上 `int` 那版碰巧打印 -2147483648，又是一个「看着挺正常」的偶然结果，不是保证。还有一点：`-Wall` 自己并不报 `1 << 31`，要显式加上 `-Wshift-overflow=2`，编译才会说 `warning: result of '1 << 31' requires 33 bits to represent, but 'int' only has 32 bits [-Wshift-overflow=]`。警告开关之间也有分工，和上一讲 `x1`、`x2` 的分别是一个道理；知道这次开着哪几个，本来就是读输出的一部分。
>
> 手动查靠不住，所以有工具把「偶然」变成「必然的报错」。`-fsanitize=address` 会编出一个在每次读写时登记地址的版本，`-g` 保留调试信息，报告才说得出是哪个文件哪一行。两者合起来不是等崩溃才出声：越界当场就报，还告诉你越过了多少字节、那块是谁分配的。把「分配两个 `int` 却写 `p[2]`」这样跑一遍，报告写着 `heap-buffer-overflow` 和 `0 bytes after 8-byte region`——意思是访问位置正好落在那个 8 字节块的末尾之后，也就是 `p[2]` 的第一个字节。`-fsanitize=undefined` 管的则是溢出、移位这一类。它在链接时要多用一个运行库，没带这个库的工具链会停在 `cannot find -lubsan`，带了的同一条命令就顺顺当当跑下去；那是少了一个库，不是命令写错，所以算术那一半放到有这个库的地方编一遍就是了。两个工具也都不是网：ASan 盯内存，UBSan 盯算术和移位，数据竞争、还有你自己想岔了的逻辑，它们一个都不管。
>
> ```text
> ERROR: AddressSanitizer: heap-buffer-overflow on address 0x123c0c620298 ...
> WRITE of size 4 at 0x123c0c620298 thread T0
>     #0 ... in main d6.c:6
> 0x123c0c620298 is located 0 bytes after 8-byte region [0x123c0c620290,0x123c0c620298)
> ```
>
> 到这里，上一讲那六句话可以落成代码了。骨架做的第一件事是读文件：`fopen`，用 `fseek` 问出大小，`malloc(size)`，再 `fread`；而这第一个 `malloc`，从一开始就有末尾那个 `free` 等着它。第二件事是逐字节拆头部：按 SPEC 定下的字节序，用 `unsigned char *` 把 magic、版本和每个长度字段一个字节一个字节取出来，别把内容 `memcpy` 进结构体——结构体成员之间有对齐填充，字段会整个读歪。第三件事是这一整讲都在走向的那一行：在往外拷贝任何东西之前，把每个长度都和文件里剩下的字节比一次，`if (name_len > remaining) return ERROR;`。这一句就是 SPEC 里 Q6 落了地，也是挡住越界读的第一道闸。最后一件事是把内存还回去，成功路径要还，每个错误分支也要还；若一开始就按单出口来写，这件事最不容易漏。

---

## 3. What Counts as Done

> Two earlier lessons each left one sentence behind. One said that handing something in is not the same as proving what you handed in; the other said that writing six decisions down is not the same as someone else computing the same bytes from them. This one adds a third: a skeleton that runs is not the same as a skeleton that can prove it never reads past the end.
>
> So the check is a small, dishonest file. Give your reader twenty bytes whose header claims the player name is 300 bytes long. A correct skeleton returns an error code; it does not crash, and it does not read past those twenty bytes to find out. Then run the same case built with AddressSanitizer and confirm the report is clean. Ask yourself where the program notices: it should be at the comparison between the declared length and the bytes left, before any content is copied, and as long as you have not called `strlen` or `memcpy` first there is nothing to overrun before that point. A reader that reaches for the name before checking its length has already lost, whatever the twenty bytes happen to contain.
>
> Close with three problems on paper: write out the four bytes of `int x = 0x01020304` as this machine stores them, give `sizeof` and `strlen` for `char t[] = "ab"`, and say what `x + 1 > x` answers under `-O2` and under `-O2 -fwrapv` at `2147483647`. Then run the two commands below, whose switches have all been taken apart earlier, and compare what the screen says with what you wrote.
>
> ```bash
> gcc -Wall -Wextra -o d1 d1.c && ./d1
> clang -fsanitize=address -g -o d6_asan d6.c && ./d6_asan
> ```
>
> After this lesson you should be able to say why `byte[0]` of `0x01020304` is `04`, tell `p` from `&p` without hesitating, explain why a program that "successfully" changes `guard` to 999 is still a bug, keep `sizeof` and `strlen` apart, say what `free` does not do, put undefined behaviour under "the standard says nothing" rather than "it might crash", and point at the exact line where a 300-byte claim is refused by a twenty-byte file.
>
> **Keep one sentence**: a skeleton that runs is not the same as a skeleton that can prove it never reads past the end.

> 前两讲各留过一句话。一句是：交上去了，和能证明自己交对了，是两件事；另一句是：写完六句，和别人照着它算得出同一串字节，是两件事。这一讲再添第三句：骨架能跑，和骨架能证明自己不会读越界，也是两件事。
>
> 所以检验用的是一份作弊文件：给它 20 个字节，头部却声明玩家名字有 300 字节。写对的骨架会返回一个错误码，不崩，也不会为了凑那 300 字节读到 20 字节之外去。然后把同一份输入用 AddressSanitizer 编出来的版本再跑一遍，确认报告是干净的。顺带问自己一句：程序是在第几步发现这件事的？应该是在「声明长度」和「剩余字节」相比的那一步，在拷贝任何内容之前；只要没有先无条件地 `strlen` 或 `memcpy`，在那之前就还没有什么可越界的。反过来，一个先去够名字、再回头查长度的读法，不管这 20 字节里恰好装了什么，都已经输了。
>
> 最后用三道手算题结束：`int x = 0x01020304` 在这台机器上是哪四个字节；`char t[] = "ab"` 的 `sizeof` 和 `strlen` 各是多少；`2147483647` 这个取值下，`x + 1 > x` 在 `-O2` 和 `-O2 -fwrapv` 下各答什么。再跑下面两条命令——里面的开关前面都拆过了——把屏幕上的结果和自己写的对一对。
>
> ```bash
> gcc -Wall -Wextra -o d1 d1.c && ./d1
> clang -fsanitize=address -g -o d6_asan d6.c && ./d6_asan
> ```
>
> 这一讲读完，你应该能说清 `0x01020304` 的 `byte[0]` 为什么是 `04`；能不犹豫地分清 `p` 和 `&p`；能讲明白一个「顺利」把 `guard` 改成 999 的程序为什么仍算 bug；能把 `sizeof` 和 `strlen` 区分开；能说出 `free` 不做哪件事；能把未定义行为归到「标准什么都没说」而不是「可能会崩」；也能指出 20 字节文件拒绝 300 字节声明的，究竟是哪一行。
>
> **最后记住一句**：骨架能跑，和骨架能证明自己不会读越界，是两件事。

> **Hand-in checklist — English template / 英文模板**
> Copy the whole block into the hand-in file. Each answer blank is a bare underline, with no square brackets: write over it and leave none behind, so the file stays easy to read when you come back to it. A commit message in this project is written as `submit(folder): what you did`; the `feat:` form from the earlier lessons is not the format here. The commit line inside the template is only a sample written in that format, not a second rule.

```text
=== WHAT TO HAND IN ===========================================

1. The only path allowed in this merge request
    submits/<handle>/P0/<file name given in the task post>
    (if the task post names a different file, change only the name)

2. Content of the hand-in file
    Copy everything between the two dashed lines into the file.
    The underlines are blanks; no square brackets go into the file.
    Commit format: submit(folder): what you did (not the feat: form).
    The commit line inside is a sample of that format, not another rule.
------------------------------------------------------------
# C11 Skeleton Check

- Four bytes of int x = 0x01020304, read one byte at a time:
  ____

- sizeof and strlen of char t[] = "ab":
  ____

- Output of x+1>x under -O2, and under -O2 -fwrapv (verbatim):
  ____

- The one line that checks a length against the bytes left:
  ____

- Result of the 20-byte file claiming a 300-byte name:
  ____

- Output of the same run under AddressSanitizer (verbatim):
  ____

- Output of gcc -Wall -Wextra -o d1 d1.c && ./d1 (verbatim):
  ____

- Commit message format for this project (not the feat: form):
  submit(folder): what you did

- Sample commit, written in that format (sample only, not the format itself):
  feat: add C11 save reader skeleton

- Commit message I used (write your own in the format above, do not copy the sample):
  ____

- Unexpected entries in git status (none, or list them):
  ____

- One sentence for the merge request description:
  ____
------------------------------------------------------------

3. Also paste into the merge request description
    - the one sentence above

4. NOT in this PR
    .gitignore        <- not part of this submission; leave it alone
    .idea/  .vscode/  caches, editor folders
    compiled binaries (d1.exe, d6_asan.exe, *.o), sample save files
    anything outside submits/<handle>/
============================================================
```

> **交什么，照着填 — 中文模板**
> 整段复制进本次要交的文件。每条横线是填空处，直接把答案写在横线上，**不要留中括号**，以后回头读更清楚。本项目的提交信息写成 `submit(提交的文件夹): 做了什么事情`，前面几讲里的 `feat:` 不是这里的格式；表里那条提交信息只是按这个格式给出的**样例**，不是另一条规矩。

```text
=== 本次要交的东西 ==========================================

1. 合并请求里只允许出现的路径
    submits/<handle>/P0/<任务发布里给的文件名>
    （任务发布若指定了别的名字，只换名字，其余一律不变）

2. 本次文件的内容
    把下面两条虚线之间整段复制进文件
    横线是填空处，文件里不要留下中括号
    提交信息格式：submit(提交的文件夹): 做了什么事情（不是 feat: 形式）
    表里那条提交信息只是按格式写的样例，不是另一条规矩
------------------------------------------------------------
# C11 骨架自检

- int x = 0x01020304 逐字节读出来的四个字节：
  ____

- char t[] = "ab" 的 sizeof 和 strlen：
  ____

- x+1>x 在 -O2 下、以及 -O2 -fwrapv 下的输出（原样）：
  ____

- 把长度和剩余字节相比的那一句：
  ____

- 20 字节文件声明名字 300 字节时的结果：
  ____

- 同一份输入在 AddressSanitizer 下的输出（原样）：
  ____

- gcc -Wall -Wextra -o d1 d1.c && ./d1 的输出（原样）：
  ____

- 本项目的提交信息格式（不是 feat: 形式）：
  submit(提交的文件夹): 做了什么事情

- 按这个格式写的一条样例提交（只是样例，不是格式本身）：
  feat: add C11 save reader skeleton

- 本次提交信息（按上面的格式写自己的，不要照抄样例）：
  ____

- git status 里不是我写的条目（无，或写具体名字）：
  ____

- 我按哪条规矩排除了什么（贴进合并请求描述）：
  ____
------------------------------------------------------------

3. 合并请求描述里另外要贴
    · 上面「我按哪条规矩排除了什么」那一句话

4. 这次明确不交
    .gitignore        ← 不属于本次提交，不要动它
    .idea/  .vscode/  缓存、编辑器目录
    编译产物（d1.exe、d6_asan.exe、*.o）、样例存档文件
    submits/<handle>/ 以外的任何文件
============================================================
```
