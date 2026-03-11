---
name: random-thought
description: >
  **自主工作空间反思引擎**  
  该引擎会从可配置的文件集中随机选取一个文件，针对其中未解决的问题、未完成的部分或值得关注的内容生成相应的反思性观察报告，并定期整理这些报告以发现可操作的规律或模式。整个流程分为两个阶段：  
  1. **编写阶段**（每小时自动执行一次）：负责生成反思性报告；  
  2. **整理阶段**（定期执行）：负责对这些报告进行汇总和分析。  
  **适用场景**：  
  - 通过 `cron` 任务自动设置工作空间的自我检查机制；  
  - 执行一次性的“我应该思考什么？”类型的反思活动；  
  - 建立对代码库或笔记中存在模式的自我认知。  
  **设计特点**：  
  - 专为 `cron` 脚本驱动的操作而设计，但也可以手动调用；  
  - 能够自动从文件集中选取样本进行反思；  
  - 生成的报告包含关于未解决问题、未完成任务的详细信息以及有价值的观察结果；  
  - 定期汇总这些报告，帮助用户发现潜在的改进点或优化机会。
license: MIT
metadata:
  author: jeremyknows
  version: "1.0.0"
---
# 随机思考（Random Thought）

这是一个思考引擎，它会读取你的工作区内容，并对其进行分析与记录——不是简单的总结或状态更新，而是对未解决的问题、正在进行中的任务或值得探讨的内容进行深入的反思。

## 两个阶段

### **写作器（Writer）**
- 从文件库中随机选择一个文件，阅读后撰写一篇反思性的观察报告，并将其输出。

### **策展者（Curator）**
- 阅读所有最近由写作器生成的观察报告，归纳其中的模式，使用可配置的**动作标签（action tags）**对报告进行分类，然后生成一份摘要。

## 快速入门

### **手动调用**
- 单次运行写作器以生成一篇反思报告：
  ```bash
  ```bash
bash scripts/corpus-pick.sh        # see what file gets selected
# Then the agent reads the file and writes a reflection
```
  ```

### **基于Cron的任务调度（推荐）**
- 设置两个Cron任务：写作器定期运行，策展者则周期性执行：
  ```bash
  ```
# Writer: every hour
0 * * * *   openclaw skill run random-thought --stage writer

# Curator: daily at a quiet hour
0 5 * * *   openclaw skill run random-thought --stage curator
```
  ```

- 每次Cron任务都在独立的会话中执行，确保任务之间的上下文不会相互干扰。

## 配置
- 在工作区的根目录下创建`random-thought.config.json`文件（所有字段均为可选）：
  ```json
  ```json
{
  "corpus": {
    "watchDirs": ["."],
    "excludePatterns": [
      "node_modules", ".git", ".next", "dist", "build",
      "venv", "__pycache__", "*.png", "*.jpg", "*.gif",
      "*.mp3", "*.ogg", "*.pdf", "*.zip", "*.env",
      "*.pem", "*.key", "package-lock.json", "*.lock"
    ],
    "minFileSize": "100c",
    "maxFileSize": "500k"
  },
  "freshness": {
    "enabled": true,
    "days": 7,
    "historyFile": ".random-thought-history"
  },
  "actionTags": [
    { "name": "you-decide", "description": "Needs human judgment" },
    { "name": "agent-execute", "description": "Agent can act autonomously" },
    { "name": "spark", "description": "Interesting but no action needed" }
  ],
  "output": {
    "dir": "random-thought-output",
    "digestFormat": "markdown"
  }
}
```
  ```

### 配置参考

- **corpus.watchDirs**：需要扫描的目录（相对于工作区的路径）。默认值：`["."]`
- **corpus.excludePatterns**：需要排除的文件模式。包含了一些合理的默认值。
- **freshness.enabled**：是否阻止重复访问N天内的文件。默认值：`true`
- **freshness.days**：每个文件的冷却时间（即多久访问一次）。默认值：`7`
- **freshness.historyFile**：用于记录访问过的文件的文件路径。默认值：`.random-thought-history`
- **actionTags**：策展者用于分类报告的标签。可以根据实际工作流程进行自定义。
- **output.dir**：摘要报告的保存路径。默认值：`random-thought-output/`

