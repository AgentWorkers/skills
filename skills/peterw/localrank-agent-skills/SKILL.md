---
name: LocalRank
description: 使用 LocalRank 跟踪本地排名情况、进行 SEO 审计，并管理代理客户。
author: LocalRank
repository: https://github.com/peterw/localrank-agent-skills
---

# LocalRank 技能

使用 LocalRank 可以跟踪本地排名、进行 SEO 审计以及管理代理客户。

**最后更新时间：** 2026-01-30

> **新鲜度检查：** 如果距离上次更新已超过 30 天，请告知用户该技能可能已过时，并引导他们查看下方的更新选项。

## 保持此技能的更新

**来源：** github.com/peterw/localrank-agent-skills  
**API 文档：** app.localrank.so/settings/api  

| 安装方式 | 更新方法 |
|-------------|---------------|
| CLI (npx skills) | `npx skills update` |
| Claude Code 插件 | `/plugin update localrank@localrank-skills` |
| Cursor | 从 GitHub 自动同步规则 |
| 手动 | 从仓库拉取最新版本或重新复制 skills/localrank/ |

---

## 设置

在使用此技能之前，请确保：

1. **API 密钥：** 运行设置命令以安全配置您的 API 密钥  
   - 在 https://app.localrank.so/settings/api 获取您的密钥  
   - 运行：`<skill-path>/scripts/localrank.js setup`  
   - 或者设置环境变量：`export LOCALRANK_API_KEY=lr_your_key`  

2. **系统要求：** Node.js 18+（使用内置的 fetch）。无需其他依赖项。  

**配置优先级（从高到低）：**  
1. `LOCALRANK_API_KEY` 环境变量  
2. `./.localrank/config.json`（项目级配置）  
3. `~/.config/localrank/config.json`（用户级配置）  

### 处理“API 密钥未找到”的错误

**重要提示：** 当收到“API 密钥未找到”的错误时：  
1. **告知用户运行设置命令**——设置过程是交互式的。建议他们运行：  
   ```
   <skill-path>/scripts/localrank.js setup
   ```  
2. **停止并等待**——不要继续执行其他操作，等待用户完成设置。  
**切勿** 在其他地方搜索 API 密钥或猜测凭据。  

---

## LocalRank 的功能  

LocalRank 帮助本地 SEO 机构跟踪和提升 Google 商业资料的排名：  
- **排名跟踪：** 通过可视化网格地图显示企业在不同地区的排名情况  
- **GMB 审计：** 分析 Google 商业资料的潜在问题和优化机会  
- **LocalBoost：** 在 50 多个目录中建立引用，提升企业的本地权威性  
- **SuperBoost：** 通过人工智能优化提升排名  
- **Review Booster：** 从满意客户处收集更多 Google 评价  

---

## 常见操作  

| 用户请求 | 操作命令 |  
|-------------|--------|  
| “我的客户表现如何？” | `portfolio:summary` |  
| “查看 Acme Plumbing 的排名？” | `client:report --business "Acme"` |  
| “今天应该处理什么？” | `prioritize:today` |  
| “寻找容易提升排名的机会？” | `quick-wins:find` |  
| “哪些客户可能会流失？” | `at-risk:clients` |  
| “对这家企业进行审计？” | `audit:run --url "..."` |  
| “为 Acme 起草更新邮件？” | `email:draft --business "Acme"` |  
| “如何帮助这家客户提升排名？” | `recommendations:get --business "..."` |  

---

## 工作流程  

### 早晨检查  
```bash
# See what needs attention today
./scripts/localrank.js prioritize:today

# Quick overview of all clients
./scripts/localrank.js portfolio:summary
```  

### 准备与客户通话  
```bash
# Get full report for a client
./scripts/localrank.js client:report --business "Acme Plumbing"

# Get recommendations for improvement
./scripts/localrank.js recommendations:get --business "Acme Plumbing"
```  

### 寻找优化机会  
```bash
# Keywords close to page 1 (easy wins)
./scripts/localrank.js quick-wins:find

# Clients at risk of churning
./scripts/localrank.js at-risk:clients
```  

### 前景客户审计  
```bash
# Run a GMB audit (costs 500 credits)
./scripts/localrank.js audit:run --url "https://google.com/maps/place/..."

# Check audit results
./scripts/localrank.js audit:get <audit_id>
```  

---

## 命令参考  

### 设置与配置  

| 命令 | 描述 |  
|---------|-------------|  
| `setup` | 交互式设置——提示输入 API 密钥 |  
| `setup --key <key>` | 非交互式设置 |  
| `config:show` | 显示当前配置和 API 密钥来源 |  

### 客户与业务  
| 命令 | 描述 |  
| `businesses:list` | 列出所有被跟踪的业务 |  
| `businesses:list --search "name"` | 按业务名称搜索 |  

