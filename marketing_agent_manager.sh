#!/bin/bash

# 营销代理智能体管理脚本
# Marketing Agent Management Script
# 版本: 1.0
# 作者: 营销代理开发团队

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目路径
PROJECT_DIR="/Users/amerlin/Desktop/market_agent_google/marketing-agency"
LOG_DIR="/var/folders/ym/bwt1dt454gd8qlg181bhfbz40000gn/T/agents_log"
PID_FILE="$PROJECT_DIR/.marketing_agent.pid"

# 函数：打印带颜色的消息
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}[$(date '+%Y-%m-%d %H:%M:%S')] ${message}${NC}"
}

# 函数：检查Poetry是否安装
check_poetry() {
    if ! command -v poetry &> /dev/null; then
        print_message $RED "错误: Poetry未安装，请先安装Poetry"
        echo "安装命令: curl -sSL https://install.python-poetry.org | python3 -"
        exit 1
    fi
    print_message $GREEN "Poetry已安装: $(poetry --version)"
}

# 函数：检查项目目录
check_project_dir() {
    if [ ! -d "$PROJECT_DIR" ]; then
        print_message $RED "错误: 项目目录不存在: $PROJECT_DIR"
        exit 1
    fi
    print_message $GREEN "项目目录存在: $PROJECT_DIR"
}

# 函数：安装依赖
install_dependencies() {
    print_message $YELLOW "正在安装项目依赖..."
    cd "$PROJECT_DIR"
    
    if poetry install; then
        print_message $GREEN "依赖安装成功"
    else
        print_message $RED "依赖安装失败"
        exit 1
    fi
}

# 函数：启动营销代理
start_agent() {
    print_message $YELLOW "正在启动营销代理智能体..."
    
    # 检查是否已经在运行
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p $pid > /dev/null 2>&1; then
            print_message $YELLOW "营销代理已在运行 (PID: $pid)"
            return 0
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    cd "$PROJECT_DIR"
    
    # 后台启动代理
    nohup poetry run adk run marketing_agency > "$PROJECT_DIR/marketing_agent.log" 2>&1 &
    local pid=$!
    
    # 保存PID
    echo $pid > "$PID_FILE"
    
    # 等待几秒检查启动状态
    sleep 5
    
    if ps -p $pid > /dev/null 2>&1; then
        print_message $GREEN "营销代理启动成功 (PID: $pid)"
        print_message $BLUE "日志文件: $PROJECT_DIR/marketing_agent.log"
        print_message $BLUE "系统日志: $LOG_DIR/agent.latest.log"
    else
        print_message $RED "营销代理启动失败"
        rm -f "$PID_FILE"
        exit 1
    fi
}

# 函数：停止营销代理
stop_agent() {
    print_message $YELLOW "正在停止营销代理智能体..."
    
    if [ ! -f "$PID_FILE" ]; then
        print_message $YELLOW "营销代理未在运行"
        return 0
    fi
    
    local pid=$(cat "$PID_FILE")
    
    if ps -p $pid > /dev/null 2>&1; then
        # 尝试优雅停止
        kill $pid
        
        # 等待进程结束
        local count=0
        while ps -p $pid > /dev/null 2>&1 && [ $count -lt 10 ]; do
            sleep 1
            count=$((count + 1))
        done
        
        # 如果还在运行，强制停止
        if ps -p $pid > /dev/null 2>&1; then
            print_message $YELLOW "强制停止进程..."
            kill -9 $pid
        fi
        
        print_message $GREEN "营销代理已停止"
    else
        print_message $YELLOW "进程已不存在"
    fi
    
    rm -f "$PID_FILE"
}

# 函数：重启营销代理
restart_agent() {
    print_message $YELLOW "正在重启营销代理智能体..."
    stop_agent
    sleep 2
    start_agent
}

# 函数：检查代理状态
check_status() {
    print_message $BLUE "检查营销代理状态..."
    
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p $pid > /dev/null 2>&1; then
            print_message $GREEN "营销代理正在运行 (PID: $pid)"
            
            # 显示进程信息
            echo -e "${BLUE}进程信息:${NC}"
            ps -p $pid -o pid,ppid,cmd,etime,pcpu,pmem
            
            # 显示端口占用
            echo -e "\n${BLUE}端口占用:${NC}"
            lsof -p $pid | grep LISTEN || echo "未找到监听端口"
            
        else
            print_message $RED "PID文件存在但进程未运行"
            rm -f "$PID_FILE"
        fi
    else
        print_message $YELLOW "营销代理未在运行"
    fi
}

