#!/bin/bash

# Google ADK 营销代理系统环境搭建自动化脚本
# 适用于 Mac M 系列芯片

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 通用虚拟环境检查函数
check_virtual_environment() {
    local venv_name="$1"
    local create_if_missing="$2"  # true/false
    
    if [ ! -d "$venv_name" ]; then
        if [ "$create_if_missing" = "true" ]; then
            log_info "创建虚拟环境 $venv_name..."
            python3 -m venv "$venv_name"
            log_success "虚拟环境 $venv_name 创建完成"
        else
            log_error "虚拟环境 $venv_name 不存在"
            return 1
        fi
    else
        log_info "虚拟环境 $venv_name 已存在"
    fi
    
    return 0
}

# 激活虚拟环境的安全函数
activate_virtual_environment() {
    local venv_name="$1"
    
    if [ ! -f "$venv_name/bin/activate" ]; then
        log_error "虚拟环境激活脚本不存在: $venv_name/bin/activate"
        return 1
    fi
    
    source "$venv_name/bin/activate"
    
    # 验证激活是否成功
    if [[ "$VIRTUAL_ENV" != *"$venv_name"* ]]; then
        log_error "虚拟环境激活失败"
        return 1
    fi
    
    log_success "虚拟环境已激活: $VIRTUAL_ENV"
    return 0
}

# 检查是否为 Mac M 系列芯片
check_mac_architecture() {
    log_info "检查系统架构..."
    if [[ $(uname -m) == "arm64" ]]; then
        log_success "检测到 Apple Silicon (M 系列芯片)"
    else
        log_warning "未检测到 Apple Silicon，脚本可能需要调整"
    fi
}

# 检查并安装 Homebrew
install_homebrew() {
    log_info "检查 Homebrew 安装状态..."
    if command -v brew &> /dev/null; then
        log_success "Homebrew 已安装"
        brew --version
    else
        log_info "安装 Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # 添加到 PATH
        ZSHRC_FILE="$HOME/.zshrc"
        if [ ! -f "$ZSHRC_FILE" ]; then
            touch "$ZSHRC_FILE"
        fi
        
        if echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> "$ZSHRC_FILE" 2>/dev/null; then
            log_info "Homebrew 环境变量已添加到 ~/.zshrc"
        else
            log_warning "无法写入 ~/.zshrc，请手动添加：eval \"\$(/opt/homebrew/bin/brew shellenv)\""
        fi
        
        eval "$(/opt/homebrew/bin/brew shellenv)"
        
        log_success "Homebrew 安装完成"
    fi
}

# 安装 Python
install_python() {
    log_info "检查 Python 安装状态..."
    
    # 优先检查Homebrew安装的Python 3.11
    if command -v /opt/homebrew/opt/python@3.11/bin/python3 &> /dev/null; then
        PYTHON_VERSION=$(/opt/homebrew/opt/python@3.11/bin/python3 --version | cut -d' ' -f2)
        log_success "发现Homebrew Python 3.11: $PYTHON_VERSION"
        
        # 确保PATH中包含Python 3.11
        export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"
        
        # 检查并更新.zshrc（添加权限检查）
        ZSHRC_FILE="$HOME/.zshrc"
        if [[ -w "$ZSHRC_FILE" ]] && ! grep -q "python@3.11" "$ZSHRC_FILE" 2>/dev/null; then
            echo 'export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"' >> "$ZSHRC_FILE"
            log_info "Python 3.11 路径已添加到 ~/.zshrc"
        elif [[ ! -w "$ZSHRC_FILE" ]]; then
            log_warning "无法写入 ~/.zshrc，请手动添加：export PATH=\"/opt/homebrew/opt/python@3.11/bin:\$PATH\""
        fi
        
        return 0
    fi
    
    # 检查系统默认Python版本
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        
        if [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -ge 11 ]]; then
            log_success "Python 版本满足要求: $PYTHON_VERSION"
            return 0
        else
            log_warning "当前Python版本 $PYTHON_VERSION 不满足要求（需要3.11+），正在安装..."
        fi
    else
        log_info "未检测到Python，正在安装Python 3.11..."
    fi
    
    # 安装Python 3.11
    brew install python@3.11
    
    # 配置PATH
    export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"
    
    # 更新.zshrc（添加权限检查）
    ZSHRC_FILE="$HOME/.zshrc"
    if [[ -w "$ZSHRC_FILE" ]] && ! grep -q "python@3.11" "$ZSHRC_FILE" 2>/dev/null; then
        echo 'export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"' >> "$ZSHRC_FILE"
        log_info "Python 3.11 路径已添加到 ~/.zshrc"
    elif [[ ! -w "$ZSHRC_FILE" ]]; then
        log_warning "无法写入 ~/.zshrc，请手动添加：export PATH=\"/opt/homebrew/opt/python@3.11/bin:\$PATH\""
    fi
    
    log_success "Python 3.11 配置完成"
}

