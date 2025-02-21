## 介绍

[MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)是最近这几个月出现的爬虫项目，当然，我并不关注它好用在哪，我关心的是它所使用的新技术

## 核心运行原理前置

它的核心代码集中在各个文件夹的 core.py

每个 core.py 都调用了一个模块：playwright.async_api

### playwright

这里首先需要介绍一下 playwright，这是它在其官网上的描述：

> Any browser • Any platform • One API
> Cross-browser. Playwright supports all modern rendering engines including Chromium, WebKit, and Firefox.
> Cross-platform. Test on Windows, Linux, and macOS, locally or on CI, headless or headed.
> Cross-language. Use the Playwright API in TypeScript, JavaScript, Python, .NET, Java.
> Test Mobile Web. Native mobile emulation of Google Chrome for Android and Mobile Safari. The same rendering engine works on your Desktop and in the Cloud.

简而言之，借助 playwright 的 API，你可以跨设备、跨平台、跨语言、跨浏览器地访问同一个页面，拦截并修改网络请求，或者在一台设备上以多个身份登录，是非常便利的自动化测试工具

### 无头浏览器

因为 playwright 使用的是**无头浏览器**，因此这里也稍微讲解一下什么是无头浏览器

无头浏览器没有 GUI，但拥有和普通浏览器一致的解析能力和发包能力，借助编写程序操控 API 来操控浏览器的行为，其诞生就是专供自动化测试使用的

但因为没有 GUI，面对 Captcha 和限制未登录用户浏览的网站面前很无力

