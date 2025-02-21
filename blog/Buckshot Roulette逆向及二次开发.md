上 steam 了，随便玩玩

## 引擎

一开始我并不认为它是 godot，因为没带 .pck 文件，虽然启动时弹了控制台。当时还想着可能是什么别的引擎，b 站有评论提到才注意到有可能是 godot，看了参考链接那篇文章发的依据，那自然 godot 没跑了

那就上 gdre 一把梭了，但是工作电脑里面没 godot，只能简单看看有个啥

## 子弹

文章中已经展示了关键位置的数组：

```
Interceptor.attach(base.add(0x184D79)
Interceptor.attach(base.add(0x184DFC)
```

但考虑到我手里的版本和文章的发布时间之间已经过去了三个月，我还是有必要自己试一试的

根据文章的指引，没费什么功夫就看到了生成子弹的代码

```c#
sequenceArray = []
tempSequence = []
ai.sequenceArray_knownShell = []
for i in range(numberOfLives):
	tempSequence.append("live")
for i in range(numberOfBlanks):
	tempSequence.append("blank")
if (shufflingArray):
	tempSequence.shuffle()
for i in range(tempSequence.size()):
	sequenceArray.append(tempSequence[i])
	ai.sequenceArray_knownShell.append(false)
	pass
```

在子弹队列清空后，根据随机生成子弹数，然后填到临时数组中，在临时数组中随机后，再填到真实数组中，也就意味着整个过程中，需要追踪的只是 `sequenceArray` 的地址

在 `RoundManager.gd` 中还有另一段生成子弹的代码

```gd
func GenerateRandomBatches():
	for b in batchArray:
		for i in range(b.roundArray.size()):
			b.roundArray[i].startingHealth = randi_range(2, 4)
			
			var total_shells = randi_range(2, 8)
			var amount_live = max(1, total_shells / 2)
			var amount_blank = total_shells - amount_live
			b.roundArray[i].amountBlank = amount_blank
			b.roundArray[i].amountLive = amount_live
			
			b.roundArray[i].numberOfItemsToGrab = randi_range(2, 5)
			b.roundArray[i].usingItems = true
			var flip = randi_range(0, 1)
			if flip == 1: b.roundArray[i].shufflingArray = true
```

由此可知实弹数量的范围是弹匣子弹数量的一半，向下取整

godot 地址固定，所以不难

### 尝试

挂 x64dbg，报错
```
---------------------------
Buckshot Roulette.exe - System Error
---------------------------
The code execution cannot proceed because steam_api64.dll was not found. Reinstalling the program may fix this problem. 
---------------------------
确定   
---------------------------
```

工作电脑没 steam，下班再战。

## 道具赛

double or nothing 模式~~（你来你也坎）~~中有大量的道具（一轮五个，且有大量新道具），有没有方式控制生成的是什么？谁不喜欢用肾上腺素猛猛吃 ai 道具呢？

除此之外，还有成就需要一回合内用完每种道具，这自然没有不错的运气还是挺难实现的。

有两个地方有关于道具的代码：`ItemInteraction.gd` 和 `HandManager.gd`

`DealerIntelligence.gd` 是对面的道具代码，我们不管

`ItemInteraction.gd`
```gd
func InteractWith(itemName : String):
	#INTERACTION
	var amountArray : Array[AmountResource] = amounts.array_amounts
	for res in amountArray:
		if (res.itemName == itemName): 
			res.amount_player -= 1
			break
	
	var isdup = false
	for it in roundManager.playerCurrentTurnItemArray:
		if (it == itemName): isdup = true; break
	if (!isdup): roundManager.playerCurrentTurnItemArray.append(itemName)
	match (itemName):
		"handcuffs":
			animator_dealerHands.play("dealer get handcuffed")
			await get_tree().create_timer(1, false).timeout
			camera.BeginLerp("enemy")
			await get_tree().create_timer(1.3, false).timeout
			camera.BeginLerp("dealer handcuffs")
			roundManager.dealerCuffed = true
			dealerIntelligence.dealerAboutToBreakFree = false
			await get_tree().create_timer(1.3, false).timeout
			camera.BeginLerp("home")
			await get_tree().create_timer(.6, false).timeout
			EnablePermissions()
		"beer":
			roundManager.playerData.stat_beerDrank += 330
			var isFinalShell = false
			if (roundManager.shellSpawner.sequenceArray.size() == 1): isFinalShell = true
			animator_playerHands.play("player use beer")
			await get_tree().create_timer(1.4, false).timeout
			shellEject_player.FadeOutShell()
			await get_tree().create_timer(4.2, false).timeout
			#check if ejected last shell
			if (!isFinalShell): EnablePermissions()
			else:
				roundManager.StartRound(true)
		"magnifying glass":
			animator_playerHands.play("player use magnifier")
			var length = animator_playerHands.get_animation("player use magnifier").get_length()
			await get_tree().create_timer(length + .2, false).timeout
			EnablePermissions()
		"cigarettes":
			roundManager.playerData.stat_cigSmoked += 1
			animator_playerHands.play("player use cigarettes")
			await get_tree().create_timer(5, false).timeout
			itemManager.numberOfCigs_player -= 1
			EnablePermissions()
		"handsaw":
			animator_playerHands.play("player use handsaw")
			roundManager.barrelSawedOff = true
			roundManager.currentShotgunDamage = 2
			await get_tree().create_timer(4.28 + .2, false).timeout
			EnablePermissions()
		"expired medicine":
			PlaySound(sound_use_medicine)
			animator_playerHands.play("player use expired pills")
			medicine.UseMedicine()
			#await get_tree().create_timer(4.28 +.2 + 4.3, false).timeout
			#EnablePermissions()
		"inverter":
			PlaySound(sound_use_inverter)
			animator_playerHands.play("player use inverter")
			if (roundManager.shellSpawner.sequenceArray[0] == "live"): roundManager.shellSpawner.sequenceArray[0] = "blank"
			else: roundManager.shellSpawner.sequenceArray[0] = "live"
			await get_tree().create_timer(3.2, false).timeout
			EnablePermissions()
		"burner phone":
			PlaySound(sound_use_burnerphone)
			animator_playerHands.play("player use burner phone")
			await get_tree().create_timer(7.9, false).timeout
			EnablePermissions()
		"adrenaline":
			PlaySound(sound_use_adrenaline)
			animator_playerHands.play("player use adrenaline")
			await get_tree().create_timer(5.3 + .2, false).timeout
			items.SetupItemSteal()
			#EnablePermissions()
	CheckAchievement_koni()
	CheckAchievement_full()
```

