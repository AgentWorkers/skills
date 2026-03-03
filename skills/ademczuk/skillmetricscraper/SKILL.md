---
name: skills-weekly
description: "**OpenClaw 技能周刊**  
——追踪 ClawHub 上的热门技能，并生成符合 GitHubAwesome 样式的 YouTube 视频脚本，这些脚本会展示技能的排名情况（分为“Movers”和“Rockets”两个类别）。"
emoji: "\U0001F4CA"
user-invocable: true
metadata:
  openclaw:
    version: "1.2.0"
    requires:
      bins: ["python3"]
      env: ["ANTHROPIC_API_KEY"]
    triggers:
      - "skills weekly"
      - "trending skills"
      - "clawhub trending"
      - "skill metrics"
      - "weekly report"
      - "skill snapshot"
      - "openclaw skills"
      - "generate report"
      - "video script"
---
# OpenClaw技能周刊

这是一个自动化流程，用于跟踪ClawHub上的热门技能，并生成适合在YouTube上发布的视频脚本（采用GitHubAwesome格式）。

## 该技能的功能

1. **ClawHub API数据抓取**：通过`GET https://clawhub.ai/api/v1/skills`接口获取约13,000项技能信息（支持分页查询），无需认证。
2. **SQLite时间序列数据存储**：将每日安装量、下载量和评分等指标记录到SQLite数据库中，以生成7天的数据变化趋势。
3. **双轨排名系统**：区分“Movers”（已存在的技能，至少30天以上）和“Rockets”（新发布的技能，发布时间小于30天），并根据安装速度进行排名。同时设置作者多样性限制，防止某个作者占据主导地位。
4. **内容采集**：从ClawHub的详细API中获取排名靠前技能的文档和作者信息。
5. **YouTube视频脚本生成**：使用Claude Haiku模型生成符合GitHubAwesome格式的视频脚本，包括技能介绍、技术规格等内容，但不包含任何流行度数据。
6. **双输出格式**：生成Markdown格式的报告文件（`.md`）和适合朗读的视频脚本文件（`.txt`）。

## 命令参数

根据用户输入的命令，执行不同的流程：

| 用户输入 | 执行模式 | 功能 |
|---|---|---|
| `weekly report` 或 `full report` 或 `generate report` | 完整流程 | 数据抓取 → 数据存储 → 排名 → 内容采集 → 脚本生成 → 输出 |
| `snapshot` 或 `daily snapshot` | 仅生成数据快照 | 将ClawHub指标记录到数据库 |
| `trending` 或 `what's trending` | 快速显示热门技能 | 从数据库中显示排名前10的技能 |
| `status` 或 `db status` | 显示系统状态和数据快照历史 |
| `video script` 或 `generate script` | 仅生成视频脚本 | 重新生成上次快照中的脚本 |

## 完整流程（每周报告）

如果尚未安装依赖项，请先执行以下命令：

```bash
cd "${SKILL_ROOT}" && pip install -r requirements.txt --quiet 2>/dev/null || pip3 install -r requirements.txt --quiet
```

然后运行完整流程：

```bash
cd "${SKILL_ROOT}" && python3 run_weekly.py --top 10 --episode ${EPISODE_NUM:-1}
```

将`${EPISODE_NUM}`替换为用户指定的剧集编号，默认值为1。

如果用户希望跳过某些功能（例如X/Twitter数据采集），可以添加`--skip-x`参数：

```bash
cd "${SKILL_ROOT}" && python3 run_weekly.py --top 10 --skip-x --episode ${EPISODE_NUM:-1}
```

**输出结果**：

- `openclaw_weekly_YYYYMMDD.md`：包含指标、排名和脚本的Markdown报告文件。
- `openclaw_weekly_YYYYMMDD_script.txt`：符合GitHubAwesome格式的音频脚本文件。

完成后，将这两个文件的路径告知用户。

**预期输出示例**：

