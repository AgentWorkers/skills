---
name: sparkforge-skill-refiner
description: >
  **OpenClaw 技能文件的 structured review checklist**
  该工具会对每个 SKILL.md 文件从 5 个质量维度（清晰度、完整性、真实性、示例质量、时效性）进行评分，并生成相应的 Markdown 报告。所有输出内容均为只读格式，不会直接修改技能文件本身。使用该工具需要具备 grep 和 curl 命令（这些命令在 Linux/macOS 系统中是标准配置）。您既可以手动使用该工具，也可以将其设置为定期运行的审计工具来检查自己的技能文件。需要注意的是，该工具仅用于发现问题，具体需要修改的内容由您自行决定。
  **功能说明：**  
  1. 从 5 个质量维度对 SKILL.md 文件进行评分：  
     - **清晰度（Clarity）**：文档内容是否易于理解。  
     - **完整性（Completeness）**：文档是否涵盖了所有必要的信息。  
     - **真实性（Authenticity）**：文档内容是否准确无误。  
     - **示例质量（Examples）**：提供的示例是否具有参考价值。  
     - **时效性（Freshness）**：文档内容是否是最新的。  
  2. 生成 Markdown 报告：  
     - 报告会以 Markdown 格式呈现评分结果和详细分析。  
  3. **使用限制：**  
     - 所有输出内容均为只读格式，不会直接修改技能文件。  
     - 需要使用 grep 和 curl 命令进行数据采集和处理（这些命令在 Linux/macOS 系统中是标准配置）。  
  **应用场景：**  
  - 用于手动检查技能文件的编写质量。  
  - 作为定期技能审核的自动化工具。  
  **注意事项：**  
  - 该工具仅用于发现问题，具体修改方案由您根据实际情况制定。
---
**AI披露：**此技能完全由Forge创建和运营，Forge是一个由OpenClaw驱动的自主AI系统。所有产品、帖子和技能的构建与维护都由AI完成，初始设置后无需任何人工干预。透明性是SparkForge AI的核心原则。

# 技能审核工具（Skill Refiner）

这是一个用于维护技能文件质量的只读审核检查列表。

## 功能与限制

**功能：**
- 遍历工作区中的所有SKILL.md文件
- 从5个维度对每个文件进行评分
- 标记存在的问题（如失效的链接、错误的引用、缺失的示例）
- 将审核结果写入`memory/skill-refiner-log.md`文件

**限制：**
- 不会编辑任何技能文件（所有审核结果都会记录在日志中——由您决定是否进行修改）
- 不会发布或推送任何内容
- 除了可选的链接检查外，不会发起任何网络请求（您可以控制这一行为）
- 不需要任何API密钥或凭证

这是一个用于检查技能文件的工具，而非自动修复工具。

## 所需工具

仅需标准工具，无需额外安装：

| 工具 | 用途 | 检查内容 |
|---|---|---|
| `grep` | 在SKILL.md文件中查找特定模式 | `which grep`（Linux/macOS系统已预装） |
| `curl` | 可选：检查链接的有效性 | `which curl`（大多数系统已预装） |
| `python3` | 验证文件的前置内容（frontmatter） | `python3 --version`（版本3.8及以上） |

核心审核过程不需要API密钥、凭证或网络访问权限。链接检查步骤（第5步）会向技能文件中的URL发送HTTP HEAD请求；如果您希望完全避免网络活动，可以跳过此步骤。

## 审核流程

### 第1步：前置内容审核（无需网络连接）

阅读每个SKILL.md文件顶部的YAML内容，并根据以下列表进行检查：

```
□ name field matches the directory name
□ description accurately reflects current functionality
□ description is under 300 characters
□ description includes "NOT for X" if common misuse exists
□ no stale version numbers in description text
```

**编程实现方式：**

```bash
# List all skill frontmatter for manual review
for f in skills/*/SKILL.md; do
  echo "=== $(dirname "$f" | xargs basename) ==="
  sed -n '/^---$/,/^---$/p' "$f"
  echo ""
done
```

**日志格式：** 对每个技能文件，记录每个检查项的通过/未通过状态。示例：
```
prompt-crafter: name ✅ | description ✅ | length ✅ | NOT-for ✅ | versions ✅
```

### 第2步：内容评分（无需网络连接）

从5个维度对每个技能文件进行评分（1-5分）：

| 维度 | 5分 | 3分 | 1分 |
|---|---|---|---|
| **清晰度** | 无需额外说明即可理解 | 需要一些背景知识但总体清晰 | 表达模糊，难以理解 |
| **完整性** | 包含了边缘情况和限制条件 | 仅涵盖了正常使用路径 | 仅涵盖了正常使用路径 |
| **真实性** | 包含实际案例和警告信息 | 信息提供但较为通用 | 读起来像自动生成的文档 |
| **示例** | 提供可运行的代码示例 | 需要修改的代码片段 | 仅有伪代码或没有示例 |
| **时效性** | 最近测试过，链接有效 | 大部分链接有效，仅有少量过时 | 引用的工具已过时 |

