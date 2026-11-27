# Conformance Vectors and Fuzzing

## 1. Before You Start: Two Ways to Be Wrong

> This lesson is about two words, conformance and fuzzing. The last lesson ended with a plan, not a program: read the file, take the header apart byte by byte, compare every length with the bytes left before copying anything out, and give the memory back on every path. It also left one cheating file to check the plan, twenty bytes whose header claims a 300-byte name, and said a correct reader must return an error code without reading past the end. We wrote no C, compiled nothing, and never ran that file. Conformance means agreeing with a specification: a conformance vector (`vector`) is one written case, a line of input bytes plus the result the specification says must come out, and `vector` here means one test case, not the arrow from mathematics. Fuzzing means letting a program supply the inputs nobody chose; the program that does it is a fuzzer. One pins down the answer we expect, the other supplies the inputs we would not have picked.
>
> One hand-written cheating file is not enough. We would change the few positions we were staring at while working out the reader, and never think of a file shorter than the header, or a length one byte either side of the bytes remaining. The fuzzer cannot call our decoder by itself, so a small piece of glue code (`glue code`), called a harness, sits between them; libFuzzer fixes the name of the entry point it will call, `LLVMFuzzerTestOneInput`, and what we write is the body of that function, in which we call our decoder. The harness makes no claim about what the format means. That last job belongs to the vectors. Carefulness is not a technique. Two machines are.
>
> A program can be wrong in two directions, and they need different tools. In the first direction it is given an input and answers wrongly: a save with a version of 2 should be refused and is read instead, or a name of 300 bytes is reported as 30. That is a question about meaning, and it is settled by writing the answers down in advance. In the second direction it is given an input and does something the language never allowed: reads one byte past a block, adds two numbers whose sum does not fit, walks off the end of a string with no terminator. That is a question about permission rather than meaning, and it is settled by handing the program a very large number of inputs nobody chose.
>
> The first machine is the vector file. It sounds almost too simple to be worth a lesson: one line of input bytes, one expected result, nothing more. The reason it is worth a lesson is that the line is written against the specification rather than against the code. If you derive your vectors by running your implementation and copying down what it printed, you have not tested anything — you have recorded your own opinion twice, once as code and once as a table. The six sentences came before the code; the vectors have to come from those sentences. This is also why a format specification published by somebody else is worth more than a private one: strangers can compute vectors from it, and strangers are exactly what the code will meet.
>
> Here is a small format and its vectors, so that the shape is concrete before we talk about coverage. The example header is a four-byte marker SVF1, one version byte fixed at 1, and a two-byte little-endian name length, followed by exactly that many name bytes. This header is borrowed only for the example; it was not derived from the six sentences. In your own specification that first field is whatever you wrote down for Q1. Nothing below depends on these particular bytes, and every sentence still holds if you substitute yours.
>
> ```text
> # input bytes (hex)                                   expected result
> 53 56 46 31 01 02 00 61 62                          0   # valid, name="ab"
> 53 56 46 31 01 00 00                                0   # valid, empty name
> 00 56 46 31 01 00 00                                1   # wrong marker
> 53 56 46 31 02 00 00                                2   # version 2, we only read 1
> 53 56 46 31 01 2c 01 61 62 63 64 65 66 67 68       3   # claims 300 bytes, only 8 name bytes follow
> ```
>
> The last line is the one from the previous lesson, now written down as data instead of as a paragraph. Notice that it carries an expected number and not just "an error": refusing is not enough, the refusal has to be the refusal the specification names. A reader that returns 3 on a bad marker and 1 on a truncated file passes any test that only asks "did it fail?", and fails a caller that branches on the code to decide whether to show the user "this file is not a save" or "this file is damaged". Error codes are part of the interface, and an interface is the specification's business. That is why every error branch you wrote in the previous lesson (the marker check, the version check, the length check) needs at least one vector that enters it, and why a vector whose expected value is a success is not enough on its own.
>
> Running the file is deliberately dull: one line per vector, a summary, and a non-zero exit status if anything disagreed.
>
> ```text
> ok   line 2: 0  (9 bytes in)
> ok   line 3: 0  (7 bytes in)
> ok   line 4: 1  (7 bytes in)
> ok   line 5: 2  (7 bytes in)
> ok   line 6: 3  (15 bytes in)
>
> 5/5 vectors passed
> ```
>
> Five vectors is a floor, not a target. Three kinds deserve a place. First, an ordinary success, so that the happy path is pinned down. Second, one vector per error code, so that no branch is dead and no two branches return the same number. Third, the boundaries, because boundaries are where specifications and implementations drift apart without either side noticing: a length of zero, a length exactly equal to the bytes remaining, a length one greater than the bytes remaining, and a file of exactly the header size with nothing after it. Each of those four is a place where an implementation can be off by one and still pass your happy-path examples. Writing them down forces you to decide, in the specification, what happens at the edge — and a decision made now in a table is much cheaper than a decision discovered later by a crashed reader on somebody else's machine.
>
> Even all of those are inputs we chose. What the fuzzer adds is a corpus of inputs: it mutates them at random, runs each result through your code, and keeps any input that reaches a piece of code no earlier input reached. It does not know what your format means, which is precisely the point: it explores exactly the region your attention did not cover. Why that corpus cannot be empty comes back below.
>
> The interface is one function, and everything else is the fuzzer's business. The parser called inside is yours; this lesson calls it `svf_decode`, and if yours is called `load_save`, that is the only word that changes. Here is the whole function we have to write:
>
> ```c
> #include <stdint.h>
> #include <stdlib.h>
> #include "svf.h"
>
> int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
>     char *name = NULL;
>     size_t name_len = 0;
>     if (svf_decode(data, size, &name, &name_len) == SVF_OK)
>         free(name);
>     return 0;
> }
> ```
>
> That is the whole harness: no loop, no input file, no arguments. The fuzzer calls it thousands of times a second, each call with a new buffer, and a crash inside is the report. The `free` is not decoration either — a harness that leaks on every call becomes a memory-exhaustion test rather than a parser test, and the leak will be reported as if it were your decoder's fault.
>
> A fuzzer needs somewhere to start. Given an empty corpus, the mutation engine has to invent the four marker bytes S, V, F, 1 from nothing, and landing those four specific bytes in the first four positions is a one-in-four-billion accident before any length byte can even matter. The measurement is blunt: from an empty corpus this example reached coverage 5 and ran 3000 executions without a single crash, because it never once produced a valid header to mutate. Hand it one valid nine-byte file and the same binary finds a real bug within a few thousand runs. A seed file is not a convenience, it is the difference between a fuzzer and a random number generator.
>
> Here is what that looks like when the decoder is written the wrong way round, allocating first and comparing later, the exact mistake the previous lesson warned about. The fuzzer changed one length byte, and the copy ran off the end of the input buffer.
>
> ```text
> ERROR: AddressSanitizer: heap-buffer-overflow on address 0x120a0e9215f9 ...
> READ of size 2306 at 0x120a0e9215f9 thread T0
>     #0 ... in __asan_memcpy
>     #1 ... in svf_decode svf.c:21
>     #2 ... in LLVMFuzzerTestOneInput fuzz_svf.c:8
> artifact_prefix='crash-'; Test unit written to crash-d791bed504c749cc8bd8b80ce0d512a8bd8d5a60
> 0x53,0x56,0x46,0x31,0x1,0x2,0x9,0x61,0x62,
> SVF1\001\002\011ab
> ```
>
> Read that report slowly, because it contains more than a bug. `READ of size 2306` is the byte count the copy attempted, and 2306 is `0x0902` — the two length bytes after mutation. The header said two thousand three hundred and six, the file held two bytes of name, and the code believed the header. The chain `#1 svf_decode svf.c:21` names the line, which is why the build keeps `-g`. And the last three lines are the part people forget to keep: the artifact is a file on disk whose name is a hash of its contents, followed by the bytes in hexadecimal and in escaped ASCII. A crash you cannot reproduce is an anecdote; those three lines are what make it evidence.
>
> Reproducing it is the next thing to get right, and this is where a sentence like "we fixed the seed" turns out to be half a promise. Two runs with the same `-seed=1000` but different starting corpora produced two different crashes, because the seed fixes the sequence of mutations, not the material being mutated. Two runs with the same seed and an identical corpus produced the identical artifact hash. So a reproducible fuzz run is a triple: the binary, the seed, and the corpus. Commit the seed and the corpus, or the third party who reruns your command gets a different report and concludes you were making it up.
>
> One more failure mode is worth naming before the assignment, because it happened while this lesson was being written. The first version of the harness asserted that no name may contain a zero byte, and aborted if one did. The specification said nothing of the kind — a name of two bytes, `a` and `0x00`, is perfectly legal data. The fuzzer found it in seconds and reported a deadly signal with a stack trace pointing at the assertion, not at the decoder. A fuzz crash means one of the two has a bug: the implementation, or the harness. Learning to tell them apart is most of the skill, and the tell is usually that the stack stops in your own `assert` rather than in the code that reads bytes.
>
> The compiler on this line deserves a paragraph of its own, because the last lesson only named it. LLVM is not a command you type; it is a collection of compiler parts, a front end that turns C or C++ into an intermediate form, an optimiser that works on that form, and a back end that turns it into machine code, together with runtime libraries such as AddressSanitizer and the fuzzing engine. `clang` is the C and C++ front end built on LLVM, and it is the name you type; `gcc` belongs to a separate toolchain of its own. That is why the AddressSanitizer run in the last lesson worked under `clang`: those checkers ship with LLVM, and `clang` links them through the same `-fsanitize=` switch. It is also why this lesson changes compiler rather than just changing a flag. `-fsanitize=fuzzer` asks for libFuzzer, the engine that mutates inputs and calls your harness; it lives in LLVM/clang, and `gcc` has no such library. So `unknown argument: '-fsanitize=fuzzer'` from another toolchain is a missing part, not a command written wrongly. Picking the compiler that owns the tool is the whole decision.
>
> Now the switches on that line can be taken apart, one by one. `-fsanitize=fuzzer` compiles the harness and links the fuzzing engine, `-fsanitize=address` adds the memory checker, `-g` keeps the line numbers that made the report readable, `-Iinclude` tells both source files where to find `svf.h`, and `-o fuzz_svf` names what comes out. On the run line, `-runs=20000` caps how many inputs are tried, `-seed=1000` fixes the sequence of mutations, `-max_len=64` caps how long a single input may grow, and `-artifact_prefix=crash-` fixes the name a saved crash gets. Manuals list these one by one and rarely say what several of them do together: `-fsanitize=fuzzer,address` is two checkers in one switch, and `-g` is what turns an address into `svf.c:21`.
>
> ```bash
> clang -Iinclude -fsanitize=fuzzer,address -g -o fuzz_svf fuzz/fuzz_svf.c src/svf.c
> mkdir out          # PowerShell: New-Item -ItemType Directory out
> ./fuzz_svf out seeds -runs=20000 -seed=1000 -max_len=64 -artifact_prefix=crash-
> ```
>
> The two directory arguments look like a detail and are not. The first is where the fuzzer may write the inputs it discovers; the second is read-only. Point the fuzzer at `seeds/` alone and it will quietly write its findings into your seed directory, so the next run starts from a different corpus and ends with a different report — the reproducibility failure described above, arriving through the command line instead of through the seed.
>
> On Windows the official LLVM package carries both runtimes, and the same two commands work from PowerShell once `clang` is on PATH (`winget install LLVM.LLVM` installs it); the binary may print one `interception_win: unhandled instruction` line at startup and then proceed normally, which is a known noise line rather than a failure. If your toolchain says `unknown argument: '-fsanitize=fuzzer'`, that is the missing part described above: pick the compiler that owns the tool instead of fighting the one that does not.
>
> Finally, what the fuzzer does not do. It does not know that version 2 must be refused, so it will never report a reader that accepts it. It does not know that a name of 300 bytes in a short file must produce code 3 rather than code 1. It reports only the failures the machine itself can see: a crash, a memory error, a hang. Meaning is the vectors' job, and the two tools divide the work the same way the previous lesson divided "it ran" from "it is right". A green fuzz run says the program was not broken by twenty thousand inputs; it does not say the program is correct.

