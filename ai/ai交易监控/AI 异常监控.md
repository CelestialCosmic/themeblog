业务指标、交易指标、服务器指标，api 接口的 qps，正常 qps、异常 qps 都需要（有多少指标、质量如何）
## 异常数据
本质是算法的问题，服务出问题了，指标会不会变化？
不是所有指标都接进去就能解决问题，要更多、更有代表性，这样才能覆盖尽可能多的面
AI 更擅长**基于历史经验识别抖动、预测未来趋势**，识别特定时间段的波峰波谷

告警噪音很大、如果阈值够用是不用做AI的

[异常检测 | Anomaly Detection综述](https://zhuanlan.zhihu.com/p/266513299)
