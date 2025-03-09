# Part0：写在前面
>本作品采用[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)进行许可。转载请注明出处，不得用于商业用途，并以相同协议共享。

这篇文章基于大量前人研究、开源仓库与个人见闻与个人实践
感谢愿意开放源代码、愿意分享的人们为这篇文章所探过的路，没有各种公开供研究的代码、文章，是无法完成这篇文章的

# Part1：AI 要用来做什么
这个相信都知道，已经再说就没意思了
下面的链接是 DeepSeek **官方推荐**的集成案例，没有本地搭建条件/需求的直接抓这些用就行
[awesome-deepseek-integration/README\_cn.md at main · deepseek-ai/awesome-deepseek-integration · GitHub](https://github.com/deepseek-ai/awesome-deepseek-integration/blob/main/README_cn.md)

# Part2：基础知识
AI 主要包含四个领域：自然语言处理（NLP）、机器学习（ML）、深度学习（DL）、计算机视觉（CV）
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
   游戏 AI、机器人行走、机器人走迷宫属于此类
   ![[Pasted image 20250226133901.png]]
   很久以前看过的视频，通过强化学习让 AI 自己探索走路方式，当时对这个印象很深刻
#### DL（深度学习、机器学习的加强版）
从属于机器学习，暴力理解就是 **pytorch**
在 openAI 的 ChatGPT3.0 铺开以后，深度学习所需标准下放，于是就有了下面这张图：
![[Pasted image 20250226135626.png]]

注：requests 是 python 最常用的请求库，不适用 AI 训练和学习

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

<hr>
<center><b>深水区警告！该部分往下仅适合拥有计算机背景的人群阅读</b></center>
<hr>

## AI 模型解析
### 基本名词
#### 参数
AI 参数模型（或**权重**）是用来描述神经网络中每个节点的数值
B 是 billion（十亿）的缩写，70B 便表示该模型包含 700 亿以上的参数

#### 量化
量化是指将模型参数和计算方式从高精度转换为低精度，以减少模型的存储和计算需求
量化涉及计算机底层存储数据的方式：**整形和浮点数**
每个参数都是通过整形或浮点数加载到显存中的，因此**要运行模型，首先需要将模型装载到显存中**
##### 量化相关数据结构
INT4、INT8、FP16、BF16、TF32、FP32 等都是用于深度学习的数值格式，它们和常规的整形、浮点数类似，但又有不同
下图是各类浮点数的量化：
![[40f81dad82708dc.webp]]
- Sign 存储正负，占用 1 个比特
- Range 存储数值范围，拥有的比特越大能表示的范围越大
- Precision 存储精度，拥有的比特越多越精准
**FP16 使用 16 位比特来表示一个参数，这 16 比特是要实打实装进显存里面的，假设需要装载 1.5B 的模型，那么就是 15 亿个这样的单元装进显存，并需要配套的 cpu、内存和硬盘**
由图类推可知： FP32 一个单元占用 32 bit，BFLOAT16 一个单元占用 16 bit，TF32 比较特殊，一个单元占用 19 个 bit，介于 2 byte 和 3 byte 中间
##### 高精度与低精度间的优劣
精度越高，需要的显存越高。除浮点数之外还有 Int8 Int4 之流的量化方式，**占用更小，但模型精度也更差**
比如将 FP32 浮点数参数量化为 Int8，可以**减少约四分之三的存储空间**（每个参数占用从 32 bit 降低至 8 bit）
可是人吃不饱饭会不干活，AI 吃不饱虽然不会拒绝干活，但幻觉、复读、答非所问出现的概率那就不得而知了

非结构化数据的解析能力需要一定规模和精度的模型才能支持
##### 精度与参数如何取舍？
**参数**数量决定了思考问题的**广度**，量化**精度**决定了思考问题的**深度**
大多数情况下推荐降低精度，增加参数量。但也不能为了追求参数量而无脑抛弃精度
1 字节 / 参数以下（也就是比 Int4 还差的量化）的量化会导致非常明显的性能下降
##### 模型的格式
对应于不同类型的量化，有不同的表达方式，其遵循如下规律：
<center>Q + X （用于存储权重的位数）+ 特定变体</center>
`X`是量化位数，也就是参数占用的比特数（和 fp16、fp32 后面的数字是一个东西），对设备性能的要求也随之有偏重

###### 特定变体解析

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
1. **IQ**：代表"Importance Quantization"（重要性量化），使用重要性矩阵来改进量化结果
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

###### 最常见的量化方式
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
   - **只能在 Hugging Face 上执行**
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

>仅推理推荐使用 gguf 和 bin

![[gguf-spec.png]]
<center>gguf 模型文件结构示意图</center>

#### 模型选型与推荐配置

##### 估算模型所需性能
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

##### 运行模型的最低要求
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
# Part3：DeepSeek 开源周
## 开源周内容总览
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

依赖包：
```
cmake libuv1-dev liblz4-dev liblzma-dev libdouble-conversion-dev libprocps-dev libdwarf-dev libunwind-dev libaio-dev libgflags-dev libgoogle-glog-dev libgtest-dev libgmock-dev clang-format-14 clang-14 clang-tidy-14 lld-14 libgoogle-perftools-dev google-perftools libssl-dev gcc-12 g++-12 libboost-all-dev
```

### 知识基础
#### 分布式文件存储系统
分布式文件存储系统的**数据存储在多台机器上**，也就是存储节点，由多个节点构成分布式集群，节点上的小的分布式文件系统组合成总的分布式文件系统，由**主服务器对总的文件系统进行管理**。用户任意访问某一台主机，都能获取到自己想要的目标文件
> 其与 RAID（冗余磁盘阵列）不同，分布式文件存储系统是多机器多硬盘，RAID 是单机器多硬盘
> 虽然存在**分布式 RAID**，但较为少见
> 其与**存储桶**也不同，存储桶是优于传统的文件系统或关系数据库的对象存储，虽然是分布式的，但不属于分布式文件存储系统

#### KVCache
KVCache（键值缓存）是大模型推理中常用的优化技术，在各种类型的模型，尤其是 Transformer 中，它通过缓存每个 token 在经过 Transformer 时生成的键（Key）和值（Value）来减少重复计算，从而提高推理速度，其本来是存放于**内存**中的，但借助 **3FS-KV**，也就是 3FS 变种，专注于共享存储分布式数据处理系统，使得 KVCache 可以放到 **SSD** 中，进一步优化模型的内存需求
>但 3FS-KV 不在本次开源的范围内

## 第六日：基础设施
该部分略过

# Part4：部署
> 该部分使用系统：archlinux & windows 11
> 没有保密需求、没有定制需求可以直接返回 Part1
> 且视作没有系统性能瓶颈，已经对计算机知识和 Part2 的内容有足够的了解
> **虚拟机部署需要支持显卡直通**

## 安装 archlinux
不再推荐传统手装，archinstall 按默认配置干过去即可，唯一要做的是预装一个编辑器，想要 swap 想要 btrfs 自己调，默认配置安装甚至比常见的其他发行版安装速度更快

这个安装不包含 KDE Xfce sway 或 hyprland，想配 DE 自己配

```sh
sudo pacman -S ollama ollama-cuda nvidia-open
ollama serve
```

如果没有装 ollama-cuda 就没有 gpu 驱动，提示 `no compatible GPUs were discovered`

## 转 safetensors 为 gguf
>没有特殊量化要求可以直接用 ollama 拉取现成镜像，直接跳过这一步
### 前置
需要事先准备好 python、pip 和 git，还有 cmake yay

> archlinux 有专门的 python 打包，绝大多数情况是没有问题的，但 yay 的包不一定可用

又不想一个个装包又不想用虚拟环境的话，暴力一些可以这么做：
```sh
pip install -r requirements.txt --break-system-packages
```

python 版本太新会有这个提示：
```
No matching distribution found for torch~=2.2.1
```
从 `requirements-convert_hf_to_gguf.txt` `requirements-convert_hf_to_gguf_update.txt` 中删除 torch 依赖后再单独装 torch 即可

```sh
python convert_hf_to_gguf.py /mnt/hgfs/DeepSeek-R1-Distill-Qwen-32B --outfile /mnt/hgfs/DeepSeek-R1-Distill-Qwen-32B/out/out.gguf --outtype q8_0
```
`outfile` 指定输出路径，`outtype` 指定量化方式，有什么量化方式不再赘述

模型输出完成后就可以导入了

## 导入模型
在 `out.gguf` 同级目录下，随便创建一个文件，这里命名为 `model.txt`，里面写如下内容：
```
FROM ./out.gguf
```

支持绝对/相对路径，只要指向这个文件怎么写都行，`FROM` 不限大小写，大写只是为了区分开语法与常规字符

```sh
ollama create 70b -f ./modelfile
```

>这个过程需要和模型大小接近的存储空间，且默认在 `~/.ollama`（archlinux）`%USERPROFILE%/.ollama`（windows），需要提前评估空间是否足够，不足应提前迁移模型存储位置

完成以后就可以运行模型了

```sh
ollama run 70b
```

等待加载完成就可以开始自由对话了

# 训练




