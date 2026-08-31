## 无码
修改 `FnDrawMosaic`,所有情况 `return true;`
搜索 `mosaic`,找到`MosaicShower`,修改 `this.Md.draw_gl_only = ture;`,为 `false`
## 无限背包
1. 搜索 `ItemStorage` 类,删掉`Add`中的以下代码：
```cs
if (!flag6 && this.getVisibleRowCount() >= this.row_max && num6 < 0 && rowhid == ItemStorage.ROWHID.VISIBLE)
{
	break;
}
```
1. 搜索 `getItemStockable`，找到 `if (!flag)`，将其更改为:  `if (!flag && (Itm.isEmptyBottle() || Itm.isEmptyLunchBox()))  `
2. 搜索 `UiItemStore` 类,修改 `getInventoryAddable`,只留 `num2 += 9999`;
## 无限钱
### 不扣钱
搜索 `CoinEntry`,在 `Reduce` 中 `this.current -= (uint)v;` 改为 `+=`
### 加钱
同在 `CoinEntry` 中,在 `Add` 中 `int num = X.Mx(0, X.Mn((int)(999999U - this.current), v)) + 9999;`
> 下面一行也可以,爱加哪加哪