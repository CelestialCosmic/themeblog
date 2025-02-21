exe 与 dll 其实都是可执行的，它们之间的区别只有一个字段：魔数

我用 dnspy 随便找了个 dll 打开，结构如下：

## DOS 头

![[Pasted image 20240219150352.png]]

重要的有两个：头部的 `e_magic` 和尾部的 `e_lfanew`
`e_magic`：魔数，一般为 5A4D，也就是 `MZ`， 用于判断是不是可执行文件
`e_lfanew`：32 位可执行文件拓展域，用于标识 DOS 头与 PE 头之间的偏移

> 如何理解 `e_lfanew`？就是 `0xF8h` 是文件头的开始，就这么简单。

## DOS 块

DOS 块介于 PE 头和 DOS 头之间，长度不固定

在上面的图中，DOS 头于 `0x3Fh` 结束，又知 PE 头于 `0xF8h` 开始，那么 `0x40h` - `0xF7h` 就是 DOS 块

这部分内容没有信息，不影响

## PE 头

PE 头分标准 PE 头和可选 PE 头

### 标准PE 头

![[Pasted image 20240219165612.png]]

重要的就如下几个：

`NumberOfSections`：存储了文件中节的总数，不同的可执行文件节的总数是不一样的，可以通过 NumberOfSections 得知当前文件节的总数
如上图，程序有 6 个节表

`SizeOfOptionalHeader`：存储了可选PE头的大小，2 字节大小，可选 PE 头的大小一般是不固定的，通常情况下 32 位程序为0xE0，64 位程序为 0xF0，此值可以自定义。

如果 PE 只有标准 PE 头，那么这部分只有 20 字节，

### 可变 PE 头

这部分不重要，也很长，包的信息很多。不谈

### 节表

节表就是后面的 .data .rsrc 等等，每个都是 40 字节，分别对应节数据

重要的是这几个：

`VirtualAddress`：节区在内存中的偏移地址

`Characteristics`：节的属性，通过属性表里的值**相加得到**

> `Characteristics` 的部分重要属性如下：
> 
> |值|对应特征|
> |---|---|
> |20h|包含可执行|
> |40h|包含已初始化的数据|
> |80h|包含未初始化的数据|
> |10000000h|该块为共享块|
> |20000000h|该块可执行|
> |40000000h|该块可读|
> |80000000h|该块可写|

以 .data 为例

![[Pasted image 20240219163912.png]]

C0000040h = 80000000h + 40000000h + 40h

该块可读、可写、数据已初始化

### 拓展节

添加代码有三种方式：
- 在空白位置添加代码（不影响文件头的任何部分）
- 添加额外的节（影响`NumberOfSections`）
- 无限拓展最后一节（影响`SizeOfImage`、`SizeOfRawData`）

> 不建议手改，有工具
## RVA 与 FOA 的互转

RVA : 相对虚拟地址(Relative Virtual Address)
FOA : 文件偏移值

1.判断 RVA 是否位于 PE 头，如果是 FOA=RVA,(在内存中和文件中PE头（DOS头+PE头+节表）是相同的，节数据不同，因为文件对其和内存大小可能不相等)

2.判断 RVA 位于哪个节  
RVA >= 节.VirtualAddress
RVA <= 节.VirtualAddress + 当前内存对齐后的大小  
差值 = RVA - 节.VirtualAddress

3.FOA = 节.PointerToRawData + 差值