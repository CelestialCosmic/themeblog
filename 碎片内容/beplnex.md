IL2CPP
## 参考资料
[Unity 逆向入門第二篇：反編譯 - Flydragon's Blog](https://flydragonw.github.io/posts/unity_reverse_2/)

## 参考资料
[es3存档文件获取密钥和修改教程，利用BepInEx和ES3SaveHook](https://www.bilibili.com/opus/1085017217017315328)
[Tutorial - Unity - How to edit/decrypt EasySave 3(.es3) Save Files](https://f95zone.to/threads/how-to-edit-decrypt-easysave-3-es3-save-files.165329/)

es3 多见于 PlayMaker,dnspy 或者游戏目录如果看到 hutonggames,那基本按下面的一把梭就行

下载 BeplnEx,将整个压缩包的内容丢到根目录下面,也有自动安装器,但是 ES3SaveHook 链接废了,不能一键装

如果是从官方源安装的,需要在 `BeplnEx/config/BeplnEx.cfg` 中启用终端
```
[Logging.Console]
## Enables showing a console for log output.
# Setting type: Boolean
# Default value: true
Enabled = true
```
再去拿 [ES3SaveHook.zip](https://pixeldrain.com/u/hanE4A33),按架构放到 `BeplnEx/plugins` 下面
启动一次游戏,读到存档了以后就会在游戏根目录下产生 `decryption.key`,拿着 key 和存档去 [EasySave3 Editor](https://es3.tusinean.ro/) 加解密,然后快乐修改就行了