# 安装 Git
install_git() {
    log_info "检查 Git 安装状态..."
    if command -v git &> /dev/null; then
        log_success "Git 已安装: $(git --version)"
    else
        log_info "安装 Git..."
        brew install git
        log_success "Git 安装完成"
    fi
}

# 安装 Google Cloud SDK
install_gcloud() {
    log_info "检查 Google Cloud SDK 安装状态..."
    
    # 检查当前目录的 Google Cloud SDK
    GCLOUD_DIR="$(pwd)/googlesdk/google-cloud-sdk"
    GCLOUD_BIN="$GCLOUD_DIR/bin/gcloud"
    
    if command -v gcloud &> /dev/null; then
        log_success "Google Cloud SDK 已安装: $(gcloud --version | head -n1)"
    elif [ -f "$GCLOUD_BIN" ]; then
        log_info "发现本地 Google Cloud SDK，配置环境变量..."
        
        # 添加到当前会话的 PATH
        export PATH="$GCLOUD_DIR/bin:$PATH"
        
        # 添加到 .zshrc
        ZSHRC_FILE="$HOME/.zshrc"
        if [ -f "$ZSHRC_FILE" ]; then
            if ! grep -q "google-cloud-sdk/bin" "$ZSHRC_FILE" 2>/dev/null; then
                if echo "export PATH=\"$GCLOUD_DIR/bin:\$PATH\"" >> "$ZSHRC_FILE" 2>/dev/null; then
                    log_info "Google Cloud SDK 路径已添加到 ~/.zshrc"
                else
                    log_warning "无法写入 ~/.zshrc，请手动添加："
                    echo "  export PATH=\"$GCLOUD_DIR/bin:\$PATH\""
                fi
            fi
        fi
        
        log_success "Google Cloud SDK 配置完成"
        log_warning "请运行 'gcloud init' 来初始化配置"
    else
        log_info "安装 Google Cloud SDK..."
        curl https://sdk.cloud.google.com | bash
        
        # 重新加载配置
        if [ -f "$HOME/.zshrc" ]; then
            source "$HOME/.zshrc" 2>/dev/null || log_warning "无法重新加载 ~/.zshrc，请手动运行: source ~/.zshrc"
        fi
        
        log_success "Google Cloud SDK 安装完成"
        log_warning "请运行 'gcloud init' 来初始化配置"
    fi
}

# 创建项目目录结构
setup_project_directory() {
    log_info "使用当前项目目录..."
    
    PROJECT_DIR="$(pwd)"
    log_success "项目目录: $PROJECT_DIR"
}

# 设置虚拟环境
setup_virtual_environment() {
    log_info "设置 Python 虚拟环境..."
    
    # 使用通用检查函数
    check_virtual_environment "venv_adk" "true"
    
    # 安全激活虚拟环境
    activate_virtual_environment "venv_adk"
    
    # 升级 pip
    pip install --upgrade pip
    
    log_success "虚拟环境配置完成"
}

# 克隆 ADK 示例代码
clone_adk_samples() {
    log_info "克隆 Google ADK 示例代码..."
    
    if [ ! -d "adk-samples" ]; then
        git clone https://github.com/google/adk-samples.git
        log_success "ADK 示例代码克隆完成"
    else
        log_info "ADK 示例代码已存在，更新中..."
        cd adk-samples
        git pull
        cd ..
        log_success "ADK 示例代码更新完成"
    fi
}

# 安装 Python 依赖
install_python_dependencies() {
    log_info "安装 Python 依赖包..."
    
    # 检查虚拟环境是否存在
    if [ ! -d "venv_adk" ]; then
        log_error "虚拟环境 venv_adk 不存在，请先创建虚拟环境"
        return 1
    fi
    
    # 激活虚拟环境
    source venv_adk/bin/activate
    
    # 检查是否成功激活
    if [[ "$VIRTUAL_ENV" != *"venv_adk"* ]]; then
        log_error "虚拟环境激活失败"
        return 1
    fi
    
    log_info "虚拟环境已激活: $VIRTUAL_ENV"
    
    # 创建正确的 requirements.txt 文件
    cat > requirements.txt << EOF
google-adk>=1.0.0
google-cloud-aiplatform>=1.38.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
requests>=2.31.0
whois>=0.9.27
typing-extensions>=4.5.0
pydantic>=2.0.0
EOF
    
    # 安装依赖包
    log_info "正在安装 Python 依赖包..."
    if pip install -r requirements.txt; then
        log_success "Python 依赖安装完成"
    else
        log_error "Python 依赖安装失败"
        return 1
    fi
    
    # 验证关键包是否安装成功
    log_info "验证包安装状态..."
    python -c "import google.cloud.aiplatform; print('✅ google-cloud-aiplatform 安装成功')" 2>/dev/null || log_warning "google-cloud-aiplatform 可能未正确安装"
    python -c "import google.generativeai; print('✅ google-generativeai 安装成功')" 2>/dev/null || log_warning "google-generativeai 可能未正确安装"
    python -c "import dotenv; print('✅ python-dotenv 安装成功')" 2>/dev/null || log_warning "python-dotenv 可能未正确安装"
}

