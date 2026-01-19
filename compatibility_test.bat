@echo off
echo === 文件重命名工具兼容性测试 ===
echo.

echo 1. 检查可执行文件...
if exist "dist\FileRenamer_V1.0.exe" (
    echo   ✓ 找到可执行文件
    echo   📏 文件大小: %~z0 bytes
) else (
    echo   ✗ 可执行文件不存在
    goto end
)

echo.
echo 2. 检查依赖项...
echo   📋 建议在其他电脑上安装: 
echo   - Microsoft Visual C++ Redistributable
echo   - .NET Framework (通常Windows自带)

echo.
echo 3. 运行测试...
echo   正在启动程序...
start "" "dist\FileRenamer_V1.0.exe"

echo.
echo === 测试完成 ===
echo 如果程序正常启动，说明兼容性良好
echo 如果启动失败，可能需要安装VC++运行库

:end
pause