> 这一讲讲两样东西：conformance 和 fuzzing。上一讲收尾留下的是一份打算，不是一个程序：读文件、逐字节拆头部、往外拷贝前把每个长度和剩余字节比一次、每条路径都把内存还回去；还留了一份作弊文件用来检验它，20 个字节，头部却声明名字有 300 字节，写对的读取器得返回错误码，不能读到文件之外去。我们没写一行 C，什么都没编译，那份文件也没跑过。conformance 是「符合规范」；一条 conformance 向量（vector）就是写下来的一个用例：一行输入字节，加上规范规定必须出现的结果，这里的 vector 是「一条用例」，不是数学里带箭头的那个。fuzzing 是让程序送来没人挑过的输入，干这件事的程序叫 fuzzer。一个把该得到的答案钉住，一个送来我们不会挑的输入。
>
> 自己写的那一份作弊文件不够。我们只会改动推导读取器时盯着的那几位，想不到一个比头部还短的文件，也想不到长度恰好卡在剩余字节上下差一的那几种。fuzzer 不会自己来调解码器，中间要一小段胶水代码（glue code），叫 harness；libFuzzer 把要调的入口函数名定成 `LLVMFuzzerTestOneInput`，改不了，我们要做的是按自己的解码器把函数体写一遍，在里面调它。harness 对格式是什么意思一个字都不判断，那是向量的活。小心不是一种技术，两台机器才是。
>
> 一个程序会往两个方向错，两个方向要两套工具。第一个方向是有输入、答错了：版本号是 2 的存档本该拒绝，结果被读了进去；声明 300 字节的名字，报出来只剩 30 字节。这是「意思」的问题，办法是提前把答案写下来。第二个方向是有输入、做了语言根本不允许的事：读到了块外一个字节，把两个装不下的数加起来，走在一条没有结尾零的字符串上。这是「许可」的问题，不是「意思」的问题，办法是丢给它一大堆没人挑过的输入。
>
> 第一台机器是那份向量文件。听起来简单得不像值得单独讲一讲：一行输入字节，一个期望结果，再没有别的。它值得讲，恰恰因为这一行是照着规范写的，不是照着代码写的。如果你是跑一遍自己的实现、把打印出来的东西抄成表，那你什么都没测——你只是把自己的看法记了两遍，一遍记成代码，一遍记成表格。六句话在代码之前；向量也只能从这六句话里长出来。这也是为什么别人公开的格式规范比私房规范值钱：陌生人能照着它算出向量，而代码将来要面对的正是陌生人。
>
> 先摆一个很小的格式和它的向量，看着具体些。示例头部是四字节标记 SVF1、一字节固定为 1 的版本、两字节小端的名字长度，后面紧跟恰好这么多字节的名字。这个头只是临时借来举例的，不是从那六句话里推出来的；你自己的规范里，开头那一格填的是你 Q1 写下的字节。下面没有一句依赖这几个具体数字，换成你的字段照样成立。
>
> ```text
> # 输入字节（hex）                                      期望结果
> 53 56 46 31 01 02 00 61 62                          0   # 合法，名字 "ab"
> 53 56 46 31 01 00 00                                0   # 合法，空名字
> 00 56 46 31 01 00 00                                1   # 标记错
> 53 56 46 31 02 00 00                                2   # 版本 2，我们只读 1
> 53 56 46 31 01 2c 01 61 62 63 64 65 66 67 68       3   # 声明 300 字节，名字只有 8 字节
> ```
>
> 最后一行就是上一讲那条作弊文件，只不过这回它是一行数据，不再是一段话。注意它带的是一个期望数字，不是一句「会报错」：拒绝还不够，得是指定的那种拒绝。一个「标记错返回 3、文件被截断返回 1」的读取器，能通过任何只问「它失败了吗」的测试，却会让按错误码决定「这不是存档」还是「这存档坏了」的调用方彻底乱套。错误码是接口的一部分，而接口是规范该管的事。所以你上一讲写的每一个错误分支（标记检查、版本检查、长度检查）都至少要有条向量能走进它；只有期望值为成功的那几条，一个分支都覆盖不到。
>
> 跑起来故意弄得很枯燥：一条向量一行输出，一行汇总，有对不上的就以非零码退出。
>
> ```text
> ok   line 2: 0  (9 bytes in)
> ok   line 3: 0  (7 bytes in)
> ok   line 4: 1  (7 bytes in)
> ok   line 5: 2  (7 bytes in)
> ok   line 6: 3  (15 bytes in)
>
> 5/5 vectors passed
> ```
>
> 五条是下限，不是目标。三类值得占位置。第一类是一条普通成功，把顺畅路径钉住。第二类是每个错误码一条，让没有分支是死的，也没有两个分支吐出同一个数字。第三类是边界，因为边界正是规范和实现悄悄走散、两边都没察觉的地方：长度为零、长度恰好等于剩余字节、长度比剩余字节多一、以及一个正好只有头部那么大的文件。这四种每一种都是「差一个」还能通过你那些顺利样例的位置。把它们写下来，等于逼自己在规范里决定边界上到底发生什么；在表里做决定，比日后在别人机器上崩一次再发现廉价得多。
>
> 可这些仍然都是我们挑的。fuzzer 多给的东西是语料库（corpus）：它维护一批输入，随机变异，把每个结果喂给你的代码，凡是走到过新代码的输入就留下来。它不知道你的格式是什么意思，而这正是重点：它探索的恰好是你注意力没覆盖到的那一块。语料库为什么不能空着，后面还会回来讲。
>
> 接口只有一个函数，其余都是 fuzzer 的事。里面调的那个解析函数是你自己的，这一讲叫它 `svf_decode`；你要是叫 `load_save`，要改的也只有这一个词。下面就是我们要写的整个函数：
>
> ```c
> #include <stdint.h>
> #include <stdlib.h>
> #include "svf.h"
>
> int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
>     char *name = NULL;
>     size_t name_len = 0;
>     if (svf_decode(data, size, &name, &name_len) == SVF_OK)
>         free(name);
>     return 0;
> }
> ```
>
> 整个 harness 就这样：没有循环，没有输入文件，没有参数。fuzzer 每秒调它几千次，每次一块新缓冲区，里面崩了就是报告。那个 `free` 也不是装饰——每次调用都漏的 harness 会变成内存耗尽测试，而这份漏会被报成你解码器的罪。
>
> fuzzer 得有个起点。语料库空着的时候，变异引擎要从零把 S、V、F、1 这四个标记字节凭空造出来，而让这四个特定字节落在开头四个位置上，是四十多亿分之一的偶然——那时长度字节还根本没轮到。实测很直白：空语料下这个例子只跑到覆盖率 5，执行 3000 次一次没崩，因为它压根没造出过一个合法头部可供变异。给它一个合法的九字节文件，同一个二进制几千次之内就抓到了真 bug。种子文件（seed）不是便利设施，它是 fuzzer 和随机数生成器之间的分界线。
>
> 当解码器写成反的，先分配、后比较，也就是上一讲警告过的那个错，它长这样。fuzzer 只改了一个长度字节，拷贝就冲出了输入缓冲区。
>
> ```text
> ERROR: AddressSanitizer: heap-buffer-overflow on address 0x120a0e9215f9 ...
> READ of size 2306 at 0x120a0e9215f9 thread T0
>     #0 ... in __asan_memcpy
>     #1 ... in svf_decode svf.c:21
>     #2 ... in LLVMFuzzerTestOneInput fuzz_svf.c:8
> artifact_prefix='crash-'; Test unit written to crash-d791bed504c749cc8bd8b80ce0d512a8bd8d5a60
> 0x53,0x56,0x46,0x31,0x1,0x2,0x9,0x61,0x62,
> SVF1\001\002\011ab
> ```
>
> 这份报告值得慢慢看，因为它装的不只是一个 bug。`READ of size 2306` 是拷贝试图读的字节数，而 2306 就是 `0x0902`——变异后的那两个长度字节。头部说两千三百零六，文件里只有两个名字字节，代码信了头部。`#1 svf_decode svf.c:21` 那一条链指出了行号，这就是编译时留 `-g` 的原因。最后三行是大家常常忘记保留的：崩溃现场（artifact）是磁盘上的一个文件，文件名是内容的哈希；后面跟着它的十六进制和转义后的样子。复现不了的崩溃只是个故事；这三行才把它变成证据。
>
> 下一步是复现，而「我们固定了 seed」这句话在这里会露馅：它只是一半的承诺。同样的 `-seed=1000`、不同的起始语料，两次跑出两个不同的崩溃，因为 seed 固定的是变异序列，不是被变异的材料。同样的 seed、一模一样的语料，两次跑出同一个 artifact 哈希。所以一次可复现的 fuzz 是三件套：二进制、seed、语料库。seed 和语料都要入库，否则照着你的命令重跑的第三个人会拿到另一份报告，然后认为你在编。
>
> 还有一种翻车值得在布置作业前说清，因为它就发生在写这一讲的时候。harness 的第一版断言「名字里不许出现零字节」，出现就 abort。规范里根本没有这一条——两字节的名字，`a` 和 `0x00`，是完全合法的数据。fuzzer 几秒钟就找到了它，报了一个 deadly signal，调用栈指在那个断言上，不在解码器上。fuzz 报崩，意味着两者之一有 bug：实现，或者 harness。分辨这两者是这门手艺的大半，而线索通常是栈停在你自己的 `assert` 里，而不是停在读字节的代码里。
>
> 这一行上的编译器值得单独说一段，因为上一讲只点过它的名字。LLVM 不是一条要敲的命令，它是一套编译器的零件：前端把 C、C++ 翻成中间表示，优化器改这份表示，后端再把它变成机器码；AddressSanitizer、fuzzing 引擎这些运行库也跟着它一起发。`clang` 是架在 LLVM 上的 C/C++ 前端，也就是你敲进终端的那个名字；`gcc` 是自成一套的另一家。上一讲那条 ASan 命令在 clang 下跑得通，原因就在这里：这些检查器随 LLVM 一起发，clang 用同一个 `-fsanitize=` 开关就能把它们链进来。这一讲换编译器，也不是为了换个牌子。`-fsanitize=fuzzer` 要的是 libFuzzer，那个负责变异输入、反复调用 harness 的引擎，它长在 LLVM/clang 里，gcc 没有这个库。所以别处看到 `unknown argument: '-fsanitize=fuzzer'`，是工具链里少了零件，不是命令写错。挑一个自带这个工具的编译器，就是全部决定。
>
> 现在可以把这一行上的开关逐个拆开了。`-fsanitize=fuzzer` 编译 harness 并链接 fuzzing 引擎，`-fsanitize=address` 加上内存检查器，`-g` 保留那些让报告可读的行号，`-Iinclude` 告诉两个源文件去哪儿找 `svf.h`，`-o fuzz_svf` 给编出来的东西起名字。运行那行上，`-runs=20000` 定下一共试多少次，`-seed=1000` 固定变异序列的起点，`-max_len=64` 定下单个输入最长能长到多少字节，`-artifact_prefix=crash-` 定下存下来的崩溃文件叫什么前缀。手册把每个开关单列一行，很少写几个连起来会是什么效果：`-fsanitize=fuzzer,address` 是把两个检查器写进同一个开关，而 `-g` 才让一个地址变成 `svf.c:21`。
>
> ```bash
> clang -Iinclude -fsanitize=fuzzer,address -g -o fuzz_svf fuzz/fuzz_svf.c src/svf.c
> mkdir out          # PowerShell 里是 New-Item -ItemType Directory out
> ./fuzz_svf out seeds -runs=20000 -seed=1000 -max_len=64 -artifact_prefix=crash-
> ```
>
> 那两个目录参数看着是个细节，其实不是。第一个是 fuzzer 可以写入它发现的新输入的地方，第二个是只读的。只把 `seeds/` 丢给它，它会悄悄把找到的东西写回你的种子目录，下一次跑就从另一个语料库起步，最后给出另一份报告——这正是上面说的复现失败，只不过是从命令行钻进来的，不是从 seed 钻进来的。
>
> 在 Windows 上，官方 LLVM 包两个运行库都带，clang 进了 PATH 之后同样两条命令在 PowerShell 里就能跑（`winget install LLVM.LLVM` 装的就是它）；程序启动时可能多打一行 `interception_win: unhandled instruction`，然后照常继续，那是已知的噪音行，不是失败。要是你的工具链打出 `unknown argument: '-fsanitize=fuzzer'`，那就是上面说的少了零件：该换到自带这个工具的编译器上，别跟没有的那个较劲。
>
> 最后是 fuzzer 不做什么。它不知道版本 2 必须被拒绝，所以它永远不会报告一个接受了版本 2 的读取器；它不知道一个短文件里声明 300 字节必须给错误码 3 而不是 1。它只报机器自己看得见的失败：崩溃、内存错误、卡死。意思是向量的活，两个工具的分工和上一讲把「跑通了」和「是对的」分开，是同一刀。fuzz 全绿只说明程序没被两万个输入弄坏，不说明程序是对的。

