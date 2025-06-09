#!/bin/bash

# 营销代理快速启动脚本
# Quick Start Script for Marketing Agent

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANAGER_SCRIPT="$SCRIPT_DIR/marketing_agent_manager.sh"

echo -e "${BLUE}营销代理智能体快速启动${NC}"
echo -e "${BLUE}========================${NC}"
echo

# 检查管理脚本是否存在
if [ ! -f "$MANAGER_SCRIPT" ]; then
    echo -e "${RED}错误: 管理脚本不存在: $MANAGER_SCRIPT${NC}"
    exit 1
fi

# 显示菜单
show_menu() {
    echo -e "${YELLOW}请选择操作:${NC}"
    echo "1. 启动营销代理"
    echo "2. 停止营销代理"
    echo "3. 重启营销代理"
    echo "4. 查看状态"
    echo "5. 查看应用日志"
    echo "6. 查看系统日志"
    echo "7. 查看所有日志"
    echo "8. 安装依赖"
    echo "9. 清理日志"
    echo "0. 退出"
    echo
}

# 主循环
while true; do
    show_menu
    read -p "请输入选项 (0-9): " choice
    echo
    
    case $choice in
        1)
            echo -e "${GREEN}启动营销代理...${NC}"
            "$MANAGER_SCRIPT" start
            ;;
        2)
            echo -e "${YELLOW}停止营销代理...${NC}"
            "$MANAGER_SCRIPT" stop
            ;;
        3)
            echo -e "${YELLOW}重启营销代理...${NC}"
            "$MANAGER_SCRIPT" restart
            ;;
        4)
            echo -e "${BLUE}检查状态...${NC}"
            "$MANAGER_SCRIPT" status
            ;;
        5)
            echo -e "${BLUE}查看应用日志...${NC}"
            "$MANAGER_SCRIPT" logs app
            ;;
        6)
            echo -e "${BLUE}查看系统日志...${NC}"
            "$MANAGER_SCRIPT" logs system
            ;;
        7)
            echo -e "${BLUE}查看所有日志...${NC}"
            "$MANAGER_SCRIPT" logs all
            ;;
        8)
            echo -e "${YELLOW}安装依赖...${NC}"
            "$MANAGER_SCRIPT" install
            ;;
        9)
            echo -e "${YELLOW}清理日志...${NC}"
            "$MANAGER_SCRIPT" clean
            ;;
        0)
            echo -e "${GREEN}退出程序${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}无效选项，请重新选择${NC}"
            ;;
    esac
    
    echo
    read -p "按回车键继续..."
    echo
done