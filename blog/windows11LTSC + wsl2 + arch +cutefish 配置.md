windows11 发布了 ltsc，正好有一台新的笔记本需要弄系统，于是选择了这套方案
## 修复 windows

### 清理 defender
从[GitHub - ionuttbara/windows-defender-remover: A tool which is uses to remove Windows Defender in Windows 8.x, Windows 10 (every version) and Windows 11.](https://github.com/ionuttbara/windows-defender-remover)的 release 里下载工具

然后执行，在此期间 windows defender 自然会疯狂自保，不停地放行脚本的操作，同时不允许 defender 获取权限，跑到 10% 左右 windows defender 就已经被破坏了

### 汉化
windows 11 ltsc 是没有中文的，在语言里面下载

语言下载以后是没有显示语言选项的，进到语言包内部再下一次才会在显示语言里面出现中文，登出应用

至于输入法的问题，用[GitHub - KumaTea/win11-chn-fix: Windows 11 中文输入法修复 Chinese Input Method Fix](https://github.com/KumaTea/win11-chn-fix)解决

windows 显示字体则在 应用 -> 可选功能 中安装“简体中文补充字体”解决一部分，下不下来还有叫“win10 默认字体.7z”的压缩包，把压缩包里的字体全装了也可以彻底解决问题，因为这东西是很久以前收集在百度网盘里面的，这里忽略

吐槽一下，微软的社区永远和没用一样，不要太指望那上面有答案

## archlinux
[GitHub - sileshn/ArchWSL2: Archlinux for WSL2 using wsldl](https://github.com/sileshn/ArchWSL2)

> 时间也是过得挺快的，四年前的 archlinux 不仅要手装，而且一堆人还看不起安装脚本，而现在大家都默认用安装脚本了，虽然我也只是在底层维护时还用手敲指令

在此之前确认开了 wsl，剩下的跟着要求做就行（如更新内核、设置默认版本之类的操作）

如果报“容器没有回应”之类的报错，检查 cpu 使用情况，我是因为 nessus 编译插件吃满了 cpu 导致失败

完了以后更新 `/etc/pacman.d/mirrorlist` 跑一次 `sudo pacman -Syu`

### 修复 systemd

虽然 `/etc/wsl.conf` 里 systemd 已经默认开启，但指令依旧没用，因为这个 wsl 没更新

还需要跑一次 `wsl --update`

更新完了以后就会发现 wsl 用不了了

按照这里操作[WSL2 fails to start with Error code: Wsl/Service/CreateInstance/CreateVm/ConfigureNetworking/HNS/0x80070424 · Issue #10755 · microsoft/WSL · GitHub](https://github.com/microsoft/WSL/issues/10755)

1. 关闭 hyper-v
2. 重启
3. 打开 wsl 然后根据提示安装功能
4. 重启
5. 再打开 wsl 的时候就发现正常了

此时 wsl 正常，systemd 也可以正常用了

如果代理是常驻的话，还会有提示：`wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理`

要解决这个，可以通过 `nano ./.wslconfig` 然后添加如下内容解决
```toml
[experimental]
autoMemoryReclaim=gradual  
networkingMode=mirrored
dnsTunneling=true
firewall=true
autoProxy=true
```

> `./` 默认打开的是 `%USERNAME%`

### 桌面环境

因为看 y7n05h 玩过 i3wm，我自己也弄过 sway 和 kde plasma，虚拟机和 VPS 见过 centos 和 ubuntu,公司有 kirin 和 tencentOS，所以这次整点别的

我想选 hyperland，但是它明确表明不支持

收集了一段时间信息后发现目前支持 wsl2 的 de 并不多，明确表明支持/已有实现的有 kde plasma,gnome,XFCE,Win-KeX(kali),fedora remix,LXQt,MATE,Cinnamon,mobaxterm,cutefish

> cosmic 不确定是否支持

换句话说，目前没看到有平铺桌面支持 wsl2 ，毕竟天生相克，不奇怪

首先去掉玩过的，然后去掉难看的，再去掉不支持的，那就只剩下 cutefish 了

#### 先头准备

需要一个驱动 [使用 WSL 运行 Linux GUI 应用 | Microsoft Learn](https://learn.microsoft.com/zh-cn/windows/wsl/tutorials/gui-apps#install-support-for-linux-gui-apps)

[opensuse/Cutefish-Arch.txt at main · vinberg88/opensuse · GitHub](https://github.com/vinberg88/opensuse/blob/main/Cutefish-Arch.txt)

> 尽信书不如无书，Cutefish-Arch.txt 的内容实际上是为 ubuntu 准备的，并不完全适合 archlinux，根据自己的经验操作

##### 实际操作

安装 xlaunch，安装完后启动，选择 One large window，接着一直 next ，直到 xlaunch 的窗口出现就可以放着不管了

`sudo pacman -S cutefish` 安装 cutefish

注意有几个包 如果 mirrorlist 里面只有 cn 镜像会 404，要用 all 的 worldwide 才能下得到 [Arch Linux - Pacman Mirrorlist Generator](https://archlinux.org/mirrorlist/)

然后装图形依赖

```sh
sudo pacman -S xorg xorg-server xorg-xinit mesa xterm xorg-twm xorg-xrandr
sudo pacman -S xorg-twm xterm xorg-xclock sddm bluedevil libqtxdg
sudo pacman -S xorg-server xorg-xinit xorg-xrandr xorg-xfontsel xorg-xlsfonts xorg-xkill xorg-xinput xorg-xwininfo
```

装完了以后，执行如下命令

```sh
sudo systemctl enable sddm
sudo systemctl set-default graphical
sudo systemctl set-default multi-user.target
sudo systemctl set-default graphical.target
sudo ln -fs /usr/lib/systemd/system/graphical.target /etc/systemd/system/default.target
```

`nano ~/.bash_profile` 添加如下内容

```sh
export XDG_SESSION_TYPE=x11
export XDG_SESSION_CLASS=user
export GDK_BACKEND=x11
export LIBGL_ALWAYS_SOFTWARE=1
```

保存后， Ctrl-C Ctrl-D 接 `wsl --shutdown`，再接 `wsl`

然后执行 
```sh
. ~/.bash_ubuntu_desktop
exec dbus-run-session /usr/bin/cutefish-session
```

现在回 xlaunch 看，应该有桌面出现了

之后再启动桌面，还是通过上面那两个指令启动，可以做成脚本

```sh
nano ./desktop.sh

. ~/.bash_ubuntu_desktop
exec dbus-run-session /usr/bin/cutefish-session

sudo chmod +x ./desktop.sh
```

做完以后发现还是 kde 好看......

但不论如何，对于轻薄本来说，这个配置能撑好一段时间了