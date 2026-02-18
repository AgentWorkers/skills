---
name: wilma-triage
version: 1.0.1
description: >
  **每日为芬兰家长整理Wilma学校的通知**：  
  该功能会收集考试信息、消息、新闻、课程安排以及作业内容，筛选出需要家长处理的紧急事项，将考试安排同步到Google日历中，并通过聊天工具向家长发送报告。  
  **所需技能与工具**：  
  - `wilma`技能  
  - `gog` CLI（或通过ClawHub提供的`gog`技能）——用于访问日历功能。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["wilma", "gog"],
            "skills": ["wilma"],
            "configPaths":
              [
                "~/.config/wilmai/config.json",
                "~/Library/Application Support/gogcli/",
              ],
          },
        "credentials":
          {
            "note": "Requires local Wilma credentials (~/.config/wilmai/config.json) for school data access and gog CLI auth (Google OAuth) for calendar sync. Both must be set up interactively before use.",
          },
      },
  }
---
# Wilma 数据分类与通知系统

该系统自动每日对 Wilma 学校的数据进行分类处理，以便家长获取重要信息。系统会过滤掉无关信息，突出显示需要处理的事件，并将考试或活动信息同步到 Google 日历中。

## 所需依赖组件

- **wilma skill**：通过 ClawHub 安装（命令：`clawhub install wilma`），用于使用 Wilma 的命令行工具（CLI）进行数据管理。
- **gog skill**：通过 ClawHub 安装（命令：`clawhub install gog`），用于与 Google 日历进行数据同步。

## 首次使用时的设置步骤

首次使用时，请收集并保存以下配置信息：

1. **获取学生信息**：运行 `wilma kids list --json` 命令，获取学生的姓名、学号及所在学校。
2. **选择日历**：运行 `gog calendar calendars` 命令，列出可用的日历。询问用户希望使用哪个日历来记录学校活动，并将日历 ID 保存到 `TOOLS.md` 文件的 `## Wilma Triage` 部分中，同时记录事件的命名规则。
3. **个性化设置**：询问用户是否有任何特定的规则（例如，某些科目的通知优先级高于其他科目）。将这些规则保存到 `MEMORY.md` 文件中，作为数据分类的参考。

随着使用时间的增加，用户可以提供关于哪些信息需要报告、哪些信息可以忽略的反馈，这些设置会自动更新到 `MEMORY.md` 文件中，从而提升系统的智能程度。

## 工作流程

1. **获取学生信息**：查看 `TOOLS.md` 文件中的学生详细信息，然后开始数据分类：
   ```bash
   # Best starting point — returns schedule, exams, homework, news, messages
   wilma summary --all-students --json

   # Drill into specifics as needed
   wilma exams list --all-students --json
   wilma schedule list --when today --all-students --json
   wilma schedule list --when tomorrow --all-students --json
   wilma homework list --all-students --limit 10 --json
   wilma grades list --all-students --limit 5 --json
   wilma messages list --all-students --limit 10 --json
   wilma news list --all-students --limit 10 --json

   # Read full content when subject line looks actionable
   wilma messages read <id> --student <name> --json
   wilma news read <id> --student <name> --json
   ```

2. **应用分类规则**：根据预设的分类规则以及 `MEMORY.md` 文件中的个性化设置对信息进行筛选。
3. **同步日历**：使用 `TOOLS.md` 文件中的 `gog CLI` 命令，将缺失的考试信息或需要处理的活动添加到 Google 日历中。
   - **添加新事件前务必检查日历中是否已有相同内容，以避免重复**。
   - 请严格按照 `TOOLS.md` 文件中规定的命名规则来命名事件。
   - 从日历中删除已取消的活动。

4. **发送通知**：如果发现需要处理的活动，请发送详细信息；如果没有需要处理的内容，可以选择不发送通知或发送简短确认信息。请根据用户设置的偏好来决定是否发送通知。

## 日历同步

具体操作方法请参考 `TOOLS.md` 文件中的日历 ID、命名规则及 `gog CLI` 命令。