---

## 2. The Assignment: Make the Machine Say No

> The work now splits into three jobs that answer three different questions. The vectors answer "does it mean what the specification says". The harness answers "can it be broken". The runner answers "can somebody else see the two answers without asking me". None of these files exists yet. The last lesson left four steps and one cheating file on the page, not a line of C, so this is the first lesson that puts code into the repository rather than into a hand-in file. The tree below is not something we are picking up from last time: it is the layout we are going to build in this lesson, fixed once and kept, so that when this stage becomes a published repository later the whole directory moves without a path changing.
>
> ```text
> savefmt/
> ├── include/svf.h
> ├── src/svf.c          the decoder, written now from those four steps
> ├── tests/vectors.txt   one line per case
> ├── tests/run_vectors.c the runner
> ├── fuzz/fuzz_svf.c     the harness
> └── seeds/valid_ab      nine bytes, so the fuzzer has a header to mutate
> ```
>
> One thing to settle before writing any of it: the decoder has to be a function that takes bytes and a length, not a program that opens a file and prints. The four steps from the last lesson put `fopen` and `fread` at the front, but from the very first line of code keep that reading in `main` and put the part that walks the header straight into a function with the signature the harness calls. Do not write it as one block and then split it later. That choice is not cosmetic. It is the difference between something a fuzzer can feed and something only a human can run.
>
> `vectors.txt` has one rule and one freedom. The rule: bytes in hexadecimal, separated by spaces, then the expected code as the last token on the line, and anything after `#` is a comment. The freedom: the codes are yours to name, as long as the header file names them the same way — `SVF_OK`, `SVF_ERR_MAGIC`, `SVF_ERR_VER`, `SVF_ERR_TRUNC` in the example. What is not free is the number of vectors. Cover every error branch your decoder has, both sides of every comparison it makes, and at least one success on each path that copies something out. Eight to twelve lines is the usual size for a header this small; if you find yourself with three, you have written examples rather than vectors.
>
> The runner is not allowed to stop at the first failure. A run that halts on line 2 tells you nothing about lines 3 to 12, and you will be fixing one thing at a time until the evening ends. Read every line, print one line per case, count, and return non-zero at the end if any disagreed — the same shape every test runner in every ecosystem has, and the reason a CI job can be built on top of it by adding one line to a workflow file.
>
> ```bash
> gcc -Wall -Wextra -Iinclude -o run_vectors tests/run_vectors.c src/svf.c && ./run_vectors tests/vectors.txt
> ```
>
> `-Iinclude` is not optional: both the runner and the decoder include `svf.h`, and that switch is what tells the compiler where to look for it. Leave it out and the first thing you see is `fatal error: svf.h: No such file or directory` — a path problem wearing the costume of a missing file.
>
> The harness is the ten lines above, no more. Its only job is to give the decoder a buffer and clean up after it. Resist the urge to assert things inside it: every assertion you add is a claim about the specification, and a wrong claim there produces a crash report that accuses your decoder of a mistake you made in the harness. If you want a semantic check, it belongs in `vectors.txt`, where it can be seen, discussed and corrected.
>
> Then, and this is the part that matters, break your own decoder on purpose. Keep the correct comparison in place, and add a second build behind a macro — allocate first, compare afterwards, one line moved. `-D` is the switch that defines a macro at compile time, so `-DALLOC_FIRST` turns the bad branch on without touching the source file, and you can build both versions from the same tree. Build that version with the fuzzer and run it until it reports. You are not looking for the bug, you already know where it is; you are looking for the shape of the report, the line `#1 ... in svf_decode`, the artifact name, and the three lines of bytes at the bottom. A student who has read a crash report once will read the next one in a minute; a student who has only seen screenshots of one will stare at it for an hour.
>
> ```bash
> clang -Iinclude -fsanitize=fuzzer,address -g -DALLOC_FIRST -o fuzz_buggy fuzz/fuzz_svf.c src/svf.c
> mkdir out
> ./fuzz_buggy out seeds -runs=5000 -seed=1000 -max_len=64 -artifact_prefix=crash-
> ```
>
> Keep the seed file. It is nine bytes, it is not embarrassing, and without it you will spend the evening watching a fuzzer fail to guess the word SVF1. Commit it under `savefmt/seeds/`, and commit the seed number and the run count in your hand-in, because those three together are what makes the run repeatable. The `out/` directory and the `crash-*` artifacts stay out of the repository: they are the fuzzer's scratch space, and a committed crash artifact is a blob of bytes nobody can read without the run that produced it. Then rerun the same command a second time from an identical corpus and confirm you get the same artifact hash. If the hash differs, something in the corpus changed between runs and you should say so rather than pretend the seed did the job.
>
> When you are done, put the correct build back, run the vectors once and the fuzzer once, and paste both outputs into the hand-in. The hand-in itself stays a single markdown file — the code lives in the repository, the evidence lives in the file, and the merge request carries both. Format the C files before you commit: `clang-format --dry-run --Werror` is what the CI job runs, where `--dry-run` means look but do not rewrite, and `--Werror` means any formatting difference counts as an error instead of a warning. Running it yourself first is faster than waiting for a red pipeline to tell you the same thing.

