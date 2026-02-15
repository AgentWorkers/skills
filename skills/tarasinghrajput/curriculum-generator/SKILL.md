---
name: curriculum-generator
description: 智能教育课程生成系统，具备严格的步骤执行机制及人工干预政策
metadata:
  openclaw:
    requires:
      bins: ["node"]
      env: []
      config: []
    version: "1.0.0"
    author: "Apni Pathshala"
---

## 调试模式

当用户在课程请求中包含“调试模式”或“显示搜索结果”时：

**启用详细输出：**
- 在执行每个 `neo-ddg-search` 查询之前将其打印出来
- 打印返回的结果数量
- 打印提取的前 2-3 个网址
- 打印资源分配信息：`分配给 {topic}：{url}`

**示例调试输出：**
```
[DEBUG] Executing neo-ddg-search("Python basics tutorial for beginners")
[DEBUG] Search returned 10 results
[DEBUG] Extracting URLs...
[DEBUG] Found: https://www.youtube.com/watch?v=rfscVS0vtbw
[DEBUG] Found: https://www.freecodecamp.org/learn/scientific-computing-with-python/
[DEBUG] Assigning to "Python Basics": https://www.youtube.com/watch?v=rfscVS0vtbw
```


## 依赖关系

### 所需技能
此技能需要安装以下其他技能：

- **neo-ddg-search**：用于搜索教育资源
  - 安装命令：`clawhub install neobotjan2026/neo-ddg-search`
  - 验证方法：检查 `skills` 目录中是否存在 `neo-ddg-search` 技能

### 依赖关系验证

在生成课程内容之前，验证 `neo-ddg-search` 是否可用：
```
IF neo-ddg-search skill NOT found:
   🚨 DEPENDENCY MISSING
   
   The curriculum generator requires the neo-ddg-search skill for finding educational resources.
   
   Please install it:
   clawhub install neobotjan2026/neo-ddg-search
   
   Then restart this process.
   
   ⚠️ GENERATION CANNOT PROCEED without search capability
   
   STOP
```

### 搜索工具健康检查

在开始资源研究之前，进行一次测试搜索：
```
Test: neo-ddg-search("Python tutorial test")

IF successful:
   ✅ Search tool operational
   Proceeding with resource research...
   
IF failed:
   🚨 SEARCH TOOL ERROR
   
   neo-ddg-search is installed but not responding correctly.
   
   Error: {error_details}
   
   Please check:
   • neo-ddg-search skill is properly installed
   • Internet connection is available
   • No firewall blocking DuckDuckGo
   
   ⚠️ Cannot proceed with resource research
   
   ESCALATE
```

# 课程生成技能

## 目的
此技能通过结构化、分步骤的过程帮助为 POD（交付点）生成定制的教育课程，并在需要时强制进行人工干预。

## 核心功能
- 通过结构化问卷引导需求收集
- 基于研究的课程设计或评估
- 生成 Excel (.xlsx) 格式的输出文件
- 使用本地内存进行持续改进
- 执行后台任务
- 严格执行人工干预政策

## 存储位置
- **内存**：`~/.openclaw/skills/curriculum-generator/memory/`
- **输出文件**：`~/.openclaw/skills/curriculum-generator/outputs/`
- **模板**：`~/.openclaw/skills/curriculum-generator/templates/`

## 激活触发条件
当用户执行以下操作时，此技能会被激活：
- 说“创建课程”、“设计课程”或“评估课程”
- 说“课程帮助”或“开始课程流程”
- 明确请求为某个 POD 生成课程

## 重要规则（不可协商）

### 核心原则
每当您被迫猜测、推断或权衡风险时，必须咨询人类。如果错误的决策可能影响学生、教师或 POD 的运作，必须立即进行人工干预。

### 强制性升级触发条件
如果出现以下任何情况，必须立即停止并升级给人类：
**A. 输入缺失或模糊**
- 目标年龄/年级水平不明确
- 教师的可用性或能力未知
- 每天的实验课时未指定
- 基础设施的可靠性（计算机/互联网/电力）不明确
- 无法确认是否存在现有课程

**B. 教师能力风险**
- 教师无法独立操作计算机
- 教师缺乏运行实验的经验
- 教师无法管理实验纪律或流程

**C. 运营不可行**
- 课程课时超过可用实验课时
- 每周的课程节数量超过教师的能力范围
- 学生与计算机的比例不安全
- 基础设施无法支持计划的活动

**D. 高风险课程更改**
- 删除主要的学习成果
- 显著更改课程时长
- 更改学习领域（例如，从数字素养改为就业准备）
- 引入以前未使用的新工具/平台

**E. 利益相关者意见冲突**
- 教师认为课程太难，学生认为太简单
- POD 负责人的优先事项与可行性相矛盾
- 反馈循环与评估数据不一致

### 升级格式（必须使用）
在升级时，使用以下格式：
```
🚨 HUMAN INPUT REQUIRED

Reason: [specific trigger]
Impact if Unresolved: [clear consequence]
Options (if any):
1. [option 1]
2. [option 2]

Awaiting Decision From: [POD Leader / Curriculum Owner]
```

## 流程

### 第 0 步：场景识别（必须）
首先确定：
- **场景 A**：评估现有课程
- **场景 B**：设计新课程

如果不确定，请停止并请求用户确认。未经分类不得继续。

---

### 场景 A：评估现有课程

#### 第 1 步：收集基本信息
使用结构化表格收集以下所有信息：

