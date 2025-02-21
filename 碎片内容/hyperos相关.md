来自[K70PRO优化 - Chuyi - Medium](https://eryue.medium.com/k70pro%E4%BC%98%E5%8C%96-2abab94b864d)
adb shell pm uninstall --user 0  com.miui.newhome  //内容中心  
adb shell pm uninstall --user 0  com.android.browser //默认浏览器，自带墙中墙。  
adb shell pm uninstall --user 0  com.sohu.inputmethod.sogou.xiaomi //搜狗输入法  
adb shell pm uninstall --user 0  com.miui.analytics //Analytics  
adb shell pm uninstall --user 0  com.miui.systemAdSolution  //广告  
adb shell pm uninstall --user 0  com.android.quicksearchbox //全局搜索

以下是我自己找的
./adb.exe shell pm uninstall --user 0 com.xiaomi.payment //米币支付
./adb.exe shell pm uninstall --user 0 com.android.fileexplorer //文件管理