> 现在的活分成三份，各回答一个问题。向量回答「它的意思是不是规范说的那个」；harness 回答「它能不能被弄坏」；runner 回答「别人能不能不问我就看到这两个答案」。这些文件现在一个都还没有。上一讲留在纸上的是四步和一份作弊文件，不是一行 C 代码，所以这一讲才是第一次把代码放进仓库，而不是放进作业文件。下面这棵树不是从上一讲接过来的东西，是这一讲要一起搭出来的结构，一次定好、以后不改，这样这一阶段日后变成公开仓库时，整目录搬走，路径一个都不用改。
>
> ```text
> savefmt/
> ├── include/svf.h
> ├── src/svf.c          这一讲按那四步写出来的解码器
> ├── tests/vectors.txt  一条一行
> ├── tests/run_vectors.c runner
> ├── fuzz/fuzz_svf.c     harness
> └── seeds/valid_ab     九字节，让 fuzzer 有个真头部可变异
> ```
>
> 写第一行代码之前先定一件事：解码器得是个「吃字节和长度」的函数，不是个自己打开文件再打印的程序。上一讲那四步把 `fopen`、`fread` 摆在最前面，但从写第一行起，就把读文件留在 `main`，走头部的那一段直接放进 harness 要调的那个签名的函数里。别先写成一整块、事后再回头拆。这个分别不是摆样子：它决定了这东西是能被 fuzzer 喂的，还是只有人能跑的。
>
> `vectors.txt` 只有一条规矩和一处自由。规矩：十六进制的字节，空格隔开，最后一个 token 是期望的错误码，`#` 之后是注释。自由：错误码叫什么由你定，只要头文件用同一套名字——示例里是 `SVF_OK`、`SVF_ERR_MAGIC`、`SVF_ERR_VER`、`SVF_ERR_TRUNC`。不自由的是向量的条数：解码器每个错误分支至少一条，每处比较的两边都各要有一条，每条往外拷贝数据的路径至少一条成功用例。这么小的头部，八到十二条是常见规模；如果你数出来只有三条，那你写的是例子，不是向量。
>
> runner 不许在第一个失败处停下。跑到第二行就退出的运行，对第三到第十二行什么都没说，所以你会一个一个修到深夜。逐行读完、每条打印一行、统计、最后有分歧就以非零码退出——这是每个生态里每个测试 runner 的同一个形状，也是为什么 CI 只需要在工作流里加一行就能骑在它上面。
>
> ```bash
> gcc -Wall -Wextra -Iinclude -o run_vectors tests/run_vectors.c src/svf.c && ./run_vectors tests/vectors.txt
> ```
>
> `-Iinclude` 不可省：runner 和解码器都要 `#include "svf.h"`，这个开关就是告诉编译器去哪儿找它。少了它，你第一眼看到的是 `fatal error: svf.h: No such file or directory`——看着像文件丢了，其实是没把路径给编译器。
>
> harness 就是上面那十行，不要更多。它唯一的职责是把缓冲区交给解码器、然后收尾。别往里面塞断言：你加的每一条断言都是一个关于规范的断言，而断言写错，产出的崩溃报告就会拿你自己在 harness 里的错去指控解码器。想做语义检查，放到 `vectors.txt` 里——那里看得见、讨论得了、改得动。
>
> 然后是最要紧的一步：故意把自己的解码器弄坏。正确的比较留着，用宏切出第二个版本——先分配、后比较，只挪一行。`-D` 是编译时定义一个宏的开关，所以 `-DALLOC_FIRST` 不用改源文件就把那条坏分支打开，同一份代码能编出两个版本。用 fuzzer 编这个版本，一直跑到它报出来。你不是在找 bug，你早知道它在哪；你是在看报告长什么样：`#1 ... in svf_decode` 那行、artifact 的名字、末尾那三行字节。读过一次真报告的人，下一次一分钟就读完；只看过报告截图的人，会盯着它看一小时。
>
> ```bash
> clang -Iinclude -fsanitize=fuzzer,address -g -DALLOC_FIRST -o fuzz_buggy fuzz/fuzz_svf.c src/svf.c
> mkdir out
> ./fuzz_buggy out seeds -runs=5000 -seed=1000 -max_len=64 -artifact_prefix=crash-
> ```
>
> 种子文件留着。它九字节，不丢人，没有它你今晚就只能看着 fuzzer 猜不出 SVF1 这四个字母。把它提交到 `savefmt/seeds/`，把 seed 数字和运行次数写进作业里，因为这三样加起来才让这次运行可重复。`out/` 目录和 `crash-*` 那些 artifact 不进仓库：它们是 fuzzer 的草稿纸，而一份提交进库的崩溃 artifact，是一坨没有那次运行就没人能读懂的字节。然后用一份一模一样的语料把同一条命令再跑一遍，确认拿到同一个 artifact 哈希。如果哈希不一样，说明两次之间语料被改过，那你该如实说出来，而不是假装 seed 已经把活干完了。
>
> 收工时把正确版本换回来，向量跑一遍、fuzzer 跑一遍，两份输出都贴进作业。作业本身仍然是一个 markdown 文件——代码住在仓库里，证据住在文件里，合并请求一次带上两样。提交前先格式化 C 文件：`clang-format --dry-run --Werror` 就是 CI 那一行要跑的东西，`--dry-run` 是只看不改，`--Werror` 是把任何格式差异都当成错误而不是警告。自己先跑一遍，比等一条红色流水线来告诉你同一件事要快得多。

