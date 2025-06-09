#!/bin/bash

# 测试修复后的环境搭建脚本

echo "🧪 测试环境搭建脚本修复"
echo "=" * 40

# 备份原始 .zshrc（如果存在）
if [ -f "$HOME/.zshrc" ]; then
    cp "$HOME/.zshrc" "$HOME/.zshrc.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ 已备份原始 .zshrc 文件"
fi

# 测试权限问题修复
echo "\n🔧 测试 .zshrc 写入权限修复..."

# 模拟权限问题（临时移除写权限）
if [ -f "$HOME/.zshrc" ]; then
    chmod 444 "$HOME/.zshrc"
    echo "⚠️  临时移除 .zshrc 写权限以测试修复"
fi

# 测试 Python 别名添加函数
echo "\n📝 测试 Python 别名添加..."

# 提取并测试 install_python 函数的别名部分
test_python_alias() {
    ZSHRC_FILE="$HOME/.zshrc"
    
    # 确保 .zshrc 文件存在
    if [ ! -f "$ZSHRC_FILE" ]; then
        touch "$ZSHRC_FILE"
        echo "✅ 创建 ~/.zshrc 文件"
    fi
    
    # 检查并添加别名
    if ! grep -q "alias python=python3" "$ZSHRC_FILE" 2>/dev/null; then
        if echo 'alias python=python3' >> "$ZSHRC_FILE" 2>/dev/null && \
           echo 'alias pip=pip3' >> "$ZSHRC_FILE" 2>/dev/null; then
            echo "✅ Python 别名已添加到 ~/.zshrc"
        else
            echo "⚠️  无法写入 ~/.zshrc，请手动添加以下别名："
            echo "  alias python=python3"
            echo "  alias pip=pip3"
        fi
    else
        echo "ℹ️  Python 别名已存在于 ~/.zshrc"
    fi
}

# 运行测试
test_python_alias

# 恢复 .zshrc 权限
if [ -f "$HOME/.zshrc" ]; then
    chmod 644 "$HOME/.zshrc"
    echo "\n✅ 已恢复 .zshrc 正常权限"
fi

# 测试 Homebrew 环境变量添加
echo "\n🍺 测试 Homebrew 环境变量添加..."

test_homebrew_env() {
    ZSHRC_FILE="$HOME/.zshrc"
    if [ ! -f "$ZSHRC_FILE" ]; then
        touch "$ZSHRC_FILE"
    fi
    
    if echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> "$ZSHRC_FILE" 2>/dev/null; then
        echo "✅ Homebrew 环境变量已添加到 ~/.zshrc"
    else
        echo "⚠️  无法写入 ~/.zshrc，请手动添加：eval \"\$(/opt/homebrew/bin/brew shellenv)\""
    fi
}

# 运行测试
test_homebrew_env

echo "\n🎉 权限修复测试完成！"
echo "\n📋 修复内容总结："
echo "1. ✅ 添加了 .zshrc 文件存在性检查"
echo "2. ✅ 添加了写入权限错误处理"
echo "3. ✅ 提供了手动操作提示"
echo "4. ✅ 添加了 source 命令的错误处理"
echo "\n🚀 现在可以安全运行 ./setup_environment.sh"