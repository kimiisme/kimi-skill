#!/bin/bash
# 飞书任务自动分发技能 - 打包脚本
# 用于创建可分发的安装包

set -e

VERSION="1.0.0"
DATE=$(date +%Y%m%d)
PACKAGE_NAME="feishu-task-dispatcher-v${VERSION}-${DATE}"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║     飞书任务自动分发技能 - 打包工具                        ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# 检查是否在正确的目录
if [ ! -f "SKILL.md" ]; then
    echo "❌ 错误: 请在 feishu-task-dispatcher 目录下运行此脚本"
    exit 1
fi

echo "📦 开始打包..."
echo ""

# 创建临时目录
TEMP_DIR="/tmp/feishu-task-dispatcher-package"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# 复制核心文件
echo "📄 复制核心文件..."
cp -r . "$TEMP_DIR/feishu-task-dispatcher"

# 删除不必要的文件
echo "🧹 清理临时文件..."
cd "$TEMP_DIR/feishu-task-dispatcher"
rm -rf __pycache__ *.pyc
rm -f .DS_Store
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# 创建配置模板
echo "📝 创建配置模板..."
cat > config_template.json << 'EOF'
{
  "mcpServers": {
    "feishu": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@larksuiteoapi/lark-mcp", "mcp", "-a", "YOUR_APP_ID", "-s", "YOUR_APP_SECRET"],
      "type": "stdio"
    }
  }
}
EOF

# 创建快速安装脚本
cat > quick_install.sh << 'EOF'
#!/bin/bash
# 快速安装脚本

echo "飞书任务自动分发技能 - 快速安装"
echo "================================"

# 检查 Claude Code
if ! command -v claude-code &> /dev/null; then
    echo "❌ 未检测到 Claude Code"
    echo "请先安装: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

echo "✅ Claude Code 已安装"

# 复制到当前目录
TARGET_DIR="$(pwd)/feishu-task-dispatcher"
if [ -d "$TARGET_DIR" ]; then
    echo "⚠️  目录已存在: $TARGET_DIR"
    read -p "是否覆盖? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 1
    fi
    rm -rf "$TARGET_DIR"
fi

cp -r feishu-task-dispatcher "$(pwd)/"
echo "✅ 技能文件已复制到: $TARGET_DIR"

# 运行安装检查
cd "$TARGET_DIR"
python install.py

echo ""
echo "🎉 安装完成！"
echo ""
echo "下一步:"
echo "1. 配置飞书 MCP (参考 INSTALL.md)"
echo "2. 登录飞书: npx -y @larksuiteoapi/lark-mcp login"
echo "3. 在 Claude Code 中使用自然语言分配任务"
EOF

chmod +x quick_install.sh

# 创建 README
cat > README.txt << 'EOF'
飞书任务自动分发技能 - 安装包
==========================

快速安装：
1. 解压此文件到任意目录
2. 运行: bash quick_install.sh（Mac/Linux）或 quick_install.bat（Windows）
3. 按照 INSTALL.md 中的说明配置飞书 MCP
4. 登录飞书账户
5. 开始使用！

详细文档：
- INSTALL.md - 完整安装指南
- QUICKSTART.md - 快速开始
- TEAM_CONFIG.md - 团队配置说明

技术支持：
如遇问题，请查看 INSTALL.md 中的"故障排查"部分
EOF

# 返回上级目录
cd "$TEMP_DIR"

# 创建压缩包
echo ""
echo "📦 创建压缩包..."
PACKAGE_FILE="${PACKAGE_NAME}.zip"
zip -rq "${PACKAGE_FILE}" feishu-task-dispatcher config_template.json quick_install.sh README.txt

# 移动到桌面
DESKTOP_DIR="$HOME/Desktop"
if [ -d "$DESKTOP_DIR" ]; then
    mv "${PACKAGE_FILE}" "$DESKTOP_DIR/"
    echo ""
    echo "✅ 打包完成！"
    echo ""
    echo "📦 安装包位置:"
    echo "   $DESKTOP_DIR/${PACKAGE_FILE}"
    echo ""
    echo "📋 安装包内容:"
    echo "   - feishu-task-dispatcher/ (技能文件)"
    echo "   - config_template.json (MCP 配置模板)"
    echo "   - quick_install.sh (快速安装脚本)"
    echo "   - README.txt (说明文档)"
    echo ""
    echo "🚀 在新电脑上安装:"
    echo "   1. 解压 ${PACKAGE_FILE}"
    echo "   2. 运行: bash quick_install.sh"
    echo ""
else
    echo ""
    echo "✅ 打包完成！"
    echo "   安装包: ${PACKAGE_FILE}"
    echo "   位置: $(pwd)"
fi

# 清理临时文件
rm -rf "$TEMP_DIR"

echo "🎉 打包成功！"
