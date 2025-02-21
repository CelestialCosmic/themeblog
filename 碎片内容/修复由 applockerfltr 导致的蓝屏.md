```
webthreatdefusersvc_xxxxx 服务因下列错误而停止: 
找不到指定的模块。
```

```
由于下列错误，applockerfltr 服务启动失败: 
系统找不到指定的文件。
```

这两个错误已经烦了我几个月了，很可能是我扬了 windows defender 导致的。因为懒加没时间一直没弄

今天稍微抽了点时间来看看到底什么导致了蓝屏

## 前期准备

打开`C:\Windows\Minidump`，里面有数份 dmp，直接开自然开不出来，所以需要工具
[Install WinDbg - Windows drivers | Microsoft Learn](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/)

直接在那下会提示*此应用包不支持通过应用安装程序安装，因为它使用了某些受限制的功能*。

但是可以绕过：
使用任意文本编辑器打开那个 `windbg.appinstaller` ，然后直接访问`MainBundle` 中的 uri 就可以下到本体了

下到了本体，还要用压缩软件如 nanazip、7z 打开那个大包，然后提取文件本体出来

为什么这么做？因为拿那打包直接安装还会提示上面的报错
## 分析

把我手里的五个 dmp 依次丢进去，然后分析

我们需要收集的内容有：`PROCESS_NAME` `FAILURE_BUCKET_ID`

收集到了这些错误：
```
nt!HalpTscQueryCounterOrdered+d
nt!PpmIdleExecuteTransition+12cb
nt!PpmIdleExecuteTransition+143c
nt!KiIpiInterruptSubDispatch+78
nt!KeQueryPerformanceCounter+94
Netwtw10!prvConnectToSsidCandidateSelectedHandler+296
```

更离谱的是 process_name 居然都是 system！

## 解决 applockerfltr
**解决这个问题会导致风险**

> [Deactivate the kernel mode filter driver - Windows Server | Microsoft Learn](https://learn.microsoft.com/en-us/troubleshoot/windows-server/installing-updates-features-roles/deactivate-kernel-mode-filter-driver#disable-filter-drivers)
> This workaround may make your computer or your network more vulnerable to attack by malicious users or by malicious software such as viruses. We do not recommend this workaround but are providing this information so that you can implement this workaround at your own discretion. Use this workaround at your own risk.
> An antivirus program is designed to help protect your computer from viruses. You must not download or open files from sources that you do not trust, visit Web sites that you do not trust, or open e-mail attachments when your antivirus program is disabled.