---

## 3. What Counts as Done

> Three things, in order of how easy they are to fake. First, the vectors: the file covers every error code and both sides of every comparison, the runner prints them all, and none of them was produced by running the code and copying the output. Second, the fuzz run: the correct build survives twenty thousand executions with no report, and the broken build produces one, on purpose, with an artifact you kept. Third, the reproduction: the command in your hand-in, run by someone else with the corpus in the repository, gives the same hash.
>
> The sentence this lesson leaves behind is the one that separates a test from a demonstration: a test you wrote yourself proves your implementation matches your imagination; a vector proves it matches the specification. Everything else here is a consequence. The vector's authority comes from being derived from the six sentences, not from the code. The fuzzer's authority comes from choosing inputs you would not have chosen. And the seed's authority comes only from being paired with the corpus — alone it is a promise, together they are a recipe.
>
> Be able to say, out loud and without opening a file: why an error code is part of the specification and not an implementation detail; which four boundary cases a length check has, and what each of them is for; why a fuzzer given an empty corpus is nearly useless on a format with a magic word; why the stack trace pointing at your own `assert` means the harness is the suspect; and why "same seed" without "same corpus" does not reproduce anything.
>
> One practical note before the checklist: write the commit message in the course format, and keep the `feat:` line in the template as a reminder of how real projects write theirs.
>
> **Keep one sentence**: a test you wrote yourself proves your implementation matches your imagination; a vector proves it matches the specification.
>
> Next lesson: this one separated "right" from "not broken"; it did not yet let anyone use what you built. The next one leaves the course repository: a README for `savefmt/` that explains why the format is shaped this way, a `v0.1.0` tag, and a public repository a stranger can read, build, and run the vectors against — which is where P0 closes. See you there.