```plaintext
============================================================
  OpenClaw技能周刊 — 完整流程（v4）
  2026年3月1日
============================================================
  第一阶段：多源数据采集（X、Reddit、Hacker News）
  [1/5] 正在抓取ClawHub技能数据...
  [2/5] 保存数据快照...
  [3/5] 根据7天内的安装速度进行排名...
  [4/5] 采集内容中...
  [5/5] 生成YouTube视频脚本中...
  完成：
    报告文件：openclaw_weekly_20260301.md
    视频脚本文件：openclaw_weekly_20260301_script.txt
```

## 仅生成数据快照（每日自动执行）

如果用户仅需要每日数据快照，可以执行以下命令：

```bash
cd "${SKILL_ROOT}" && python3 run_weekly.py --snapshot-only --skip-x
```

随后向用户说明捕获了多少技能以及数据库中存储了多少个快照。

## 快速显示热门技能

无需重新获取数据，即可快速显示当前数据库中的热门技能：

```bash
cd "${SKILL_ROOT}" && python3 main.py --list-db
```

## 系统状态查询

执行以下命令可查看系统状态：

```bash
cd "${SKILL_ROOT}" && python3 main.py --list-db
```

输出内容包括：数据库路径、快照总数、不同日期的数据记录以及当前安装量最高的技能列表。

## 命令行选项说明

| 选项 | 默认值 | 说明 |
|---|---|---|
| `--top N` | 10 | 显示排名前N的技能 |
| `--days N` | 7 | 计算速度趋势的日期范围 |
| `--episode N` | 1 | 视频脚本对应的剧集编号 |
| `--skip-x` | false | 不捕获X/Twitter数据 |
| `--snapshot-only` | false | 仅生成数据快照，不生成脚本 |
| `--max-pages N` | 0 | 限制API请求的页面数（用于测试） |
| `--model MODEL` | claude-haiku-4-5-20251001 | 用于生成脚本的Anthropic模型 |
| `--output FILE` | auto-dated | 自动指定输出文件路径 |
| `--mock` | false | 使用合成数据进行离线开发 |

## 环境变量设置

| 变量 | 是否必填 | 说明 |
|---|---|---|
| `ANTHROPIC_API_KEY` | 是 | 用于通过Claude模型生成视频脚本 |
| `GITHUB_TOKEN` | 否 | 用于从GitHub获取源代码的README文件 |
| `XAI_API_KEY` | 否 | 用于通过xAI捕获X/Twitter数据 |
| `CLAWHUB_BASE_URL` | 否 | 可自定义ClawHub的API地址（默认：https://clawhub.ai） |

## 视频脚本格式

生成的脚本遵循GitHubAwesome的“GitHub Trending Weekly”格式：

- 开场白：“欢迎收看OpenClaw技能周刊，本期为第N期……”
- 每项技能的展示时间约为20秒，包括技能介绍和技术规格。
- 旁白中不包含任何流行度数据（如下载量、安装量或评分）。
- 采用简洁、客观的播报风格，避免使用夸张的表述。
- 每期内容以最后一个技能展示结束。

## 系统架构

系统由多个模块组成，共同完成上述功能：

- `run_weekly.py`：负责整个流程的协调。
- `main.py`：提供命令行接口（`--list-db`选项可用）。
- `discovery.py`：负责从ClawHub API获取技能数据。
- `storage.py`：使用SQLite数据库存储数据。
- `ranker.py`：实现双轨排名系统。
- `harvester.py`：从ClawHub详细API中提取内容及作者信息。
- `script_generator.py`：生成视频脚本。
- `community_signals.py`：负责加载和展示多源数据。
- `x_capture.py`：整合X/Twitter数据源。
- `reddit_capture.py`：捕获Reddit和Hacker News上的相关数据。
- `hourly_heartbeat.py`：每小时生成最新的技能快照和项目元数据。
- `project_tracker.py`：跟踪OpenClaw在GitHub上的仓库信息。
- `data/metrics.db`：存储所有处理后的数据。