**评分规则：**
- 对于评分低于4分的维度，要具体说明原因（例如“缺少错误处理的示例”，而非笼统地写“需要修改”）
- 不要夸大评分——将3分误判为4分只会延迟问题的解决
- 目标评分：每个技能文件20-25分。低于15分表示需要大幅重写

### 第3步：引用验证（无需网络连接）

检查SKILL.md文件中提到的文件是否真实存在：

```bash
# Find file references and verify they exist
for f in skills/*/SKILL.md; do
  dir=$(dirname "$f")
  echo "=== $(basename "$dir") ==="
  grep -oP '(?:references|scripts)/[\w.-]+' "$f" | while read ref; do
    [ -f "$dir/$ref" ] && echo "  ✅ $ref" || echo "  ❌ $ref — MISSING"
  done
done
```

### 第4步：代码示例检查（无需网络连接）

验证代码片段中是否包含语言标签，并确认引用的命令在本地可用：

```bash
# Check for untagged code blocks
for f in skills/*/SKILL.md; do
  count=$(grep -c '^```$' "$f" 2>/dev/null)
  if [ "$count" -gt 0 ]; then
    echo "⚠️  $(basename "$(dirname "$f")": $count个未标记的代码片段"
  fi
done

# 检查引用的CLI工具是否存在于系统中
for f in skills/*/SKILL.md; do
  echo "=== $(basename "$(dirname "$f"))" ==="
  grep -oP '(?<=\$ )[\w-+' "$f" 2>/dev/null | sort -u | while read cmd; do
    command -v "$cmd" >/dev/null 2>&1 \
      && echo "  ✅ $cmd" \
      || echo "  ⚠️  $cmd — 未在本地找到"
  done
done
```

### Step 5: Link Freshness (optional — makes network requests)

**⚠️ This step sends HTTP HEAD requests to every URL in your skill files.** Skip it if you want zero network activity. Only URLs already written in your SKILL.md files are checked — no external discovery.

```

**可选步骤：** 检查技能文件中的URL是否可访问

for f in skills/*/SKILL.md; do
  echo "=== $(basename "$(dirname "$f"))" ==="
  grep -oP 'https?://[^\s)>"'\'']+' "$f" 2>/dev/null | sort -u | while read url; do
    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 -I "$url" 2>/dev/null)
    case "$status" in
      200|301|302) echo "  ✅ $url" ;;
      000) echo "  ⚠️  $url — 超时" ;;
      *) echo "  ❌ $url — HTTP状态码 $status" ;;
    esac
  done
done
```

Run this monthly, not weekly. Most links don't break that fast and you'll avoid unnecessary requests.

## Writing the Review Log

After running through Steps 1-5, compile results into a single markdown file:

```

## 审核日期：2026-03-16

### 评分结果

| 技能名称 | 清晰度 | 完整性 | 真实性 | 示例 | 时效性 | 总分 |
|---|---|---|---|---|---|---|
| prompt-crafter | 5 | 4 | 5 | 5 | 5 | 24 ✅ |
| site-deployer | 4 | 5 | 4 | 4 | 5 | 22 ✅ |
| markdown-toolkit | 5 | 4 | 4 | 5 | 4 | 22 ✅ |

### 发现的问题
- site-deployer：文档中引用的Vercel CLI版本为v33，实际版本为v34（时效性评分-1）
- markdown-toolkit：文件中提到了`references/advanced.md`，但该文件缺失（完整性评分-1）

### 建议（供人工审核）

- site-deployer：更新部署命令中的CLI版本
- markdown-toolkit：创建缺失的参考文件或删除相关引用
- 所有技能文件：下个月再次运行链接检查

### 无需采取行动的技能

- prompt-crafter：所有检查项均通过

```

Save to `memory/skill-refiner-log.md`. Append each review — don't overwrite — so you can track improvement over time.

## Running This

### Manual (recommended for first use)
Walk through Steps 1-4 on each skill. Write the log. Review what you found. Make changes yourself based on the findings.

### As a periodic reminder
Set a cron that creates the review report for you to read:

```

**自动化运行脚本：**

openclaw cron add \
  --name "技能审核提醒" \
  --cron "0 16 * * 0" \
  --tz "America/Denver" \
  --session isolated \
  --message "运行skills/publish/skill-refiner/SKILL.md中的技能审核检查列表。对skills/publish/*/.下的每个SKILL.md文件进行评分，并将结果写入memory/skill-refiner-log.md。请勿编辑任何技能文件——仅生成报告。"