> 三件事，按「多容易被糊弄」排序。第一，向量：文件覆盖了每个错误码、每处比较的两边，runner 把每一条都打了出来，而且没有一条是「跑一遍代码把输出抄下来」得来的。第二，fuzz：正确版本跑完两万次没有报告，坏版本在你故意留下它的地方报出一次，artifact 你留着。第三，复现：作业里那条命令，换别人在仓库里带着语料跑一遍，拿到同一个哈希。
>
> 这一讲留下的一句话，是把「测试」和「演示」分开的那一句：自己写的测试证明的是实现符合你的想象，向量证明的才是实现符合规范。别的都是它的推论。向量的权威来自它从六句话里长出来，不是从代码里抄出来；fuzzer 的权威来自它挑了你不会挑的输入；而 seed 的权威只在和语料配对时才成立——单独一个 seed 是句承诺，两样合起来才是配方。
>
> 要能不打开文件就讲清：为什么错误码属于规范而不是实现细节；长度检查有哪四个边界用例、各自是干什么的；为什么给一个带魔法字的格式配空语料，fuzzer 基本等于没用；为什么栈停在你自己的 `assert` 上时，嫌疑人是 harness；以及为什么只有「同 seed」没有「同语料」，什么都复现不了。
>
> 填表前提醒一句：提交信息按课程格式写；表单里那条 `feat:` 是真实项目写法的样例，留着认一认，别照它交。
>
> **最后记住一句**：自己写的测试证明的是实现符合你的想象，向量证明的才是实现符合规范。
>
> 下一讲：这一讲把「对」和「没崩」分开了，但还没让任何人能用你的东西。下一讲走出课程库：给 `savefmt/` 写 README 讲清「为什么这样设计」，打上 `v0.1.0`，让它成为一个陌生人点进来能读懂、能编译、能跑通向量的公开仓库——P0 就在这里收口。下一讲见。

