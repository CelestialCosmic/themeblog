## 伪协议

某种编程语言或应用，为了解决应用内部的需求，自行编制的协议
如下是php的伪协议：

|伪协议|协议所做的事|
|---|---|
| [file://](https://www.php.net/manual/zh/wrappers.file.php)| 访问本地文件系统
| [http://](https://www.php.net/manual/zh/wrappers.http.php)| 访问 HTTP(s) 网址
| [ftp://](https://www.php.net/manual/zh/wrappers.ftp.php)| 访问 FTP(s) URLs
| [php://](https://www.php.net/manual/zh/wrappers.php.php)| 访问各个输入/输出流（I/O streams）
| [zlib://](https://www.php.net/manual/zh/wrappers.compression.php)| 压缩流
| [data://](https://www.php.net/manual/zh/wrappers.data.php)| 数据（RFC 2397）
| [glob://](https://www.php.net/manual/zh/wrappers.glob.php)| 查找匹配的文件路径模式
| [phar://](https://www.php.net/manual/zh/wrappers.phar.php)| PHP 归档
| [ssh2://](https://www.php.net/manual/zh/wrappers.ssh2.php)| 安全外壳协议 2
| [rar://](https://www.php.net/manual/zh/wrappers.rar.php)| RAR
| [ogg://](https://www.php.net/manual/zh/wrappers.audio.php)| 音频流
| [expect://](https://www.php.net/manual/zh/wrappers.expect.php)| 处理交互式的流

## php伪协议利用代审通解

跟踪输入点
输入点进入到文件系统操作函数:`readfile()`、`file()`、`file_get_contents()` `cURL()` 这种
能够控制参数的开头

```
<?php
$input = $_GET['input'];
file_get_contents($input."qq");  //有缺陷
file_get_contents("qq".$input);  //没有缺陷
?>
```

上面的代码中，`file_get_contents($input."qq")`会将用户输入的内容与字符串"qq"合并，然后使用`file_get_contents`函数来读取文件。这种方法存在安全风险，因为用户可以通过在输入中添加恶意内容来访问系统中的任何文件，可能导致信息泄露或文件损坏。这种做法是不安全的，因为用户输入没有经过过滤或验证。

## 过滤绕过

### 30x 跳转
30x跳转也是SSRF漏洞利用中的一个经典绕过方式，当防御方限制只允许http(s)访问或者对请求的host做了正确的校验后，可以通过30x方式跳转进行绕过。

针对只允许http(s)协议的情况，我们可以通过

`Location: dict://127.0.0.1:6379`跳转到dict协议，从而扩大我们攻击面，来进行更深入的利用。

针对没有禁止 url 跳转，但是对请求 host 做了正确判断的情况，我们则可以通过 `Location: http://127.0.0.1:6379` 的方式来绕过限制

### URL 解析绕过
比如说，在 python3 中，对于同一个 url `:http://baidu.com\@qq.com`，urllib 和 urllib3 的解析就不一致

对于`http://baidu.com\@qq.com`来说，urllib3 取到的是 baidu.com，而 urllib 取到的却是qq.com

urllib3 与 chrome 的解析保持一致（将`\`视为`/`）。如果在 check_ssrf 中解析 url 函数用的是 urllib3，而业务代码发送请求时采用的是 urllib，两者之间的解析差异就会导致绕过的情况

> url 解析非常底层，其还涉及了 url 跳转，oauth 认证，同源策略（如 postMessage 中 origin 的判断）等一切会涉及到 host 判断的场景
> **编程语言对协议解析不一致，导致可能出现 SSRF**

### DNS 时间差

时间差对应 DNS 中的机制是 TTL。TTL 表示 DNS 里面域名和 IP 绑定关系的 Cache 在 DNS 上存活的最长时间。即请求了域名与 IP 的关系后，请求方会缓存这个关系，缓存保持的时间就是 TTL。而缓存失效后就会删除，这时候如果重新访问域名指定的IP的话会重新建立匹配关系及 Cache

当我们设置 TTL 为 0 时，当第一次解析域名后，第二次会重新请求 DNS 服务器获取新的 ip。DNS 重绑定攻击的原理是：利用服务器两次解析同一域名的短暂间隙，更换域名背后的 ip 达到突破同源策略或过 waf 进行 ssrf 的目的。

不过有些公共 DNS 服务器，比如 114.114.114 还是会把记录进行缓存，但是 8.8.8.8 是严格按照 DNS 协议去管理缓存的，如果设置 TTL 为 0，就不会进行缓存

除此之外，Linux 默认不会进行 DNS 缓存，mac 和 windows 会缓存(所以复现的时候不要在 mac、windows 上尝试)

### TLS

网站会和用户协商 TLS 链接，为了降低资源消耗，TLS/SSL提供了会话恢复的方式，允许客户端和服务端在某次关闭连接后，下一次客户端访问时恢复上一次的会话连接。所以有时候在请求同一个 https 站点时，因为会话的恢复，curl 会 re-use 之前的 session id
会话恢复有两种，一种是基于 session id 恢复，一种是使用 Session Ticket 的 TLS 扩展

那么利用方式就是这样的：session id 是服务器提供给客户端的，如果我们构建一个恶意的 tls 服务器，然后将我们的恶意 session id 发送给客户端，然后通过 dns rebinding，将服务器域名的地址指向内网 ip 应用，例如 memcache，客户端在恢复会话时就会带上恶意的 session id 去请求内网的 memcache，从而攻击了内网应用

这种攻击利用有限：依赖客户端，TLS 携带特殊字符时服务器解析失败等，但还是非常有启发性的攻击方式

### 利用 IPv6

## 修复方式
1. 去除 url 中的特殊字符
2. 判断是否属于内网 ip
3. 如果是域名的话，将 url 中的域名改为 ip
4. 请求的 url 为 3 中返回的 url
5. 请求时设置 host header为ip
6. 不跟随 30x 跳转（跟随跳转需要从1开始重新检测）