首先从上到下，道具包括如下类型：
- 手铐
- 啤酒
- 放大镜
- 香烟
- 手锯
- 过期药品
- 逆转器
- 一次性手机
- 肾上腺素

下面还有两个成就，顺带提一下：

**Digita,Orava and Koni**
```gd
func CheckAchievement_koni():
	if ("cigarettes" in roundManager.playerCurrentTurnItemArray and "beer" in roundManager.playerCurrentTurnItemArray and "expired medicine" in roundManager.playerCurrentTurnItemArray): ach.UnlockAchievement("ach9")
```
在一回合内抽烟喝酒加嗑药，那还真是“冠军的早餐”

**Full House**
```gd
func CheckAchievement_full():
	var all = ["handsaw", "magnifying glass", "beer", "cigarettes", "handcuffs", "expired medicine", "burner phone", "adrenaline", "inverter"]
	var pl = roundManager.playerCurrentTurnItemArray
	if (all.size() == pl.size()): ach.UnlockAchievement("ach12")
```
九个道具，八个槽。如果希望一回合用上所有道具，那手里至少有肾上腺素，还要去偷 AI 东西，也许上回合上手铐再加这回合就算九个？

接着，`ItemManager.gd` 在中有生成道具的代码，这里截取了最重要的那部分出来：

```gd
func GrabItem():
	if (roundManager.playerData.currentBatchIndex == 1 && roundManager.currentRound == 1):
		if (spook_counter == 1 && !spook_fired && !roundManager.playerData.seenGod):
			GrabSpook()
			roundManager.playerData.seenGod = true
			spook_fired = true
			return
		spook_counter += 1
	#GET RANDOM ITEM
	PlayItemGrabSound()
	interaction_intake.interactionAllowed = false
	var selectedResource : ItemResource
	
	#SET PLAYER AVAILABLE ITEMS ACCORDING TO MAX COUNTS
	var amountArray : Array[AmountResource] = amounts.array_amounts
	availableItemsToGrabArray_player = []
	for res in amountArray:
		if (res.amount_active == 0): continue
		if (res.amount_player != res.amount_active):
			availableItemsToGrabArray_player.append(res.itemName)
	#for res in amountArray: availableItemsToGrabArray_player.append(res.itemName)
	
	randindex = randi_range(0, availableItemsToGrabArray_player.size() - 1)
	
	numberOfItemsGrabbed += 1
	#SPAWN ITEM
	for i in range(instanceArray.size()):
		if (availableItemsToGrabArray_player[randindex] == instanceArray[i].itemName):
			selectedResource = instanceArray[i]
	var itemInstance = selectedResource.instance.instantiate()
	
	for res in amountArray:
		if (selectedResource.itemName == res.itemName):
			res.amount_player += 1
			break
```

第一段是 GOD 的弃权书，没什么好说的，给你看一眼然后放回去了

第二段似乎是在一个名叫“可获取物品”的数组中随机生成了物品，并且玩家和 GOD 共享这个数组，玩家因物品超限剩下来的道具会给到 GOD，但 GOD 也会因此拿不到最后那几个道具

但不管怎么样，玩家亏道具说什么都是亏的，就和扎了肾上腺素以后纠结拿什么道具一样，也是白搭一个肾上腺素

## 参考链接
[godot 引擎逆向初探 | in1t's blog](https://in1t.top/2024/01/23/godot-%E5%BC%95%E6%93%8E%E9%80%86%E5%90%91%E5%88%9D%E6%8E%A2/)