> **Hand-in checklist — English template / 英文模板**
> Copy the whole block into the hand-in file. Each answer blank is a bare underline, with no square brackets: write over it and leave none behind. The code goes into the repository under `savefmt/`; this file carries the evidence. This course writes commit messages as `submit(folder): what you did`; a real open-source project uses a lowercase English type such as `feat:` instead, and the template keeps one line as a sample of that convention — it is not the format for this hand-in.

```text
=== WHAT TO HAND IN ===========================================

1. The only paths allowed in this merge request
    submits/<handle>/P0/CONFORMANCE.md
    savefmt/  (decoder, vectors, runner, harness, seed file)
    Nothing else.

2. Content of the hand-in file
    Copy everything between the two dashed lines into the file.
    The underlines are blanks; no square brackets go into the file.
    Answer in English only, one line per blank. No Chinese, no brackets.
    Commit format here: submit(folder): what you did — one line, English.
    The feat: line below shows the real-community convention; both are kept.
    Write your own in the course format.
------------------------------------------------------------
# Conformance and Fuzz Check

## Vectors

- How many vectors, and which error codes they cover:
  ____

- The four boundary cases and the expected code for each:
  ____

- `./run_vectors tests/vectors.txt` output, verbatim:
  ____

## Fuzzing

- The correct build, command and result:
  ____

- The broken build: what you changed, and the first four lines of the report:
  ____

- Artifact hash and the input bytes (hex):
  ____

- Replay command, and whether the second run gave the same hash:
  ____

## Submission

- Commit message format for this course:
  submit(folder): what you did

- Community convention, kept as a sample (not the format for this hand-in):
  feat: add conformance vectors and fuzz harness

- Commit message I used (write in the course format, do not copy the sample):
  ____

- Which files are code and which are evidence:
  ____

- `git status` entries that are not mine (none, or name them):
  ____

- What I excluded by which rule (paste into the merge request description):
  ____
------------------------------------------------------------

3. Also paste into the merge request description
    - the "what I excluded by which rule" sentence

4. NOT in this PR
    fuzz_buggy, crash-* artifacts, *.o, *.exe
    .idea/  .vscode/
    any file outside submits/<handle>/ and savefmt/
============================================================
```

