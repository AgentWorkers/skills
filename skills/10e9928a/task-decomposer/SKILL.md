---
name: task-decomposer
description: 该技能可以将复杂的用户请求分解为可执行的子任务，识别所需的技能，然后在 skills.sh 中查找现有的技能；如果找不到合适的解决方案，则会创建新的技能。当用户提交一个复杂的多步骤请求、希望自动化工作流程，或者需要帮助将大型任务分解为可管理的部分时，应使用该技能。
---

# 任务分解器与技能生成器

该技能能够帮助将复杂的用户请求分解为可执行的子任务，识别每个任务所需的能力，从开放的技能生态系统中搜索现有的技能，并在无法找到现有解决方案时自动创建新技能。

## 核心工作流程

```
User Request → Task Decomposition → Capability Identification → Skill Search → Gap Analysis → Skill Creation → Execution Plan
```

## 第1阶段：任务分析与分解

收到用户请求后，请按照以下步骤操作：

### 第1步：理解用户意图

分析请求以确定：
- **核心目标**：最终目标是什么？
- **涉及的领域**：需要哪些专业技能？
- **触发机制**：是一次性操作、定期任务还是事件驱动？

**示例分析：**
```
User Input: "Help me get email summaries every morning and send them to Slack"

Analysis:
- Core objective: Automated email digest delivery to Slack
- Domains: Email access, content summarization, messaging
- Trigger: Scheduled (daily morning)
```

### 第2步：分解为原子任务

将复杂任务分解为最小的可执行单元：

```yaml
Task Decomposition:
  - task_id: 1
    name: "Access and retrieve email list"
    type: "data_retrieval"
    input: "Email credentials/session"
    output: "List of emails with metadata"
    dependencies: []
    
  - task_id: 2
    name: "Extract key information from emails"
    type: "data_extraction"
    input: "Email list"
    output: "Structured email data"
    dependencies: [1]
    
  - task_id: 3
    name: "Generate email summary"
    type: "content_generation"
    input: "Structured email data"
    output: "Formatted summary text"
    dependencies: [2]
    
  - task_id: 4
    name: "Send message to Slack"
    type: "message_delivery"
    input: "Summary text, Slack webhook/token"
    output: "Delivery confirmation"
    dependencies: [3]
    
  - task_id: 5
    name: "Configure scheduled execution"
    type: "scheduling"
    input: "Workflow script, schedule config"
    output: "Active scheduled job"
    dependencies: [4]
```

## 第2阶段：能力识别

将每个子任务映射到通用能力分类法中的相应能力类型。

### 通用能力类型

| 能力 | 描述 | 搜索关键词 |
|------------|-------------|-----------------|
| `browser_automation` | 网页导航、交互、数据抓取 | browser, selenium, puppeteer, playwright, scrape |
| `web_search` | 网页搜索和信息检索 | search, google, bing, duckduckgo |
| `api_integration` | 与第三方API进行通信 | api, rest, graphql, webhook, {service-name} |
| `data_extraction` | 解析和提取结构化数据 | parse, extract, scrape, ocr, pdf |
| `data_transformation` | 转换、清洗、处理数据 | transform, convert, format, clean, etl |
| `content_generation` | 创建文本、图像或其他内容 | generate, write, create, summarize, translate |
| `file_operations` | 读写、操作文件 | file, read, write, csv, excel, json, pdf |
| `message_delivery` | 发送通知或消息 | notify, send, email, slack, discord, telegram |
| `scheduling` | 基于时间的任务执行 | schedule, cron, timer, daily, weekly |
| `authentication` | 身份和访问管理 | auth, oauth, login, token, credentials |
| `database_operations` | 数据库CRUD操作 | database, sql, mongodb, query, store |
| `code_execution` | 运行脚本或程序 | execute, run, script, shell, python |
| `version_control` | Git和代码仓库操作 | git, github, gitlab, commit, pr, review |
| `testing` | 自动化测试和质量保证 | test, jest, pytest, e2e, unit |
| `deployment` | 应用程序部署和持续集成/持续交付 | deploy, docker, kubernetes, ci-cd, release |
| `monitoring` | 系统和应用程序监控 | monitor, alert, log, metrics, health |

### 能力识别过程

对于每个子任务：
1. 分析任务描述和要求
2. 与一个或多个能力类型匹配
3. 生成用于搜索技能的关键词