# 函数：查看实时日志
view_logs() {
    local log_type=$1
    
    case $log_type in
        "app")
            print_message $BLUE "查看应用日志 (Ctrl+C 退出)..."
            if [ -f "$PROJECT_DIR/marketing_agent.log" ]; then
                tail -f "$PROJECT_DIR/marketing_agent.log"
            else
                print_message $RED "应用日志文件不存在"
            fi
            ;;
        "system")
            print_message $BLUE "查看系统日志 (Ctrl+C 退出)..."
            if [ -f "$LOG_DIR/agent.latest.log" ]; then
                tail -f "$LOG_DIR/agent.latest.log"
            else
                print_message $RED "系统日志文件不存在"
            fi
            ;;
        "all")
            print_message $BLUE "查看所有日志文件..."
            echo -e "\n${YELLOW}=== 应用日志 (最后50行) ===${NC}"
            if [ -f "$PROJECT_DIR/marketing_agent.log" ]; then
                tail -50 "$PROJECT_DIR/marketing_agent.log"
            else
                echo "应用日志文件不存在"
            fi
            
            echo -e "\n${YELLOW}=== 系统日志 (最后50行) ===${NC}"
            if [ -f "$LOG_DIR/agent.latest.log" ]; then
                tail -50 "$LOG_DIR/agent.latest.log"
            else
                echo "系统日志文件不存在"
            fi
            
            echo -e "\n${YELLOW}=== 日志目录文件列表 ===${NC}"
            if [ -d "$LOG_DIR" ]; then
                ls -la "$LOG_DIR"
            else
                echo "日志目录不存在"
            fi
            ;;
        *)
            print_message $RED "无效的日志类型: $log_type"
            echo "可用选项: app, system, all"
            ;;
    esac
}

# 函数：清理日志
clean_logs() {
    print_message $YELLOW "正在清理日志文件..."
    
    # 清理应用日志
    if [ -f "$PROJECT_DIR/marketing_agent.log" ]; then
        > "$PROJECT_DIR/marketing_agent.log"
        print_message $GREEN "应用日志已清理"
    fi
    
    # 清理系统日志（谨慎操作）
    read -p "是否清理系统日志目录? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -d "$LOG_DIR" ]; then
            rm -f "$LOG_DIR"/*.log
            print_message $GREEN "系统日志已清理"
        fi
    fi
}

# 函数：显示帮助信息
show_help() {
    echo -e "${BLUE}营销代理智能体管理脚本${NC}"
    echo -e "${BLUE}================================${NC}"
    echo
    echo "用法: $0 [命令] [选项]"
    echo
    echo "可用命令:"
    echo "  start          启动营销代理"
    echo "  stop           停止营销代理"
    echo "  restart        重启营销代理"
    echo "  status         检查代理状态"
    echo "  install        安装项目依赖"
    echo "  logs [type]    查看日志"
    echo "                 type: app (应用日志), system (系统日志), all (所有日志)"
    echo "  clean          清理日志文件"
    echo "  help           显示此帮助信息"
    echo
    echo "示例:"
    echo "  $0 start                    # 启动营销代理"
    echo "  $0 logs app                 # 查看应用日志"
    echo "  $0 logs system              # 查看系统日志"
    echo "  $0 status                   # 检查运行状态"
    echo
    echo "日志文件位置:"
    echo "  应用日志: $PROJECT_DIR/marketing_agent.log"
    echo "  系统日志: $LOG_DIR/agent.latest.log"
    echo
}

# 函数：环境检查
check_environment() {
    print_message $BLUE "正在检查运行环境..."
    
    # 检查操作系统
    if [[ "$OSTYPE" == "darwin"* ]]; then
        print_message $GREEN "操作系统: macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_message $GREEN "操作系统: Linux"
    else
        print_message $YELLOW "操作系统: $OSTYPE (未完全测试)"
    fi
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        print_message $GREEN "Python3: $(python3 --version)"
    else
        print_message $RED "错误: Python3未安装"
        exit 1
    fi
    
    check_poetry
    check_project_dir
    
    # 检查日志目录
    if [ -d "$LOG_DIR" ]; then
        print_message $GREEN "日志目录存在: $LOG_DIR"
    else
        print_message $YELLOW "日志目录不存在，将在运行时创建"
    fi
}

# 主函数
main() {
    case $1 in
        "start")
            check_environment
            start_agent
            ;;
        "stop")
            stop_agent
            ;;
        "restart")
            check_environment
            restart_agent
            ;;
        "status")
            check_status
            ;;
        "install")
            check_environment
            install_dependencies
            ;;
        "logs")
            view_logs $2
            ;;
        "clean")
            clean_logs
            ;;
        "help" | "-h" | "--help")
            show_help
            ;;
        "")
            show_help
            ;;
        *)
            print_message $RED "未知命令: $1"
            echo "使用 '$0 help' 查看可用命令"
            exit 1
            ;;
    esac
}

# 脚本入口
main "$@"