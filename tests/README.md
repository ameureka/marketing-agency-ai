# 🚀 Google ADK 营销代理系统 - Mac M 系列环境搭建

欢迎使用 Google ADK 营销代理系统！本项目为您提供了在 Mac M 系列芯片上搭建完整开发环境的全套资源。

## 📁 项目文件说明

| 文件名 | 描述 | 用途 |
|--------|------|------|
| `environment_setup_guide.md` | 📖 详细环境搭建指南 | 完整的手动搭建步骤说明 |
| `setup_environment.sh` | 🤖 自动化搭建脚本 | 一键执行大部分配置步骤 |
| `configuration_checklist.md` | ✅ 配置检查清单 | 验证环境配置和故障排除 |
| `agent_collaboration_analysis.md` | 🔍 系统架构分析 | 深度分析多代理协作机制 |
| `agent_collaboration_diagram.svg` | 📊 架构关系图 | 可视化代理协作流程 |

## 🎯 快速开始

### 方式一：自动化脚本（推荐）

```bash
# 1. 运行自动化搭建脚本
./setup_environment.sh

# 2. 按照提示完成手动配置步骤
# 3. 验证环境配置
cd ~/adk-marketing-project
./quick_start.sh
```

### 方式二：手动搭建

1. 📖 阅读 `environment_setup_guide.md`
2. 🔧 按步骤执行所有配置
3. ✅ 使用 `configuration_checklist.md` 验证

## 📋 环境搭建步骤概览

### 🔧 基础环境
- [x] 安装 Homebrew
- [x] 安装 Python 3.9+
- [x] 安装 Git
- [x] 安装 Google Cloud SDK

### ☁️ Google Cloud 配置
- [ ] 初始化 gcloud (`gcloud init`)
- [ ] 启用必要的 API
- [ ] 创建服务账号
- [ ] 下载密钥文件
- [ ] 设置环境变量

### 🐍 Python 环境
- [x] 创建虚拟环境
- [x] 安装依赖包
- [x] 克隆 ADK 示例代码

### ⚙️ 项目配置
- [ ] 配置 `.env` 文件
- [ ] 验证环境设置
- [ ] 运行测试脚本

## 🛠️ 系统要求

- **操作系统:** macOS 12.0+ (Monterey 或更高)
- **芯片:** Apple M1/M2/M3 系列
- **内存:** 建议 8GB 以上
- **存储:** 至少 5GB 可用空间
- **网络:** 稳定的互联网连接

## 📊 Google ADK 营销代理系统架构

### 🏗️ 多代理协作架构
```
营销协调代理 (marketing_coordinator)
├── 域名创建代理 (domain_create_agent)
├── 网站创建代理 (website_create_agent)
├── 营销材料代理 (marketing_create_agent)
└── Logo设计代理 (logo_create_agent)
```

### 🔄 工作流程
1. **域名选择** → 2. **网站创建** → 3. **营销策略** → 4. **Logo设计**

### ☁️ Google Cloud 服务依赖
- **Vertex AI:** AI/ML 平台
- **Gemini API:** 大语言模型
- **Imagen API:** 图像生成
- **Cloud Storage:** 文件存储
- **Cloud Monitoring:** 监控服务

## 🧪 环境验证

### 快速检查
```bash
# 检查基础环境
brew --version
python3 --version
gcloud --version

# 检查项目环境
cd ~/adk-marketing-project
source adk-env/bin/activate
python test_environment.py
```

### 完整验证
使用 `configuration_checklist.md` 中的详细检查清单。

## 🚨 常见问题

### Q1: M 系列芯片兼容性问题
**A:** 使用 `export ARCHFLAGS="-arch arm64"` 或 Rosetta 模式安装包。

### Q2: Google Cloud 认证失败
**A:** 运行 `gcloud auth login` 和 `gcloud auth application-default login`。

### Q3: Python 包安装失败
**A:** 确保虚拟环境已激活，使用 `pip install --upgrade pip` 更新 pip。

### Q4: API 权限错误
**A:** 检查服务账号权限，确保已启用必要的 Google Cloud API。

更多问题解决方案请查看 `configuration_checklist.md`。

## 📚 学习资源

### 官方文档
- [Google ADK 官方文档](https://developers.google.com/adk)
- [Google Cloud AI Platform](https://cloud.google.com/ai-platform)
- [Vertex AI 文档](https://cloud.google.com/vertex-ai/docs)

### 示例代码
- [ADK 示例仓库](https://github.com/google/adk-samples)
- [营销代理示例](https://github.com/google/adk-samples/tree/main/python/agents/marketing-agency)

## 🎯 下一步计划

环境搭建完成后，您可以：

1. **🔍 探索系统架构**
   - 阅读 `agent_collaboration_analysis.md`
   - 查看 `agent_collaboration_diagram.svg`

2. **🧪 运行示例代码**
   ```bash
   cd ~/adk-marketing-project/adk-samples/python/agents/marketing-agency
   python -m marketing_agency.agent
   ```

3. **🛠️ 自定义开发**
   - 修改代理配置
   - 扩展功能模块
   - 集成其他服务

4. **📈 生产部署**
   - 配置生产环境
   - 设置监控告警
   - 优化性能参数

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进本项目：

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

本项目遵循 MIT 许可证。详情请查看 LICENSE 文件。

## 📞 技术支持

如果您在环境搭建过程中遇到问题：

1. 📖 查看相关文档和检查清单
2. 🔍 搜索已知问题和解决方案
3. 💬 在 GitHub Issues 中提问
4. 📧 联系技术支持团队

---

**祝您使用愉快！🎉**

*最后更新: 2024年12月*