**示例：**
```yaml
Task: "Send message to Slack"
Capability: message_delivery
Search Keywords: ["slack", "notification", "message", "webhook"]
```

## 第3阶段：技能搜索

使用Skills CLI在 https://skills.sh/ 上搜索现有的技能。

### 搜索过程

对于每个能力需求，使用相关的关键词进行搜索：

```bash
# Search for skills matching the capability
npx skills find <keyword>

# Examples:
npx skills find slack notification
npx skills find browser automation
npx skills find pdf extract
npx skills find github api
```

### 评估搜索结果

当返回结果时：
```
Install with npx skills add <owner/repo@skill>

owner/repo@skill-name
└ https://skills.sh/owner/repo/skill-name
```

评估每个结果：
- **相关性**：它是否符合所需的能力？
- **完整性**：它是否涵盖了所有需要的功能？
- **质量**：它的文档是否完善且维护得当？

### 生成能力映射

```yaml
Capability Mapping:
  - task_id: 1
    capability: browser_automation
    search_query: "browser email automation"
    found_skills:
      - name: "anthropic/claude-skills@browser-use"
        url: "https://skills.sh/anthropic/claude-skills/browser-use"
        match_score: high
    recommendation: "Install browser-use skill"
    
  - task_id: 4
    capability: message_delivery
    search_query: "slack notification"
    found_skills: []
    recommendation: "Create new skill: slack-notification"
```

## 第4阶段：差距分析

识别没有匹配技能的任务：

### 内置能力（无需额外技能）

这些能力通常由代理的本地功能处理：
- `content_generation` - LLM的本地文本生成功能
- `data_transformation` - 通过代码进行的基本数据操作
- `code_execution` - 直接执行脚本
- `scheduling` - 系统级别的cron/scheduler配置

### 所需技能

对于没有内置支持的能力，需要确定：
1. **技能是否存在**：从skills.sh安装该技能
2. **技能未找到**：创建新技能

## 第5阶段：技能创建

当没有现有技能能够满足需求时，创建新技能。

### 技能创建过程

1. **定义范围**：确定技能的功能
2. **设计接口**：定义输入、输出和使用方式
3. **创建SKILL.md**：编写技能定义文件
4. **添加资源**：根据需要包含脚本、参考资料或资产

### 技能模板

```markdown
---
name: {skill-name}
description: {Clear description of what the skill does and when to use it. Written in third person.}
---

# {Skill Title}

{Brief introduction explaining the skill's purpose.}

## When to Use

{Describe scenarios when this skill should be triggered.}

## Prerequisites

{List any required installations, configurations, or credentials.}

## Usage

{Detailed usage instructions with examples.}

### Basic Usage

```bash
{基本命令或代码示例}
```

### Advanced Usage

{More complex examples and options.}

## Configuration

{Any configuration options or environment variables.}

## Examples

### Example 1: {Use Case}

{Step-by-step example with code.}

## Troubleshooting

{Common issues and solutions.}
```

### 初始化新技能

```bash
# Create skill using the skills CLI
npx skills init <skill-name>

# Or manually create the structure:
# skill-name/
# ├── SKILL.md (required)
# ├── scripts/ (optional)
# ├── references/ (optional)
# └── assets/ (optional)
```

## 第6阶段：生成执行计划

将所有信息编译成结构化的执行计划：

```yaml
Execution Plan:
  title: "{Task Description}"
  
  prerequisites:
    - "{Prerequisite 1}"
    - "{Prerequisite 2}"
  
  skills_to_install:
    - skill: "owner/repo@skill-name"
      command: "npx skills add owner/repo@skill-name -g -y"
      url: "https://skills.sh/owner/repo/skill-name"
  
  skills_to_create:
    - name: "{new-skill-name}"
      capability: "{capability_type}"
      description: "{What it does}"
  
  execution_steps:
    - step: 1
      task: "{Task name}"
      skill: "{skill-name | built-in}"
      action: "{Specific action to take}"
      
    - step: 2
      task: "{Task name}"
      skill: "{skill-name | built-in}"
      action: "{Specific action to take}"
  
  verification:
    - "{How to verify step 1 succeeded}"
    - "{How to verify step 2 succeeded}"
```

## 任务分解原则

### 原则1：原子性
每个子任务都应该是具有明确输入和输出的最小可执行单元。

### 原则2：独立性
尽可能减少任务之间的依赖关系，以便并行执行。

### 原则3：可验证性
每个任务都应该有明确的方法来验证其是否成功完成。

