
做了几天功课，显卡到了，装上，把线理清楚（没想到库存的两根 hdmi 一根 DP 一根不稳定，两根坏了，安装加测试用了两个小时），收尾完立刻最快速度点亮，上 deepseek
## 硬件条件
电脑配置：
1. cpu:amd 9950X
2. gpu:RTX 4070ti super 16G
3. 内存:48G * 2
4. 硬盘:1T nvme SSD * 2

其他的不重要，总之一开始上这个配置就是为了战未来，如今未来已至

VMware 配置：
1. 处理器:32
2. 内存:78.1G（80000MB）
3. 硬盘:8G（实际用了 2 G，不得不感叹 archlinux 还是这么小，虽然它的安装镜像不可避免地膨胀到了 1G 以上）
## 安装 archlinux
现在 archlinux 安装不用以前那么麻烦了，甚至比大多数常见的 OS 更快。直接 archinstall 按默认配置干过去就可以了，只需要 chroot 提前安装 nano 就行，其实也可以直接在 archinstall 里面加
tty 的中文块也是习惯就好，不习惯就装 openssh 然后在外面用 alacritty ssh 上去
配 yay archlinuxcn 是后话（我还想上 hyprland，当然也是后话），现在的目标是最快速度上 deepseek
## 开始配置
### 配置 VMware 的共享文件夹
VMware 添加路径，然后安装 vmware tools，如下两种方式都是可行的
#### pacman 安装
```
sudo pacman -S open-vm-tools
```
#### vmtools 构建
```shell
mkdir cdr
mkdir install
mount /dev/sr0 ~/cdr
tar xzvf VMwareTools-xxx.tar.gz -C ~/install
cd ~/install/vmware-tools-distrib
sudo ./vmware-install.pl
```

理论上一路 Enter 就行

如果提示 `What is the directory that contains the init directories (rc0.d/ to rc6.d/)?`，新开一个 tty，然后进行如下操作：
```
cd /etc
sudo mkdir init.d
cd init.d
for i in {0,1,2,3,4,5,6}; do mkdir rc$i.d; done
```
### 挂载共享目录
```
sudo vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other
```

此时 /mnt/hgfs 就有共享文件了（一次性），如果有需要每次都自动挂载就需要重做 fstab
模型两天前就下好了，就等着这一刻
## 配置 deepseek 前置
```
sudo pacman -S docker ollama ollama-cuda nvidia-open
ollama serve
```

ollama 检测到我没有没给这台机器导入 ssh 公钥，给我生成了一个 `id_ed25519` 的，明明我有一个 `id_ed25519` 用了好几年的......
如果没有装 ollama-cuda 就没有 gpu 驱动，提示 `no compatible GPUs were discovered`

![[Pasted image 20250220001410.png]]

除了 ollama serve，也可以用 systemd 自启 ollama
```
sudo systemctl start ollama
sudo systemctl status ollama
```

现在 ollama 起来了，hugging face 上下下来的是 `.safetensors`，不能直接用，需要一次转化

## 转 safetensors 为 gguf
### 前置
需要事先准备好 python、pip 和 git，还有 cmake yay

> archlinux 有专门的 python 打包，绝大多数情况是没有问题的，但 yay 的包不一定可用

暴力一些
```
pip install -r requirements.txt --break-system-packages
```

结果 pip 也出事：
```
No matching distribution found for torch~=2.2.1
```
原来是 python 版本太新，从 `/requirements-convert_hf_to_gguf.txt` `requirements-convert_hf_to_gguf_update.txt` 中删除 torch 再单装 torch

来回装了三四轮，archlinux 硬盘（8G）满了！
关机扩容，然后回来分区
```shell
sudo fdisk /dev/sda
F
e
2


w
lsblk
sudo btrfs filesystem resize max /
```

```
Resize device id 1 (/dev/sda2) from 7.00GiB to max
```
扩容完成，原来安装脚本默认分了 1G 给 EFI，真是豪华

扫除了所有障碍，终于将所有的包都安装完了
有三个警告，先不管：
```
WARNING: The script transformers-cli is installed in '/home/celestial/.local/bin' which is not on PATH.
WARNING: The scripts gguf-convert-endian, gguf-dump, gguf-new-metadata and gguf-set-metadata are installed in '/home/celestial/.local/bin' which is not on PATH.
WARNING: The script f2py is installed in '/home/celestial/.local/bin' which is not on PATH.
```

