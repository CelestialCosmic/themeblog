今天实习最后一天，而且机场流量居然也被用完了，真正的百无聊赖

## step1
扫血，发现靶子是 100 的 4byte，改成 1 然后一发秒了

## step2
锁血，打了一架飞机以后，第二架飞机打了个超级大伤害秒了，此路不通

断血量代码，发现断点命中了三次，意味着它们共享血量代码逻辑

代码是 `sub [rax+60],edx` 我的血量地址是 `0150D090` ，所以等到 ax 是 `0150D030` 时，修改 dx 为 `0h`，其他的就修改成 `99999h`

顺利通关

## step3
人物可以移动？扫坐标吧

反复横跳了几轮确实扫出来了，是浮点数

又借助些许资料，得知有变量掌管绿板子的数量，满 12 时全绿

先扫 1 ，又走了块板子，再扫 2 ，确实出来了

改成 12 后 AI 修改了逻辑，把门堵上了

修改 X ，结果撞上了 AI，爆炸

多次修改后，得到位置大概是 1.0

想先过去再改板子，结果掉了下去......因为没有扫 Y，上不来了

被迫重启程序

这次就有经验了：先扫描小于 0 的浮点数，再动几轮得到地址

再踩板子，得到板子的地址，然后改成 12

AI 按照预期把门堵上了，落地，修改 X 为 1，这次成功了

## 最后

弄完也就快半个小时，打字都占了三分之一......

而且弄完了发现 github 也上不去，还没法直接发，真是难受