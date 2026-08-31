### 打包
完成 .desktop apprun 文件

QT_DEBUG_PLUGINS=1 检查qt依赖缺失

装入缺失依赖
```
./appimagetool.AppImage a.AppDir/ --runtime-file ,.runtime-x86_64
```

### 解包
 ```
 ./target.AppImage --appimage-extract
 ```