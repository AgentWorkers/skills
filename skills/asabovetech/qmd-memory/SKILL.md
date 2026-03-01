# QMD：OpenClaw 的内存优化技能  
## 本地混合搜索功能——每月可节省 50 至 300 美元的 API 使用费用  

**作者：** As Above Technologies  
**版本：** 1.0.0  
**ClawHub：** 即将推出  

---

## 💰 价值主张  

### 您目前支付的 API 使用费用  

| 操作        | API 费用    | 频率      | 每月费用    |  
|-------------|-----------|---------|-----------|  
| memory_search (embedding) | $0.02–0.05   | 50–200 次/天 | $30–300    |  
| Context retrieval | $0.01–0.03   | 100 次/天以上 | $30–90    |  
| Semantic queries | $0.03–0.08   | 20–50 次/天 | $18–120    |  
| **总计**       |           |          | **$78–510/月** |  

### 使用 QMD 本地搜索功能后  

| 操作        | 费用      | 原因       |  
|-------------|---------|-----------|         |  
| 所有搜索      | **$0**     | 在您的机器上运行   |  
| 嵌入式查询      | **$0**     | 使用本地 GGUF 模型 |  
| 重新排序      | **$0**     | 使用本地 LLM   |  
**每月节省费用：** $50–300+**  

**只需一次性设置，即可永久享受免费搜索服务。**  

---

## 🚀 快速入门  

```bash
# Install the skill
clawhub install asabove/qmd-memory

# Run setup (installs QMD, configures collections)
openclaw skill run qmd-memory setup

# That's it. Your memory is now supercharged.
```  

---

## 您将获得什么  

### 1. 自动化集合配置  

根据您的工作区结构，我们会为您创建优化的搜索集合：  

```
✓ workspace     — Core agent files (MEMORY.md, SOUL.md, etc.)
✓ daily-logs    — memory/*.md daily logs
✓ intelligence  — intelligence/*.md (if exists)
✓ projects      — projects/**/*.md (if exists)
✓ documents     — Any additional doc folders you specify
```  

### 2. 智能上下文描述  

我们为每个搜索集合添加上下文信息，以便 QMD 能够理解数据的来源和含义：  

```
qmd://workspace    → "Agent identity and configuration files"
qmd://daily-logs   → "Daily work logs and session history"
qmd://intelligence → "Analysis, research, and reference documents"
```  

### 3. 预配置的定时任务  

我们为您自动配置定时任务，以定期更新搜索数据：  

```bash
# Auto-update index (nightly at 3am)
0 3 * * * qmd update && qmd embed

# Keep your memory fresh without thinking about it
```  

### 4. 与 OpenClaw 的集成  

现在，OpenClaw 的内存搜索功能会自动使用 QMD：  
- `memory_search` → 通过 QMD 的混合搜索引擎执行查询  
- `memory_get` → 从 QMD 的搜索集合中获取结果  
- 查看结果时，会显示相应的集合上下文信息  

### 5. 多代理 MCP 服务器（可选）  

```bash
# Start shared memory server
openclaw skill run qmd-memory serve

# All your agents can now query collective memory
# Forge, Thoth, Axis — shared knowledge base
```  

---

## 📊 搜索模式  

| 模式        | 命令        | 适用场景    |  
|-------------|-----------|-----------|  
| **关键词搜索**   | `qmd search "查询内容"` | 精确匹配，快速响应 |  
| **语义搜索**   | `qmd vsearch "查询内容"` | 基于概念的相似性 |  
| **混合搜索**   | `qmd query "查询内容"` | 最佳搜索效果（推荐） |  

### 示例查询  

```bash
# Find exact mentions
qmd search "Charlene" -n 5

# Find conceptually related content
qmd vsearch "how should we handle customer complaints"

# Best quality — expansion + reranking
qmd query "what decisions did we make about pricing strategy"

# Search specific collection
qmd search "API keys" -c workspace
```  

---

## 🔧 配置选项  

### 添加自定义搜索集合  

您可以自定义搜索集合的内容和结构：  

```bash
openclaw skill run qmd-memory add-collection ~/Documents/research --name research
```  

### 添加上下文信息  

我们为您的搜索结果添加相关的上下文描述：  

```bash
openclaw skill run qmd-memory add-context qmd://research "Market research and competitive analysis"
```  

### 刷新索引  

我们定期更新索引数据，以确保搜索结果的准确性：  

```bash
openclaw skill run qmd-memory refresh
```  

---

## 💡 模板模板  

### 适用于不同工作场景的模板  

我们提供了多种模板，以满足不同工作场景的需求：  

---  
**交易/投资工作区模板**  
- `intelligence`：交易系统、仪表盘、交易信号  
- `market-data`：价格历史数据、市场分析  
- `research`：尽职调查报告  
- `daily-logs`：交易记录  

---  
**内容创作工作区模板**  
- `articles`：已发布的文章  
- `drafts`：未完成的草稿  
- `research`：研究资料  
- `ideas`：头脑风暴记录、灵感笔记  

---  
**开发者工作区模板**  
- `docs`：技术文档  
- `notes`：技术笔记  
- `decisions`：决策记录、架构方案  
- `snippets`：代码片段、示例代码  

---

## 📈 节费计算器  

运行此工具，即可估算您的节省费用：  

```bash
openclaw skill run qmd-memory calculate-savings
```  

**节省费用：**  
```
Your Current API Memory Costs (estimated):
  memory_search calls/day:     ~75
  Average cost per call:       $0.03
  Monthly API cost:            $67.50

With QMD Local:
  Monthly cost:                $0.00

YOUR MONTHLY SAVINGS:          $67.50
YOUR ANNUAL SAVINGS:           $810.00

ROI on skill purchase:         40x (if skill was $20)
```  

---

## 🛠️ 技术细节  

### 使用的模型（会自动下载）  

| 模型        | 用途        | 大小（MB）    |  
|-------------|-----------|-----------|  
| embeddinggemma-300M-Q8_0 | 向量嵌入模型 | 约 300MB   |  
| qwen3-reranker-0.6b-q8_0 | 重新排序引擎 | 约 640MB   |  
| qmd-query-expansion-1.7B-q4_k_m | 查询扩展模块 | 约 1.1GB   |  
**总计：** 约 2GB（一次性下载量）  

### 系统要求**  
- Node.js 版本 >= 22  
- 硬盘空间：约 3GB（用于存储模型和索引）  
- 内存需求：嵌入操作时需约 2GB RAM，之后使用量较低  

### 数据存储位置  

数据会存储在您的本地服务器上，确保数据安全。  

---  

## 🤝 技术支持  

**如有疑问？**  
- GitHub 问题反馈：[github.com/asabove/qmd-memory-skill]  
- Discord 社区：[As Above Technologies 社区]  
- 电子邮件：[support@asabove.tech]  

**觉得这个工具有用吗？**  
- 请在 ClawHub 上给我们点赞  
- 与其它 OpenClaw 用户分享该工具  
- 订阅我们的新闻通讯，获取更多优化建议  

---

## 📜 许可证  

**许可证：** MIT 许可——可自由使用，根据需要修改代码。  

QMD 本身由 Tobi Lütke 开发（[github.com/tobi/qmd]）。  
该工具可帮助您更轻松地集成 OpenClaw 的搜索功能。  

---

**“不要再为不必要的数据存储支付费用了。让知识为您创造价值吧。”**  
**As Above Technologies** — 专注于为人类提供高效的代理（agent）基础设施解决方案。