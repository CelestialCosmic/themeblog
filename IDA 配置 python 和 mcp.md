## 配置 python
如果装有 python 但是没有配，会有类似这样的提示：
```
Checking "Python 3.13" (3.13)
Found: "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0" (version: 3.13.14 ('3.13.14150.1013'))
Ignoring unusable AppStore Python "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\python3.dll"
no "No suitable Python installations were found
```

在 IDA 安装根目录下有 `idapyswitch.exe` ，执行如下命令：

```powershell
idapyswitch.exe --force-path "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\python3.dll"
```

然后再执行一次，选择 0 ，之后再启动时就不会报错了