在下面的这个 issue 中，就是使用无头浏览器对抗 biliblil.com 的请求加密的例子：
[Web 风控相关问题: buvid3, buvid4 获取及激活(ExClimbWuzhi 上传设备指纹消息) · Issue #933 · SocialSisterYi/bilibili-API-collect · GitHub](https://github.com/SocialSisterYi/bilibili-API-collect/issues/933)

### 爬取数据的难点

疫情前，针对爬虫的手段就已层出不穷，三年后，爬虫更是难上加难

> 各类国内平台都针对爬虫进行了或多或少的限制，包括但不限于：防火墙阻断、限制高频访问、魔改前端字体库、仅可通过限定 API 爬取内容、请求加密、Captcha、阻断 F12 调试、序列化加密等等

## 核心运行原理
### main
`main` 函数就是一个启动器：

```py
parser.add_argument('--platform', type=str, help='Media platform select (xhs | dy | ks | bili | wb)',
                        choices=["xhs", "dy", "ks", "bili", "wb"], default=config.PLATFORM)
```

`platform` 设置爬取平台，包括五个平台：

>很戏剧性的一点就是：我使用了 AutoLinkTItle 这个插件，它就是用来在粘贴链接时自动获取网页标题的，下面的爬取到的结果正好也能一窥各个平台对待这些自动化工具的态度
>通过浏览器正常点开下面的链接，每一个都如求偶的鸟儿一般，在页面中展示它们有多么“诱人”，但面对自动化工具，它们又会换上另一套嘴脸，表示它们并不欢迎这些流量

- xhs [滑块验证](https://www.xiaohongshu.com/)
- dy [Site Unreachable](https://www.douyin.com/)
- ks [kuaishou.com/new-reco](https://www.kuaishou.com/)
  正常浏览时显示页面，自动化工具返回
  `{"result":2,"error_msg":null,"request_id":"712548355460264049"}`
- bili [哔哩哔哩 (゜-゜)つロ 干杯\~-bilibili](https://www.bilibili.com/)
- wb [微博](https://m.weibo.cn/)

```py
parser.add_argument('--lt', type=str, help='Login type (qrcode | phone | cookie)',
                        choices=["qrcode", "phone", "cookie"], default=config.LOGIN_TYPE)
```

 `login_type` 设置登录方式，包括了三种方式：
- qrcode 扫码登录
- phone 电话号码+密码登录
- cookie 提取 cookie 登录

```py
parser.add_argument('--type', type=str, help='crawler type (search | detail | creator)',
                        choices=["search", "detail", "creator"], default=config.CRAWLER_TYPE)
```

`type` 设置爬取方式，包括了三种方式：
- search 热搜
- detail 指定内容
- creator 指定作者

### weibo 爬取

```py
   if config.ENABLE_IP_PROXY:
      ip_proxy_pool = await create_ip_pool(config.IP_PROXY_POOL_COUNT, enable_validate_ip=True)
    ip_proxy_info: IpInfoModel = await ip_proxy_pool.get_proxy()
    playwright_proxy_format, httpx_proxy_format = self.format_proxy_info(ip_proxy_info)

  async with async_playwright() as playwright:
    chromium = playwright.chromium
      self.browser_context = await self.launch_browser(
        chromium,
        None,
        self.mobile_user_agent,
        headless=config.HEADLESS
     )
```

如果在设置中开启了代理池，流量将通过代理池到达平台

> 代理池就是一堆 IP，这堆 IP 对应着一堆服务器，这些服务器可以接受来自主机的请求，并协助发包，这些服务器可以用来突破单 IP 对平台访问量的限制，避免平台和 ISP 封禁，也可以同时发包，加速结果收集。也可以隐藏主机 IP，让代理池充当白手套

然后同样通过无头参数启动了 chrmoium

```py
if not await self.wb_client.pong():
    login_obj = WeiboLogin(
        login_type=self.login_type,
        login_phone="",  # your phone number
        browser_context=self.browser_context,
        context_page=self.context_page,
        cookie_str=config.COOKIES
    )
    await self.context_page.goto(self.index_url)
    await asyncio.sleep(1)
    await login_obj.begin()
```

在模拟客户端后，如果没有得到客户端的回应，将会开启模拟登录流程：根据之前设置的参数来进行登录

```py
utils.logger.info("[WeiboCrawler.start] redirect weibo mobile homepage and update cookies on mobile platform")
                await self.context_page.goto(self.mobile_index_url)
                await asyncio.sleep(2)
                await self.wb_client.update_cookies(browser_context=self.browser_context)
```

登录完毕后，跳转到手机版微博获取 cookie 来使登录状态持久化

在登录完毕后，根据一开始输入的类型爬取对应的内容，其中包括：
- search 微博热搜
- get_specified_notes 爬取指定 ID 微博
- get_note_info_task 根据微博 ID 获取详情
- batch_get_notes_comments 根据微博 ID 批量爬取评论
- get_note_comments 爬取指定微博评论

### bilibili 爬取

根据我之前做 RSS 的体验来看，整体而言爬取数据难度是在一直上升的，光 RSS 源本身就经常更新且不稳定，这里引用其他项目中一位开发者的原话：

>自从 api.bilibili.cn 被关闭后，就大概知道 b 站对于爪巴数据的人是什么态度了。biliob.com 也能证明这点。
>况且现在 b 站 api 也在往更难逆向的方向发展了，以前能用浏览器抓包，看个变量名就能懂个大概；现在 protobuf，二进制数据，还要翻 js 源码才能序列化

但是这个项目让我看到了另一个可能性：利用伪装的无头浏览器“浏览”内容，然后将浏览器返回的内容处理成我们所希望的东西，前端“所见即所得”的特性使得只要内容能公开访问，就一定存在什么方式能爬下来，前天是人力，昨天是 RSS，今天是 MediaCrawler，明天就会是 AI

闲聊就到此为止，开始这部分的解析代码

#### 代码解析

```py
async with async_playwright() as playwright:
       chromium = playwright.chromium
       self.browser_context = await self.launch_browser(
           chromium,
          None,
          self.user_agent,
         headless=config.HEADLESS
        )
```

很明显，项目通过设置 playwright 和无头参数启动了一个无头的 chromium

```py
await self.browser_context.add_init_script(path="libs/stealth.min.js")
self.context_page = await self.browser_context.new_page()
await self.context_page.goto(self.index_url)
```

并且通过启动时加载 `stealth.min.js` 反反爬虫

>前面提到过，平台也会部署反爬虫措施，`stealth.min.js` 也就应运而生：它最初是由 puppeteer 团队开发用来抹除其自动化特征的，后来被提取出来，存放在[GitHub](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)中，支持加载 js 的自动化测试工具，包括 selenium,playwright 等，都可以通过加载这个 js 的方式，抹除其自动化特征，在一定程度上避免触发 captcha

```py
if self.crawler_type == "search":
    await self.search()
elif self.crawler_type == "detail":
     await self.get_specified_videos()
else:
    pass
```

在模拟客户端后，如果没有得到客户端的回应，就要开始模拟登录了

```py
self.bili_client = await self.create_bilibili_client(httpx_proxy_format)
  if not await self.bili_client.pong():
       login_obj = BilibiliLogin(
           login_type=self.login_type,
         login_phone="",  # your phone number
          browser_context=self.browser_context,
        context_page=self.context_page,
        cookie_str=config.COOKIES
        )
    await login_obj.begin()
    await self.bili_client.update_cookies(browser_context=self.browser_context)
```

在登录完毕后，根据一开始输入的类型爬取对应的内容，其中包括：
- search
- batch_get_video_comments
- get_comments
- get_specified_videos
- get_video_info_task