### 原则4：可重用性
识别可重用的模式，并优先创建通用技能。

### 原则5：单一职责
每个任务应该专注完成一项任务。

## 输出格式

以结构化格式呈现分解结果：

```
════════════════════════════════════════════════════════════════
📋 TASK DECOMPOSITION REPORT
════════════════════════════════════════════════════════════════

🎯 Original Request:
{User's original request}

────────────────────────────────────────────────────────────────
📊 SUBTASKS
────────────────────────────────────────────────────────────────
┌─────┬────────────────────────┬───────────────────┬───────────┐
│ ID  │ Task                   │ Capability        │ Status    │
├─────┼────────────────────────┼───────────────────┼───────────┤
│ 1   │ {task name}            │ {capability}      │ Found     │
│ 2   │ {task name}            │ {capability}      │ Built-in  │
│ 3   │ {task name}            │ {capability}      │ Create    │
└─────┴────────────────────────┴───────────────────┴───────────┘

────────────────────────────────────────────────────────────────
🔍 SKILL SEARCH RESULTS
────────────────────────────────────────────────────────────────
Task 1: {task name}
  Search: npx skills find {keywords}
  Found: owner/repo@skill-name
  URL: https://skills.sh/owner/repo/skill-name
  
Task 3: {task name}
  Search: npx skills find {keywords}
  Found: No matching skills
  Action: Create new skill

────────────────────────────────────────────────────────────────
🛠️ SKILLS TO CREATE
────────────────────────────────────────────────────────────────
1. {skill-name}
   Capability: {capability_type}
   Description: {what it does}

────────────────────────────────────────────────────────────────
📝 EXECUTION PLAN
────────────────────────────────────────────────────────────────
Prerequisites:
  • {prerequisite 1}
  • {prerequisite 2}

Steps:
  1. {action} using {skill}
  2. {action} using {skill}
  3. {action} using {skill}

════════════════════════════════════════════════════════════════
```

## 示例

### 示例1：工作流自动化

**用户请求：**
```
Create a workflow that monitors GitHub issues, summarizes new issues, and posts notifications to Discord
```

**分解结果：**
```yaml
Subtasks:
  1. Monitor GitHub repository for new issues
     Capability: api_integration
     Search: "npx skills find github issues"
     
  2. Extract issue content and metadata
     Capability: data_extraction
     Status: Built-in (code)
     
  3. Generate issue summary
     Capability: content_generation
     Status: Built-in (LLM)
     
  4. Send notification to Discord
     Capability: message_delivery
     Search: "npx skills find discord notification"
     
  5. Configure webhook or polling trigger
     Capability: scheduling
     Status: Built-in (system)
```

### 示例2：数据管道

**用户请求：**
```
Search for AI research papers, download PDFs, extract key findings, and save to Notion
```

**分解结果：**
```yaml
Subtasks:
  1. Search for AI research papers
     Capability: web_search
     Search: "npx skills find academic search"
     
  2. Download PDF files
     Capability: browser_automation
     Search: "npx skills find browser download"
     
  3. Extract text from PDFs
     Capability: data_extraction
     Search: "npx skills find pdf extract"
     
  4. Generate summaries of key findings
     Capability: content_generation
     Status: Built-in (LLM)
     
  5. Save to Notion database
     Capability: api_integration
     Search: "npx skills find notion"
```

## 最佳实践

1. **先进行技能搜索**：在创建新技能之前，始终查看 https://skills.sh/
2. **使用具体的搜索词**：将能力关键词与领域术语结合使用
3. **利用内置能力**：避免为代理可以原生完成的功能创建额外技能
4. **创建可重用技能**：尽可能设计通用技能
5. **详细记录文档**：新技能应提供清晰的使用说明
6. **执行前进行验证**：在执行任务前确认技能已正确安装
7. **优雅地处理错误**：在执行计划中包含备用策略

## 与`find-skills`的集成

该技能与`find-skills`技能协同工作，用于发现现有的解决方案：

```bash
# Search the skills ecosystem
npx skills find <query>

# Install a discovered skill
npx skills add <owner/repo@skill> -g -y

# Browse all available skills
# Visit: https://skills.sh/
```

## 注意事项

- 在创建新技能之前，始终先搜索现有的技能
- 内置能力（如LLM、基本代码）不需要额外技能
- 创建技能前需要用户确认
- 复杂的工作流程可能需要多个技能协同工作