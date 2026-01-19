@echo off
echo === 设置EXE文件图标 ===
echo.

echo 方法1: 使用第三方工具（需要下载）
echo 可以下载 Resource Hacker 或类似工具手动设置图标
echo.

echo 方法2: 使用Python创建带图标的EXE
echo 我们已尝试使用 pyinstaller --icon 参数

echo.
echo 当前状态:
echo - EXE文件: dist/FileRenamer_V1.0.exe
echo - 图标文件: proper_icon.ico
echo - 图标大小: 4286 字节
echo.
echo 建议: 
echo 1. 手动使用 Resource Hacker 工具设置图标
echo 2. 或者使用专业的安装程序制作工具
echo 3. 图标可能在某些系统上需要刷新缓存

pause
