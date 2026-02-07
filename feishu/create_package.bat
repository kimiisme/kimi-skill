@echo off
REM 飞书任务自动分发技能 - Windows 打包脚本

setlocal enabledelayedexpansion

echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║     飞书任务自动分发技能 - 打包工具 (Windows)               ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM 检查是否在正确的目录
if not exist "SKILL.md" (
    echo ❌ 错误: 请在 feishu-task-dispatcher 目录下运行此脚本
    pause
    exit /b 1
)

echo 📦 开始打包...
echo.

REM 设置版本和日期
set VERSION=1.0.0
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
set PACKAGE_NAME=feishu-task-dispatcher-v%VERSION%-%mydate%

REM 创建临时目录
set TEMP_DIR=%TEMP%\feishu-task-dispatcher-package
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

REM 复制文件
echo 📄 复制核心文件...
xcopy /E /I /Q "%CD%" "%TEMP_DIR%\feishu-task-dispatcher\" >nul

REM 清理临时文件
echo 🧹 清理临时文件...
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc >nul 2>&1

REM 创建配置模板
echo 📝 创建配置模板...
(
echo {
echo   "mcpServers": {
echo     "feishu": {
echo       "command": "cmd",
echo       "args": ["/c", "npx", "-y", "@larksuiteoapi/lark-mcp", "mcp", "-a", "YOUR_APP_ID", "-s", "YOUR_APP_SECRET"],
echo       "type": "stdio"
echo     }
echo   }
echo }
) > "%TEMP_DIR%\config_template.json"

REM 创建 Windows 快速安装脚本
(
echo @echo off
echo echo 飞书任务自动分发技能 - 快速安装
echo echo ================================
echo.
echo REM 检查 Claude Code
echo where claude-code ^>nul 2^>nul
echo if errorlevel 1 (
echo     echo ❌ 未检测到 Claude Code
echo     echo 请先安装: npm install -g @anthropic-ai/claude-code
echo     pause
echo     exit /b 1
echo ^)
echo echo ✅ Claude Code 已安装
echo.
echo REM 复制到当前目录
echo set TARGET_DIR=%CD%\feishu-task-dispatcher
echo if exist "!TARGET_DIR!" ^(
echo     echo ⚠️  目录已存在: !TARGET_DIR!
echo     set /p confirm="是否覆盖? (y/N): "
echo     if /i not "%%confirm%%"=="y" (
echo         echo 安装已取消
echo         pause
echo         exit /b 1
echo     ^)
echo     rd /s /q "!TARGET_DIR!"
echo ^)
echo.
echo xcopy /E /I /Q feishu-task-dispatcher "%CD%\"
echo echo ✅ 技能文件已复制到: !TARGET_DIR!
echo.
echo REM 运行安装检查
echo cd "!TARGET_DIR!"
echo python install.py
echo.
echo echo.
echo echo 🎉 安装完成！
echo echo.
echo echo 下一步:
echo echo 1. 配置飞书 MCP (参考 INSTALL.md^)
echo echo 2. 登录飞书: npx -y @larksuiteoapi/lark-mcp login
echo echo 3. 在 Claude Code 中使用自然语言分配任务
echo pause
) > "%TEMP_DIR%\quick_install.bat"

REM 创建 README
(
echo 飞书任务自动分发技能 - 安装包
echo ==========================
echo.
echo 快速安装：
echo 1. 解压此文件到任意目录
echo 2. 运行: quick_install.bat
echo 3. 按照 INSTALL.md 中的说明配置飞书 MCP
echo 4. 登录飞书账户
echo 5. 开始使用！
echo.
echo 详细文档：
echo - INSTALL.md - 完整安装指南
echo - QUICKSTART.md - 快速开始
echo - TEAM_CONFIG.md - 团队配置说明
echo.
echo 技术支持：
echo 如遇问题，请查看 INSTALL.md 中的"故障排查"部分
) > "%TEMP_DIR%\README.txt"

REM 创建压缩包
echo.
echo 📦 创建压缩包...
set PACKAGE_FILE=%PACKAGE_NAME%.zip

REM 使用 PowerShell 创建压缩包
powershell -Command "Compress-Archive -Path '%TEMP_DIR%\*' -DestinationPath '%PACKAGE_FILE%' -Force" >nul

REM 移动到桌面
if exist "%USERPROFILE%\Desktop" (
    move "%PACKAGE_FILE%" "%USERPROFILE%\Desktop\" >nul
    echo.
    echo ✅ 打包完成！
    echo.
    echo 📦 安装包位置:
    echo    %USERPROFILE%\Desktop\%PACKAGE_FILE%
    echo.
    echo 📋 安装包内容:
    echo    - feishu-task-dispatcher\ (技能文件^)
    echo    - config_template.json (MCP 配置模板^)
    echo    - quick_install.bat (快速安装脚本^)
    echo    - README.txt (说明文档^)
    echo.
    echo 🚀 在新电脑上安装:
    echo    1. 解压 %PACKAGE_FILE%
    echo    2. 运行: quick_install.bat
    echo.
) else (
    echo.
    echo ✅ 打包完成！
    echo    安装包: %PACKAGE_FILE%
    echo    位置: %CD%
)

REM 清理临时文件
rd /s /q "%TEMP_DIR%"

echo 🎉 打包成功！
echo.
pause