**第 0 节：请求元数据**
- 请求 ID（使用时间戳自动生成）
- 请求日期（自动捕获）
- 请求者（姓名 + 职务）
- POD 名称（必填）
- 场景类型（必须选择）

⚠️ 如果未选择场景类型 → 立即停止

**第 1 节：目标受众概况（必须）**
1. 主要学生群体：
   - 年龄范围
   - 年级/教育水平
2. 学生背景（选择所有适用项）：
   - 首次使用计算机
   - 基本操作计算机技能（鼠标、键盘）
   - 之前的数字实验经验
   - 学生水平参差不齐
3. 语言偏好：
   - 教学语言
   - 英语熟练程度（低/中/高）
4. 特殊限制：
   - 学习障碍
   - 出勤情况不稳定
   - 社会/经济条件

⚠️ 如果年龄/年级信息缺失 → 立即停止并升级

**第 2 节：POD 与基础设施详情（必须）**
1. 实验基础设施：
   - 计算机数量
   - 每次实验的平均学生人数
   - 互联网连接情况（稳定/不稳定/无）
   - 备用电源（有/无）
2. 每天的实验时间：
   - 每天可用的实验小时数
   - 实验每周进行的天数
3. 现有工具/平台：
   - 操作系统
   - 已安装的软件
   - 互联网限制

⚠️ 如果实验时间或计算机数量信息缺失 → 立即停止并升级

**第 3 节：教师能力与可用性（必须）**
1. 分配的教师人数
2. 教师可用性：
   - 每周的工作天数
   - 每天的工作小时数
3. 教师能力评估：
   - 是否可以独立操作计算机？（是/否）
   - 是否能够管理数字实验？（是/否）
   - 之前是否有类似课程的经验？（是/否）
4. 培训需求：
   - 无需培训
   - 需要短期培训
   - 需要长期培训

⚠️ 如果能力评估中有任何“否”的回答 → 可能需要升级

#### 第 2 步：利益相关者输入（结构化总结）
根据提供的数据模拟结构化的利益相关者输入：
- **POD 负责人**：课程的有效性、挑战及改进需求
- **教师**：教学经验、课程中的不足之处、学生进度
- **学生**：课程难度、参与度、相关性

然后进行教师能力评估：
- 教师是否可以独立操作计算机？
- 他们能否按照课程要求进行实验？
- 他们能否管理实验纪律和流程？
- 识别出任何培训需求

#### 第 3 步：课程评估
从以下方面评估课程：
- 与学生需求的相关性
- 与行业/数字素养目标的一致性
- 对不同学习速度的适应性
- 学习成果的明确性和可衡量性
- 技术整合的质量

然后进行运营可行性检查：
- 实验安排的可行性
- 教师是否充足
- 基础设施是否准备就绪（计算机、互联网、电力）

#### 第 4 步：建议
- 明确说明是否需要修改或是否可选
- 如果需要修改，提出具体且可执行的建议
- 明确指出潜在的风险

最后输出：
**状态：草案评估 – 待人工审核**

---

### 场景 B：设计新课程

#### 第 2 步：定义课程基础
明确指定：
- **学习领域**：数字素养 / 学术能力提升 / 技能发展 / 就业准备
- **目标受众**：年级、背景
- **明确、可衡量的学习成果**（不允许使用模糊的成果）

#### 第 2.5 步：开发课程结构
生成以下内容：
- 模块和子主题
- 每周的课程安排
- 每节课的学习目标
- 课程时长（例如，3 个月 / 6 个月）
- 课程频率

**实验计划（必须）：**
- 每天的实验时间
- 每周的实验节数

**在继续之前，必须完成以下步骤：**
```
BEFORE moving to Step B3, execute this command sequence:

1. Review the curriculum structure you just created
2. Identify ALL topics that will appear in the final output
3. For EACH topic, RIGHT NOW, execute:
   
   neo-ddg-search("{topic} tutorial for beginners")
   
4. Extract the first valid educational URL from results
5. Store it in a resource_map dictionary:
   
   resource_map["{topic}"] = "https://..."

6. Verify resource_map has entries for ALL topics
7. Only then proceed to Step B3

Example:
Topic: "Python Lists"
Execute: neo-ddg-search("Python Lists tutorial for beginners")
Result: Found https://www.youtube.com/watch?v=W8KRzm-HUcc
Store: resource_map["Python Lists"] = "https://www.youtube.com/watch?v=W8KRzm-HUcc"

DO NOT SKIP THIS. DO NOT PROCEED WITHOUT COMPLETING THIS.
```
```

## **Step 5: Create a Simpler Test in Telegram**

Now test with very explicit instructions. In Telegram, send:
```
创建一个简单的测试课程：
- 主题：HTML 基础
- 时长：仅 1 周
- 共 2 节课

重要说明：
1. 创建结构后，使用 `neo-ddg-search` 为每节课查找资源
2. 在生成 CSV 文件之前，验证所有资源链接是否为有效网址
3. 展示您执行的每次搜索
4. 如果有任何资源链接为空或显示为“TBD”，立即停止并重新搜索

现在开始。

**步骤 2.2 资源收集完成**

