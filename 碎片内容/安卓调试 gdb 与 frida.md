对某个手机 APP 进行渗透测试，测试内容包括虚拟定位检测、调试检测、注入检测、劫持检测、代理检测、篡改检测等内容

>这是一次经过授权的测试，请不要在未授权的情况下对进行非法目的的渗透测试！
>本文章仅分享检测内容的前置条件预备，不分享测试的技术细节。

### 关闭 selinux
>需要模拟定位时关掉，但这东西不会自己开回去，记得开回去，也有模块自动做这事
```
adb shell getenforce
```
如果返回 `Enforcing`，说明开启，返回`Permissive` 说明关闭

使用 `setenforce 0` 临时关闭
如果需要永久关闭 selinux，需要编辑 `/etc/sysconfig/selinux`
`SELINUX=enforcing` 替换为 `SELINUX=disabled`
重启后，运行命令 `sestatus`
SELinux status 是 `disabled` 就可以了

### 获取日志
`adb shell logcat --pid 1234`

## IDA
在 IDA 的 `dbgsrv` 文件夹里自带一个 `android_server64` 和 `android_server`，`adb push` 进去
>这里 32 位的用 32 位，64 位的用 64 位，如果不知道先启 64 位的，在附加时会有\[32\] \[64\]说明是 32 还是 64 的
>IDA 也要开对位数！

给授权，开调试服务器

```sh
su
cd /data/local/tmp
chmod 777 ./android_server64
./android_server64
```

再开个终端转发端口

```
adb forward tcp:23946 tcp:23946
```

最后将 IDA 附加上去就可以了

如果卡 libc.so，就是在 fopen 有反调试，不必纠缠了，叫开发把加固下了

## Frida
### 前置准备
下载 frida-gadget 到如下路径：
```
%APPDATA%\Local\Microsoft\Windows\INetCache\frida\gadget-android-arm64.so
```
INetCache 可能是隐藏文件夹，输路径进去

文件名也要对上，github 上下下来的不叫这个名字
### 电脑上需要进行的操作
```
pip install frida frida-tools
```

输入 `frida-ps` 有进程说明成功
### 安卓上需要进行的操作
在 github 下载对应包，`adb push` 推进去
```
adb push <source> <destination> args
```

如果遇到 `remote secure_mkdirs() failed: Permission denied` 

先 `adb root` 再重试

输入 `frida-ps -U` 有进程说明成功

`frida -U -f app 连接测试 app

如果连不上，试试 `frida-ps -U -a`

>这个操作会让安卓开发者设置中的调试应用调整为测试的 app，事后记得关掉

如果反馈这个
```
Failed to spawn: shell command failed (am start -D $(cmd package resolve-activity --brief 'app'| tail -n 1))
```


## GDB


## HttpCanary
按着引导走就可以了，导出证书的时候要注意一个点：
系统 CA 证书格式都是特殊的 `.0` 格式，要将抓包工具内置的 CA 证书以这种格式导出后再转为系统信任的证书

## 参考资料
[frida入门总结 - 吾爱破解 - 52pojie.cn](https://www.52pojie.cn/thread-1128884-1-1.html)
## 检测判断依据
### 敏感配置
envir_type_mic_status：敏感配置常出现于本地IP代理配置、允许USB调试、允许模拟地理位置等配置项被设置为允许、设备麦克风正被调用，对应用可能造成较大安全风险。
USB 调试开启：敏感配置常出现于本地IP代理配置、允许USB调试、允许模拟地理位置等配置项被设置为允许、设备麦克风正被调用，对应用可能造成较大安全风险。
### 调试
调试行为常被攻击者用于动态运行过程中分析程序的执行逻辑，通过使用工具进行动态调试，攻击者可以一步步分析程序的执行流程，函数返回结果。
系统 23946 端口开放，此端口常见于调试工具使用，例如frida，ida等
### 风险应用
com.lerist.fakelocation
com.topjohnwu.magisk
### root
该设备存在文件 /system/bin/su 、/system/bin/su 、/system/bin/su 、/system/bin/ ，该特征的存在被判定为root手机。
该设备存在 Magisk 软件，该特征的存在被判定为root手机。
## 进攻与防御
### 照片活化防御
炫彩认证、加强算法强度
### 实时换脸