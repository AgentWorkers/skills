---
name: arxiv-watcher
description: Monitor new papers on arXiv by category. Use when user wants to check latest papers, track research topics, or manage reading lists. Trigger phrases: "check arxiv", "new papers", "arxiv category", "watch arxiv", "latest papers on".
---

# ArXiv Watcher

这是一个用于监控和追踪 arXiv.org 上新论文的工具，支持按类别进行筛选。

## 概述

该工具可帮助您：
- 从指定的 arXiv 类别中获取最新论文
- 生成格式化的 Markdown 摘要
- 将论文标记为星标（starred），以便日后阅读

## 快速入门

```bash
# 查看某个类别的最新论文
/arxiv-watcher cs.AI

# 多个类别
/arxiv-watcher cs.AI cs.CL cs.LG

# 查看被标记为星标的论文
/arxiv-watcher --starred
```

## 可用类别

### 计算机科学 (cs.*)
| 类别 | 描述 |
|----------|-------------|
| cs.AI | 人工智能 |
| cs.CL | 计算与语言 |
| cs.CV | 计算机视觉 |
| cs.LG | 机器学习 |
| cs.NE | 神经与进化计算 |
| cs.RO | 机器人技术 |
| cs.SE | 软件工程 |

### 物理学 (physics.*)
| 类别 | 描述 |
|----------|-------------|
| astro-ph | 天体物理学 |
| cond-mat | 凝聚态物理 |
| hep-ex | 高能物理（实验） |
| hep-th | 高能物理（理论） |
| quant-ph | 量子物理 |

### 数学 (math.*)
| 类别 | 描述 |
|----------|-------------|
| math.AG | 代数几何 |
| math.CO | 组合数学 |
| math.DG | 微分几何 |
| math.NT | 数论 |
| math.ST | 统计理论 |

### 统计学 (stat.*)
| 类别 | 描述 |
|----------|-------------|
| stat.ML | 机器学习 |
| stat.TH | 统计理论 |

完整类别列表：https://arxiv.org/categorytaxonomy

## 命令

### 获取最新论文

```bash
python scripts/arxiv_watcher.py fetch <category> [--limit N]
```

从 arXiv 获取最新论文，并以 Markdown 格式输出：
- 论文标题和 arXiv ID
- 作者
- 摘要预览（前 200 个字符）
- 论文全文链接

### 将论文标记为星标

```bash
python scripts/arxiv_watcher.py star <arxiv_id>
```

将论文添加到星标列表中。

### 取消标记论文

```bash
python scripts/arxiv_watcher.py unstar <arxiv_id>
```

从星标列表中移除论文。

### 查看被标记为星标的论文

```bash
python scripts/arxiv_watcher.py starred
```

列出所有被标记为星标的论文及其详细信息。

## 输出格式

论文以 Markdown 格式显示：

```markdown
## [2403.12345] 论文标题
**作者:** John Doe, Jane Smith
**类别:** cs.AI
**提交时间:** 2024-03-15

**摘要:**
本文提出了一种新的...方法...

**链接:**
- arXiv: https://arxiv.org/abs/2403.12345
- PDF: https://arxiv.org/pdf/2403.12345.pdf

---
```

被标记为星标的论文会显示一个 ⭐ 标记，便于识别。

## 工作流程

当用户请求查看 arXiv 论文时：
1. **确定类别** - 解析用户请求的类别名称
2. **获取论文** - 运行 `arxiv_watcher.py fetch <category>`
3. **格式化输出** - 以易读的 Markdown 格式展示论文
4. **提供操作选项** - 提问用户是否需要将某些论文标记为星标

### 示例交互

**用户:** “查看 cs.AI 类别的新论文”

**助手:** 运行 fetch 命令，显示 5-10 篇最新论文，并询问用户是否需要将其中某篇标记为星标。

**用户:** “将第二篇论文标记为星标”

**助手:** 从输出中提取 arxiv_id，执行 star 命令，并确认操作。

**用户:** “显示我标记的论文”

**助手:** 运行 starred 命令，显示带有详细信息的论文列表。

## 资源

### scripts/
- `arxiv_watcher.py`：用于获取和管理论文的主要命令行工具

### assets/
- `starred.json`：存储被标记为星标的论文的文件（自动创建）