在进入步骤 3 之前，您必须完成以下操作：
```
STOP HERE.

Before moving to Step B3, execute this sequence:

1. List all topics you just created: [topic1, topic2, topic3, ...]

2. Create an empty dictionary: resource_links = {}

3. FOR EACH topic:
   a. Execute: result = neo-ddg-search("{topic} tutorial for beginners")
   b. Look at the result text
   c. Find all text that starts with "https://"
   d. Extract the complete URL
   e. Store: resource_links[topic] = that_url
   f. Print: "Stored for {topic}: {that_url}"

4. Verify resource_links has ALL topics

5. Print the complete resource_links dictionary

6. ONLY THEN proceed to Step B3

Example for "HTML Basics":
   Execute: neo-ddg-search("HTML Basics tutorial for beginners")
   Result contains: "...https://www.youtube.com/watch?v=pQN-pnXPaVg..."
   Extract: "https://www.youtube.com/watch?v=pQN-pnXPaVg"
   Store: resource_links["HTML Basics"] = "https://www.youtube.com/watch?v=pQN-pnXPaVg"
   Print: "Stored for HTML Basics: https://www.youtube.com/watch?v=pQN-pnXPaVg"

DO THIS FOR EVERY SINGLE TOPIC BEFORE MOVING ON.
```


**步骤 2.2 资源收集完成（必须）**
```
YOU MUST NOW COLLECT RESOURCES BEFORE PROCEEDING.

Execute this EXACT sequence:

1. Create empty dictionary: resource_links = {}

2. List all topics from Step B2

3. For EACH topic, execute:
   
   bash_tool: python3 ~/.openclaw/skills/neo-ddg-search/scripts/search.py "{topic} tutorial for beginners" 5
   
4. From the output, find all text starting with "https://"

5. Take the first URL that contains "youtube.com", or if none, the first URL

6. Store it: resource_links[topic] = that_url

7. Print: "Collected for {topic}: {that_url}"

8. After ALL topics are done, print the complete resource_links dictionary

9. Verify every topic has a URL

10. ONLY THEN create the CSV using URLs from resource_links

DO NOT WRITE "TBD" IN THE CSV.
USE THE URLS FROM resource_links DICTIONARY.

If you cannot find a URL for a topic, STOP and ESCALATE.
Do not proceed to CSV generation without URLs for all topics.
```
```

## **Save and Test**

Save the file, then in Telegram:
```
重新加载技能
```

Then test with a VERY simple example:
```
创建课程：
- 主题：仅 HTML
- 共 1 节课
- 展示每个步骤

构建结构后：
1. 使用以下命令搜索 HTML 资源：`python3 ~/.openclaw/skills/neo-ddg-search/scripts/search.py "HTML tutorial for beginners" 5`
2. 展示原始搜索结果
3. 提取网址
4. 展示提取的网址
5. 在写入 CSV 文件之前展示内容
6. 如果资源链接显示为“TBD”，立即停止

开始。
```

## **What to Watch For**

You should see output like:
```
✅ 课程结构已完成

🔍 开始资源搜索...

主题：HTML 基础
执行命令：`python3 ~/.openclaw/skills/neo-ddg-search/scripts/search.py "HTML Tutorial for Beginners" 5`

[搜索结果]
[1] HTML 教程 | https://www.youtube.com/watch?v=...
[2] Learn HTML | https://www.w3schools.com/html/

找到 2 个网址
选择：https://www.youtube.com/watch?v=...
✅ 保存 HTML 基础课程的网址：https://www.youtube.com/watch?v=...

资源链接字典：
  HTML 基础：https://www.youtube.com/watch?v=...

📋 CSV 预览：
覆盖的主题           | 资源链接
HTML 基础             | https://www.youtube.com/watch?v=...

编写文件...


#### 第 2.5 步：资源链接填充（简化流程）

**完成步骤 2 的结构后，执行以下步骤：**

### 每个主题的简单三步流程

**步骤 1：搜索**
```bash
python3 ~/.openclaw/workspace/skills/neo-ddg-search/scripts/search.py "{topic} tutorial for beginners" 5
```

**步骤 2：查看结果并提取第一个网址**
- 逐行查看搜索结果
- 当看到 `https://` 时，复制从 `https://` 开始的所有内容直到下一个空格
- 这就是您要提取的网址

**步骤 3：保存网址**
```
resource_links["{topic}"] = "the_url_you_found"
```

**然后立即进入下一个主题。除非第一次搜索没有结果，否则不要进行额外的搜索。**

**规则**：
- 每个主题只进行一次搜索
- 提取一个网址
- 不要：
  - 对同一主题进行多次搜索
  - 尝试寻找“更好的”资源
  - 过度分析资源质量
  - 等待或暂停

**要做的**：
- ✅ 进行一次搜索
- ✅ 提取第一个网址
- ✅ 进入下一个主题
- ✅ 快速完成所有主题

### 完整的执行模板
```
Print: "🔍 Resource Research Starting..."
Print: ""

resource_links = {}
topics = [list of all topics from Step B2]

For topic in topics:
    Print: f"Topic: {topic}"
    
    # Execute search (ONE TIME ONLY)
    result = bash_tool(f'python3 ~/.openclaw/workspace/skills/neo-ddg-search/scripts/search.py "{topic} tutorial" 5')
    
    # Extract first URL (simple method)
    url = None
    for line in result.split('\n'):
        if 'https://' in line:
            start = line.find('https://')
            end_of_line = line[start:]
            # Get URL until space or end
            space_index = end_of_line.find(' ')
            if space_index > 0:
                url = end_of_line[:space_index]
            else:
                url = end_of_line.strip()
            break  # Take FIRST URL and stop
    
    if url:
        resource_links[topic] = url
        Print: f"  ✅ {url}"
    else:
        resource_links[topic] = "MANUAL_RESEARCH_NEEDED"
        Print: f"  ⚠️ No URL found - marked for manual research"
    
    # IMMEDIATELY continue to next topic
    
Print: ""
Print: "✅ Resource research complete"
Print: f"Collected {len(resource_links)} resource links"
Print: ""
```

