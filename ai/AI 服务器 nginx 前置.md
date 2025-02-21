AI 以集群方式部署时，需要 nginx 对流量进行分流 ^2lULjwD9

```
upstream www.example.com{   //分流，根据不同的策略
        server  www.example.com:8080 weight=1;
        server  www.example.com:9080 weight=1;
        #server 192.168.1.1:8080 //也可以用每一个tomcat的IP来配置
        #server 192.168.1.2:9080 
}
server{
  listen 80; //监听在80端口
  autoindex on;
  server_name example.com www.example.com;  // 表示监听后转到哪里去
  access_log /usr/local/nginx.logs.access.log combined;
  index index.html index.html index.jsp index.php

  location /{
        proxy_pass http://www.example.com;  // 表示匹配的路径，指向到域名，然后此域名到上面进行分流，负载均衡
        add_header Access-Control-Allow-Origin *;
  }
}
```

## nginx负载均衡配置、常用策略、场景及特点

- 轮询（默认）

优点：实现简单

缺点： 不考虑每台服务器的处理能力

```java
upstream www.example.com{
        server  www.example.com:8080;
        server  www.example.com:9080;
}
```

- 权重 （电脑配置不一致）

```java
upstream www.example.com{
        server  www.example.com:8080 weight=15;
        server  www.example.com:9080 weight=10;
}
```

- IP hash （前面介绍过，根据 ip 算hash）

优缺点： 前面讲过

```java
upstream www.example.com{
        ip_hash;
        server  www.example.com:8080;
        server  www.example.com:9080;
}
```

- url hash （第三方，需要装一个插件）

优点：能实现同一个服务访问同一个服务器

缺点：根据url hash分配请求会不均匀，请求频繁的url会请求到同一个服务器上

- fair（第三方）

按后端服务器的响应时间来分配，响应时间短的优先分配

```xml
upstream www.example.com{
        server  www.example.com:8080;
        server  www.example.com:9080;
        fair;
}
```

- backup（备机）

```java
upstream www.example.com{
        ip_hash;
        server  www.example.com:9090 down; (down表示当前的server暂时不参与负载)
        server  www.example.com:8080 weight=2;(weight默认为1，weight越大，负载的权重就越大)
        server  www.example.com:6060;
        server  www.example.com:7070 backup;（其它所有的非backup机器down或者忙的时候，请求backup机器）
}
```

backup: 备用机器