> **作业清单 — 中文模板**
> 整段复制进作业文件。每条横线都是填空处，文件里不要留下中括号。代码进仓库的 `savefmt/`，这个文件装证据。本课程用 `submit(提交的文件夹): 做了什么事情`；真实社区用的是 `feat:` 这类英文小写类型，表单里留一条样例作对照，这次不要照它写。

```text
=== 本次要交的东西 ==========================================

1. 合并请求里只允许出现的路径
    submits/<handle>/P0/CONFORMANCE.md
    savefmt/  （解码器、向量、runner、harness、种子文件）
    其他一律不要

2. 本次文件的内容
    把下面两条虚线之间整段复制进文件
    横线是填空处，文件里不要留下中括号
    每条横线只写一行，不要中英混填
    提交信息只写一行英文，类型和说明里都不要出现中文
    提交信息格式：submit(提交的文件夹): 做了什么事情
    表里那条 feat: 是真实社区写法的样例，两种都留着
    本次按课程格式写自己的那一条
------------------------------------------------------------
# Conformance 与 Fuzz 自检

## 向量

- 一共几条，覆盖了哪些错误码：
  ____

- 四个边界用例，各自的期望码：
  ____

- `./run_vectors tests/vectors.txt` 的输出，原样：
  ____

## Fuzz

- 正确版本：命令和结果：
  ____

- 坏版本：你改了什么，以及报告的前四行：
  ____

- artifact 哈希和输入字节（hex）：
  ____

- 重放命令，以及第二次跑是否拿到同一个哈希：
  ____

## 提交

- 本课程的提交信息格式：
  submit(提交的文件夹): 做了什么事情

- 真实社区里的写法，留作样例（不是这次要交的格式）：
  feat: add conformance vectors and fuzz harness

- 本次提交信息（按课程格式写自己的，不要照抄样例）：
  ____

- 哪些文件是代码、哪些是证据：
  ____

- git status 里不是我写的条目（无，或写具体名字）：
  ____

- 我按哪条规矩排除了什么（贴进合并请求描述）：
  ____
------------------------------------------------------------

3. 合并请求描述里另外要贴
    · 上面「我按哪条规矩排除了什么」那一句话

4. 这次明确不交
    fuzz_buggy、crash-* 之类 artifact、*.o、*.exe
    .idea/  .vscode/
    submits/<handle>/ 和 savefmt/ 以外的任何文件
============================================================
```
