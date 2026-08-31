## 相关通报
[【安全通告】Fastjson 远程代码执行漏洞风险通告](https://cloud.tencent.com/announce/detail/2381)
[fastjson <= 1.2.83 任意代码执行漏洞](https://avd.aliyun.com/detail?id=AVD-2026-1896768)

## 利用条件
1. 无需开启 autoTypeSupport
2. 无需 classpath gadget
3. 任意 JDK 版本

## poc 视频
![[Ek5dbqAkK35wUCfX.mp4]]

## 处置措施
1. 立即排查各 Java 项目中是否有直接或间接引入 com. alibaba:fastjson 1.x 依赖的情况，如有则需要立即紧急开启 `-Dfastjson.parser.safeMode=true` 或者在配置文件中加入 `fastjson.parser.safeMode=true`
2. 审计所有处理用户输入、消息队列、RPC 请求及任何涉及到 JSON 反序列化入口代码
3. 迁移至 Fastjson2 / Jackson / Gson 等正在维护的 JSON 解析器