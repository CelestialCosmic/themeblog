token输入 token输出
模型有局限性：固化于训练语料、时限性较差，无法获取内部资料
机器人-》数字人

序列建模：生成式AI的核心
输出 text audio image 3D video DNA protein molecule animation 

transformer depoting 模型都是序列建模的解决方案
transformer：hugging face的工具链
langchain：组织编排工具（工作流）

transformer 的原理
编码器任务
seq2seq

带状态的LLM

深度学习：图像序列从稀疏卷积到密集
有监督的训练材料太少，全链接在图像领域应用不好
后来有了 alexnet，参数空间减少了（一个像素点只和周围的一些区域相关，而不再是一个个像素地识别）
卷积层：特征提取
密集层：任务头
强迫语言模型理解上下文，并预测下一个token
浮点数乘权重并相加（可微分），最后得到一个 loss，通过反向传播修改权重以达到训练的目的
预测时，cat 80%,dog15%,bird5%，实际cat100%，那么 loss 为 20%
再训练迭代，cat86%,dog10%bird4%，那么loss变成14%
我们的目的就是要让loss变成0%
离散标签：对词/词组做成token，早期nlp时，输入bert进行处理后，进行对输入的sequence（[90%pos，10%neg]）预测，再预测输出，最后再预测回应
huggingface 为什么火爆：api多，有playground


（44分钟）
pipeline组件：前处理（token转换为张量）、推送、后处理（模型输出的浮点数解释为可读语言）
输入 ->encode 为数字 -> 加分类头 -> 输入 tensor -> 输出 tensor -> 翻译 -> 评分 -> 输出
模型带有的 config.json 中的 model_type 就是解释了模型使用的 tokenizer、结构、模型架构、注意力方向是单向的还是双向的等内容
tensor：张量：一系列浮点数进去一系列浮点数出来

embedding：输入内容并强迫模型理解全文语义
通过 embedding table（从词表中查id） 和 embedding layers 去理解词的意思



transformer：输入内容，也是通过table的方式，并添加 residual（残差） 防止偏离太远
注意力：输入序列时同时通入上下文，避免歧义
  value进入神经网络卷积
  query与key两个张量进行相乘，算出来 attension 矩阵 ，query和每个key之间的相关性，相关性越高，权重越大，模型也越倾向于使用
然后 value 再和 attension 进行计算，得到的张量通过输出神经网络，再组织输出

bert模型：编码器模型，将 transformer 做大了，也是它开了微调的头
适合用于语言推理的主干，[mask]预测

HFpipeline:编码器，负责特征提取、token分类（输入输出等宽，分类人名地名等关键信息）、掩码填充（预测语气、预测输出）、文本分类
现在bert依靠迁移学习，只需要训练任务头就能达到很好的效果

modelsize 分为 small med large xl etc
distil：借助基本模型和监督学习进行蒸馏
迁移学习、微调：sst2 conil squad2.0

无token预测、QA（逐token预测）等

性能最好的模型 modelsize 小于 1b，适用于专业场景

翻译任务中，不同的语言输入不一样，不能逐token处理，也不能完成输入法语输出中文这样的任务
所以提出编码器、解码器进行预测：编码器能看到整句话，解码器只能看到下一个token
解码器、编码器各有优缺：编码器能充分考虑上下文，适合逐token精细化处理、语义处理
解码器适合文本生成、m->n的任务
所以为了在合适的时间内能训练出来模型用编码器更合适
理想情况下，应该用编码器-解码器合作，衍生出了T5架构的模型，但训练成本高，不适合上下文和回复区分低的模型

不受限的自回归不好

![[Pasted image 20250515140133.png]]


transformer的优势：适合处理有序的序列

图片切成3x3（可以自定），每个块视作一个token，到 embedding转换为向量

图像和文本有相似性：
输入 text encoder 和 image encoder，预训练转换为向量


所以提出双编码器：通过两个模态的相似性克服模态差异

chatgpt就是decoder形式的

## 数据工作流
编排系统和多联动
通过编排、检索（语义工具进行相似度查询、VDB检索文档、数据库）、增强辅助llm
再增加 工具调用、借助路由切换提示词（分类器决定是否回答这个问题）来创造智能体