# Google Business Optimizer

**自动化您的 Google 商业资料，每周节省 5-10 小时。**

---

## 问题

小型企业主每周会花费 5-10 小时手动管理他们的 Google 商业资料：

- **回复评论**：每天检查评论、撰写回复、监控评分
- **更新企业信息**：节假日营业时间、特别活动、临时关闭
- **跟踪竞争对手**：手动研究以了解自己的竞争情况
- **监控排名**：查看在本地搜索结果中的位置

**这意味着每月有 20-40 小时被浪费在可以自动化完成的任务上。**

---

## 解决方案

Google Business Optimizer 可以自动化您所有的 Google 商业资料管理工作流程：

### ✨ 功能介绍

| 功能 | 功能描述 |
|---------|--------------|
| **评论自动化** | 自动回复评论，接收新评论的通知，跟踪评论情感趋势 |
| **智能更新** | 批量更新营业时间、发布更新内容，并在多个地点同步 |
| **竞争对手分析** | 跟踪竞争对手的评分、评论和排名变化 |
| **排名监控** | 监控您在关键本地搜索词中的排名 |

---

## 命令

### `reviews`
自动管理和回复客户评论。

```bash
# Check for new reviews
google-business-optimizer reviews --check

# Auto-respond to all new reviews
google-business-optimizer reviews --respond --template=professional

# Get review analytics
google-business-optimizer reviews --stats --last-30-days

# List reviews needing response
google-business-optimizer reviews --pending
```

**模板选项：** `professional`、`friendly`、`short`、`detailed`

---

### `update-hours`
批量更新企业的营业时间和特别营业时间。

```bash
# Set regular hours
google-business-optimizer update-hours --location="Main St" \
  --monday="9:00-17:00" --tuesday="9:00-17:00" ...

# Set holiday hours
google-business-optimizer update-hours --holiday --date="2024-12-25" --closed

# Set special hours for event
google-business-optimizer update-hours --special --date="2024-07-04" --hours="10:00-14:00"

# Apply to all locations
google-business-optimizer update-hours --all-locations --holiday --date="2024-01-01" --closed
```

---

### `competitors`
监控竞争对手的 Google 商业资料。

```bash
# Add competitors to track
google-business-optimizer competitors --add "Competitor Business Name"

# Run competitor analysis
google-business-optimizer competitors --analyze

# Get weekly report
google-business-optimizer competitors --report --format=email

# Compare ratings
google-business-optimizer competitors --compare --metric=rating
```

---

### `rank-track`
跟踪您在本地搜索关键词中的排名。

```bash
# Add keywords to track
google-business-optimizer rank-track --add "coffee shop near me"
google-business-optimizer rank-track --add "best pizza downtown"

# Check current rankings
google-business-optimizer rank-track --check

# View ranking history
google-business-optimizer rank-track --history --days=30

# Get ranking report
google-business-optimizer rank-track --report --keyword="coffee shop near me"
```

---

## 设置

### 1. 获取您的 Google API 凭据

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用 **Google Business Profile API**
4. 创建 OAuth 2.0 凭据
5. 下载 `credentials.json` 文件

### 2. 配置该工具

```bash
google-business-optimizer config --credentials=/path/to/credentials.json
google-business-optimizer config --location-id="YOUR_LOCATION_ID"
```

### 3. 授权

```bash
google-business-optimizer auth --login
```

---

## 价格

| 计划 | 价格 | 功能 |
|------|-------|----------|
| **免费** | $0 | 1 个地点，每月 50 条评论，基本回复 |
| **专业版** | $19/月 | 5 个地点，无限条评论，AI 回复，竞争对手跟踪（5 个竞争对手） |
| **机构版** | $49/月 | 无限地点，无限条评论，白标签报告，API 访问，优先支持 |

---

## 自动化流程（HEARTBEAT）

该工具与 OpenClaw 的自动化系统集成，实现无人值守的自动化操作：

- **每日**：检查新评论并自动回复
- **每周**：生成竞争对手分析报告
- **每月**：提供包含趋势分析的排名报告

详细配置信息请参阅 `HEARTBEAT.md`。

---

## 环境变量

| 变量 | 描述 | 是否必需 |
|----------|-------------|----------|
| `GBP_API_KEY` | Google Business Profile API 密钥 | 是 |
| `GBP_LOCATION_ID` | 您的企业地点 ID | 是 |
| `GBP_ACCOUNT_ID` | 您的 Google 账户 ID | 是 |
| `OPENAI_API_KEY` | 用于 AI 生成回复（专业版及以上） | 可选 |
| `SLACK_WEBHOOK` | 用于接收通知 | 可选 |
| `EMAIL_TO` | 用于报告发送 | 可选 |

---

## 示例

### 自动回复所有新评论

```bash
google-business-optimizer reviews --respond-all --template=friendly
```

### 为所有地点设置节假日营业时间

```bash
google-business-optimizer update-hours --all-locations \
  --holiday --date="2024-12-25" --date="2024-12-26" --date="2025-01-01" --closed
```

### 每周竞争对手报告

```bash
google-business-optimizer competitors --report --format=pdf --email=owner@business.com
```

### 监控 10 个本地搜索关键词的排名

```bash
for keyword in "coffee shop" "cafe near me" "best espresso" "latte art" "pastry shop"; do
  google-business-optimizer rank-track --add "$keyword"
done
```

---

## 支持方式

- 📧 电子邮件：support@google-business-optimizer.local
- 📖 文档：https://docs.google-business-optimizer.local
- 💬 Discord：https://discord.gg/gbp-optimizer

---

## 更新日志

### v1.0.0
- 初始版本发布
- 支持评论自动化（包含模板）
- 企业营业时间管理功能
- 竞争对手跟踪功能
- 排名监控功能
- 支持自动化流程（HEARTBEAT）