因为同时要装一个在线设备和一个离线设备，所以既有在线的也有离线的步骤
## 为 IDA 配置 python
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

## 安装 uv
官方给的是这个
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

验证是否正常
```powershell
uv --version
uv 0.12.4 (77803aa22 2026-08-13 x86_64-pc-windows-msvc)
```

离线安装可以先去 [GitHub - astral-sh/uv: An extremely fast Python package and project manager, written in Rust. · GitHub](https://github.com/astral-sh/uv)的 release 下载安装包，然后以管理员身份启动 powershell，执行如下指令
```powershell
$env:Path = "C:\Users\root\.local\bin;$env:Path"
```

uv 的可执行放在哪个路径就什么路径，安装脚本是在 `%USERPROFILE%/.local/bin`

> 直接右键执行脚本大概率会跳一行红的然后瞬间退出
```powershell
.\uv-installer.ps1 : 无法将“.\uv-installer.ps1”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，
  如果包括路径，请确保路径正确，然后再试一次。
  所在位置 行:1 字符: 1
  + .\uv-installer.ps1
  + ~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (.\uv-installer.ps1:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
```

```powershell
Set-ExecutionPolicy ByPass
```

## 配置 IDA-MCP

```powershell
pip install --upgrade git+https://github.com/mrexodia/ida-pro-mcp
```

离线时需要根据指定版本先下载再安装，而且因为 python 版本不同，所以也有不同
```powershell
pip download git+https://github.com/mrexodia/ida-pro-mcp --python-version 3.12 --platform win_amd64 --abi cp312 --only-binary=:all: -d ./
```

然后执行安装（按空格选择需要的编辑器）

```powershell
ida-pro-mcp.exe --install
[MCP] No IDA instances discovered, using default 127.0.0.1:13337
Installed IDA Pro plugin (IDA restart required)
  loader: C:\Users\root\AppData\Roaming\Hex-Rays\IDA Pro\plugins\ida_mcp.py
  package: C:\Users\root\AppData\Roaming\Hex-Rays\IDA Pro\plugins\ida_mcp
Select transport mode: Streamable HTTP (recommended)
Select installation scope: Project (current directory)
Select project targets to install: VS Code
Installed VS Code MCP server (restart required)
  Config: C:\Users\root\.vscode\mcp.json
```
```powershell
ida-pro-mcp.exe" --config
```

配置完以后 vscode 会提示 `不应再在用户设置中配置 MCP 服务器。请改用专用 MCP 配置。`，点更新处理一下就行

都配置完成以后点击 Edit->Plugins->MCP
```
[MCP] Registered instance: 通话录音.exe (pid=14712, port=13337)
  Discovery file: C:\Users\root\AppData\Roaming\Hex-Rays\IDA Pro\mcp\instances\instance_13337.json
```

这样就完成了