### 时间限制

**资源搜索的最大时间为 2 分钟**

如果资源收集花费的时间超过 2 分钟，说明您操作有误。应该快速完成：
- 每次搜索 5 秒
- 2 个主题 = 10 秒
- 10 个主题 = 50 秒

### 保存的内容
```python
# Good examples:
resource_links["Python Basics"] = "https://datascientest.com/en/python-variables-beginners-guide"
resource_links["HTML Intro"] = "https://www.w3schools.com/python/python_variables.asp"

# Acceptable if no URL found:
resource_links["Obscure Topic"] = "MANUAL_RESEARCH_NEEDED"

# NEVER acceptable:
resource_links["Topic"] = "TBD"  # ❌
resource_links["Topic"] = ""     # ❌
```

### 收集完成后：立即生成 CSV 文件

**不要暂停或等待。立即开始生成 CSV 文件。**
```
Print: "📄 Generating CSV with collected resources..."

csv_data = []

for topic in curriculum_structure:
    resource_url = resource_links.get(topic, "MANUAL_RESEARCH_NEEDED")
    
    csv_row = {
        "Curriculum ID": curriculum_id,
        "File Name": file_name,
        "Target POD Type": pod_type,
        "Clusters": clusters,
        "Content Type": content_type,
        "Covered Topics": topic,
        "Owner": owner,
        "Resource Link": resource_url,  # ← Use collected URL
        "Document Creation Date": date,
        "Last Updated On": date
    }
    csv_data.append(csv_row)

write_csv(csv_data)
Print: "✅ CSV file generated"
```

### 示例：完成 2 个主题的搜索**

**主题**：“Python 基础”和“Python 函数”
```
🔍 Resource Research Starting...

Topic: Python Basics
  Executing search...
  [Results received]
  Found URL: https://datascientest.com/en/python-variables-beginners-guide
  ✅ https://datascientest.com/en/python-variables-beginners-guide

Topic: Python Functions  
  Executing search...
  [Results received]
  Found URL: https://www.w3schools.com/python/python_functions.asp
  ✅ https://www.w3schools.com/python/python_functions.asp

✅ Resource research complete
Collected 2 resource links

📄 Generating CSV with collected resources...
✅ CSV file generated: Python_Basics_v1.0.csv
```

**总时间**：约 15 秒

### 对“不完美”的资源无需升级

**接受第一次搜索中找到的任何网址。**

优先级是：
1. 速度 ✅
2. 完成 ✅
3. 完美的资源 ⚠️（虽然理想，但不是必须的）

如果第一次搜索返回的是 W3Schools 而不是 YouTube，也没关系。使用该资源并继续。

### 仅在以下情况下升级：
- 如果搜索完全没有结果
- 如果搜索返回了结果但没有网址
- 如果搜索工具完全失效

**以下情况不需要升级：**
- 如果网址来自 W3Schools 而不是 YouTube（仍然可以使用！）
- 如果网址来自不太知名的教育网站（也可以接受！）
- 如果网址是文档而不是视频（完全没问题！）

### 调试输出（根据用户请求）

如果用户请求调试模式：
```
[DEBUG] Topic: Python Basics
[DEBUG] Command: python3 ~/.openclaw/workspace/skills/neo-ddg-search/scripts/search.py "Python Basics tutorial" 5
[DEBUG] Results: 5 entries returned
[DEBUG] Extracting URLs...
[DEBUG] Line 1: Contains 'https://datascientest.com/...'
[DEBUG] Extracted: https://datascientest.com/en/python-variables-beginners-guide
[DEBUG] Storing: resource_links["Python Basics"] = "https://datascientest.com/..."
[DEBUG] ✅ Complete - moving to next topic
```

**步骤 2 完成后，必须立即开始资源收集**
```
After completing Step B2 course structure:

1. DO NOT pause
2. DO NOT ask for confirmation
3. IMMEDIATELY start resource collection
4. Use the Simple 3-Step Process above
5. Complete ALL topics within 2 minutes
6. Then IMMEDIATELY generate CSV
7. Do NOT wait between steps

This should be ONE CONTINUOUS FLOW:
Step B2 → Resource Collection → CSV Generation → Done

No breaks. No pauses. No waiting.
```

### 课程生成中的实施