**避免重复规则：**
- 在添加任何事件之前，请先检查日历中该日期范围内是否已有相同事件。
- 如果存在相同日期、学生和科目关键词的事件，请跳过该事件。
- 只有在日历中不存在该事件时才添加新事件。

## 理解 Wilma 发送的消息类型

Wilma 发送的消息来源多样，其重要性与信息的“信号强度”（即信息的实际价值）也各不相同。正确区分这些消息类型对于有效的数据分类至关重要：

- **Viikkoviesti（每周通讯）**：来自班主任的消息，具有很高的信息价值。这些通讯虽然看起来像普通的新闻简报，但实际上经常包含重要的通知内容（如即将到来的考试、需要携带的资料、课程安排变更、郊游信息等）。**务必阅读全部内容**，切勿仅根据邮件标题就忽略它们。
- **教师消息**：通常涉及具体的考试、作业或班级活动，信息价值较高。
- **学校办公室消息**：包含课程安排变更、活动通知、政策更新等行政信息，信息价值中等。请快速浏览以获取关键信息。
- **Kuukausitiedote（月度通讯）**：来自学校办公室的月度公告，通常包含重要的日期信息（如节假日、学年开始/结束时间、活动安排、报名截止日期等）。请务必阅读这些通讯。
- **全市性通知**：来自赫尔辛基市政府或相关部门的通知，多为健康宣传、交通信息或调查内容，对于日常数据分类来说属于“噪音”信息。请快速浏览标题，除非内容明确需要处理，否则可以忽略。
- **家长协会消息**：默认信息价值较低（如筹款活动、志愿者招募等）。不过，如果用户积极参与家长协会的活动，这些通知的优先级会提高。

**经验法则：**
- 如果消息来自教师（班主任或学科教师），请务必阅读。
- 如果消息来自学校办公室或市政府，只需快速浏览标题，除非内容明确需要处理，否则可以忽略。

## 分类规则

### **必须报告（需要立即处理）**：
- 需要填写的表格、授权表格或回复请求。
- 截止日期（如报名截止时间、费用支付、需要携带的资料）。
- 课程安排变更（如提前放学、课程取消、代课安排）。
- 特殊装备或资料的需求（例如“请携带滑雪装备”、“户外服装”）。
- 孩子可能感兴趣的课后活动（如迪斯科派对、电影之夜）。
- 考试安排更新或新增考试信息。
- 日历中已标记为取消的活动——请将其从日历中删除。

### **简要报告（值得提及）**：
- 郊游信息、有具体日期安排的特别活动。
- 学校关闭或假期安排变更。
- 健康相关通知（如虱子预警、疾病爆发）。
- 新成绩更新（简要提及成绩情况）。

### **重要提示：务必阅读每周通讯（Viikkoviesti）**
班主任发布的每周通讯中通常包含许多重要的通知内容（如考试信息、需要携带的资料、课程安排变更等）。**务必阅读每周通讯的全部内容**，切勿仅根据标题就忽略它们。

### **可以忽略的信息**：
- 音乐会、文化表演（仅供参考）。
- 通用的“欢迎回来”或季节性问候。
- 全市性的信息通知（如健康宣传、交通信息、调查问卷）。
- 家长协会的消息（除非用户积极参与协会活动——请查看 `MEMORY.md` 文件中的设置）。

**请查看 `MEMORY.md` 文件，了解用户根据使用经验提供的额外忽略/报告规则（例如某些科目的通知优先级调整、学校特定的筛选条件）。**

## 建议的 Cron 任务调度设置

建议每天在当地时间 07:00 作为独立任务运行该脚本。为避免 API 使用频率限制，建议与其他早晨任务（如 07:05 的邮件检查任务）错开执行时间。

## 输出格式示例

```
📚 Wilma Update

Child A (8th grade)
• Math exam tomorrow — yhtälöt, kpl 1-8
• Friday short day (9:20-12:35) — kulttuuripäivä, bring laptop + outdoor clothes

Child B (6th grade)
• No actionable items

📅 Calendar: Added Child A math exam (Feb 10), removed cancelled disco (Feb 11)
```

请保持输出信息简洁，每条信息占用一行。保持沉默总比发送不必要的信息要好。