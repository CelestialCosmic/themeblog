xml 本质是用来标记 xml/html 节点的，但是也开发出了查询手段，于是就更多的被用作查询了

## xpath 语法

> 在XPath中,XML文档被作为节点树对待,XPath中有七种结点类型：元素、属性、文本、命名空间、处理指令、注释以及文档节点（或成为根节点）。
> 
> nodename：选取此节点的所有节点
> 
> /：从根节点选取
> 
> //：表示选取所有的子元素，不考虑其在文档的位置
> 
> .：选取当前节点
> 
> ..：选取当前节点的父节点
> 
> @：选取属性
> 
> 函数：
> 
> starts-with 匹配一个属性开始位置的关键字
> 
> contains 匹配一个属性值中包含的字符串
> 
> text（） 匹配的是显示文本信息

比如说这样的 xml：

```xml
<users>
     <user>
         <firstname>Ben</firstname>
         <lastname>Elmore</lastname>
         <loginID>abc</loginID>
         <password>test123</password>
     </user>
     <user>
         <firstname>Shlomy</firstname>
         <lastname>Gantz</lastname>
         <loginID>xyz</loginID>
         <password>123test</password>
     </user>
</users>
```

那么 Shlomy Gantz 的 id 和密码的 xpath 就是 `//users/user[loginID/text()='xyz'and password/text()='123test']`

就像 sql 那样，xpath 也可以用 `' or 1=1 or ''='` 得到永真的结果

所以 `//users/user[loginID/text()=''or 1=1 or ''='' and password/text()='' or 1=1 or ''='']` 永真

## 如何利用

### 测试是否存在漏洞

在提交的 url 中只填写一个 `'` 然后提交

如果前端直接报错，则存在漏洞
### 利用漏洞

提交登录表单时，众所周知架构简单的网站都是把填写的内容体现在 url 上的。所以在查询时如果永真，将返回我们需要的东西。