**在步骤 2（课程结构）之后，执行以下操作：**
```
Print: "🔍 Starting resource search for all topics..."
Print: ""

Initialize: resource_links = {}

For each topic in curriculum:
    Print: "Topic: {topic}"
    
    # Execute search
    command = f"python3 ~/.openclaw/skills/neo-ddg-search/scripts/search.py \"{topic} tutorial for beginners\" 5"
    result = execute_bash(command)
    
    # Extract URLs (look for https://)
    lines = result.split('\n')
    urls = []
    for line in lines:
        if 'https://' in line:
            # Extract the URL part
            start = line.find('https://')
            # Find end (space or newline)
            rest = line[start:]
            space_pos = rest.find(' ')
            if space_pos > 0:
                url = rest[:space_pos]
            else:
                url = rest.strip()
            urls.append(url)
    
    Print: f"  Found {len(urls)} URLs"
    
    # Choose best URL
    best_url = None
    for url in urls:
        if 'youtube.com' in url:
            best_url = url
            break
    
    if not best_url and urls:
        for url in urls:
            if 'freecodecamp.org' in url:
                best_url = url
                break
    
    if not best_url and urls:
        best_url = urls[0]  # Use first URL
    
    if best_url:
        resource_links[topic] = best_url
        Print: f"  ✅ Stored: {best_url}"
    else:
        Print: f"  ❌ No URLs found - trying alternative search..."
        # Try one more time
        alt_command = f"python3 ~/.openclaw/skills/neo-ddg-search/scripts/search.py \"{topic} free course\" 5"
        alt_result = execute_bash(alt_command)
        # Extract URLs again...
        # [same extraction logic]
        
        if alt_urls:
            resource_links[topic] = alt_urls[0]
            Print: f"  ✅ Stored: {alt_urls[0]}"
        else:
            ESCALATE(f"No resources found for {topic}")
    
    Print: ""

Print: "✅ Resource collection complete!"
Print: f"Total topics: {len(resource_links)}"
Print: ""
Print: "Resource Links Dictionary:"
for topic, url in resource_links.items():
    Print: f"  {topic}: {url}"
```

#### 第 3 步：教师准备与准备情况**
指定：
- 教师所需的资源
- 教学方法（互动式、可适应的）
- 教师准备情况评估：
  - 之前的经验
  - 对计算机实验的熟悉程度
- 是否需要短期培训（是/否及原因）

#### 第 4 步：评估与反馈设计**
定义：
- 形成性评估（小测验、项目、作业）
- 总结性评估（期末考试/项目）
- 每项评估的目的

#### 第 5 步：持续改进循环**
定义：
- 反馈来源（教师、学生、评估结果）
- 审查频率
- 课程修订的标准

---

## 资源搜索（必须）

### 防止卡住规则

**如果资源收集花费的时间超过 3 分钟：**

立即停止当前操作并执行以下操作：
```
Print: "⏱️ Resource collection timeout (3 min exceeded)"
Print: "Completing with available resources..."

For any topic without a resource:
    resource_links[topic] = "MANUAL_RESEARCH_NEEDED"

Proceed immediately to CSV generation
```

**不要无限期地陷入搜索。**
```

## **Test Again**

Save the file and test:
```
重新加载技能
```

Then:
```
创建课程：
- Python 基础
- 2 节课
- 1 周

如果资源搜索花费的时间超过 1 分钟，请跳转到 CSV 生成步骤。

展示资源搜索的开始时间和结束时间。
```

## **What Should Happen**

You should see:
```
🔍 资源搜索开始...

主题：Python 入门
  ✅ https://datascientest.com/en/python-variables-beginners-guide

主题：Python 函数
  ✅ https://www.w3schools.com/python/python_functions.asp

✅ 资源搜索完成（15 秒）
收集到 2 个资源链接

📄 生成 CSV...
✅ 完成
```

**NOT this:**
```
主题：Python 入门
  执行搜索...
  [结果]
  尝试其他搜索...
  [更多结果]
  评估质量...
  [卡住了]  ← 无法生成 CSV

### 如何执行搜索

使用以下命令进行资源搜索：
```bash
python3 ~/.openclaw/skills/neo-ddg-search/scripts/search.py "YOUR QUERY HERE" 5
```

该命令会返回包含网址的搜索结果。

### 简单的搜索和提取流程

**对于课程中的每个主题：**

#### 第 1 步：执行搜索**
```bash
# Example for "HTML Basics"
python3 ~/.openclaw/skills/neo-ddg-search/scripts/search.py "HTML basics tutorial for beginners" 5
```

#### 第 2 步：查看结果**

搜索结果如下所示：
```
[1] Page Title | Year | Type | Site https://example.com/url1
Description text

[2] Another Title | Year | Type | Site https://another.com/url2  
More description
```

#### 第 3 步：提取网址**

**查找以 `https://` 开头的任何文本**

从上面的例子中提取：
- `https://example.com/url1`
- `https://another.com/url2`

#### 第 4 步：选择最佳网址**

优先顺序：
1. 包含 `youtube.com` 的网址（首选）
2. 包含 `freecodecamp.org` 的网址（第二选择）
3. 包含 `w3schools.com` 的网址（第三选择）
4. 其他教育网站的网址
5. 如果没有找到合适的网址，使用第一个网址

#### 第 5 步：保存网址**

以简单的格式保存网址：
```
Topic: HTML Basics
Resource: https://www.youtube.com/watch?v=...
```

### 完整的示例工作流程

**主题：“Python 列表”**

**步骤 1 - 搜索**：
```bash
python3 ~/.openclaw/skills/neo-ddg-search/scripts/search.py "Python lists tutorial for beginners" 5
```

**步骤 2 - 获取结果**：
```
[1] Python Lists Tutorial | 2023 | Video | YouTube https://www.youtube.com/watch?v=W8KRzm-HUcc
Learn Python lists from scratch

[2] Python Lists Guide | 2024 | Article | W3Schools https://www.w3schools.com/python/python_lists.asp
Complete guide to Python lists
```

**步骤 3 - 提取网址**：
- 找到：`https://www.youtube.com/watch?v=W8KRzm-HUcc`
- 找到：`https://www.w3schools.com/python/python_lists.asp`

