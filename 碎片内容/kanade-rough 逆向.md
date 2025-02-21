整个文件夹里面最大的文件是 `data.dxa`

在字符串中搜索 dxa，发现 `..\..\..\..\..\Source\Library\Main\DxArchive_.cpp` 和 `..\..\..\..\..\Source\Library\Main\DxASyncLoad.cpp`

很明显用了这个文件，在 github 上稍微搜索，翻出了源文件

[DxLib/source/DxArchive\_.cpp at master · yumetodo/DxLib · GitHub](https://github.com/yumetodo/DxLib/blob/master/source/DxArchive_.cpp)

可见其属于 DxLib 部分，文件中又包含了 `DxArchive_.h`

没花多少功夫也找到了

[chinesize/DxLib/exBin/DxLib/DxArchive\_.h at 0c7be6eed8e1a0c5ab7b25024fc5e21125967c7f · regomne/chinesize · GitHub](https://github.com/regomne/chinesize/blob/0c7be6eed8e1a0c5ab7b25024fc5e21125967c7f/DxLib/exBin/DxLib/DxArchive_.h#L4)

看不出东西，所以上 ida

x64dbg 停在了 `00391729` 上时开始读文件，所以密钥的触发会在之前

“符号”中定位基址为 `00100000` ，进去看发现是 `00101000`，ida 基址则为 `00401000`

离他最近的函数是 `00692500`，进去看

```
.text:00692506 A1 F0 58 AA 00                mov     eax, ___security_cookie
```

开局就能让人感到振奋

```
.data:00AA58F0 4E E6 40 BB                   ___security_cookie dd 0BB40E64Eh        ; DATA XREF: sub_4013C0+14↑r
```

这段还带出来了一个新地址：`sub_4013C0+14`

```
.text:004013D4 A1 F0 58 AA 00                mov     eax, ___security_cookie
```

在十六进制中，发现了它：
```
38 5E 6B 30 42 7D 86 4E 57 30 7E 30 57 30 5F 30
```

```
NW0~0W0_0
```

当然了，后来发现并不是

## 第二次尝试

![[Pasted image 20240417082341.png]]

这次我尝试从读取开始找

游戏第一件做的事情是读取声音，所以查找字符串定位过去

在所有的 `push ebp` 上打了断点

## 其他的一些发现

```json
地址=001310B9
反汇编=mov dword ptr ss:[ebp-C4],game.580C24
字符串地址=00580C24
字符串=L"---"

地址=0013150A
反汇编=push game.580CEC
字符串地址=00580CEC
字符串=L"FOOTER_STATUS_%d"

地址=001318E2
反汇编=push game.580D4C
字符串地址=00580D4C
字符串=L"LV:"

地址=00131910
反汇编=push game.57F3FC
字符串地址=0057F3FC
字符串=L"%d"

地址=0013197E
反汇编=push game.580D40
字符串地址=00580D40
字符串=L"EXP:"

地址=001319AA
反汇编=push game.57F3FC
字符串地址=0057F3FC
字符串=L"%d"

地址=00131A18
反汇编=push game.580470
字符串地址=00580470
字符串=L"MANA:"

地址=00131B0D
反汇编=push game.57F3FC
字符串地址=0057F3FC
字符串=L"%d"

地址=00131B78
反汇编=push game.580D78
字符串地址=00580D78
字符串=L"HP:"

地址=00131BD0
反汇编=push game.580A2C
字符串地址=00580A2C
字符串=L"%d/%d"

地址=00131CBC
反汇编=push game.580D54
字符串地址=00580D54
字符串=L"(%d * %d%% + %d)"

地址=00131CDD
反汇编=push game.580D88
字符串地址=00580D88
字符串=L"MP:"

地址=00131DF3
反汇编=push game.580A2C
字符串地址=00580A2C
字符串=L"%d/%d"

地址=00131EC6
反汇编=push game.580D54
字符串地址=00580D54
字符串=L"(%d * %d%% + %d)"

地址=00131EE8
反汇编=push game.580D80
字符串地址=00580D80
字符串=L"EP:"

地址=00131F28
反汇编=push game.57FC4C
字符串地址=0057FC4C
字符串=L"%d%%"

地址=00131F93
反汇编=push game.580D9C
字符串地址=00580D9C
字符串=L"ATK:"

地址=00131FC8
反汇编=push game.57F3FC
字符串地址=0057F3FC
字符串=L"%d"

地址=00132081
反汇编=push game.580D54
字符串地址=00580D54
字符串=L"(%d * %d%% + %d)"

地址=001320A0
反汇编=push game.580D90
字符串地址=00580D90
字符串=L"DEF:"

地址=001320D5
反汇编=push game.57F3FC
字符串地址=0057F3FC
字符串=L"%d"

地址=00132184
反汇编=push game.580D54
字符串地址=00580D54
字符串=L"(%d * %d%% + %d)"

地址=001321A3
反汇编=push game.580DC0
字符串地址=00580DC0
字符串=L"SPD:"

地址=001321D8
反汇编=push game.57F3FC
字符串地址=0057F3FC
字符串=L"%d"

地址=00132287
反汇编=push game.580D54
字符串地址=00580D54
字符串=L"(%d * %d%% + %d)"

地址=001322A6
反汇编=push game.580DA8
字符串地址=00580DA8
字符串=L"Resistance:"

```

明显这一段是关于人物状态的，下面还有，但太多了就没写