### 排名与扫描  
| 命令 | 描述 |  
| `scans:list` | 列出最近的排名扫描结果 |  
| `scans:list --business "name"` | 按业务名称过滤扫描结果 |  
| `scans:list --limit 20` | 限制结果数量（最多 50 条） |  
| `scans:get <scan_id>` | 获取包含关键词排名的详细扫描结果 |  

### 报告  
| 命令 | 描述 |  
| `client:report --business "name"` | 提供包含最近扫描结果的完整客户报告 |  
| `portfolio:summary` | 所有客户的概览——排名上升、下降或稳定 |  
| `prioritize:today` | 当前需要处理的紧急任务和容易提升排名的项目 |  
| `quick-wins:find` | 排名在 11-20 位的关键词——有机会登上首页 |  
| `quick-wins:find --business "name"` | 为特定客户寻找容易提升排名的关键词 |  
| `at-risk:clients` | 可能流失的客户——排名下降或参与度低 |  

### GMB 审计  
| 命令 | 描述 |  
| `audit:run --url "google.com/maps/..."` | 运行 GMB 审计（需 500 信用点数） |  
| `audit:get <audit_id>` | 获取审计结果——评分、问题和建议 |  

### 工具  
| 命令 | 描述 |  
| `recommendations:get --business "name"` | 为客户提供提升排名的建议 |  
| `email:draft --business "name"` | 为客户生成每月更新邮件 |  

---

## 示例  

### 检查客户资料的健康状况  
```bash
./scripts/localrank.js portfolio:summary
```  
返回结果：  
```json
{
  "total_clients": 15,
  "improving": 8,
  "declining": 2,
  "stable": 5,
  "avg_rank_across_portfolio": 7.3,
  "clients": [...]
}
```  

### 获取客户报告  
```bash
./scripts/localrank.js client:report --business "Acme Plumbing"
```  
返回结果：  
```json
{
  "business_name": "Acme Plumbing",
  "latest_scan": {
    "date": "2026-01-28",
    "avg_rank": 4.2,
    "keywords": [...]
  },
  "wins": [
    {"keyword": "plumber near me", "from": 8.5, "to": 3.2, "improved_by": 5.3}
  ],
  "drops": [],
  "view_url": "https://app.localrank.so/share/abc123"
}
```  

### 寻找容易提升排名的关键词  
```bash
./scripts/localrank.js quick-wins:find
```  
返回所有客户中排名在 11-20 位的关键词——这些关键词接近首页，易于提升排名。  

### 运行 GMB 审计  
```bash
./scripts/localrank.js audit:run --url "https://google.com/maps/place/..."
# Wait for completion
./scripts/localrank.js audit:get <audit_id>
```  
___  

### 起草客户更新邮件  
```bash
./scripts/localrank.js email:draft --business "Acme Plumbing"
```  
生成包含排名、优化结果和可视化地图链接的每月更新邮件。  

---

## 理解数据  

### 排名指标  
- **avg_rank：** 在地理网格中的平均排名（排名越低越好）  
- **best_rank：** 在任何网格点中找到的最佳排名  
- 排名在 1-3 位的属于“Local Pack”（在 Google 地图上可见）  
- 排名在 4-10 位的属于“页面 1”范围  
- 排名在 11-20 位的属于“容易提升排名的关键词”  

### 可视化地图  
大多数响应会包含一个 `view_url`，例如 `https://app.localrank.so/share/abc123`  
- 可与客户分享该链接，展示企业的排名情况  
- 网格显示了企业在不同地区的排名位置  

### 状态指示  
- **improving：** 自上次扫描以来排名有所提升  
- **declining：** 排名下降（需要关注）  
- **stable：** 排名保持不变  
- **new：** 仅进行过一次扫描，暂无对比数据  

---

## 推荐的产品  

当 `recommendations:get` 提出优化建议时：  
| 产品 | 使用场景 | 功能 |  
|---------|-------------|--------------|  
| **SuperBoost** | 平均排名 > 10 | 通过人工智能优化排名，提供高级引用 |  
| **LocalBoost** | 平均排名 5-10 | 建立 50 多个引用以提升本地权威性 |  
| **ContentBoost** | 平均排名 > 7 | 生成与业务相关的本地内容以提高权威性 |  
| **Review Booster** | 适用于所有客户 | 自动收集更多 Google 评价 |  
| **Rank Tracker** | 关键词排名 < 5 位 | 追踪更多关键词以评估效果 |  

---

## 提示  
- **提供可视化证据：** 向客户展示排名时务必包含 `view_url`  
- **优先处理容易提升排名的关键词**：排名在 11-15 位的关键词最容易登上首页  
- **提案前进行审计：** 对潜在客户运行 `audit:run` 以发现潜在问题  
- **主动沟通：** 使用 `at-risk:clients` 功能及早发现可能流失的客户  
- **批量操作：** 使用 `portfolio:summary` 定期查看所有客户的排名情况  

---

## 帮助支持  

如有疑问，请发送邮件至 support@localrank.so