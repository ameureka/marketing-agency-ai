#  该设计文档主要介绍了在google之中使用的SDK模式进行账号管理以及业务部署的，后续可以参思路做其它云的部署SDK的说明
# 包含 tencent cloud ,cloudflare supabase等先关的云服务的设计内容
-------------------------------------谷歌云基础设置-------------------------------
## 🚀 完整配置流程
### 步骤 1: 环境准备
# 1. 确保已安装 Google Cloud SDK
gcloud --version

# 2. 登录 Google Cloud
gcloud auth login

# 3. 初始化配置
gcloud init

步骤 2: 项目设置

# 1. 创建或选择项目
gcloud projects create your-marketing-project-id
gcloud config set project your-marketing-project-id

# 2. 启用计费（必需）
# 在 Google Cloud Console 中为项目启用计费

步骤 3: 服务账号配置
# 1. 创建服务账号
gcloud iam service-accounts create marketing-agent \
    --display-name="Marketing Agent"

# 2. 下载密钥文件
gcloud iam service-accounts keys create ~/marketing-agent-key.json \
    --iam-account=marketing-agent@your-project-id.iam.gserviceaccount.com

# 3. 设置权限
gcloud projects add-iam-policy-binding your-project-id \
    --member="serviceAccount:marketing-agent@your-project-id.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

步骤 4: 更新配置文件

# Google Cloud 配置
GOOGLE_CLOUD_PROJECT=your-actual-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/Users/amerlin/marketing-agent-key.json

# API 配置
VERTEX_AI_ENDPOINT=https://us-central1-aiplatform.googleapis.com

# 模型配置
GEMINI_MODEL=gemini-2.5-pro-preview-05-06
IMAGEN_MODEL=imagen-3.0-generate-002

# 调试模式
DEBUG=True
步骤 5: 验证配置
# 1. 激活虚拟环境
source venv_adk/bin/activate

# 2. 运行测试脚本
python test_environment.py

# 3. 验证营销代理
python validate_marketing_agent.py

##  重要注意事项
1. 计费警告: 确保在 Google Cloud Console 中设置预算警报
2. 安全性: 不要将 .env 文件提交到版本控制系统
3. 权限: 服务账号需要适当的 IAM 权限
4. 区域一致性: 确保所有服务使用相同的区域
## 🔍 故障排除
如果遇到问题，请检查：

- Google Cloud 项目是否已启用计费
- API 是否已正确启用
- 服务账号密钥文件路径是否正确
- 环境变量是否正确设置
按照以上步骤配置后，您的 Google ADK 营销代理系统就可以正常运行了！








-------------------------------------

## 📋 配置文件参数详解
### 1. Google Cloud 基础配置 GOOGLE_CLOUD_PROJECT
当前值: your-project-id 配置步骤:


# 或列出现有项目
gcloud projects list
# 2. 设置默认项目
gcloud config set project your-actual-project-id
# 3. 更新 .env 文件
GOOGLE_CLOUD_PROJECT=your-actual-project-id


GOOGLE_CLOUD_LOCATION
当前值: us-central1 说明: 这是推荐的区域设置，通常无需修改 可选区域: us-east1 , us-west1 , europe-west1 , asia-east1

当前值: /Users/amerlin/Desktop/market_agent_google/adk-samples/credentials/google_service-account-key.json 
配置步骤:
# 1. 创建服务账号
gcloud iam service-accounts create marketing-agent-sa \
    --display-name="Marketing Agent Service Account"

# 2. 授予必要权限
gcloud projects add-iam-policy-binding your-project-id \
    --member="serviceAccount:marketing-agent-sa@your-project-id.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding your-project-id \
    --member="serviceAccount:marketing-agent-sa@your-project-id.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# 3. 创建并下载密钥文件
gcloud iam service-accounts keys create ~/marketing-agent-key.json \
    --iam-account=marketing-agent-sa@your-project-id.iam.gserviceaccount.com

# 4. 更新 .env 文件
GOOGLE_APPLICATION_CREDENTIALS=/Users/amerlin/Desktop/market_agent_google/adk-samples/credentials/google_service-account-key.json


### 2. API 配置 VERTEX_AI_ENDPOINT
当前值: https://us-central1-aiplatform.googleapis.com 说明: 根据您的区域自动生成，格式为 https://{region}-aiplatform.googleapis.com

启用必要的 API:

# 启用 Vertex AI API
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# 验证 API 状态
gcloud services list --enabled

### 3. 模型配置 GEMINI_MODEL
当前值: gemini-2.5-pro-preview-05-06 说明: 这是 Google 的最新 Gemini 模型版本 可选模型:

- gemini-1.5-pro
- gemini-1.5-flash
- gemini-2.0-flash-exp IMAGEN_MODEL
当前值: imagen-3.0-generate-002 说明: 用于图像生成的 Imagen 模型 可选模型:

- imagen-2.0-generate-001
- imagen-3.0-generate-001
### 4. 调试配置 DEBUG
当前值: True 说明: 开发阶段建议保持为 True ，生产环境设置为 False




该项目主要部署在Google Cloud的Vertex AI Agent Engine上，而不是传统的虚拟机。

### 核心部署服务
1. Vertex AI Agent Engine - 主要部署平台
   
   - 这是Google Cloud的托管AI代理服务
   - 无服务器架构，无需管理虚拟机
   - 自动扩缩容和负载均衡
   - 通过 agent_engines.create() 方法部署
2. 相关Google Cloud服务
   
   - Vertex AI : 提供Gemini模型推理服务
   - Cloud Storage : 存储生成的文件和资源
   - Imagen API : 图像生成服务
   - Cloud Monitoring : 监控和日志记录
### 部署架构特点 无服务器部署
- 项目使用 AdkApp 框架包装代理逻辑
- 通过 vertexai.agent_engines.create() 部署到托管环境
- 无需配置或管理虚拟机、容器或服务器

部署流程

# 部署到Vertex AI Agent Engine
python3 deployment/deploy.py --create

依赖的云服务
- Vertex AI Agent Engine : 代理运行环境
- Cloud Storage : 文件存储（需要配置bucket）
- Vertex AI API : 模型调用
- Gemini API : 文本生成
- Imagen API : 图像生成

特性 Vertex AI Agent Engine 传统虚拟机 服务器管理 完全托管，无需管理 需要配置和维护 扩缩容 自动扩缩容 手动配置 计费方式 按使用量计费 按实例时间计费 部署复杂度 简单，一键部署 需要配置环境 运维负担 极低 较高

项目采用现代化的无服务器架构，主要部署在Google Cloud的Vertex AI Agent Engine上，这是一个完全托管的AI代理服务平台。用户无需管理虚拟机、容器或服务器基础设施，只需通过简单的部署脚本即可将代理部署到云端，享受自动扩缩容、高可用性和按需计费的优势。