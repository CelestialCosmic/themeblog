在前后端分离的服务器上，前端允许 get 携带一些内容，如 `Content-Length` 和 `Transfer-Encoding` ，而后端不允许时，可能导致前后端对请求的理解不一致，进而导致漏洞

![[12067578-ef5919dd26ad0c56.webp]]
正常请求
![[12067578-f3179f4f268a3ef1.webp]]
走私后的请求会将上一个包的一部分截留下来，后面再发送请求时，上一个包的部分内容会和新的包一起解析

上一个包：

```http
POST ...
...
...
1
F
G
```

发第二个 GET 的时候就会变成这样：

```http
FGGET ...
...
...
```

上一个 POST 包的 FG 被截留下来，然后接到的后一个 GET 包的前面

回显时的具体表现就是前端返回 400/403 等，但是后端返回了我们需要的东西

针对此类漏洞，有如下三种分类：

- CLTE：前端服务器使用 `Content-Length` 头，后端服务器使用 `Transfer-Encoding` 头
- TECL：前端服务器使用 `Transfer-Encoding` 标头，后端服务器使用 `Content-Length` 标头。
- TETE：前端和后端服务器都支持 `Transfer-Encoding` 标头，但是可以通过以某种方式（如混淆）来诱导其中一个服务器不处理它。

