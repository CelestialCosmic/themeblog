# Part0：知识协议与写在前面
>本文章采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 进行许可。转载请注明出处，不得用于商业用途，并以相同协议共享。

这篇文章基于大量前人研究、开源仓库、英伟达 DLI、个人见闻与实践写成
感谢愿意开放源代码、愿意分享的人们为这篇文章所探过的路，没有各种公有或私有的可供研究的代码、文章，是无法完成这篇文章的
# Part1：大模型是什么
## AI 的不同形态
- 在用户眼中，是产品（产品分析、客户筛选、调研）
- 在科学家眼中，是一堆权重（gguf、safetensors）
- 在开发者眼中，是接口（
  https://api.deepseek.com
  https://generativelanguage.googleapis.com/v1beta/openai/
  https://api.openai.com/v1/
  ）
![[Pasted image 20250310164627.png]]

但要解释清楚大模型的本质是什么，要先说什么是模型，也就是从最基本的模型：单模态模型开始
## 模型的本质
模型的本质是一大堆权重（俗称参数），用户输入的内容经过分割后，给相应的权重进行分析，通过打散重组以后，输出的新东西。或者说一个 **garbage in garbage out** 的过程，只是说这个 garbage 比较有参考意义
## 单模态模型
单模态模型包括文字模型、图片模型等，其应用场景包括纯文字处理、内容总结、以图搜图等功能，[[#^ccb332|如何训练一个单模态模型]]介绍了训练一个这样的模型的思路
但这种模型是单模态的，文字模型只能处理文字，图片模型只能处理图片
这世界是多彩的：图片上可能有字、视频有文字有图片还有声音
为了克服这个问题，所以提出了多模态模型
## 多模态模型
多模态模型就是将两个单模态的模型合在一起，至于是怎么合在一起的，[[#^257ae8|将两个单模态模型合成为多模态模型]]会介绍到

### 人的感知与模型
人有五大感觉，加上大脑作为中枢，哪怕再人机也是有知觉的
机器徒有躯壳，需要通过各式各样的传感器来完成“感觉”
![[Pasted image 20250510162910.png]]

一个传感器再厉害，也只体现在其对这方面的精度，要实现多种数据交融，就需要多个传感器协同

>简单举两个例子：
>##### 例子一：
>两个机器人 A、B 在路上走，但两个机器人不一样：
>A 只能感知周围的物体有多远（点云模型）
>B 只能看到周围的物体有多大（点阵模型）
>它们单独在路上走都会撞到别人
>但通过合模，它就知道路上有什么东西，它有多大个，就可以在路上正常走路了
>##### 例子二：
>四个机器人 A、B、C、D 在电影院看电影，但每个机器人都有各有优劣：
>A 只有嘴和耳朵（语言模型）
>B 只有眼睛（视觉语言模型）
>C 只有左脑（重新排序模型）
>D 只有右脑（嵌入模型）
>单独采访任何一个，问电影怎么样就和盲人摸象一样
>但通过合模，把它们的思考结果组装起来，我们就得到了一份完整的影评

这两个例子，一个是现在的 L2 辅助驾驶（曾经宣传为 L3 智驾），一个是现在的 “AI 视频总结”
## 大模型
大模型之所以“大”，就是因为它参数量非常大，如[deepseek-ai/DeepSeek-R1 · Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-R1)就是一个单模态的超大权重模型，modelsize 为 685B，其针对文字处理非常强大，但不能处理图片和视频
多模态的大模型大在模态多，且每个模态的参数量都不小，如 [deepseek-ai/deepseek-vl2-tiny · Hugging Face](https://huggingface.co/deepseek-ai/deepseek-vl2-tiny) 由视觉编码器 Vision Encoder、视觉-语言适配器 VL Adaptor 和 DeepSeek-MoE 语言模型组成，modelsize 为 3.37B，所以其能处理图片、视频等更为复杂的内容，但在语言组织能力上不如 DeepSeek-R1
在线平台的 AI 还会附加**联网搜索能力**，使得模型从自己推理结果改成了引用和总结互联网的结果，因此输出的结果更加受控和准确。但再厉害的 AI 也不是许愿机，之所以能回答比以前准确还是因为**它只是总结了人所完成的东西，人的作用依旧不可忽视**
### 大模型也不是万能的
大模型只是在按设置好的流程去执行，**没有良好的引导** AI 是产不出好结果的，正所谓 garbage in garbage out
你问它银行怎么走，它不知道你在哪，不知道你要去哪家银行，不知道你要办什么业务，它可能猜到了，给了离你最近的那家银行，那家银行能办你需要的业务吗？
问 AI 一个专业性相关或者非常识性的问题，一定要先组织好自己的语言，最好自己先做过，知道有什么坑，再去问，这样才会有令人满意的结果
### 大模型也会被误导
大模型的幻觉大家有目共睹，现在基于传统 SEO 又衍生出了 **AI SEO**
 AI SEO 就是利用做传统 SEO 的内容农场，在互联网大量抛洒引导性信息，再利用普通人对 AI 结果的信任，进而宣传自己的产品甚至误导大众

## 总结
大模型因为复杂的结构和巨大的训练量，能给出的回答比过去任何时候都更近似人类的语言，也由于其巨大的输入数据和训练拟合，其回答准确度相当于在相关领域有一定经验的人，但我们依旧需要清楚：大模型的训练是基于大量的语言输入而非逻辑思考，所以对于很多领域的深入一些的问题，模型是没有办法给出正确的回答的。语言模型只是语言模型，它只能拟合而不能理解语言，更不要说语言背后的逻辑。在具有专业性的内容上表现也不佳。
 在这个时代，诸如DeepSeek这样的大模型为普通人进一步认识世界和学习新知识提供了极大的便利，想查找参考文献，写代码，从多角度解释新的概念等都变得前所未有地方便。然而这并不意味着能提供专业内容的论坛、平台没有意义。相反地，在大多数问题都能被大模型回答的时候，这些论坛、平台正是能回答那些大模型不能回答的问题的少数平台之一。
 对于“AI 出来了，那些 Q&A 平台、论坛还有什么意义”这样的论调，我们更应该问：“大部分普通人的人生还有什么意义”。毕竟很多人并没有什么大模型不懂但自己懂且还对社会有价值的知识/技能/认知。只要人类学习科研还需要老师一天，AI 就还需要人类带路一天。
# Part2：前置知识
这部分主要介绍训练模型所需的四个领域：自然语言处理（NLP）、机器学习（ML）、深度学习（DL）、计算机视觉（CV）
## 前置领域
### NLP（文字处理基础）
**NLP**：即自然语言处理（Natuarl Language Processing），*主要研究人类语言活动中，信息成分的发现、提取、存储、加工与传输*，在 AI 模型中，将一句话分为很多个 token 就是由 NLP 完成的。常见的**中文分词工具**包括 jieba、FoolNLTK、HanLP、NLPIR、THULAC、LTP 等
**Token**：文本的最小单元、可以是一个词，也可以是一个字
   Token 的处理分为按词分割和按字分割

按词分割时，结果如下：
```python
"hello world" = ["hello","world"] # 2Token
"你好，AI" = ["你好","，","AI"] # 3Token
```
按字分割时，结果如下：
```python
"hello world" = ["h","e","l","l","o","w","o","r","l","d"] # 10Token
"你好，AI" = ["你","好","，","A","I"] # 5Token
```

该领域的终极目标：**强人工智能**
1. **弱人工智能**：建立一个足够精确的语言数学模型使计算机通过编程来完成自然语言的相关任务。如：听、读、写、说，释义，翻译，回答问题等
2. **强人工智能**：让用户能通过自然语言与计算机自由对话

### ML（学习记忆支撑）
机器学习的类型有如下几种：
1. **监督学习（Supervised Learning）**：使用带标签的数据进行训练，模型学习输入到输出的映射关系
 人工标记*数据集*，提供足够的训练资料，  比如从赵本山的小品中提取足够的语料进行训练，便可以获得一个会说小品的 AI
2. **无监督学习（Unsupervised Learning）**：使用不带标签的数据进行训练，模型寻找数据中的模式或结构
   不标记任何*数据集*，让 AI 找出其中的规律，AI 代替人类探索可能的蛋白质结构属于此类
3. **半监督学习（Semi-Supervised Learning）**：结合少量带标签的数据和大量不带标签的数据进行训练。
   介于监督学习和无监督学习之间，*数据集*有少量标注，但人类标记的数据集将为机器学习提供大致方向
4. **强化学习（Reinforcement Learning, RL）**：通过与环境的互动学习策略，以最大化累积奖励
   游戏人机、机器人行走、机器人走迷宫属于此类
   ![[Pasted image 20250226133901.png]]
   很久以前看过的视频，通过强化学习让 AI 自己探索走路方式，当时对这个印象很深刻
#### DL（深度学习、机器学习的加强版）
从属于机器学习，暴力理解就是 **pytorch**
在 openAI 的 ChatGPT3.0 铺开以后，普通人使用 AI 的标准下放，于是就有了下面这张图：
![[Pasted image 20250226135626.png]]

注：requests 是 python 最常用的请求库，不适用 AI 训练和学习（调库侠！）

> **为什么是 ChatGPT3.0？**
> ChatGPT3.0 发布是 AI 技术在国外大规模铺开的**重要里程碑**
> 更早期的都是一小群人在玩图像生成、文字生成。如 2022 年，NovelAI 在国内有一定程度的传播，但生成的图像普遍存在严重问题（人们对 AI 生成的都是残次品这样的偏见也是在那个时期出现的）
> 该模型的出现降低了人们对 AI 生成内容的偏见，也是此时 ChatGPT 开始大规模传播
### CV（部分非结构化数据处理）
视频有各种各样的编码，MPEG、H.26X 等等，图片也是如此。AI 和人一样，看不了二进制形态的视频和图片，所以需要解码后进行**特征提取**、**目标检测**、**行为识别**等一系列处理，才能理解内容。openCV 是最常见的计算机视觉库。
#### 名词解释
**结构化数据**：二维数据表，有严格组织结构的二维数据，如数据库、csv 
对人类可读性差，对机器可读性强
**非结构化数据**：各类 office 文件、图片、视频等非二维数据表
对人类可读性强，对机器可读性差
**半结构化数据**：非二维数据表，较非结构化数据复杂度更低，如 json toml xml log 等
对人类可读性一般，对机器可读性一般
# Part3：大模型相关知识
这里介绍大模型专有的知识
## 量化
量化是指将模型参数和计算方式从高精度转换为低精度，以减少模型的存储和计算需求
量化涉及计算机底层存储数据的方式：**整形和浮点数**
每个参数都是通过整形或浮点数加载到显存中的，因此**要运行模型，首先需要将模型装载到显存中**
### 量化相关数据结构
INT4、INT8、FP16、BF16、TF32、FP32 等都是用于深度学习的数值格式，它们和常规的整形、浮点数类似，但又有不同
下图是各类浮点数的量化：
![[40f81dad82708dc.webp]]
- Sign 存储正负，占用 1 个比特
- Range 存储数值范围，拥有的比特越大能表示的范围越大
- Precision 存储精度，拥有的比特越多越精准
**FP16 使用 16 位比特来表示一个参数，这 16 比特是要实打实装进显存里面的，假设需要装载 1.5B 的模型，那么就是 15 亿个这样的单元装进显存，并需要配套的 cpu、内存和硬盘**
由图类推可知： FP32 一个单元占用 32 bit，BFLOAT16 一个单元占用 16 bit，TF32 比较特殊，一个单元占用 19 个 bit，介于 2 byte 和 3 byte 中间
### 高精度与低精度间的优劣
精度越高，需要的显存越高。除浮点数之外还有 Int8 Int4 之流的量化方式，**占用更小，但模型精度也更差**
比如将 FP32 浮点数参数量化为 Int8，可以**减少约四分之三的存储空间**（每个参数占用从 32 bit 降低至 8 bit）
可是人吃不饱饭会不干活，AI 吃不饱虽然不会拒绝干活，但幻觉、复读、答非所问出现的概率那就不得而知了

非结构化数据的解析能力需要一定规模和精度的模型才能支持

### 模型幻觉能不能消除
不能，AI 在人类未知的领域中，“幻觉”是创造力。但在人类已知的领域，“幻觉”会给所有人带来困扰。“幻觉”是双刃剑，是模型的一体两面

下图可以看到，上下文越长，AI 正确率越低，幻觉越严重（思考本身也会加重幻觉）
![[Pasted image 20250310161645.png]]

而幻觉又是 Transformer 架构的通病，因此无法避免，原因有两个：
1. 模型在数据集中遇到大量重复内容时，如果“不确定”下一步怎么做，往往会选择重复上下文中的内容。一旦开始重复，这种行为就会自我加强，导致无限循环。温度调节和重复惩罚可以缓解这种情况，但无法彻底消除这个问题
2. 模型在对话过程中会识别和捕捉模式。如果模型对话前后两个消息中使用了相同的短语，那么这个短语就会像定式一样不断重复出现，除非你自己手动编辑 AI 输出的内容

**但即便 AI 精度再高，最重要的还是人**。人的知识水准必须比模型更懂，AI 幻觉对于水平低于 AI 的人很难被察觉
人的造谣是有局限性的，而且产量有限，而 AI 生成的造谣栩栩如生、身临其境，工业化的生产能力效率极高，甚至只能靠某个细节反推才能知道 AI 在胡说八道，借助矩阵号、营销号很快就能传染、扩散，即便快速辟谣，错误的东西也已经在互联网上留下了伤痕
### 精度与参数如何取舍？
**参数**数量决定了思考问题的**广度**，量化**精度**决定了思考问题的**深度**
人类阅读速度在 5-10 token/s 之间，低于 5token/s 的输出会让人类觉得慢
大多数情况下推荐降低精度，增加参数量。但也不能为了追求参数量而无脑抛弃精度
1 字节 / 参数以下（也就是比 Int4 还差的量化）的量化会导致非常明显的性能下降
### 模型的格式
对应于不同类型的量化，有不同的表达方式，其遵循如下规律：
<center>Q + X （用于存储权重的位数）+ 特定变体</center>
`X`是量化位数，也就是参数占用的比特数（和 fp16、fp32 后面的数字是一个东西），对设备性能的要求也随之有偏重

#### 特定变体解析

1. **0/1**：表示对称/非对称量化，0 表示对称量化，1 表示非对称量化
2.  **K**：分块量化
   >分块量化的特点为**层次化**，能将用户的复杂问题分解为小问题去分析，**适合在旧硬件、Mac 电脑或纯 CPU 推理的情况下对模型进行量化**
>其后面一定跟着详细的分块规格字母 S、N、L ：
>- **S**：小块（shrunken），小块量化
>- **XS**：超小块（extra small block），超小块量化
>- **XXS**：超超小块（extra extra small block），即更小块的量化
>- **NL**：非线性（nonlinear）方法的量化
>- **M**：中等块（medium）
>- **L**：大块（large），大块量化
>
>这几类都表示参数被**分块量化**了，区别在于参数块的大小，虽然优化了显存，其对调度要求更高，计算效率也存在一定下降
3. **IQ**：代表"Importance Quantization"（重要性量化），使用重要性矩阵来改进量化结果
   >**重要性矩阵（Importance Matrix）**：其能根据不同权重的重要性来调整量化的精度，可以达到不显著降低模型精度的情况下，对重要性较低的权重进行更高程度的量化，而对重要性较高的权重进行较低程度的量化
4. **Q**：代表"Quantization"（传统量化）
  >I 和 K 都是量化优化，
  >I 是通过优化参数组织方式
  >K 是通过参数分组进行优化
  >二者不可共存
5. **F**：浮点数（Floating-point），传统浮点数
6. **BF**：脑浮点（Brain Floating-point），优化过的浮点数
7. **TF**：张量浮点（Tensor Floating-point），优化过的浮点数
>BF 系列适合推理，TF 系列适合训练，F 系列适合存储
8. **UD**：动态量化，根据输入数据的分布动态调整量化参数，可以降低推理所需资源

按照上面提供的格式可以得知每种模型量化后的特点与优缺点
hugging face 提供了一整套量化方式，如下表所示（删除了已废弃的量化方式）：

| 类型      | 描述                                                                                           |
| ------- | -------------------------------------------------------------------------------------------- |
| F64     | 64 位标准 IEEE 754 双精度浮点数。                                                                      |
| I64     | 64 位定宽整数。                                                                                    |
| F32     | 32 位标准 IEEE 754 单精度浮点数。                                                                      |
| I32     | 32 位定宽整数。                                                                                    |
| F16     | 16 位标准 IEEE 754 半精度浮点数。                                                                      |
| BF16    | 16 位缩短版的 32 位 IEEE 754 单精度浮点数。                                                               |
| I16     | 16 位定宽整数。                                                                                    |
| Q8_K    | 8 位量化，每个块有 256 个权重。仅用于量化中间结果。所有 2-6 位点积均为此量化类型实现。权重公式：w = q * block_scale。                   |
| I8      | 8 位定宽整数                                                                                      |
| Q6_K    | 6 位量化，超级块有 16 个块，每个块有 16 个权重。权重公式：w = q * block_scale（8 位），结果为 6.5625 位/权重。                  |
| Q5_K    | 5 位量化，超级块有 8 个块，每个块有 32 个权重。权重公式：w = q * block_scale（6 位） + block_min（6 位），结果为 5.5 位/权重。     |
| Q4_K    | 4 位量化，超级块有 8 个块，每个块有 32 个权重。权重公式：w = q * block_scale（6 位） + block_min（6 位），结果为 4.5 位/权重。     |
| Q3_K    | 3 位量化，超级块有 16 个块，每个块有 16 个权重。权重公式：w = q * block_scale（6 位），结果为 3.4375 位/权重。                  |
| Q2_K    | 2 位量化，超级块有 16 个块，每个块有 16 个权重。权重公式：w = q * block_scale（4 位） + block_min（4 位），结果为 2.5625 位/权重。 |
| IQ4_NL  | 4 位量化，有重要性矩阵，超级块有 256 个权重。                                                                   |
| IQ4_XS  | 4 位量化，有重要性矩阵，超级块有 256 个权重。其大小为 4.25 位 / 权重。                                                  |
| IQ3_S   | 3 位量化，有重要性矩阵，超级块有 256 个权重。其大小为 3.44 位 / 权重。                                                  |
| IQ3_XXS | 3 位量化，有重要性矩阵，超级块有 256 个权重。其大小为 3.06 位 / 权重。                                                  |
| IQ2_XXS | 2 位量化，有重要性矩阵，超级块有 256 个权重。其大小为 2.06 位 / 权重。                                                  |
| IQ2_S   | 2 位量化，有重要性矩阵，超级块有 256 个权重。其大小为 2.50 位 / 权重。                                                  |
| IQ2_XS  | 2 位量化，有重要性矩阵，超级块有 256 个权重。其大小为 2.31 位 / 权重。                                                  |
| IQ1_S   | 1 位量化，有重要性矩阵，超级块有 256 个权重。其大小为 1.56 位 / 权重。                                                  |
| IQ1_M   | 1 位量化，有重要性矩阵，超级块有 256 个权重。其大小为 1.75 位 / 权重。                                                  |
>**名词解释**
>位 == 比特
>权重 == 参数

所以，号称“量化仙人”的 unsloth 提供了如下几种格式的 DeepSeek 671B：

| 模型名称                                                                                                                | 模型格式     | 模型大小（G） | 预估显存（G） |
| :------------------------------------------------------------------------------------------------------------------ | :------- | :------ | ------- |
| [DeepSeek-R1-UD-IQ1_S](https://huggingface.co/unsloth/DeepSeek-R1-GGUF/tree/main/DeepSeek-R1-UD-IQ1_S)              | gguf（分卷） | 141     | 180     |
| [DeepSeek-R1-UD-IQ2_XXS](https://huggingface.co/unsloth/DeepSeek-R1-GGUF/tree/main/DeepSeek-R1-UD-IQ2_XXS)          | gguf（分卷） | 197.5   | 250     |
| [DeepSeek-R1-Zero-Q2_K_XS](https://huggingface.co/unsloth/DeepSeek-R1-Zero-GGUF/tree/main/DeepSeek-R1-Zero-Q2_K_XS) | gguf（分卷） | 223.9   | 280     |

这些模型都能在一台少于八卡的 AI 服务器中正常运行
>默认显卡是显存 64G 以上的运算卡

实际部署时，这种参数量小、精度又低的模型，经常连话都听不懂

#### 最常见的量化方式
`convert_hf_to_gguf.py` 提供如下量化方式：`f32,f16,bf16,q8_0,tq1_0,tq2_0,auto`
这里需要额外解释一个 **TQ**：Tensor Quantization，张量量化。其将每个参数极致压缩至 1、2 位整数，这么压模型当然小，但精度就那回事了。其还有一个严重问题是 ollama 不支持这两种量化方式
上面提到的除 TQ 系列之外的量化方式，ollama 都支持

>个人体感上 
>q8_0 显存占用高，token 输出速度快，对 gpu 需求高，对 cpu 存储几乎没有需求
>bf16 显存占用低，token 输出速度低，对 gpu 需求一般，对 cpu 存储需求高
>f16 

llama.cpp 支持如下量化方式：
- `q2_k`：将 Q4_K 用于 attention.vw 和 feed_forward.w2 张量，Q2_K用于其他张量。
- `q3_k_l`：将 Q5_K 用于 attention.wv、attention.wo 和 feed_forward.w2 张量，否则Q3_K
- `q3_k_m`：将 Q4_K 用于 attention.wv、attention.wo 和 feed_forward.w2 张量，否则Q3_K
- `q3_k_s`：将Q3_K用于所有张量
- `q4_0`：原始量化方法，4 位。
- `q4_1`：精度高于q4_0但不如q5_0。但是，与 q5 模型相比，推理速度更快。
- `q4_k_m`：将 Q6_K 用于一半的 attention.wv 和 feed_forward.w2 张量，否则Q4_K
- `q4_k_s`：将Q4_K用于所有张量
- `q5_0`：  原始量化方法，5位。精度更高，资源使用率更高，推理速度更慢。
- `q5_1`：精度高于q5_0但不如q6_k。但是，与 q6 模型相比，推理速度更快。
- `q5_k_m`：将 Q6_K 用于一半的 attention.wv 和 feed_forward.w2 张量，否则Q5_K
- `q5_k_s`：将Q5_K用于所有张量
- `q6_k`：将Q8_K用于所有张量
- `q8_0`：与16位浮点数几乎无法区分。资源使用率高，速度慢。不建议大多数用户使用。

## AI 模型的存储方式
1. safetensors：高速型
   - 安全性高，无代码注入风险。加载速度快，支持内存映射，适合加载大型模型
   - 不能在 windows 上部署
2. gguf：笨重型、高效型
   - 高效推理设计，支持多种量化方案，适合在资源受限设备上运行
   - 模型转化强制依赖 llama.cpp、高精度量化占用大
3. ckpt：训练特化型
   - 保存模型参数和优化器状态，支持训练过程的中断与恢复
   - 有代码注入风险，存在**安全问题**
4. bin：通用型
   - 适配框架多、通用性强
   - 需要自定义逻辑读取和保存
5. pth：开发型、训练特化型
   - 可直接对接 pytorch
   - 不能直接用于其他框架，存在**安全问题**

>仅推理推荐使用 safetensors,gguf 和 bin

![[gguf-spec.png]]
<center>gguf 模型文件结构示意图</center>

## 模型选型与推荐配置

### 估算模型所需性能
1. 依据参数量和量化方式进行估算
   *所需显存 M = （参数数量 P × 参数占用字节 B）÷（32 ÷ 加载模型位数 Q）× 1.2*
   **70B、f32**: M = 70 × 4 ÷ (32 ÷ 32) × 1.2 = 336.00 GB
   **32B、f32**: M = 32 × 4 ÷ (32 ÷ 32) × 1.2 = 153.60 GB
2. 依据模型所需存储进行估算
   *推理所需显存 ≈ 模型大小 × 1.2*
   **70B、f32**: M = 282 × 1.2 = 338.40 GB
   **32B、f32**: M = 131.1 × 1.2 = 157.32 GB

根据如上估算公式，并保留一定余量，可以算出来模型大致需要如下显存：
>**note**：
>1. 依据量化精度为 bf16，模型格式为 gguf，系统为信创系统进行估算
>2. 低于模型最低配置时是无法部署的
>3. 按照常规 bare metal 估算，所以最低配置就是 32C128G
>   常规家用电脑大致都在 1.5B 上下，游戏本等有一定计算能力的电脑可以达到 14B，顶配电脑经过量化可以跑到 32B，极限
>4. 集群部署需要交换机和对应的网卡

| 模型参数大小（B） | 所需显存（G） | 所需内存（G） | 所需核心数（个） | 所需存储（GB） | 节点间高速网络（Gbps） | 高性能网卡与配套交换机 |
| :-------- | :------ | :------ | -------- | -------- | ------------- | ----------- |
| 671       | 1800    | 512     | 64       | 4000     | 200           | 需要          |
| 70        | 256     | 512     | 64       | 2000     | 0             | 不需要         |
| 32        | 128     | 512     | 32       | 1000     | 0             | 不需要         |
| 14        | 64      | 256     | 32       | 500      | 0             | 不需要         |
| 8         | 32      | 128     | 32       | 300      | 0             | 不需要         |
| 7         | 32      | 128     | 32       | 300      | 0             | 不需要         |
| 1.5       | 32      | 128     | 32       | 300      | 0             | 不需要         |

### 运行模型的最低要求
**专用显存**与**共享 GPU 内存**之和大于模型需求显存

|        | 专用显存 (VRAM) | 共享 GPU 内存（DRAM） | SWAP                         |
| ------ | ----------- | --------------- | ---------------------------- |
| 连接方式   | 直通          | PCIE            | PCIE                         |
| 数据传输速度 | 非常快         | 相对较慢            | 慢                            |
| 延迟     | 低           | 中               | 高                            |
| RAM 占用 | 专有内存        | 减少系统内存<br>增加显存  | 增加系统内存<br>降低系统运行速度<br>减少硬盘寿命 |
共享 GPU 内存以推理速度为代价，使显存较小的机器装下更大的模型
SWAP 不可以共享给 GPU 做拓展内存

>**其他影响因素**
>1. 网络速度影响**集群**推理效率
>2. 显卡算力影响 token 输出速度
>3. 存储影响模型的启动速度、模型参数大小也对存储需求有影响
>4. 高并发的场景对显存需求影响不大，但对显卡算力影响很大

# Part5：从 DeepSeek 开源周一瞥 AI 架构
## 对开源周的官方总结
[GitHub - deepseek-ai/open-infra-index: Production-tested AI infrastructure tools for efficient AGI development and community-driven innovation](https://github.com/deepseek-ai/open-infra-index)
## 第一日：FlashMLA（MLA 解码内核优化）
[GitHub - deepseek-ai/FlashMLA: FlashMLA: Efficient MLA Decoding Kernel for Hopper GPUs](https://github.com/deepseek-ai/FlashMLA)
FlashMLA 是针对 Hopper GPU 优化的高效 MLA 解码内核，专为处理可变长度序列而设计，优化了显卡的运算能力
开源后不久已得到大量社区支持：
1. MetaX（沐曦）
2. Moore Threads（摩尔线程）
3. Hygon DCU（海光）
4. Intellifusion（云天励飞）
5. Iluvatar Corex（天数智芯）
6. AMD Instinct（AMD）
这些企业都提供了相似的实现以支持自身的运算卡
## 第二日：DeepEP
[GitHub - deepseek-ai/DeepEP: DeepEP: an efficient expert-parallel communication library](https://github.com/deepseek-ai/DeepEP)
DeepEP 是专为混合专家（MoE）和专家并行（EP）而定制的通信库。其提供如下能力：
提供了高吞吐量和低延迟的全对全 GPU 内核，也称为 MoE 分发和组合
增强推理解码内核延迟，分发支持精度下放到 FP8。
并针对 NVLink 和 RDMA 域之间的数据传输进行了优化，支持NVLink 和 RDMA 的节点内和节点间通信，确保高效的数据传输
该仓库为 AI 推理和训练提供了更高效的支持，减少了推理和训练时对算力的需求
## 第三日：DeepGEMM
[GitHub - deepseek-ai/DeepGEMM: DeepGEMM: clean and efficient FP8 GEMM kernels with fine-grained scaling](https://github.com/deepseek-ai/DeepGEMM)
DeepSeek 改良后的高性能的通用矩阵乘法（GEMM），优化了 MoE 模型，提升 FP8 的运算能力，使用 JIT 技术，代码可以在运行时动态生成和优化
其使得在 FP8 量化下运行的 DeepSeek 可以运行得更快，训练时修改代码的成本降低
## 第四日：DualPipe、EPLB、Profiling Data in DeepSeek Infra（参数调优策略相关）
[GitHub - deepseek-ai/DualPipe: A bidirectional pipeline parallelism algorithm for computation-communication overlap in V3/R1 training.](https://github.com/deepseek-ai/DualPipe)
[GitHub - deepseek-ai/EPLB: Expert Parallelism Load Balancer](https://github.com/deepseek-ai/eplb)
[GitHub - deepseek-ai/profile-data: Analyze computation-communication overlap in V3/R1.](https://github.com/deepseek-ai/profile-data)
### DualPipe
[GitHub - deepseek-ai/DualPipe: A bidirectional pipeline parallelism algorithm for computation-communication overlap in V3/R1 training.](https://github.com/deepseek-ai/DualPipe)
实现了双向管道并行算法，使得前向和后向计算-通信阶段的完全重叠，减少通信中断流的时间，提升了通信效率
### EPLB（专家并行负载平衡器）
[GitHub - deepseek-ai/EPLB: Expert Parallelism Load Balancer](https://github.com/deepseek-ai/EPLB)
专家在进行任务时，天然不能平均地分配任务，就会导致某些专家空转而某些专家满载的情况，进而导致 GPU 负载不均衡。通过采用冗余专家策略，复制负载重的专家打包到空闲的 GPU 上，并尽可能将同一组的专家放置在同一个节点上，以减少节点间的数据传输。该仓库就是这种均衡算法的实现。
## 第五日：3FS
[GitHub - deepseek-ai/3FS: A high-performance distributed file system designed to address the challenges of AI training and inference workloads.](https://github.com/deepseek-ai/3FS)
全名为 Fire-Flyer File System，译名“萤火虫文件系统”，因为 Fire-Flyer 都以 F 开头，File System 简称为 FS，故命名为 3FS

相关论文：[Fire-Flyer AI-HPC: A Cost-Effective Software-Hardware Co-Design for Deep Learning](https://arxiv.org/pdf/2408.14158)
相关论文解析：[DeepSeek 万卡集群及软硬件协同设计框架Fire-Flyer](https://www.toutiao.com/article/7430708784164651556/?wid=1740839204455)

相较常规文件系统，其有如下特性：
1. 利用链式复制分配查询 CRAQ 提供强一致性
2. 利用 replication 复制做容错和故障恢复
3. 文件系统元数据存储在分布式 KV 中，支持快速并发访问
4. 利用元服务并发做数据的并发访问控制
5. 可通过增加节点扩容存储和计算能力
配合软硬件协同设计框架 Fire-Flyer AI-HPC 架构，即便是万卡集群，其也能吃满存储和网络的能力极限，达到极致的数据吞吐，并保证计算-存储集成网络无拥塞，同时还能降低训练成本和能源消耗
### 依赖
工具链：
- libfuse 3.16.1^
- FoundationDB 7.1^
- Rust toolchain

依赖软件包：
```
cmake libuv1-dev liblz4-dev liblzma-dev libdouble-conversion-dev libprocps-dev libdwarf-dev libunwind-dev libaio-dev libgflags-dev libgoogle-glog-dev libgtest-dev libgmock-dev clang-format-14 clang-14 clang-tidy-14 lld-14 libgoogle-perftools-dev google-perftools libssl-dev gcc-12 g++-12 libboost-all-dev
```

### 知识基础
#### 分布式文件存储系统
分布式文件存储系统的**数据存储在多台机器上**，也就是存储节点，由多个节点构成分布式集群，节点上的小的分布式文件系统组合成总的分布式文件系统，由**主服务器对总的文件系统进行管理**。用户任意访问某一台主机，都能获取到自己想要的目标文件
> 其与 RAID（冗余磁盘阵列）不同，分布式文件存储系统是多机器多硬盘，RAID 是单机器多硬盘
> 虽然存在**分布式 RAID**，但较为少见
> 其与**存储桶**也不同，存储桶优于传统的文件系统或关系数据库的对象存储，虽然是分布式的，但不属于分布式文件存储系统

#### KVCache
KVCache（键值缓存）是大模型推理中常用的优化技术，在各种类型的模型，尤其是 Transformer 中，它通过缓存每个 token 在经过 Transformer 时生成的键（Key）和值（Value）来减少重复计算，从而提高推理速度，其本来是存放于**内存**中的，但借助 **3FS-KV**，也就是 3FS 变种，专注于共享存储分布式数据处理系统，使得 KVCache 可以放到 **SSD** 中，进一步优化模型的内存需求
*但 3FS-KV 不在本次开源的范围内*

## 第六日：基础架构分享
[One More Thing, DeepSeek-V3/R1 Inference System Overview](https://github.com/deepseek-ai/open-infra-index/blob/main/202502OpenSourceWeek/day_6_one_more_thing_deepseekV3R1_inference_system_overview.md)
官方中文全文：[DeepSeek-V3 / R1 推理系统概览](https://zhuanlan.zhihu.com/p/27181462601)
解释了 deepseek 通过哪些技术，使得其比其他模型消耗更少，可行性更高

总体思路：
1. 节省性能，每层包含 256 个专家，但在推理过程中，每个 token 仅激活其中 8 个专家，是大模型里面激活量最稀疏的一批，导致占用大但实际使用少，所以使用跨节点计算增大专家使用
2. 计算通信重叠，跨节点推理，并利用推理空隙完成其他工作，榨干算力
3. 闲时调用更多算力训练：白天高负荷时全节点部署推理，夜间低负荷时释放节点用于训练/研究。资源有效弹性伸缩，避免长期空置。

# Part4：如何启动大模型及其附属模型
## 大模型
### Ollama
搭建难度低
特点：简单、跨平台
步骤：
1. 安装 ollama、下载模型
2. 完成 modelfile
3. 引入模型
4. 运行模型
5. done
### Vllm
搭建难度中等
特点：高效
步骤：
1. 安装 cuda 12.4 以上版本
2. 拉取 docker
3. 运行 dorker
4. done
## 附属模型
### XInference
步骤：
1. 拉取 docker
2. 运行 docker
3. 访问前端
4. 搭建模型
5. done
# Part5：训练和微调模型
这部分涉及线性代数、激活函数，神经网络（普通，卷积，循环），实用的分类和聚类算法
如果熟悉卷积神经网络的构建方式，就可以跳过这部分了
## 了解数据集间的合作

### 准备需要使用的库

```py
import numpy as np
```
numpy ：加载和处理数据
```py
import matplotlib.pyplot as plt
from matplotlib import animation
```
matplotlib：数据可视化
```py
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
from torch.optim import Adam
```
pytorch：深度学习、机器学习的核心库
```py
from PIL import Image
```
pillow（PIL）：图像处理的核心库
```py
from IPython.display import Image as IPy_img
```
IPython：Jupyter 增强
```py
import utils
import os
```
utils、os：基础库
```py
from scipy.io import wavfile
from scipy import fft
```
scipy：高阶抽象和物理模型库，其中 fft 是快速傅里叶变换（FFT），wavfile 则是音频处理

```py
import nibabel as nib
```
nibabel：神经科学和医学影像分析领域的库
### 准备数据集
#### 构建数据集
这里以音频数据为例

#### 构建混合数据集
这是三个各不相同的物体，我们需要让机器人感知到这些物体不至于撞上
![[Pasted image 20250511131735.png]]
所有用于训练的数据都应该做成 pytorch 数据集，所以先从准备数据入手
### 构建一个 RGB 图像数据
RGB 图像是大家喜闻乐见的图片，以 `png` 形式存储，用 pillow 库读取可以看到这是一个 64x64 的位图
```py
data_img = Image.open('data/replicator_data_parallel/rgb/0163.png')
plt.imshow(data_img)
```
![[Pasted image 20250511113643.png]]

### 构建一个 LiDAR 数据

#### 什么是 LiDAR
LiDAR 是一种传感器，其可以用于测距
![[Pasted image 20250511140924.png]]
#### 处理 LiDAR
产生的数据集为 `npy`，用 pillow 读取可以看到这是一个 64x64 的位图
```py
data = np.load('data/replicator_data_parallel/lidar/0163.npy')
plt.imshow(data, cmap=utils.cmap)
data.shape
```
![[Pasted image 20250511113518.png]]

### 对齐数据
因为 LiDAR 使用的是不可见光进行探测的，每束光线都有不同的角度，所以使得这 LiDAR 输出的图像如同被翻转了一般，为了让它们对齐，我们需要获取 LiDAR 每束光线的天顶角（Zenith Angle）和方位角（Azimuth Angle）

![[Pasted image 20250511115558.png]]

```py
zenith = np.load("data/replicator_data_parallel/zenith.npy")
print(zenith.shape)
zenith
azimuth = np.load("data/replicator_data_parallel/azimuth.npy")
print(azimuth.shape)
azimuth
```
天顶角
```py
array([-0.27925268, -0.27052602, -0.2617994 , -0.25307274, -0.2443461 ,
       -0.23561946, -0.2268928 , -0.21816616, -0.20943952, -0.20071286,
       -0.19198622, -0.18325958, -0.17453292, -0.16580628, -0.15707964,
       -0.14835298, -0.13962634, -0.1308997 , -0.12217305, -0.1134464 ,
       -0.10471976, -0.09599311, -0.08726646, -0.07853982, -0.06981317,
       -0.06108652, -0.05235988, -0.04363323, -0.03490658, -0.02617994,
       -0.01745329, -0.00872665,  0.        ,  0.00872665,  0.01745329,
        0.02617994,  0.03490658,  0.04363323,  0.05235988,  0.06108652,
        0.06981317,  0.07853982,  0.08726646,  0.09599311,  0.10471976,
        0.1134464 ,  0.12217305,  0.1308997 ,  0.13962634,  0.14835298,
        0.15707964,  0.16580628,  0.17453292,  0.18325958,  0.19198622,
        0.20071286,  0.20943952,  0.21816616,  0.2268928 ,  0.23561946,
        0.2443461 ,  0.25307274,  0.2617994 ,  0.27052602], dtype=float32)
```
方位角
```py
array([-0.27925265, -0.27052593, -0.26179934, -0.25307274, -0.24434602,
       -0.23561943, -0.22689271, -0.21816611, -0.20943952, -0.2007128 ,
       -0.1919862 , -0.18325949, -0.17453289, -0.1658063 , -0.15707958,
       -0.14835298, -0.13962626, -0.13089967, -0.12217295, -0.11344635,
       -0.10471976, -0.09599304, -0.08726645, -0.07853973, -0.06981313,
       -0.06108654, -0.05235982, -0.04363322, -0.03490651, -0.02617991,
       -0.01745319, -0.0087266 ,  0.        ,  0.00872672,  0.01745331,
        0.02618003,  0.03490663,  0.04363322,  0.05235994,  0.06108654,
        0.06981325,  0.07853985,  0.08726656,  0.09599316,  0.10471976,
        0.11344647,  0.12217307,  0.13089979,  0.13962638,  0.14835298,
        0.1570797 ,  0.1658063 ,  0.17453301,  0.1832596 ,  0.1919862 ,
        0.20071292,  0.20943952,  0.21816623,  0.22689283,  0.23561954,
        0.24434614,  0.25307274,  0.26179945,  0.27052605], dtype=float32)
```

现在通过三角定位将光束与直线对齐
```py
x_surface = np.ones_like(data) * np.sin(-azimuth[:, None])
plt.imshow(x_surface, cmap=utils.cmap)
y_surface = np.ones_like(data) * np.cos(-azimuth[:, None]) * np.cos(-zenith[None, :])
plt.imshow(y_surface, cmap=utils.cmap)
z_surface = np.ones_like(data) * np.sin(-zenith[None, :])
plt.imshow(z_surface, cmap=utils.cmap)
```
至于是用 sin 还是用 cos，取决于 Z 轴。如果 Z 轴是上下的，x_surface就用 sin，否则用 cos，y、z 轴依据 x_surface 使用的是正弦还是余弦而改变

传感器是有范围限制的，为了保证 LiDAR 图像的激光正常运作到物体上而不是撞墙了，需要创建一个掩膜来确认激光已达到最大行程没有返回

```py
a = [data != data.max()][0]
plt.imshow(a, cmap=utils.cmap)
```

![[Pasted image 20250511121756.png]]

可以看到，激光只碰到了我们需要的三个物体，没有其他的东西干扰

到现在，我们已经排除了角度对距离的干扰、其他物体对激光的干扰，现在可以正确地将两个数据合模了

```py
lidar_depth = data

x = lidar_depth * x_surface
z = lidar_depth * z_surface
y = lidar_depth * y_surface

plt.clf()
plt.subplot(1, 4, 1)
plt.imshow(x, cmap=utils.cmap)
plt.subplot(1, 4, 2)
plt.imshow(z, cmap=utils.cmap)
plt.subplot(1, 4, 3)
plt.imshow(y, cmap=utils.cmap)
plt.subplot(1, 4, 4)
plt.imshow(a, cmap=utils.cmap)
plt.show()
```

![[Pasted image 20250511122318.png]]

从左到右，依次是 X 轴上离传感器的距离、Y 轴上离传感器的距离、Z 轴上离传感器的距离与激光是否有效碰撞了物体

但单纯以二维图像的方式显示物体的远近并不直观，我们可以根据距离远近对图像进行着色，离传感器越近的地方显示为红色，越远的地方则显示为蓝色

```py
c = np.copy(z)
c_min = np.min(c)
c_max = np.max(c)
c = (c - c_min) / (c_max - c_min)
```

![[Pasted image 20250511123202.png]]

这样我们一眼就能看出来什么东西近什么东西远了！但这样还有不足：三个物体糊成一团，我们不知道谁对谁，它们的相对位置如何，让我们进一步拓展，让这张图以三维的形式动起来：

```py
def init():
    ax.scatter(x_scatter, y_scatter, z_scatter, c=c_scatter, cmap="rainbow", marker='o')
    return fig,

def animate(i):
    ax.view_init(elev=30., azim=i)
    return fig,

file_path = 'pointcloud.gif'
if not os.path.exists(file_path):
    anim = utils.animation.FuncAnimation(
        fig, animate, init_func=init, frames=360, interval=20, blit=True
    )
    anim.save(file_path, fps=30)
IPy_img(open(file_path,'rb').read())
```

![[pointcloud.gif]]

这样，这个组合数据就变得至臻完美了
## 训练一个单模态模型
^ccb332
### 制作数据集
训练一个单模态模型需要数据集，先从 LiDAR 数据入手
通过这段代码将 LiDAR 数据转换为张量（Tensor）
```py
def get_torch_xyza(lidar_depth, azimuth, zenith):
    x = lidar_depth * torch.sin(-azimuth[:,None])
    z = lidar_depth * torch.sin(-zenith[None,:])
    y = lidar_depth * torch.cos(-azimuth[:,None]) * torch.cos(-zenith[None,:])
    a = torch.where(lidar_depth < 50.0, torch.ones_like(lidar_depth), torch.zeros_like(lidar_depth))
    xyza = torch.stack((x, y, z, a))
    return xyza
```

然后创建一个 pytorch 数据集
```py
IMG_SIZE = 64
BATCH_SIZE = 32
VALID_BATCHES = 10
N = 9999

img_transforms = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor(),  # Scales data into [0,1]
])
```

这样是通过原始数据创建的数据集，一般来说还要进行数据增强（裁剪、翻转），进行数据增强时，其他要用于训练的数据也要完成相同的数据增强
```py
class MyDataset(Dataset):
    def __init__(self, root_dir, start_idx, stop_idx):
        self.root_dir = root_dir
        self.imgs = []
        self.lidar_depths = []
        self.positions = np.genfromtxt(
            root_dir + "positions.csv", delimiter=",", skip_header=1
        )[start_idx:stop_idx]

        self.azimuth = torch.from_numpy(azimuth).to(device)
        self.zenith = torch.from_numpy(zenith).to(device)

        for idx in range(start_idx, stop_idx):
            file_number = "{:04d}".format(idx)
            rgb_img = Image.open(self.root_dir + "rgb/" + file_number + ".png")
            rgb_img = img_transforms(rgb_img).to(device)
            self.imgs.append(rgb_img)

            lidar_depth = np.load(self.root_dir + "lidar/" + file_number + ".npy")
            lidar_depth = torch.from_numpy(lidar_depth).to(torch.float32).to(device)
            self.lidar_depths.append(lidar_depth)

    def __len__(self):
        return len(self.positions)

    def __getitem__(self, idx):
        rgb_img = self.imgs[idx]
        lidar_depth = self.lidar_depths[idx]
        lidar_xyza = get_torch_xyza(lidar_depth, self.azimuth, self.zenith)

        position = self.positions[idx]
        position = torch.from_numpy(position).to(torch.float32).to(device)

        return rgb_img, lidar_xyza, position
```

这样，数据集就准备好了
### 测试数据集
```py
train_data = MyDataset("data/replicator_data_parallel/", 0, N-VALID_BATCHES*BATCH_SIZE)
train_dataloader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, drop_last=True)
valid_data = MyDataset("data/replicator_data_parallel/", N-VALID_BATCHES*BATCH_SIZE, N)
valid_dataloader = DataLoader(valid_data, batch_size=BATCH_SIZE, shuffle=False, drop_last=True)
for i, sample in enumerate(train_data):
    print(i, sample[0].shape, sample[1].shape, sample[2].shape)
    if i == 5:
        break
```
经过之前的操作，我们知道数据集中包含三个物体，包含有三组 RGB 图、三组 LiDAR 图和三组位置数据
所以如果这里的数据集显示 `torch.Size` 是九个就正确了
### 开始训练
现在，创建一个单模态模型，因为 LiDAR 和图像这两种数据的形状相同，所以都可以使用卷积神经网络
```py
num_positions = 9

class Net(nn.Module):
    def __init__(self, in_ch):
        super().__init__()
        kernel_size = 3
        self.conv1 = nn.Conv2d(in_ch, 50, kernel_size, padding=1)
        self.conv2 = nn.Conv2d(50, 100, kernel_size, padding=1)
        self.conv3 = nn.Conv2d(100, 200, kernel_size, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(200 * 8 * 8, 1000)
        self.fc2 = nn.Linear(1000, 100)
        self.fc3 = nn.Linear(100, num_positions)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
```

### 常用损失函数
使用什么样的损失函数呢？均方误差？交叉熵损失？Hinge Loss？Huber Loss？还是负对数似然损失？

>- **均方误差（MSE, Mean Squared Error）**：用于回归任务，计算预测值与真实值之差的平方均值。
>- **交叉熵损失（Cross-Entropy Loss）**：常用于分类任务，衡量预测的概率分布与真实分布之间的差距。
>- **Hinge Loss**：用于最大化分类。
>- **Huber Loss**：结合了 MSE 和 MAE（Mean Absolute Error），在回归任务中对异常值较为鲁棒。
>- **负对数似然损失（Negative Log-Likelihood, NLL）**：用于概率模型，例如生成模型或序列建模。

均方误差等同于毕达哥拉斯定理，但没有开方。因为最小化 MSE 同时也会最小化 RMSE，所以这里可以直接用 MSE 损失函数
所以这里使用均方误差，然后进行二十轮循环训练
```py
loss_func = nn.MSELoss()
def train_model(model, optimizer, inputs_idx, epochs=20):
    train_losses = []
    valid_losses = []
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for step, batch in enumerate(train_dataloader):
            optimizer.zero_grad()
            outputs, target = utils.get_outputs(model, batch, inputs_idx)
            loss = loss_func(outputs, target)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        train_loss = train_loss / (step + 1)
        train_losses.append(train_loss)
        utils.print_loss(epoch, train_loss, outputs, target, is_train=True)
        
        model.eval()
        valid_loss = 0
        for step, batch in enumerate(valid_dataloader):
            outputs, target = utils.get_outputs(model, batch, inputs_idx)
            valid_loss += loss_func(outputs, target).item()
        valid_loss = valid_loss / (step + 1)
        valid_losses.append(valid_loss)
        utils.print_loss(epoch, valid_loss, outputs, target, is_train=False)
    return train_losses, valid_losses
epochs = 20

rgb_net = Net(4).to(device)
rgb_opt = Adam(rgb_net.parameters(), lr=0.0001)

xyz_net = Net(4).to(device)
xyz_opt = Adam(xyz_net.parameters(), lr=0.0001)

print("Training rgb_net")
rgb_train_loss, rgb_valid_loss = train_model(rgb_net, rgb_opt, 0)
print("Training xyz_net")
xyz_train_loss, xyz_valid_loss = train_model(xyz_net, xyz_opt, 1)
```

训练完成以后，我们需要验证训练是否有效，并逐步优化

```py
plot_x = range(epochs)
plt.xlabel("Epoch")
plt.ylabel("Average Loss")
plt.plot(plot_x, rgb_train_loss, "green", label = "RGB Train Loss")
plt.plot(plot_x, rgb_valid_loss, "darkgreen", label = "RGB Valid Loss")
plt.plot(plot_x, xyz_train_loss, "orchid", label = "XYZ Train Loss")
plt.plot(plot_x, xyz_valid_loss, "darkorchid", label = "XYZ Valid Loss")
plt.legend()
plt.show()
```

## 将两个单模态模型合成为多模态模型
^257ae8
### 前融合、后融合、中间融合
#### 后融合
在前面那些模型的基础上，通过一种相对简单的方法将两个模型合在一起：将每个模型的输出连接到最终输出，就像在创建一个集成模型，每个模型都会处理输入内容，并对最终结果进行加权投票

```py
networks = [rgb_net, xyz_net]

for network in networks:
    for param in network.parameters():
        param.requires_grad = False

class MyMultimodalModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.rgb_net = rgb_net
        self.xyz_net = xyz_net
        self.fc1 = nn.Linear(num_positions * len(networks), num_positions * 10)
        self.fc2 = nn.Linear(num_positions * 10, num_positions)

    def forward(self, x_img, x_xyz):
        x_rgb = self.rgb_net(x_img)
        x_xyz = self.xyz_net(x_xyz)
        x = torch.cat((x_rgb, x_xyz), 1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
```

上面的代码先分别分析每种数据类型，最后才将两个数据流合并，这种多模态模型被称为后融合

```py
mm_late_net = MyMultimodalModel().to(device)
mm_late_opt = Adam(mm_late_net.parameters(), lr=0.0001)
mm_late_train_loss, mm_late_valid_loss = utils.train_model(
    mm_late_net,
    mm_late_opt,
    get_mm_late_inputs,
    epochs,
    train_dataloader,
    valid_dataloader
)
```
#### 前融合
还有一种是前融合：将图片的颜色和位置的网络从一开始就进行混合处理
```py
def get_mm_early_inputs(batch):
    inputs_rgb = batch[0].to(device)
    inputs_xyz = batch[1].to(device)
    inputs_mm_early = torch.cat((inputs_rgb, inputs_xyz), 1)
    return (inputs_mm_early,)
mm_early_net = Net(8).to(device)
mm_early_opt = Adam(mm_early_net.parameters(), lr=0.0001)
mm_early_train_loss, mm_early_valid_loss = utils.train_model(
    mm_early_net,
    mm_early_opt,
    get_mm_early_inputs,
    epochs,
    train_dataloader,
    valid_dataloader
)
```

让我们看看两种融合方式的优劣
```py
plt.xlabel("Epoch")
plt.ylabel("Average Loss")
plt.plot(plot_x, xyz_train_loss, "goldenrod", label = "LiDAR Train Loss")
plt.plot(plot_x, xyz_valid_loss, "darkgoldenrod", label = "LiDAR Valid Loss")
plt.plot(plot_x, mm_late_train_loss, "green", label = "Late Fusion Train Loss")
plt.plot(plot_x, mm_late_valid_loss, "darkgreen", label = "Late Fusion Valid Loss")
plt.plot(plot_x, mm_early_train_loss, "orchid", label = "Early Fusion Train Loss")
plt.plot(plot_x, mm_early_valid_loss, "darkorchid", label = "Early Fusion Valid Loss")
plt.legend()
plt.show()
```

![[Pasted image 20250513115341.png]]

可以看到，在多次训练后，损失率都维持在较低的水平

#### 中间融合
前面的数据使用了三个大小形状不一的物体，使用前融合和后融合是没有物体的
可是三个大小形状相同，只有颜色不同的物体呢？我们引入中间融合来对这种情况进行处理
中间融合分为连接法和矩阵乘法
```
single_mode_data = np.genfromtxt("data/cubes_only_single_mode_results.csv", delimiter=',', skip_header=1)

plot_x = range(len(single_mode_data))
plt.xlabel("Epoch")
plt.ylabel("Average Loss")
plt.plot(plot_x, single_mode_data[:, 1], "green", label = "RGB Train Loss")
plt.plot(plot_x, single_mode_data[:, 2], "darkgreen", label = "RGB Valid Loss")
plt.plot(plot_x, single_mode_data[:, 3], "orchid", label = "XYZ Train Loss")
plt.plot(plot_x, single_mode_data[:, 4], "darkorchid", label = "XYZ Valid Loss")
plt.title("Cubes Only Single Mode Results")
plt.legend()
plt.show()
```
### 三种融合方式的优劣
中期融合解释性差，排错难，但效果最好
前期融合效果好，但必须考虑数据集间的相性
如果不想完全黑盒或者不想高误差，就用后期融合
## 微调