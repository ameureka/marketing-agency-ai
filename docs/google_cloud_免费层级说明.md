









## 🎯 Vertex AI Agent Engine 免费额度概览
### 新用户免费试用额度
Google Cloud新客户可获得高达$300的免费试用额度 5 ，可用于试用Vertex AI和其他Google Cloud产品。

### AI Applications专项免费额度
$1,000免费试用额度专门用于AI Applications 1 ，包括：

- 额度有效期： 1年 （从2023年7月18日账户注册开始计算）
- 适用范围：AI Applications相关服务
- 包含Vertex AI Agent Builder等服务
## 📊 Vertex AI Agent Engine具体限制
### 免费层级配额
根据官方文档，Vertex AI Agent Engine在每个项目每个区域有以下限制 6 ：

操作类型 免费限制 创建/删除/更新 Agent Engine 每分钟10次 创建/删除/更新 Sessions 每分钟100次 查询/流式查询 Agent Engine 每分钟60次 向Sessions添加事件 每分钟100次 最大Agent Engine资源数量 100个

### Vertex AI Search免费配额
每月10,000次查询免费 1 ，用于探索Vertex AI Search功能（不包括高级生成式答案）。

## 💰 定价结构
### Agent Engine运行时定价
基于计算资源使用量计费 2 ：

- 按vCPU小时和内存GiB小时计费
- 部署到Agent Engine托管运行时的代理消耗的资源
### Gemini模型定价示例
以Gemini 2.5 Flash为例 3 ：

- 输入（文本、图像、视频）：$0.15/百万tokens
- 文本输出：$0.60/百万tokens
- 音频输入：$1.00/百万tokens
## 🚀 成本优化建议
### 1. 充分利用免费额度
- 优先使用$300新用户额度进行初期开发
- 利用$1,000 AI Applications专项额度
- 合理规划每月10,000次免费查询
### 2. 开发阶段优化
- 在开发阶段使用较小的模型进行测试
- 利用批处理API获得50%折扣 3
- 合理设计Agent架构，避免不必要的API调用
### 3. 生产环境规划
- 监控配额使用情况，避免超出限制
- 考虑使用Provisioned Throughput获得可预测的服务级别
- 实施适当的缓存策略减少重复调用
## 📋 项目配置检查
基于您当前的营销代理项目，建议：

1. 环境配置验证 ：确保已正确设置Google Cloud项目和服务账号
2. 配额监控 ：定期检查Agent Engine使用量，避免超出免费限制
3. 成本预算 ：设置预算警报，监控实际使用成本
4. 开发策略 ：在免费额度内完成原型开发和测试