### 开始转化
> 不止要下最大的文件，json也要下
```shell
python convert_hf_to_gguf.py /mnt/hgfs/DeepSeek-R1-Distill-Qwen-32B --outfile /mnt/hgfs/DeepSeek-R1-Distill-Qwen-32B/out/out.gguf --outtype f32
```
这里的参数很重要，决定了模型需要的显存！
#### 参数解释
模型参数的占用可以参考这篇文章：[模型参数、量化方式与显存需求对照表](https://www.bytenote.net/article/250124376567971840)
更详细的参数可以参考这篇文章：[clvsit 个人博客](https://clvsit.github.io/%E6%A8%A1%E5%9E%8B%E5%8F%82%E6%95%B0%E9%87%8F%E5%8F%8A%E6%98%BE%E5%AD%98%E5%88%86%E6%9E%90/)
精度分为 FP32、TF32、FP16、BF16、FP8、FP4、NF4、INT8
带 F 的都是浮点数精度，INT  和 NF 是量化精度
越高的精度表达越准确，消耗也越大
为了减少资源占用，又发明了量化
量化后，资源占用减少，结果相似

在之前提到的文章中给出了公式**（训练）**
*所需显存 M ≈ 参数数量 P × 参数占用字节 B ÷ 1.073*
**70B**: M = 70 × 4 ÷ 1.073 = 260.95 GB
**32B**: M = 32 × 4 ÷ 1.073 = 119.29 GB

海光 DCU 提供了计算公式**（推理）**
*所需显存 M = （参数数量 P × 参数占用字节 B）÷（32 ÷ 加载模型位数 Q）× 1.2*
**70B**: M = 70 × 4 ÷ (32 ÷ 32) × 1.2 = 336.00 GB
**32B**: M = 32 × 4 ÷ (32 ÷ 32) × 1.2 = 153.60 GB

	[LLM-Model-VRAM-Calculator](https://huggingface.co/spaces/NyxKrage/LLM-Model-VRAM-Calculator)给出了另一种算法
> 模型大小（Model Size）：模型文件本身的大小
> 可训练参数数量（trainable Params）：一个模型自带的固定值，需要通过程序计算，以 Billion（B）为单位

推理：
*推理所需显存 ≈ 模型大小 × 1.2*
**70B**: M = 282 × 1.2 = 338.40 GB
**32B**: M = 131.1 × 1.2 = 157.32 GB
LoRA微调（训练）：
*训练所需显存 ≈ (模型大小 + 可训练参数数量 ×16 ÷ 8 × 4) ×1.2

> **额外参考：**
> [复刻ChatGPT语言模型系列 - 知乎](https://www.zhihu.com/column/c_1639029520995934208)
> [LLM训练指南:Token及模型参数准备](https://zhuanlan.zhihu.com/p/636812912)
> [LLM训练指南(二):模型参数、计算量、显存、计算时间计算](https://zhuanlan.zhihu.com/p/639872915)
#### 模型转换
报错！定睛一看，少了从 05 开始的 3 个部分，去查文件，原来少下了一个
释怀地笑了.....补一个就好了
转化需要 282G 空间，把电脑放着就行了，当时划分时，200G 给了系统，剩下的特地只分了一个区
一觉睡醒应该就可以了！（凌晨2:38）
事实转化速度很快，虚拟机跑了大概一个小时左右就完成了。131.1G 的 32B 大概 10 分钟不到也跑完了
两个模型和原来下下来的文件一起，吃了577.1G！
## 将模型导入 ollama
在 `out.gguf` 同级目录下，随便创建一个文件，我这里命名为 `modelfile`，里面写如下内容：
```
FROM ./out.gguf
```
准确来说写什么都行，只要 FROM 这个模型就可以了

```
ollama create 70b -f ./modelfile
```

```
copying file sha256:ae58d0bbc356411dd166d153cb44d18c4f0bdd05bc8b1d648f8fa710c2e5d1c6 100%
Error: write /home/celestial/.ollama/models/blobs/sha256-2405104184: no space left on device
```

原来加载模型会把模型写进硬盘，再扩容！

```
ollama run 70b 
提示需要 250G 内存
ollama run 32b
提示需要 100G 内存
ollama run 14b 
爆显存

```

## 收尾工作
### 转移启动分区
因为 windows 是先装的，EFI 分区在最前面，archlinux 又带了一个 EFI 分区，现在需要合并它们
挂载 windows 的 EFI，然后将其下的 EFI 全部复制到 /boot （不要再叫 EFI，重命名一下）
确认 os-prober 开启后，再做一次 grub-mkconfig 即可