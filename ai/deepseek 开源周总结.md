## 总结
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

软件包：
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
*但 3FS-KV 不在本次开源的范围内*


