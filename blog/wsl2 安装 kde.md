最终 cutefish 没能留下

## 我是如何玩炸 WSL 的

```sh
sudo pacman -S plasma
sudo pacman -S lightdm xorg-server-xephyr
```

然后启动 VcXsrv，选择下面两个中随便一个启动

之后在终端里面输入 `startplasma-wayland` 然后出现了数个新的窗口，支持操作，但是图形界面根本残废一个

根据[Ivon的部落格](https://ivonblog.com/posts/run-linux-desktop-on-wsl/)所言，看样子只能跑 x11 了

根据其中的内容添加了系统变量

```sh
export XDG_SESSION_TYPE=x11
export GDK_PLATFORM=x11
export GDK_BACKEND=x11
export QT_QPA_PLATFORM=xcb
export WAYLAND_DISPLAY=
export DISPLAY=:1
```

编辑 `/etc/lightdm/lightdm.conf`

```toml
[Seat:*]
user-session=plasma
[LightDM]
start-default-seat=false
[XDMCPServer]
enabled=true
port=177
```

结果这一波操作下来，把 arch wsl 弄炸了，还一直报 0x8007019e 不允许重装，彻底没得玩了。

倒腾了两天，最终以把在“应用”里面的整个 wsl 和 wsl 更新从 windows 里面彻底删除为代价，救回了 wsl 重装的能力。

代价是 wsl 回退到了 wsl1 ，并且失去了自动更新的能力和，只能手动更新至 wsl2，systemd 也彻底报废了

## 第二次尝试

先用 pacman 装 fish

```sh
sudo pacman -S fish
set -U fish_greeting ""
```

安装 aur
```sh
git config --global --replace-all core.fileMode false
git clone https://aur.archlinux.org/yay.git
makepkg -si
```

>不能以 root 身份进行 git clone

如果在 makepkg 时提示 fakeroot 环境有问题，编辑 `/etc/pacman.conf`，更改如下内容：

```
IgnorePkg = fakeroot
```

如果还不行，就将 fakeroot 换成 fakeroot-tcp：

先执行 [Setup fakeroot-tcp without SystemV IPC support. · GitHub](https://gist.github.com/tytydraco/df14e4f7af737e7b51ba35842f75342b)这个脚本，新版的贴在下面了

```sh
#!/bin/bash

cd /tmp
wget http://ftp.debian.org/debian/pool/main/f/fakeroot/fakeroot_1.31.orig.tar.gz
tar xvf fakeroot_1.31.orig.tar.gz
cd fakeroot-1.31/
./bootstrap
./configure --prefix=/opt/fakeroot \
        --libdir=/opt/fakeroot/libs \
        --disable-static \
        --with-ipc=tcp
make
sudo make install
OLDPATH="$PATH"
export PATH="/opt/fakeroot/bin:$PATH"

cd /tmp
rm fakeroot_1.31.orig.tar.gz
rm -rf fakeroot-1.31/

git clone https://aur.archlinux.org/fakeroot-tcp.git
cd fakeroot-tcp
makepkg -si

cd /tmp
rm -rf fakeroot-tcp
sudo rm -rf /opt/fakeroot

export PATH="$OLDPATH"
```

做完了这个再去执行就不会有问题了

如果下载过程有问题的话，那就是 go 的问题，换源

此时装完了 xdrp

接着根据[Can't use X-Server in WSL 2 · Issue #4106 · microsoft/WSL · GitHub](https://github.com/microsoft/WSL/issues/4106)来设置默认的显示器

```sh
export DISPLAY=$(route.exe print | grep 0.0.0.0 | head -1 | awk '{print $4}'):0.0
```

打开 xlaunch ，然后设置 one large window、显示器设置为 0、Start no client、取消 Primary Selection 的选择、选择 Disable access control，最后在参数中加入 `-ac`

```
org.kde.startup: "kapplymousetheme" QList("breeze_cursors", "24") exited with code 2
kf.kirigami.platform: Failed to find a Kirigami platform plugin for style "Fusion"
Failed to build graphics pipeline state
Failed to compile shader:
Source was:
#version 120

struct buf
{
    mat4 matrix;
    float opacity;
};

uniform buf ubuf;

attribute vec4 vertexCoord;
varying vec4 color;
attribute vec4 vertexColor;
attribute float _qt_order;

void main()
{
    gl_Positi^Con = ubuf.matrix * vertexCoord;
    color = vertexColor * ubuf.opacity;
    gl_Position.z = _qt_order * gl_Position.w;
}
```