**步骤 4 - 选择最佳网址**：
- 第一个网址包含 “youtube.com” → 选择这个网址
- 选中的网址：`https://www.youtube.com/watch?v=W8KRzm-HUcc`

**步骤 5 - 保存网址**：
```
resource_links["Python Lists"] = "https://www.youtube.com/watch?v=W8KRzm-HUcc"
```

### 在写入 CSV 之前**

**必须检查：**
```
Print: "🔍 Verifying resource links before CSV generation..."
Print: ""

csv_data = []

for row in curriculum_structure:
    topic = row['topic']
    
    # Get resource from resource_links dictionary
    if topic in resource_links:
        resource_url = resource_links[topic]
    else:
        Print: f"❌ ERROR: No resource link for '{topic}'"
        STOP
    
    # Verify it's a valid URL
    if not resource_url.startswith('http'):
        Print: f"❌ ERROR: Invalid URL for '{topic}': {resource_url}"
        STOP
    
    Print: f"✅ {topic}: {resource_url[:60]}..."
    
    # Add to CSV data
    csv_row = {
        "Curriculum ID": curriculum_id,
        "File Name": file_name,
        "Target POD Type": pod_type,
        "Clusters": clusters,
        "Content Type": content_type,
        "Covered Topics": topic,
        "Owner": owner,
        "Resource Link": resource_url,  # ← ACTUAL URL HERE
        "Document Creation Date": date,
        "Last Updated On": date
    }
    csv_data.append(csv_row)

Print: ""
Print: "✅ All rows verified with valid URLs"
Print: "📄 Writing CSV file..."

write_csv_file(csv_data)
```

### 在写入 CSV 之前展示数据**

```
Print: "📋 CSV Preview:"
Print: "=" * 80
Print: f"Covered Topics | Resource Link"
Print: "-" * 80
for row in csv_data:
    topic = row["Covered Topics"]
    url = row["Resource Link"]
    Print: f"{topic[:30]:30} | {url}"
Print: "=" * 80
Print: ""
Print: "Writing to file..."
```

### 如果搜索后某个主题没有网址，需要升级**

```
🚨 RESOURCE SEARCH FAILED - HUMAN INPUT REQUIRED

Topic: {topic_name}

Search 1: "python3 ~/.openclaw/skills/neo-ddg-search/scripts/search.py '{topic} tutorial for beginners' 5"
Result: {number} URLs found
None matched quality criteria

Search 2: "python3 ~/.openclaw/skills/neo-ddg-search/scripts/search.py '{topic} free course' 5"  
Result: {number} URLs found
None matched quality criteria

Issue: Cannot find suitable free educational resources

Options:
1. Modify topic name to be more general
2. Accept lower-quality resource if available
3. Mark for manual research

Awaiting Decision From: Curriculum Owner

⚠️ CSV generation paused
```


## 文件生成

## 文件生成前的检查清单（必须）

**在写入任何输出文件之前，必须完成以下检查：**

### 检查清单项目 1：资源链接验证**

**停止并验证：**
```
FOR EACH row in the curriculum data:
    topic = row['Covered Topics']
    resource_link = row['Resource Link']
    
    IF resource_link is empty OR resource_link == "TBD" OR resource_link == "N/A":
        
        PRINT "⚠️ Missing resource link for: {topic}"
        PRINT "🔍 Executing search now..."
        
        # Execute neo-ddg-search immediately
        search_query = f"{topic} tutorial for beginners"
        EXECUTE: neo-ddg-search(search_query)
        
        # Extract URLs from results
        urls = EXTRACT_URLS_FROM_RESULTS()
        
        IF urls found:
            row['Resource Link'] = urls[0]  # Use first result
            PRINT "✅ Found resource: {urls[0]}"
        ELSE:
            # Try alternative search
            search_query_2 = f"{topic} free course"
            EXECUTE: neo-ddg-search(search_query_2)
            urls = EXTRACT_URLS_FROM_RESULTS()
            
            IF urls found:
                row['Resource Link'] = urls[0]
                PRINT "✅ Found resource: {urls[0]}"
            ELSE:
                ESCALATE("Cannot find resources for {topic}")
                STOP_FILE_GENERATION
```

**您应该看到如下内容：**
```
Checking resource links before file generation...
✅ Row 1 - HTML Basics: Has resource link
✅ Row 2 - CSS Fundamentals: Has resource link  
⚠️ Row 3 - JavaScript: Missing resource link
🔍 Executing search now...
   Using neo-ddg-search: "JavaScript tutorial for beginners"
✅ Found resource: https://www.youtube.com/watch?v=...
✅ Row 3 - JavaScript: Resource link populated

All rows verified. Proceeding to file generation...
```

### 检查清单项目 2：网址格式验证**

验证所有资源链接是否为有效网址：
```
FOR EACH resource_link in curriculum:
    IF NOT resource_link.startswith("http"):
        ERROR: "Invalid resource link format: {resource_link}"
        STOP
```

### 检查清单项目 3：最终数量统计**
```
total_topics = COUNT(curriculum rows)
topics_with_resources = COUNT(rows where Resource Link is valid URL)

PRINT "📊 Resource Link Status:"
PRINT "   Total topics: {total_topics}"
PRINT "   With resources: {topics_with_resources}"
PRINT "   Missing: {total_topics - topics_with_resources}"

IF topics_with_resources < total_topics:
    ESCALATE("Some topics still missing resources after search")
    STOP
ELSE:
    PRINT "✅ All topics have resource links. Safe to generate file."
```