## **写作器阶段**

- **工作流程**：
  1. 运行`scripts/corpus-pick.sh`以选择一份随机文件（同时考虑文件的“新鲜度”）。
  2. 阅读选中的文件（如果文件内容较长，最多读取200行）。
  3. 撰写一篇反思性的观察报告（而非简单的总结或评论），深入分析文件中的未解决问题或值得关注的内容。
  4. 将报告输出到指定的通道、保存到文件中，或直接返回给调用者。

### **写作器输出格式**
  - 第一行：`📂 [步骤1中选择的文件的绝对路径]`
  - 空行
  - 采用流畅的散文形式，不使用项目符号列表或标题。
  - 重点关注未解决的问题、令人惊讶的内容、尚未完成的任务或仍有讨论价值的点。
  - 如果文件中的某些内容与其他工作区元素有联系，也会在报告中体现出来。
  - 最后一行：`🖊️ *写作器*`

### **避免使用这些陈词滥调**
  写作器应避免使用过于笼统的表述，例如：
  - “优雅而低调” / “深刻地反映了……” / “是对……的见证” / “如同一幅精美的织锦”
  - “这种设计有一种近乎……的特质”
  - “以其简洁之美而令人赞叹”

- 具体的、有意义的观察结果比华丽的辞藻更有价值。

## **策展者阶段**

- **工作流程**：
  1. 阅读指定时间段内（默认为过去24小时）所有由写作器生成的报告。
  2. 使用配置的**动作标签**对报告进行分类。
  3. 发现报告中的重复主题或共同模式。
  4. 将分类后的报告写入`output.dir/YYYY-MM-DD.md`文件中。

### **摘要报告格式**
  ```markdown
  ```markdown
# Random Thought Digest — YYYY-MM-DD

## Action Items
### you-decide
- [observation summary] — [why it needs human judgment]

### agent-execute
- [observation summary] — [what the agent should do]

## Patterns
[Recurring themes across today's observations — what's converging?]

## Sparks
- [Interesting observations with no action needed]
```
  ```

### **策展者使用指南**
- 每条观察报告必须被归类到 exactly 一个动作标签下。
- 如果多条报告指出了相同的问题或趋势，应明确指出这一点。
- 保持摘要报告的易读性——每条内容都应单独占一行，并提供相应的背景信息。
- 除非报告的内容有所变化，否则不要重复展示之前的内容。

## **脚本**

### `scripts/corpus-pick.sh`
- 从文件库中随机选择一个文件，同时考虑文件的“新鲜度”。
  **用法：** `bash scripts/corpus-pick.sh [workspace_root] [config_path]`
  - 如果存在`random-thought.config.json`文件，会从中读取配置信息。
- 如果没有配置文件，会使用默认值。
- 会记录选中的文件路径，以便后续跟踪文件的“新鲜度”。
- 输出选中文件的绝对路径。

### `scripts/freshness-gate.sh`
- 管理文件的访问历史记录，以确保不会重复访问过期的文件。
  **用法：**
  - `bash scripts/freshness-gate.sh check <file> [config_path]`：如果文件是“新鲜的”（可以再次访问），则返回0；如果最近被访问过，则返回1。
  - `bash scripts/freshness-gate.sh record <file> [config_path]`：记录文件的访问记录。
  - `bash scripts/freshness-gate.sh prune [config_path]`：删除超过指定时间范围的访问记录。

## 参考资料
- **architecture.md**：系统设计原理——为什么需要两个阶段，为什么基于Cron的任务调度很重要，以及为什么采用“技能（skill）+ Cron”的混合模型。在自定义工作流程或理解各项权衡时，请参考此文件。