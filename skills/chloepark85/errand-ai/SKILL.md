# ErrandAI 技能

## 概述  
该技能使您的人工智能助手能够通过 ErrandAI 平台为人类工作者发布和管理任务。它将 OpenClaw 与 ErrandAI 的去中心化任务市场集成在一起。

## 主要功能  
- 🤖 **自然语言命令**：使用对话式语言发布任务  
- 📊 **状态跟踪**：实时查看任务的状态和提交情况  
- ✅ **工作审核**：批准或拒绝任务并给出反馈  
- 💰 **自动支付**：任务批准后自动发放 USDC 付款  
- 🌍 **全球覆盖**：可以在全球任何地点发布任务  

## 安装  

### 先决条件  
- OpenClaw v1.0.0 或更高版本  
- Node.js v14.0.0 或更高版本  
- ErrandAI API 密钥（从 [errand.be/dashboard](https://errand.be/dashboard) 获取）  

### 快速安装  
```bash
openclaw skill install errand-ai
```  

### 手动安装  
1. 下载技能文件  
2. 将文件复制到 OpenClaw 的技能目录中：  
   ```bash
   cp -r errand-ai ~/.openclaw/skills/
   ```  
3. 设置您的 API 密钥：  
   ```bash
   export ERRANDAI_API_KEY="your_api_key_here"
   ```  
4. 启用该技能：  
   ```bash
   openclaw skill enable errand-ai
   ```  

## 配置  

### 环境变量  
```bash
# Required
ERRANDAI_API_KEY=your_api_key_here

# Optional (defaults shown)
ERRANDAI_API_URL=https://api.errand.be
```  

### OpenClaw 配置  
```yaml
# ~/.openclaw/config.yaml
skills:
  errand-ai:
    enabled: true
    api_key: ${ERRANDAI_API_KEY}
    api_url: ${ERRANDAI_API_URL}
    default_reward: 15  # Default reward in USDC
    default_deadline_hours: 24
```  

## 使用示例  

### 发布任务  
```
You: Post an errand to check iPhone 15 stock at Apple Store Gangnam for $20
OpenClaw: ✅ Errand posted successfully!
Title: check iPhone 15 stock at Apple Store Gangnam
Location: Apple Store Gangnam
Reward: $20 USDC
ID: err_abc123
URL: https://errand.be/errand/err_abc123
```  

### 查看状态  
```
You: Check errand err_abc123
OpenClaw: 📋 Errand Status
Title: check iPhone 15 stock at Apple Store Gangnam
Status: in_progress
Reward: $20 USDC
Submissions: 2
```  

### 审核提交  
```
You: Approve submission sub_def456
OpenClaw: ✅ Submission approved! Payment has been released to the worker.
```  

## 支持的命令  
| 命令 | 描述 | 示例 |  
|---------|-------------|---------|  
| `post errand` | 创建新任务 | “发布任务：去星巴克拍摄菜单照片，费用 15 美元” |  
| `check errand` | 查看任务状态 | “查看任务 err_123456 的状态” |  
| `list my errands` | 列出所有已发布的任务 | “显示我发布的任务” |  
| `review submission` | 批准/拒绝任务提交 | “批准提交 sub_789” |  

## 自然语言模式  
该技能支持多种自然语言指令：  
- “创建一个任务……”  
- “我需要有人……”  
- “为……发布一个任务”  
- “查看……的状态”  
- “批准/拒绝任务提交……”  

## 支持的任务类别  
- 📸 **摄影**：产品拍照、位置验证  
- 🔍 **产品验证**：库存检查、商品可用性  
- 💰 **价格调研**：价格比较、市场调研  
- 📝 **翻译**：文档翻译、菜单翻译  
- 📊 **调研**：调查、访谈、数据收集  
- 📦 **配送**：包裹取件、配送确认  
- 🎯 **其他**：自定义任务  

## API 集成  

### 使用的端点  
- `POST /api/openclaw/errands`：创建新任务  
- `GET /api/openclaw/errands/{id}`：查看任务状态  
- `POST /api/openclaw/submissions/{id}/review`：审核任务提交  
- `GET /api/openclaw/errands`：列出用户的所有任务  

### 响应格式  
```json
{
  "success": true,
  "errand": {
    "id": "err_abc123",
    "title": "Check iPhone stock",
    "status": "in_progress",
    "reward_amount": 20,
    "submissions_count": 2,
    "url": "https://errand.be/errand/err_abc123"
  }
}
```  

## 错误处理  
该技能能够优雅地处理常见错误：  
- API 密钥缺失：提示用户设置 ERRANDAI_API_KEY  
- 网络错误：采用指数级退避策略重试  
- 无效命令：提供相关示例  
- API 错误：返回明确的错误信息  

## 安全性  
- API 密钥存储在环境变量中  
- 所有 API 调用均使用 HTTPS  
- 验证 Webhook 签名  
- 不记录任何敏感数据  

## 故障排除  

### API 密钥相关问题  
```bash
# Verify API key is set
echo $ERRANDAI_API_KEY

# Test API connection
curl -H "X-API-Key: $ERRANDAI_API_KEY" https://api.errand.be/api/openclaw/health
```  

### 技能无法加载  
```bash
# Check skill status
openclaw skill status errand-ai

# Reload skills
openclaw skill reload

# Check logs
tail -f ~/.openclaw/logs/skills.log
```  

### 常见问题  
| 问题 | 解决方案 |  
|-------|----------|  
| “API 密钥未配置” | 设置 ERRANDAI_API_KEY 环境变量 |  
| “无法发布任务” | 检查网络和 API 状态 |  
| “任务未找到” | 验证任务 ID 格式（err_xxxxx） |  
| “未经授权” | 检查 API 密钥的有效性 |  

## 高级功能  
- **批量操作**  
- **自动化工作流程**  
- **自定义验证规则**  

## 性能指标  
- 平均响应时间：<500 毫秒  
- 同时处理的任务数量限制：10 个  
- 每分钟请求限制：100 次  
- Webhook 延迟：<100 毫秒  

## 更新日志  
### v1.0.0 (2024-02-14)  
- 初始版本发布  
- 基本的任务发布和管理功能  
- 自然语言处理  
- 任务审核功能  
- USDC 支付集成  

## 支持方式  
- 📧 电子邮件：support@errand.be  
- 💬 Discord：[ErrandAI 社区](https://discord.gg/errandai)  
- 🐛 问题反馈：[GitHub](https://github.com/errandai/openclaw-skill/issues)  
- 📖 文档：[docs.errand.be](https://docs.errand.be)  

## 许可证  
MIT 许可证——详情请参阅 LICENSE 文件  

## 贡献指南  
我们欢迎您的贡献！请参阅 [CONTRIBUTING.md](https://github.com/errandai/openclaw-skill/blob/main/CONTRIBUTING.md) 以获取贡献指南。  

## 致谢  
该技能由 ErrandAI 团队为 OpenClaw 生态系统开发。