#!/bin/bash

echo "🚀 启动 Google ADK 营销代理系统开发环境"
echo "=================================================="

# 激活虚拟环境
if [ -d "venv_adk" ]; then
    source venv_adk/bin/activate
    echo "✅ 虚拟环境已激活"
else
    echo "❌ 虚拟环境不存在，请先运行环境搭建脚本"
    exit 1
fi

# 检查配置文件
if [ -f ".env" ]; then
    echo "✅ 配置文件存在"
else
    echo "⚠️  配置文件不存在，请复制 .env.template 为 .env 并配置"
fi

echo ""
echo "🔍 运行环境测试..."
python test_environment.py

echo ""
echo "📂 项目结构："
tree -L 2 2>/dev/null || ls -la

echo ""
echo "🎯 可用命令："
echo "  python test_environment.py  - 测试环境配置"
echo "  cd adk-samples/python/agents/marketing-agency  - 进入营销代理目录"
echo "  python -m marketing_agency.agent  - 运行营销代理（需要正确配置）"

echo ""
echo "🎉 环境准备完成！"