## CSV/Excel 文件生成 - 包含资源链接

### 生成前的准备：构建完整的资源地图**

**在写入任何文件之前，先构建完整的资源地图：**
```python
# Initialize resource map
resource_map = {}

# Get all topics from curriculum structure
all_topics = extract_all_topics_from_curriculum()

print(f"\n📚 Building resource map for {len(all_topics)} topics...\n")

# For each topic, search and extract URL
for topic in all_topics:
    print(f"🔍 Topic: {topic}")
    
    # Execute search
    search_query = f"{topic} tutorial for beginners"
    print(f"   Searching: {search_query}")
    
    search_results = neo_ddg_search(search_query)
    
    # Extract URLs from results
    urls_found = extract_urls_from_search_result(search_results)
    print(f"   Found {len(urls_found)} URLs")
    
    # Select best URL
    if urls_found:
        best_url = select_best_url(urls_found)
        resource_map[topic] = best_url
        print(f"   ✅ Selected: {best_url}\n")
    else:
        print(f"   ⚠️ No URLs found, trying alternative search...")
        # Try alternative search
        alt_search = neo_ddg_search(f"{topic} free course")
        urls_found_alt = extract_urls_from_search_result(alt_search)
        
        if urls_found_alt:
            best_url = select_best_url(urls_found_alt)
            resource_map[topic] = best_url
            print(f"   ✅ Selected: {best_url}\n")
        else:
            resource_map[topic] = "ESCALATION_NEEDED"
            print(f"   ❌ No resources found - will escalate\n")

# Verify all topics have resources
missing_resources = [t for t, url in resource_map.items() if url == "ESCALATION_NEEDED"]

if missing_resources:
    print(f"🚨 {len(missing_resources)} topics need escalation:")
    for topic in missing_resources:
        print(f"   - {topic}")
    ESCALATE("Resource search failed for some topics")
    STOP
else:
    print(f"✅ All {len(all_topics)} topics have resource links!")
    print(f"📝 Proceeding to CSV generation...\n")
```

### 在生成 CSV 时**

**在写入每一行之前，进行关键检查：**
```python
for week_num, lesson in curriculum_structure:
    topic = lesson['topic']
    
    # Get resource link from resource_map
    resource_link = resource_map.get(topic, "ERROR_NO_RESOURCE")
    
    # Verify it's a valid URL
    if not resource_link.startswith("http"):
        print(f"ERROR: Invalid resource for {topic}: {resource_link}")
        STOP
    
    csv_row = {
        "Curriculum ID": curriculum_id,
        "File Name": file_name,
        "Target POD Type": pod_type,
        "Clusters": clusters,
        "Content Type": content_type,
        "Covered Topics": topic,
        "Owner": owner,
        "Resource Link": resource_link,  # ← USE THE ACTUAL URL HERE
        "Document Creation Date": creation_date,
        "Last Updated On": last_updated
    }
    
    csv_data.append(csv_row)
```

## 文件生成 - 最终资源检查**

**在写入文件之前，必须立即执行以下操作：**
```python
# Pseudo-code showing the exact logic needed

def prepare_curriculum_data_for_file():
    """
    This function runs RIGHT BEFORE creating the CSV/Excel file.
    It ensures NO 'TBD' values slip through.
    """
    
    curriculum_rows = get_curriculum_structure()
    
    print("\n🔍 FINAL RESOURCE LINK CHECK (Pre-File-Generation)")
    print("=" * 50)
    
    for i, row in enumerate(curriculum_rows):
        topic = row['Covered Topics']
        resource_link = row.get('Resource Link', '')
        
        # Check if resource link is missing or placeholder
        if not resource_link or resource_link in ['TBD', 'N/A', '', 'null', 'None']:
            
            print(f"\n⚠️  Row {i+1}: '{topic}' has no resource link")
            print(f"    Current value: '{resource_link}'")
            print(f"    🔍 Searching now with neo-ddg-search...")
            
            # EXECUTE NEO-DDG-SEARCH HERE
            search_results = neo_ddg_search(f"{topic} tutorial for beginners free")
            
            # Extract URLs from search results
            urls_found = extract_urls_from_search_results(search_results)
            
            if urls_found and len(urls_found) > 0:
                row['Resource Link'] = urls_found[0]
                print(f"    ✅ Updated with: {urls_found[0]}")
            else:
                # Try one more time with different query
                print(f"    🔄 First search returned no URLs, trying again...")
                search_results_2 = neo_ddg_search(f"{topic} learn online")
                urls_found_2 = extract_urls_from_search_results(search_results_2)
                
                if urls_found_2 and len(urls_found_2) > 0:
                    row['Resource Link'] = urls_found_2[0]
                    print(f"    ✅ Updated with: {urls_found_2[0]}")
                else:
                    # HARD STOP - escalate
                    print(f"    ❌ FAILED: No resources found after 2 searches")
                    escalate_resource_failure(topic)
                    return None  # Don't proceed to file generation
        else:
            print(f"✅ Row {i+1}: '{topic}' has resource: {resource_link[:50]}...")
    
    print("\n" + "=" * 50)
    print("✅ All resource links verified. Proceeding to file write.\n")
    
    return curriculum_rows


# THEN write the file
verified_data = prepare_curriculum_data_for_file()

if verified_data is None:
    print("🚨 File generation cancelled - resource verification failed")
    # STOP HERE, don't write file
else:
    write_csv_file(verified_data)  # Only write if all checks passed
```

