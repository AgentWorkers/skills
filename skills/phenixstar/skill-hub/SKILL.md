---
name: skill-hub
description: "OpenClaw 的技能发现、安全审核及安装功能：  
- 从 ClawHub 注册表和 awesome-openclaw-skills 目录中搜索 3000 多个精选技能；  
- 评估技能的可信度，检测潜在的命令注入行为及恶意模式；  
- 管理技能的安装过程；  
- 定期在 GitHub 上查找新的技能更新。"
license: MIT
version: 1.0.0
homepage: https://github.com/PhenixStar/openclaw-skills-collection
user-invocable: true
disable-model-invocation: false
auto_activate:
  - "find skill"
  - "install skill"
  - "search skills"
  - "what skills exist"
  - "skill for"
  - "discover skill"
  - "vet skill"
  - "scan skill"
  - "skill security"
  - "new skills"
  - "skill updates"
  - "browse skills"
allowed-tools:
  - Bash
  - Read
  - Write
---

# 技能中心 (Skill Hub)

OpenClaw 提供统一的技能发现、安全审核及安装功能。

## 命令

### 搜索技能
可以通过关键词、类别或可信度评分来查找技能。

```bash
python3 scripts/skill-hub-search.py --query "spreadsheet"
python3 scripts/skill-hub-search.py --category "DevOps" --min-score 60
python3 scripts/skill-hub-search.py --query "auth" --live        # include live ClawHub results
python3 scripts/skill-hub-search.py --installed                  # show only installed
python3 scripts/skill-hub-search.py --not-installed --limit 20   # discovery mode
```

### 安装技能
找到所需技能后，可通过 ClawHub 进行安装：

```bash
npx clawhub@latest install <skill-slug>
```

### 审核技能（安全扫描）
扫描技能是否存在恶意代码、命令注入或逻辑漏洞。

```bash
python3 scripts/skill-hub-vet.py --slug google-sheets     # vet single skill
python3 scripts/skill-hub-vet.py --all-installed           # vet all installed
python3 scripts/skill-hub-vet.py --category "DevOps"       # vet category
python3 scripts/skill-hub-vet.py --top 10                  # vet top N unvetted
```

### 状态仪表盘
查看已安装的技能与目录中的技能覆盖情况，以及未经过审核的技能和相应的警告信息。

```bash
python3 scripts/skill-hub-status.py
```

### 快速检查（GitHub API）
快速检查自上次同步以来是否有新技能添加。使用 `gh` CLI 实现——无需完整下载数据。

```bash
python3 scripts/skill-hub-quick-check.py              # check for updates
python3 scripts/skill-hub-quick-check.py --sync        # auto-sync if updates found
python3 scripts/skill-hub-quick-check.py --query "ai"  # check + search new skills
```

### 浏览完整目录
将技能目录导出为格式化的表格（适用于终端或 Markdown），并按类别进行分组。

```bash
python3 scripts/skill-hub-table-export.py                          # terminal table
python3 scripts/skill-hub-table-export.py --format markdown        # markdown table
python3 scripts/skill-hub-table-export.py --category "AI"          # filter category
```

### 同步目录
从 GitHub 的 awesome-list 服务器重新获取所有技能信息。会保留审核结果，并显示更新内容。

```bash
python3 scripts/skill-hub-sync.py
```

## 可信度评分（0-100）

| 评分等级 | 评分范围 | 含义 |
|------|-------|---------|
| 可信赖 | 85-100 | 经过精心挑选和审核，功能成熟 |
| 良好 | 60-84 | 经过挑选或审核，但存在部分安全风险 |
| 未审核 | 30-59 | 仅存在于注册表中，尚未经过安全扫描 |
| 警告 | 0-29 | 存在安全风险或未通过审核 |

## 安全检查内容

- **代码层面**：包括代码执行、shell 注入、代码混淆、网络访问、环境信息收集以及破坏性操作等风险。
- **自然语言处理/命令层面**：包括隐藏指令、角色劫持、不可见的 Unicode 字符、数据泄露指令、权限提升以及社会工程学攻击等风险。

## 使用场景

- 当用户询问“如何找到某个技能”或“是否有适合某需求的技能”时。
- 当用户希望使用新工具来扩展系统功能时。
- 当用户想要确认已安装的技能是否安全时。
- 在从注册表中安装未知技能之前。