# 创建配置模板
create_config_templates() {
    log_info "创建配置文件模板..."
    
    # 创建 .env 模板
    cat > .env.template << EOF
# Google Cloud 配置
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json

# API 配置
VERTEX_AI_ENDPOINT=https://us-central1-aiplatform.googleapis.com

# 模型配置
GEMINI_MODEL=gemini-2.5-pro-preview-05-06
IMAGEN_MODEL=imagen-3.0-generate-002

# 调试模式
DEBUG=True
EOF
    
    # 创建环境测试脚本
    cat > test_environment.py << 'EOF'
#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_environment():
    print("🔍 环境配置检查")
    print("=" * 50)
    
    # 检查 Python 版本
    python_version = sys.version
    print(f"🐍 Python 版本: {python_version}")
    
    # 检查环境变量
    required_vars = [
        'GOOGLE_CLOUD_PROJECT',
        'GOOGLE_CLOUD_LOCATION',
        'GOOGLE_APPLICATION_CREDENTIALS'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value and value != 'your-project-id' and value != '/path/to/your/service-account-key.json':
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: 未正确设置")
    
    # 检查服务账号密钥文件
    key_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if key_file and os.path.exists(key_file):
        print(f"✅ 服务账号密钥文件存在: {key_file}")
    else:
        print(f"❌ 服务账号密钥文件不存在或未设置: {key_file}")
    
    # 测试包导入
    packages_to_test = [
        ('google.cloud.aiplatform', 'Google Cloud AI Platform'),
        ('google.generativeai', 'Google Generative AI'),
        ('dotenv', 'Python Dotenv'),
        ('requests', 'Requests'),
        ('whois', 'Python Whois')
    ]
    
    for package, name in packages_to_test:
        try:
            __import__(package)
            print(f"✅ {name} 导入成功")
        except ImportError as e:
            print(f"❌ {name} 导入失败: {e}")
    
    # 测试 Google Cloud 连接（如果配置正确）
    if all(os.getenv(var) and os.getenv(var) not in ['your-project-id', '/path/to/your/service-account-key.json'] for var in required_vars):
        try:
            from google.cloud import aiplatform
            aiplatform.init(
                project=os.getenv('GOOGLE_CLOUD_PROJECT'),
                location=os.getenv('GOOGLE_CLOUD_LOCATION')
            )
            print("✅ Google Cloud AI Platform 连接成功")
        except Exception as e:
            print(f"❌ Google Cloud AI Platform 连接失败: {e}")
    else:
        print("⚠️  Google Cloud 配置未完成，跳过连接测试")
    
    print("\n🎉 环境检查完成！")
    print("\n📝 下一步操作：")
    print("1. 复制 .env.template 为 .env 并填入正确的配置")
    print("2. 运行 'gcloud init' 初始化 Google Cloud")
    print("3. 创建服务账号并下载密钥文件")
    print("4. 再次运行此脚本验证配置")

if __name__ == "__main__":
    test_environment()
EOF
    
    chmod +x test_environment.py
    
    log_success "配置文件模板创建完成"
}

# 创建快速启动脚本
create_quick_start_script() {
    log_info "创建快速启动脚本..."
    
    cat > quick_start.sh << 'EOF'
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
EOF
    
    chmod +x quick_start.sh
    
    log_success "快速启动脚本创建完成"
}

# 显示后续步骤
show_next_steps() {
    log_success "\n🎉 自动化环境搭建完成！"
    echo
    log_info "📋 后续手动步骤："
    echo "1. 运行 'gcloud init' 初始化 Google Cloud"
    echo "2. 启用必要的 API："
    echo "   gcloud services enable aiplatform.googleapis.com"
    echo "   gcloud services enable storage.googleapis.com"
    echo "3. 创建服务账号和密钥文件"
    echo "4. 复制 .env.template 为 .env 并填入正确配置"
    echo "5. 运行 './quick_start.sh' 启动开发环境"
    echo
    log_info "📁 项目目录: $(pwd)"
    log_info "🔧 激活虚拟环境: source venv_adk/bin/activate"
    log_info "🧪 测试环境: python test_environment.py"
    echo
}

# 主函数
main() {
    echo "🚀 Google ADK 营销代理系统环境搭建脚本"
    echo "适用于 Mac M 系列芯片"
    echo "=================================================="
    echo
    
    check_mac_architecture
    install_homebrew
    install_python
    install_git
    install_gcloud
    setup_project_directory
    setup_virtual_environment
    clone_adk_samples
    install_python_dependencies
    create_config_templates
    create_quick_start_script
    show_next_steps
}

# 运行主函数
main