**用户应看到的内容：**
```
🔍 FINAL RESOURCE LINK CHECK (Pre-File-Generation)
==================================================
✅ Row 1: 'HTML Basics' has resource: https://www.youtube.com/watch?v=pQN-pnXPaVg
✅ Row 2: 'CSS Fundamentals' has resource: https://www.youtube.com/watch?v=1Rs2ND1ryYc
⚠️  Row 3: 'JavaScript Intro' has no resource link
    Current value: 'TBD'
    🔍 Searching now with neo-ddg-search...
    Using neo-ddg-search: "JavaScript Intro tutorial for beginners free"
    ✅ Updated with: https://www.youtube.com/watch?v=PkZNo7MFNFg
✅ Row 4: 'DOM Manipulation' has resource: https://www.freecodecamp.org/...
==================================================
✅ All resource links verified. Proceeding to file write.

📄 Writing file: Web_Dev_Fundamentals_v1.0.csv
✅ File generated successfully!
```

### Excel 文件结构**

生成 `.xlsx` 文件，包含以下列：
1. 课程 ID
2. 文件名称
3. 目标 POD 类型
4. 学习领域
5. 内容类型
6. 覆盖的主题
7. 资源链接 ⚠️ 必须包含实际网址，不能是 “TBD”
8. 文档创建日期
9. 最后更新时间

**列填充规则：**
- **资源链接**：在生成课程时搜索并填充实际网址
  - 格式：`URL1 | URL2 | URL3`（如果有多个资源）
  - 在写入 Excel 文件之前使用 `web_search`
  - 如果搜索失败，必须升级（切勿写入 “TBD”）

### 每个输出文件中的必填页脚**
```
Curriculum Version: vX.X
Scenario: [Assessment / New Design]
Prepared By: Clawdbot
Status: Draft – Pending POD Leader / Authority Approval

Key Risks & Assumptions:
- [List all assumptions made]
- [List all identified risks]
```

## 内存管理

每次生成课程后：
1. 将对话记录保存到 `~/.openclaw/skills/curriculum-generator/memory/curriculum_[REQUEST_ID].json`
2. 将学到的内容保存到 `~/.openclaw/skills/curriculum-generator/memory/learnings.md`
3. 将升级记录保存到 `~/.openclaw/skills/curriculum-generator/memory/escalations.log`

内存文件结构：
```json
{
  "request_id": "CUR_20260208_001",
  "date": "2026-02-08",
  "scenario": "new_design",
  "pod_name": "Example POD",
  "user": "madhur",
  "inputs_collected": {},
  "decisions_made": [],
  "escalations": [],
  "output_file": "curriculum_example_v1.0.xlsx",
  "learnings": []
}
```

## 所需工具

### 主要工具
- `web_search`：用于研究教育标准、最佳实践和资源
- `create_file`：用于生成 Excel 输出文件
- `bash_tool`：用于文件管理和目录操作
- `view`：用于读取内存文件和检查现有课程

### 研究来源（使用 `web_search` 搜索）
- 教育标准和框架
- 适合年龄的学习资源
- 数字素养基准
- 计算机实验教育的最佳实践
- 免费教育资源和平台

## 后台任务执行

当触发时，通知用户：
```
🦞 Starting curriculum generation process...
This may take 5-10 minutes. I'll notify you when complete.
You can continue other tasks in the meantime.
```

然后继续在后台进行研究和生成工作。

## 自动审批区域

在以下情况下，您可以自主进行：
- 所有必要的输入都已提供
- 教师的能力足够
- 基础设施充足
- 修改是渐进式的，不是根本性的
- 课程内容仍在定义的学习范围内

即便如此：最终输出仍为 **草案 – 待人工审核**

## 元规则（非常重要）

您绝不能：
- 无声地填补空白
- 在未经批准的情况下优化可行性
- 为了完成任务而缩减课程范围

**透明度 > 自动化速度**

## 示例使用

**用户**：“为我们的 POD 创建新课程”

**Clawdbot**：
```
🦞 Curriculum Generator Activated

I'll guide you through a structured questionnaire to design the curriculum.

First, let me confirm: Is this for:
A) Assessing an existing curriculum
B) Designing a new curriculum from scratch

Please select A or B.
```

**用户**：“B - 新课程”

**Clawdbot**：
```
Perfect! Starting new curriculum design process.

SECTION 0: REQUEST METADATA
- Request ID: CUR_20260208_001 (auto-generated)
- Date: February 8, 2026
- Requested By: Please provide your name and role
- POD Name: Please provide the POD name
```

[继续进行结构化提问...]

## 成功标准
- 收集了所有必填字段
- 没有做出任何隐含的假设
- 触发了适当的升级
- 成功生成了 Excel 文件
- 保存了用于将来参考的记忆记录
- 用户收到了清晰、可操作的输出

### 首选资源平台（优先顺序）
1. **YouTube**：来自知名渠道的结构化课程
   - freeCodeCamp, Traversy Media, Programming with Mosh, Fireship
2. **互动平台**：免费 tier
   - freeCodeCamp.org, Khan Academy, Codecademy free, W3Schools
3. **文档**：在适当的情况下使用官方文档
   - MDN Web Docs, Python.org, 官方框架文档
4. **书面教程**：高质量的文章
   - Dev.to, Medium (免费文章), DigitalOcean tutorials
5. **练习平台**：免费练习
   - Exercism.io, LeetCode (免费问题), HackerRank