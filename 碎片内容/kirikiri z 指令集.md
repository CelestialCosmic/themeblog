o.角色日文名.func 就能直接调用chara里的接口
### 添加物品
game.party.insertItem
### 队伍
game.party.entry(game.chara[0])  
X对应不同角色 game.chara[0].name 更改数字 0可以依次看到对应角色的名字 0是男主 1是基友 2就是莉泽尔

game.guest.entry(o.ポラリス)  
这个代码可以将角色添加到右方支援队伍，ポラリス是女神大人的名字，你想添加其他的也可以输入对应的角色名字，我没试过太多角色
### 地图
game.map.unlockAllArea=true;
game.map.showAllArea=true;
全开图
game.map.battleRate = 0.005 //遇怪概率 改成0为不遇怪 改成1 每走一步遇一次怪