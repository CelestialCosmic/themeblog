CMS 识别工具：whatweb、webrobo、御剑 web、轻量 web 指纹识别、椰树
apache 是静态网页，tomcat 是动态网页

## 回源
ping IP 时有 CDN 一般都会返回 CDN 地址
但是在 CDN 未覆盖的位置，会直接回到源站点，也就是回源
拿到真实 IP 后，可以通过直接访问 IP 验货，不过如果打不开也不是说明结果就不正确
拿到真实 IP 并不是很重要，但是拿到以后能从更多角度开展攻击

## cookie 的工作原理
cookie 是唯一的识别码，在报文中产生 `Set-cookie:123`，收到响应后，浏览器就会在 cookie 中添加一行，后续都会将这个 cookie 取出并加到请求报文的首行，如 `Cookie:123`。

## 危险头部参数
User-Agent（UA）：网站经常基于 UA 发送不同的页面，伪装 UA 可绕过检测
X-Forwarded-For（XFF）：它是请求来源的真实 IP，负载均衡、http代理时都会带这个头，`X-Forwarded-For:client,proxy1,proxy2`，这样分隔做出来的 IP 会显示从头到尾每级路由的 IP
Referer：跳转时告知目标网页跳转时的来源（上一个访问的页面是哪个页面）