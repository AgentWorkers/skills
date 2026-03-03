---
name: last30days-weekly
description: "每周的 OpenClaw 技能情报更新：通过 API 捕获 ClawHub 上的热门技能信息，研究 Reddit、X 和 Web 社区中的相关讨论，并生成适合在 YouTube 上发布的简报。每日更新以积累数据，每周生成一份完整报告。"
emoji: "\U0001F4CA"
user-invocable: true
metadata: {"openclaw": {"version": "1.0.0", "requires": {"bins": ["python3", "curl"]}, "triggers": ["skills weekly", "trending skills", "clawhub", "skill metrics", "weekly report", "skill snapshot", "last30days weekly", "openclaw skills"]}}
---
# OpenClaw技能周刊 — 社区情报功能

这是一个自动化工具，用于跟踪OpenClaw/ClawHub上的热门技能以及社区讨论动态。

## 该功能的主要作用：

1. **ClawHub API数据抓取**：通过`GET https://clawhub.ai/api/v1/skills`接口获取所有技能信息，并使用分页机制进行数据抓取。将每日抓取的数据存储到SQLite数据库中，以便分析7天内的技能使用趋势。
2. **社区讨论监控**：在Reddit、X/Twitter等平台上搜索过去7天内关于OpenClaw技能的讨论内容，并将这些讨论内容分类存储到JSON文件中。
3. **热门技能分析**：计算技能的安装速度（当前安装量与过去7天的安装量之差），以识别出最受欢迎的技能。
4. **YouTube宣传脚本生成**：为最热门的技能生成简短的15秒宣传视频脚本。

## 命令说明：

根据用户输入的命令，执行相应的功能：

| 用户输入 | 功能模式 | 执行操作 |
|---|---|---|
| `snapshot` 或 `daily snapshot` | 获取当前数据快照 | 将ClawHub的指标数据记录到数据库中 |
| `report` 或 `weekly report` | 生成完整报告 | 包括技能快照、排名、社区讨论内容及宣传脚本 |
| `trending` 或 `what's trending` | 显示数据库中安装速度最快的前10个技能 |
| `community` 或 `community buzz` | 监控社区讨论动态 | 在Reddit/X/Twitter等平台上搜索相关讨论 |
| `status` 或 `db status` | 查看数据库状态及快照记录 |

### 快照模式（每日执行）

```bash
python3 "${SKILL_ROOT}/scripts/clawhub_snapshot.py" snapshot
```

该命令会从ClawHub API获取所有技能信息，并将数据记录到SQLite数据库中。建议每天执行一次，以构建完整的技能使用趋势数据。

**预期输出示例：**
```
[SNAPSHOT] 正在从https://clawhub.ai/api/v1/skills...获取数据...
[SNAPSHOT] 第1页：共100个技能...
[SNAPSHOT] 操作完成：共记录了13,729个技能（时间戳：2026-03-01T09:00:00）
[SNAPSHOT] 数据库中保存了5个快照日期，总记录行数为68,645行
```

**输出会告知用户捕获了多少个技能以及存在多少个快照记录。**

### 完整报告模式（每周执行一次）

```bash
python3 "${SKILL_ROOT}/scripts/clawhub_snapshot.py" report --top 10
```

该命令会生成包含技能排名和社区讨论内容的Markdown报告，并将结果输出到指定路径。

**示例报告内容：**
```
# OpenClaw技能周刊 — 2026年3月1日

| # | 技能名称 | 安装量 | 7天变化量 | 评分 |
|---|-------|----------|----------|-------|
| 1 | Gog   | 1,304    | +127     | 593   | 0.42  |
```

**系统会提示报告已生成，并建议用户同时执行社区讨论监控功能。**

### 社区讨论监控模式

使用OpenClaw内置的WebSearch工具来搜索最近的社区讨论：

1. 搜索：“openclaw skills”（在Reddit网站上，时间范围为过去7天）
2. 搜索：“clawhub trending skill”（时间范围为过去7天）
3. 搜索：“openclaw skill tutorial OR guide OR demo”（时间范围为过去7天）

对于每个搜索到的结果：
- 提取标题、URL和简短摘要
- 根据内容将其分类为“教程”、“安全”、“生态系统”、“展示”、“讨论”或“市场”等类别
- 将结果保存到`weekly_signals.json`文件中

```bash
python3 "${SKILL_ROOT}/scripts/clawhub_snapshot.py" community --save
```

### 状态查询模式

```bash
python3 "${SKILL_ROOT}/scripts/clawhub_snapshot.py" status
```

该命令会显示数据库路径、总记录行数、不同的快照日期以及当前安装量最高的10个技能。

### 配置说明：

该脚本仅使用Python 3的标准库（`sqlite3`、`urllib`、`json`）。无需安装额外的库（如`pip`）。

- 数据库路径：`/home/node/.local/share/skills-weekly/metrics.db`
- 社区讨论数据文件路径：`/home/node/.local/share/skills-weekly/weeklysignals.json`

### 自动化执行：

- **每日快照**：可以将该脚本添加到服务器的任务调度器或cron任务中，例如：
  ```bash
  # 每日上午9点执行每日快照任务
  docker exec -u node openclaw-gateway-secure python3 /home/node/.openclaw/workspace/skills/last30days-weekly/scripts/clawhub_snapshot.py snapshot
  ```
- **每周报告**：可以设置每周一上午9点执行完整报告任务：
  ```bash
  # 每周一上午9点生成每周报告
  docker exec -u node openclaw-gateway-secure python3 /home/node/.openclaw/workspace/skills/last30days-weekly/scripts/clawhub_snapshot.py report --top 10
  ```