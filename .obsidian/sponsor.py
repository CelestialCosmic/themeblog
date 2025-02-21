import re
text1 = """
this.containerEl.createEl("hr");
    this.containerEl.createEl("p", { text: "If you like this plugin and want to support its development, you can do so through my website by clicking this fancy image!" });
    this.containerEl.createEl("a", { href: "https://ellpeck.de/support" }).createEl("img", { attr: { src: "https://ellpeck.de/res/generalsupport.png" }, cls: "custom-frames-support" });
"""
text2 = """
const r=n.createDiv("coffee");r.addClass("ex-coffee-div"),r.createEl("a",{href:"https://ko-fi.com/zsolt"}).createEl("img",{attr:{src:"https://cdn.ko-fi.com/cdn/kofi3.png?v=3"}}).height=45,
"""

text3 = """
.ex-coffee-div{margin-bottom:10px;text-align:center}.excalidraw-scriptengine-install td>img{max-width:800px;width:100%}.excalidraw-scriptengine-install img.coffee{width:130px}
"""

text4 = """
t.createElement(a.Center.MenuItemLink,{icon:ICONS.heart,href:"https://ko-fi.com/zsolt",shortcut:null,"aria-label":"Donate to support Excalidraw-Obsidian"},' Say "Thank You" & support the plugin.')
"""

text5 = """
n.createEl("div",{text:"Developed by "}).createEl("a",{text:"Pr0dt0s",href:"https://github.com/Pr0dt0s"}),n.createEl("br");const w=n.createEl("div",{text:"If you want to see the documentation, submit a bug, or a feature request you can do so "});w.createEl("a",{text:"here",href:"https://github.com/Pr0dt0s/obsidian-html-server"}),w.appendText(".");const k=new e.Setting(this.containerEl).setName("Donate").setDesc("If you like this Plugin, consider donating to support continued development."),j=document.createElement("a");j.setAttribute("href","https://github.com/sponsors/Pr0dt0s"),j.addClass("templater_donating");const E=document.createElement("img");E.src="https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86",j.appendChild(E);const S=document.createElement("a");S.setAttribute("href","https://www.paypal.com/donate/?business=JGQK6YQBWZJ4A&currency_code=USD"),S.addClass("templater_donating");const O=document.createElement("img");O.src="https://img.shields.io/badge/paypal-Pr0dt0s-blue?logo=paypal",
"""

text6 = """
const r=n.createDiv("coffee");r.addClass("ex-coffee-div"),r.createEl("a",{href:"https://ko-fi.com/zsolt"}).createEl("img",{attr:{src:"https://cdn.ko-fi.com/cdn/kofi3.png?v=3"}}).height=45,
"""

"""
t.createElement(a.Center.MenuItemLink,{icon:ICONS.YouTube,href:"https://www.youtube.com/@VisualPKM",shortcut:null,"aria-label":"Visual PKM YouTube Channel"}," Check out the Visual PKM YouTube channel."),t.createElement(a.Center.MenuItemLink,{icon:ICONS.Discord,href:"https://discord.gg/DyfAXFwUHc",shortcut:null,"aria-label":"Join the Visual Thinking Discord Server"}," Join the Visual Thinking Discord Server"),t.createElement(a.Center.MenuItemLink,{icon:ICONS.twitter,href:"https://twitter.com/zsviczian",shortcut:null,"aria-label":"Follow me on Twitter"}," Follow me on Twitter"),t.createElement(a.Center.MenuItemLink,{icon:ICONS.heart,href:"https://ko-fi.com/zsolt",shortcut:null,"aria-label":"Donate to support Excalidraw-Obsidian"},' Say "Thank You" & support the plugin.')
"""