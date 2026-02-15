---
name: nova-act-usability
version: 1.0.2
description: **使用 Amazon Nova Act 进行的人工智能驱动的可用性测试**  
该工具通过生成虚拟用户角色（personas），执行测试以收集原始数据，解析用户反馈以判断测试目标是否达成，并生成 HTML 格式的测试报告。测试内容包括真实用户的工作流程（如预订、结账、发布等），同时具备必要的安全防护机制（safety guardrails）。适用于以下场景：  
- 测试网站可用性  
- 运行可用性测试  
- 生成可用性报告  
- 评估用户体验  
- 测试结账流程  
- 测试预订流程  
- 分析网站的用户界面（UX）。
metadata:
  openclaw:
    requires:
      config:
        - ~/.openclaw/config/nova-act.json
      bins:
        - python3
---

# Nova Act可用性测试 v1.0.2

**由AI编排的**可用性测试，使用基于Amazon Nova Act的数字孪生角色进行测试。

## ⚠️ 先决条件与凭据

**此技能需要一个Amazon Nova Act API密钥。**

| 需求 | 详情 |
|-------------|---------|
| **API密钥** | 来自[AWS控制台](https://console.aws.amazon.com/)的Nova Act API密钥 |
| **配置位置** | `~/.openclaw/config/nova-act.json` |
| **格式** | `{"apiKey": "your-nova-act-api-key-here"}` |
| **依赖项** | `pip3 install nova-act pydantic playwright` |
| **浏览器** | `playwright install chromium`（约300MB下载量） |

## 🔒 数据与隐私声明

**此技能访问的内容：**
- **读取：** `~/.openclaw/config/nova-act.json`（您的API密钥）
- **写入：** `./nova_act_logs/`（包含截图的跟踪文件），`./test_results_adaptive.json`，`./nova_act_usability_report.html`

**跟踪文件包含的内容：**
- 访问的每个页面的截图
- 页面的全部内容（HTML，文本）
- 浏览器操作和AI决策

**建议：**
- 仅在**非生产环境**或**测试环境**中运行测试
- 请注意，跟踪文件可能会捕获测试页面上可见的**个人身份信息（PII）或敏感数据**
- 如果跟踪文件包含敏感内容，请在使用后删除它们
- 对于不受信任的网站，考虑在**沙箱环境**（容器/虚拟机）中运行测试

---

## 特性

**代理驱动的解释**：脚本不再解释响应。您（代理）必须：
1. 运行测试脚本 → 收集原始数据
2. 读取JSON → 解释每个`raw_response`
3. 设置`goal_achieved`和`overall_success`
4. 生成报告

没有硬编码的正则表达式。不需要额外的API调用。执行工作的代理已经在运行中。

## 快速入门（针对AI代理）

**当用户请求测试一个网站时，您（AI代理）必须完成所有4个阶段：**

| 阶段 | 发生的事情 | 执行者 |
|-------|--------------|-------------|
| 1. 设置 | 生成角色，运行测试脚本 | 代理 + 脚本 |
| 2. 收集 | 脚本捕获原始的Nova Act响应 | 脚本 |
| 3. 解释 | 读取JSON，确定每个步骤的目标是否达成 | **代理** |
| 4. 生成 | 生成包含解释结果的HTML报告 | 代理 |

**⚠️ 脚本不解释响应或生成最终报告。您必须完成第3-4阶段。**

### 🎯 推荐：AI代理生成角色

**您已经是AI（Claude）了 - 使用您的智能来生成符合上下文的角色！**

```python
import subprocess
import os
import sys
import json
import tempfile

# Step 1: Check dependencies
try:
    import nova_act
    print("✅ Dependencies ready")
except ImportError:
    print("📦 Dependencies not installed. Please run:")
    print("   pip3 install nova-act pydantic playwright")
    print("   playwright install chromium")
    sys.exit(1)

# Step 2: Verify Nova Act API key
config_file = os.path.expanduser("~/.openclaw/config/nova-act.json")
with open(config_file, 'r') as f:
    config = json.load(f)
    if config.get('apiKey') == 'your-nova-act-api-key-here':
        print(f"⚠️  Please add your Nova Act API key to {config_file}")
        sys.exit(1)

# Step 3: YOU (the AI agent) generate personas
# Example for https://www.pgatour.com/ (golf tournament site)
website_url = "https://www.pgatour.com/"

personas = [
    {
        "name": "Marcus Chen",
        "archetype": "tournament_follower",
        "age": 42,
        "tech_proficiency": "high",
        "description": "Avid golf fan who follows multiple tours and tracks player stats",
        "goals": [
            "Check current tournament leaderboard",
            "View recent tournament results",
            "Track favorite player performance"
        ]
    },
    {
        "name": "Dorothy Williams",
        "archetype": "casual_viewer",
        "age": 68,
        "tech_proficiency": "low",
        "description": "Occasional golf viewer who watches major tournaments",
        "goals": [
            "Find when the next tournament is",
            "See who won recently",
            "Understand how to watch online"
        ]
    }
]

# Step 4: Save personas and run test
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(personas, f, indent=2)
    personas_file = f.name

skill_dir = os.path.expanduser("~/.openclaw/skills/nova-act-usability")
test_script = os.path.join(skill_dir, "scripts", "run_adaptive_test.py")

# Run with AI-generated personas
subprocess.run([sys.executable, test_script, website_url, personas_file])

# Clean up temp file
os.unlink(personas_file)
```

**角色模板：**
```json
{
  "name": "FirstName LastName",
  "archetype": "descriptive_identifier",
  "age": 30,
  "tech_proficiency": "low|medium|high",
  "description": "One sentence about who they are",
  "goals": [
    "First goal relevant to this website",
    "Second goal relevant to this website",
    "Third goal relevant to this website"
  ]
}
```

### 📝 替代方案：简单的自定义角色

如果用户指定了角色描述，请将其作为字符串传递：

```python
# User: "Test PGA Tour site as a golf enthusiast"
website_url = "https://www.pgatour.com/"
user_persona = "golf enthusiast who follows tournaments closely"

subprocess.run([sys.executable, test_script, website_url, user_persona])
# Script will parse this and create personas automatically
```

### ⚠️ 回退方案：自动生成（不推荐）

让脚本根据基本类别关键词猜测角色：

```python
# Generic, less contextual personas
subprocess.run([sys.executable, test_script, website_url])
```

### 为什么您应该生成角色

**✅ 优势：**
- **更好的上下文理解**：您拥有完整的对话历史和领域知识
- **更智能的推理**：您可以分析URL、行业和用户意图
- **避免重复的API调用**：您已经是Claude了 - 不需要再次调用自己！
- **根据用户偏好进行调整**：您可以根据用户声明的偏好进行适应
- **澄清问题**：您可以询问用户关于目标人群的信息

**❌ 应避免的做法：**
- 不要让Python脚本自己调用Claude API（浪费资源）
- 不要依赖通用的回退角色（准确性较低）
- 不要跳过角色生成（会影响测试质量）

### 💡 角色生成的技巧

**分析网站：**
- **URL域名**：`.gov` → 市民，`.edu` → 学生/教职员工
- **关键词**："shop" → 购物者，"book" → 旅行者，"play" → 游戏玩家
- **行业**：Golf → 粉丝/玩家，Banking → 客户/企业

**创建多样化的角色：**
- 混合不同的经验水平（初学者，中级，专家）
- 混合不同的技术熟练程度（低，中，高）
- 混合不同的年龄范围（年轻，中年，老年）
- 混合不同的动机（随意，专业，热情）

**生成现实的目标：**
- 与网站的目的具体相关
- 可操作且可衡量
- 与角色的特征相匹配

**按行业划分的示例：**
- **电子商务**：bargain_hunter，comparison_shopper，impulse_buyer
- **新闻**：daily_reader，topic_follower，casual_browser
- **体育**：die_hard_fan，casual_viewer，stats_tracker
- **旅行**：business_traveler，vacation_planner，deal_seeker
- **SaaS**：power_user，evaluator，beginner
## 用户调用方式

用户可以通过以下方式触发此技能：
- “测试[网站URL]的可用性”
- “对[网站URL]运行可用性测试”
- “为[网站URL]生成可用性报告”
- “分析[网站URL]的用户体验问题”
- **新功能：** “测试[网站]的预订流程”
- **新功能：** “测试[电子商务网站]的结账流程”
- **新功能：** “测试[社交媒体网站]的发布工作流程”

**AI将自动：**
1. 加载Nova Act手册以获取指导
2. 分析页面以理解其功能
3. 检测该网站是否是基于工作流程的（预订，电子商务，社交媒体等）
4. **生成符合上下文的角色：**
   - 如果指定了自定义角色 → 创建与该描述匹配的角色
   - 如果没有自定义角色 → 使用Claude AI推断出3种最可能的真实用户类型
   - 如果AI无法生成，则使用基于类别的角色
5. 创建真实的测试用例（在适当的情况下包括完整的工作流程）
6. 使用Nova Act运行自适应的、迭代的测试
7. **新功能：** 在执行可能产生重大影响的操作（支付，发布，账户创建）之前设置安全停止
8. 生成包含跟踪链接的全面HTML报告
9. 提供查看说明

## 工作流程测试

**此版本的新功能：** 该技能现在测试完整的用户旅程，而不仅仅是查找信息！

### 支持的工作流程

**电子商务：**
- 产品搜索 → 加入购物车 → 结账 → **在支付前停止**

**航班/酒店预订：**
- 搜索 → 选择 → 填写详情 → **在预订前停止**

**社交媒体：**
- 创建帖子 → 添加内容 → **在发布前停止**

**账户注册：**
- 填写注册信息 → **在最终提交前停止**

**表单提交：**
- 填写表单 → **在提交前停止**

### 安全保障

该技能**绝不会：**
- 完成实际购买
- 创建真实账户
- 公开发布内容
- 发送电子邮件/消息
- 订阅新闻通讯
- 执行任何具有金钱/法律/声誉影响的操作

该技能**始终会：**
- 测试到（但不包括）最终操作
- 验证最终按钮是否存在且可访问
- 在观察结果中记录安全停止情况

## 🧠 代理分析（至关重要）

**您（AI代理）必须分析测试结果！** 脚本收集原始响应，但不解释它们。

### 为什么需要代理分析？

脚本返回的原始Nova Act响应例如：
- `"No"` - 有价格链接吗？
- `"I don't see any documentation"` - 有文档吗？
- `"Amazon Nova Act"` - 标题是什么？

**您必须确定每个响应是否表示目标已经达成：**

| 响应 | 目标是否达成？ |
|----------|---------------|
| `"No"` | ❌ 未达成 |
| `"I don't see..."` | ❌ 未达成 |
| `"Not found"` | ❌ 未达成 |
| `"Yes, I found..."` | ✅ 达成 |
| `"Amazon Nova Act"`（内容） | ✅ 达成 |
| `"The pricing is $29/mo"` | ✅ 达成 |

### 结果数据结构

测试脚本运行后，读取JSON结果。每个步骤包含：

```json
{
    "step_name": "check_nav_for_pricing",
    "prompt": "Is there a pricing link in the navigation?",
    "expected_outcome": "Find pricing in navigation",
    "raw_response": "No",
    "api_success": true,
    "needs_agent_analysis": true,
    "attempts": [
        {
            "prompt": "Is there a pricing link in the navigation?",
            "response": "No",
            "approach": "original"
        }
    ]
}
```

**您需要分析的关键字段：**
- `raw_response`：实际的Nova Act响应 - 您需要确定其含义
- `api_success`：API调用是否成功？（脚本会处理这一点）
- `needs_agent_analysis`：始终为`true` - 表示需要您进行解释
- `attempts`：尝试的次数（脚本最多尝试3种替代方法）

### 如何分析

**对于每个步骤，确定：**
1. `goal_achieved`：响应是否表示成功或失败？
2. `friction_level`：难度如何？（尝试次数 > 1 = 存在障碍）
3. `observations`：来自响应的用户体验洞察

**分析示例：**

```
Step 1: "Is there a pricing link?" 
  → Response: "No" (1 attempt)
  → Goal achieved: NO (explicit negative)
  → Friction: HIGH (not discoverable)

Step 2: "What is the headline?" 
  → Response: "Amazon Nova Act" (1 attempt)
  → Goal achieved: YES (actual content)
  → Friction: LOW (immediately visible)

Step 3: "Find documentation" 
  → Response: "I found a docs link in the footer" (3 attempts)
  → Goal achieved: YES (found eventually)
  → Friction: MEDIUM (required multiple approaches)
```

### 辅助函数（用于脚本集成）

`response_interpreter.py`提供了结构化提示的辅助函数：

```python
from scripts.response_interpreter import (
    format_for_agent_analysis,
    create_agent_prompt_for_interpretation,
    create_agent_prompt_for_alternative
)

# Format all results for analysis
formatted = format_for_agent_analysis(results)

# Get interpretation prompt for one step
prompt = create_agent_prompt_for_interpretation(step_result)

# Get retry prompt when goal not achieved  
retry_prompt = create_agent_prompt_for_alternative(
    original_prompt="Is there a pricing link?",
    failed_response="No",
    attempt_number=2
)
```

### 完整的分析工作流程（必须完成）

**脚本不会自动生成最终报告。** 您（代理）必须：**

1. **运行测试脚本** → 输出包含原始数据的`test_results_adaptive.json`
2. **将JSON读入您的上下文**
3. **解释每个步骤** → 根据`raw_response`设置`goal_achieved: true/false`
4. **设置整体成功** → 为每个测试设置`overall_success: true/false`
5. **保存更新后的JSON**
6. **调用报告生成器** 并传递解释结果

**代理执行的步骤代码：**

```python
import json
import os
import sys

# Add skill scripts to path
sys.path.insert(0, os.path.expanduser("~/.openclaw/skills/nova-act-usability/scripts"))
from enhanced_report_generator import generate_enhanced_report

# 1. Read raw results
with open('test_results_adaptive.json', 'r') as f:
    results = json.load(f)

# 2. YOU (the agent) interpret each step
for test in results:
    goals_achieved = 0
    for step in test.get('steps', []):
        raw = step.get('raw_response', '')
        
        # AGENT INTERPRETS: Does this response indicate goal was achieved?
        # You decide based on the response content and expected outcome
        # Example interpretations:
        #   "No" → goal_achieved = False
        #   "Leaderboard, News, Schedule, Players" → goal_achieved = True (content found)
        #   "Yes" → goal_achieved = True
        #   "I don't see any..." → goal_achieved = False
        
        step['goal_achieved'] = ???  # YOU set this based on your interpretation
        if step['goal_achieved']:
            goals_achieved += 1
    
    # 3. Set overall success (e.g., >= 50% goals achieved)
    total = len(test.get('steps', []))
    test['goals_achieved'] = goals_achieved
    test['overall_success'] = (goals_achieved / total >= 0.5) if total > 0 else False

# 4. Save interpreted results
with open('test_results_adaptive.json', 'w') as f:
    json.dump(results, f, indent=2)

# 5. Generate report with interpreted data
page_analysis = {
    'title': '...',  # From your earlier analysis
    'purpose': '...',
    'navigation': [...]
}
all_traces = []
for r in results:
    all_traces.extend(r.get('trace_files', []))

report_path = generate_enhanced_report(page_analysis, results, all_traces)
print(f"Report: {report_path}")
```

**为什么需要代理进行解释：**
- 没有硬编码的正则表达式或模式匹配
- 您理解上下文（“Yes”对于这个特定问题的含义）
- 您可以推理部分成功的情况和边缘情况
- 不需要重复调用Claude API - 您已经在运行中！

## ⚠️ 关键：保持Nova Act提示的简洁性

**Nova Act是一个浏览器自动化工具，而不是推理引擎。**

Claude代理（您）负责所有关于以下内容的推理：
- 根据角色决定测试什么
- 结果是好还是坏
- 用户体验的影响是什么

Nova Act仅负责：
- 点击，输入，滚动
- 报告它所看到的内容

### ❌ 错误做法：让Nova Act进行推理

```python
# DON'T ask Nova Act to think about personas
nova.act("As a beginner user, can you easily find the documentation?")
nova.act("Would a business professional find the pricing clear?")
nova.act("Is this task accomplishable for someone with low technical skills?")
```

### ✅ 正确的做法：简单的、直接的浏览器命令

```python
# Simple browser actions
nova.act("Click the Documentation link in the navigation")
nova.act("Find and click a link containing 'Pricing'")
nova.act_get("What text is displayed in the main heading?")
nova.act_get("List the navigation menu items visible on this page")
```

### 正确的工作流程

1. **代理**（您）根据角色决定要测试什么：例如“Dorothy 68岁，技术水平较低 - 她想知道如何在线观看高尔夫”
2. **代理** 生成简单的Nova Act提示：“在导航栏中点击‘Watch & Listen’”
3. **Nova Act** 执行浏览器任务并返回原始结果：“点击了‘Watch & Listen’，现在进入视频页面”
4. **代理** 解释结果：“Dorothy会觉得这很困惑，因为选项不够清晰……”

## 工作原理

**您（AI）是整个过程的协调者。** 该技能提供：
1. **Nova Act手册**（`references/nova-act-cookbook.md`） - 最佳实践、工作流程模式和安全指南（在测试开始时自动加载）
2. **自适应测试编排器**（`run_adaptive_test.py`） - 主要的执行脚本，负责工作流程检测
3. **动态策略生成器**（`scripts/dynamic_exploration.py`） - 生成适合工作流程的测试策略
4. **会话管理**（`scripts/nova_session.py`） - Nova Act的封装层
5. **报告生成器**（`enhanced_report_generator.py`） - 自动生成的HTML报告

**执行流程：**

### 关键：首先检查依赖项

**在运行任何测试之前，请检查依赖项是否已安装：**

```bash
# Check if nova-act is installed
python3 -c "import nova_act" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Dependencies not installed. Please run:"
    echo "  pip3 install nova-act pydantic playwright"
    echo "  playwright install chromium"
    exit 1
fi

# Check API key
if ! grep -q '"apiKey":.*[^"]' ~/.openclaw/config/nova-act.json; then
    echo "⚠️  Please add your Nova Act API key to ~/.openclaw/config/nova-act.json"
    exit 1
fi
```

**或者使用Python来检查：**

```python
import sys

# Check if nova-act is installed
try:
    import nova_act
    print("✅ Dependencies already installed")
except ImportError:
    print("📦 Dependencies not installed. Please run:")
    print("   pip3 install nova-act pydantic playwright")
    print("   playwright install chromium")
    sys.exit(1)
```

### 在确认依赖项后运行测试**

当用户请求进行可用性测试时：

```bash
# Find the skill directory
SKILL_DIR=~/.openclaw/skills/nova-act-usability

# Run the adaptive test script
python3 "$SKILL_DIR/scripts/run_adaptive_test.py" "https://example.com"

# This will:
# - Create nova_act_logs/ in current directory
# - Create test_results_adaptive.json in current directory
# - Create nova_act_usability_report.html in current directory
# - Provide 60-second status updates during test
```

### ⏱️ 超时指南

**推荐的超时时间：30分钟（1800秒）**

使用3个角色×3个目标的完整可用性测试可能需要10-20分钟以上，具体取决于：
- 网站加载时间（如媒体内容较多的体育网站加载较慢）
- Nova Act API的响应时间（每个act()调用需要5-60秒）
- 网络条件

**优雅关闭：** 如果测试被中断（超时，SIGTERM，SIGINT），它将：
1. 将所有完成的测试结果保存到`test_results_adaptive.json`
2. 生成一个明确标记为不完整的**部分报告**
3. 显示已完成与计划中的测试数量

**对于较短的测试：** 使用较少的人物或目标：**
```python
# Quick test with 1 persona
personas = [{"name": "Test User", "archetype": "casual", ...}]
```

### 您（AI）需要做的：

1. **检查依赖项**（运行上述检查）
2. **如果缺少依赖项**：告诉用户运行`pip3 install nova-act pydantic playwright && playwright install chromium`
3. **如果依赖项已安装**：从用户请求中提取网站URL
4. **使用URL作为参数运行测试**
5. **监控进度**（每60秒更新一次状态）
6. **与用户分享报告的查看说明**

## 快速入门

**当用户请求进行可用性测试时：**

```python
import subprocess
import os

# Get skill directory
skill_dir = os.path.expanduser("~/.openclaw/skills/nova-act-usability")
if not os.path.exists(skill_dir):
    # Try workspace location
    skill_dir = os.path.join(os.getcwd(), "nova-act-usability")

script_path = os.path.join(skill_dir, "scripts", "run_adaptive_test.py")

# Run test
result = subprocess.run(
    ["python3", script_path, "https://example.com"],
    env={**os.environ, "NOVA_ACT_SKIP_PLAYWRIGHT_INSTALL": "1"},
    capture_output=True,
    text=True
)

print(result.stdout)
```

## 详细的工作流程（内部）

自适应测试脚本（`run_adaptive_test.py`）处理：

### 第1步：页面分析
- 使用Nova Act加载页面
- 提取标题、导航栏、页面目的
- 识别关键元素（文档、演示、价格）

### 第2步：生成符合上下文的角色
- 如果页面侧重于API或代码，则生成开发人员角色
- 如果页面提供演示内容，则生成业务角色
- 如果页面提供演示内容，则生成初学者角色

### 第3步：生成真实的测试用例
- 为每个角色生成3个最常见的用例
- 基于页面的实际内容
- 与角色的目标相匹配

### 第4步：迭代测试执行

对于每个角色+任务组合：

```python
from scripts.nova_session import nova_session
from nova_act import BOOL_SCHEMA
import time

observations = []

with nova_session(website_url) as nova:
    start_time = time.time()
    
    # Initial navigation
    observations.append({
        "step": "navigate",
        "action": f"Loaded {website_url}",
        "success": True,
        "notes": "Initial page load"
    })
    
    # Execute task step-by-step (AI-orchestrated)
    # Break into small act() calls based on cookbook guidance
    
    # Example: "Find pricing information" task
    
    # Step 1: Look for pricing link
    nova.act("Look for a link or button for pricing, plans, or subscription")
    found = nova.act_get(
        "Is there a visible pricing or plans link?",
        schema=BOOL_SCHEMA
    )
    
    observations.append({
        "step": "find_pricing_link",
        "action": "Search for pricing navigation",
        "success": found.parsed_response,
        "notes": "Easy to find" if found.parsed_response else "Not immediately visible - UX friction"
    })
    
    if found.parsed_response:
        # Step 2: Navigate to pricing
        nova.act("Click on the pricing or plans link")
        
        # Step 3: Analyze pricing page
        is_clear = nova.act_get(
            "Is the pricing information clearly displayed with prices and features?",
            schema=BOOL_SCHEMA
        )
        
        observations.append({
            "step": "view_pricing",
            "action": "Accessed pricing page",
            "success": is_clear.parsed_response,
            "notes": "Clear pricing display" if is_clear.parsed_response else "Pricing unclear or confusing"
        })
    else:
        # Alternative path - try search
        nova.act("Look for a search function")
        # ... continue orchestrating
    
    duration = time.time() - start_time
    
    # Document overall task result
    task_success = all(obs["success"] for obs in observations if obs["success"] is not None)
    
    results.append({
        "persona": persona_name,
        "task": task_description,
        "success": task_success,
        "duration": duration,
        "observations": observations,
        "friction_points": [obs for obs in observations if not obs.get("success")]
    })
```

### 第5步：汇总和分析结果

所有测试完成后：
1. 识别不同角色之间的共同障碍点
2. 注意低技术水平角色的可用性问题
3. 标记效率问题（步骤过多）
4. 记录任务失败的情况（重大的用户体验问题）

### 第6步：生成报告

```python
import json
from scripts.enhanced_report_generator import generate_enhanced_report

# Save results
with open("test_results_adaptive.json", "w") as f:
    json.dump(results, f, indent=2)

# Generate HTML report
report_path = generate_enhanced_report(
    page_analysis=page_analysis,
    results=test_results
)

print(f"Report: {report_path}")
```

## 关键原则

### 动态任务分解

AI应根据以下因素决定如何分解每个任务：
- 网站的复杂性
- 角色的技术水平
- 任务的性质（导航、数据输入、搜索）

**低技术水平角色的示例：**
```python
# More explicit, step-by-step
nova.act("Look for a button labeled 'Contact' or 'Contact Us'")
nova.act("Click on the Contact button")
result = nova.act_get("Is there a phone number or email address visible?")
```

**高技术水平角色的示例：**
```python
# Test efficiency features
nova.act("Look for keyboard shortcuts or quick access features")
nova.act("Try to use search (Ctrl+K or Cmd+K)")
```

### 实时观察

在每次`act()`调用后，分析：
- 是否成功？
- UI元素是否易于找到？
- 标签是否清晰？
- 需要尝试多少次？
- 有错误信息吗？

立即在观察结果中记录障碍情况。

### 根据角色特征调整提示

根据角色的特征调整`act()`的提示：
- **老年人/技术水平较低的用户**：寻找明显的、有标签的按钮；阅读所有内容
- **高级用户**：尝试键盘快捷键、高级功能
- **移动设备用户**：测试移动设备的响应性、触摸目标
- **屏幕阅读器用户**：测试键盘导航、ARIA标签

## 资源

### `references/nova-act-cookbook.md**
**在开始任何测试之前必须阅读。** 包含以下方面的最佳实践：**
- 有效的act()提示
- 任务分解策略
- 数据提取模式
- 错误处理
- 角色适应

### `references/persona-examples.md**
包含详细角色的模板：
- 技术娴熟的千禧一代
- 年长的初学者
- 忙碌的专业人士
- 注重预算的学生
- 关注无障碍设计的用户
- 国际用户/非母语者

### `scripts/nova_session.py`
提供Nova Act会话的基本封装：

```python
with nova_session(url, headless=True, logs_dir="./logs") as nova:
    nova.act("action")
    result = nova.act_get("query", schema=Schema)
```

### `scripts/enhanced_report_generator.py**
将观察结果编译成包含跟踪链接的HTML可用性报告。

### `assets/report-template.html`
专业的HTML报告模板。

## ⚠️ 重要提示：首次使用前需要设置

**使用此技能之前，必须安装相关依赖项。**

### 对于AI代理：依赖项检查

**在运行测试之前，始终检查依赖项是否已安装：**

```python
# Quick dependency check
try:
    import nova_act
    print("✅ Dependencies installed")
except ImportError:
    print("📦 Dependencies not installed. Please run:")
    print("   pip3 install nova-act pydantic playwright")
    print("   playwright install chromium")
    print("")
    print("This will take 2-3 minutes to download browsers (~300MB)")
```

### 对于用户：一次性设置

**步骤1：安装Python包**
```bash
pip3 install nova-act pydantic playwright
```

**步骤2：安装Playwright浏览器**
```bash
playwright install chromium
```

**步骤3：配置API密钥**
1. 从[AWS控制台](https://console.aws.amazon.com/)获取您的Nova Act API密钥
2. 创建配置文件：
```bash
mkdir -p ~/.openclaw/config
echo '{"apiKey": "your-key-here"}' > ~/.openclaw/config/nova-act.json
```
3. 将`your-key-here`替换为实际的Nova Act API密钥

## 示例：AI编排的测试

**用户请求：** “测试example.com对老年用户”

**AI编排过程：**

1. 阅读`references/nova-act-cookbook.md`
2. 阅读`references/persona-examples.md`
3. 生成老年角色（Dorothy，72岁，技术水平较低）
4. 生成任务：
   - “查找联系信息”
   - “阅读关于服务的信息”
   - “导航到FAQ”
5. 对于每个任务，动态地编排Nova Act：
   - 启动会话
   - 执行小的act()步骤
   - 观察并分析每个结果
   - 根据观察结果进行记录
   - 根据观察结果继续或进行调整
6. 汇总观察结果
7. 生成包含发现和建议的HTML报告

**所有步骤都由AI决定。** 该技能仅提供工具和指导。

## 文件结构

```
nova-act-usability/
├── SKILL.md                          # This file
├── README.md                         # User documentation
├── skill.json                        # Skill manifest
├── scripts/
│   ├── run_adaptive_test.py          # Main orchestrator (accepts URL arg)
│   ├── nova_session.py               # Session wrapper
│   ├── enhanced_report_generator.py  # HTML report generator
│   └── trace_finder.py               # Extract trace file paths
├── references/
│   ├── nova-act-cookbook.md          # Best practices
│   └── persona-examples.md           # Template personas
└── assets/
    └── report-template.html          # HTML template

```

## 输出文件（在工作目录中创建）

运行测试时，这些文件将在当前工作目录中创建：

```
./
├── nova_act_logs/                    # Nova Act trace files
│   ├── act_<id>_output.html         # Session recordings
│   └── ...
├── test_results_adaptive.json        # Raw test results
└── nova_act_usability_report.html   # Final report
```

所有路径都是相对的 - 适用于任何安装位置！