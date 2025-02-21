这种东西应该是有现成仓库的，结果查了半天发现都是 java 的
那玩毛，自己写！

借着[这篇博客](https://www.cnblogs.com/duanguyuan/p/16205179.html)，我知道了 maven 仓库有接口可以查

又通过分析 url 和包名的关系，发现了包的命名规律：
比如 org.springframework.spring-expression
它的 url 是 org.springframework/spring-expression
也就是将 - 前面的 . 替换成 / 就可以了
可以批量搞了

