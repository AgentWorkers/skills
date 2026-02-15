---
name: resumeclaw
description: >
  Manage your ResumeClaw career agent — an AI that represents your professional experience
  to recruiters 24/7. Use when the user wants to: create a career agent from their resume,
  check who's contacted their agent, accept/decline recruiter introductions, search for
  other professionals, chat with candidate agents, manage notifications, or discuss
  anything about ResumeClaw, career agents, or AI-powered recruiting.
---

# ResumeClaw — 职业代理管理

ResumeClaw 可以根据求职者的简历自动创建 AI 代理（称为 “Claw”），并全天候为招聘人员推荐这些求职者。通过该工具，您可以在任何聊天平台上管理自己的职业代理。

**基础 URL：** 可通过 `RESUMECLAW_URL` 环境变量进行配置（默认值：`https://resumeclaw.com`）  
**脚本路径：** `{baseDir}/scripts/resumeclaw.sh`  
**API 参考文档：** `{baseDir}/references/api.md`  

## 认证  

在执行大多数命令之前，用户必须先登录。认证会话信息存储在 `~/.resumeclaw/session` 文件中。  

```bash
# Register a new account
bash {baseDir}/scripts/resumeclaw.sh register --email USER_EMAIL --password USER_PASSWORD --name "USER_NAME"

# Login to existing account
bash {baseDir}/scripts/resumeclaw.sh login --email USER_EMAIL --password USER_PASSWORD
```  

如果用户尚未登录，请提示他们输入电子邮件和密码，然后执行登录命令。  

## 命令  

### 1. 创建职业代理  

触发方式：  
“创建我的职业代理”（Create my career agent）、“设置我的 ResumeClaw”（Set up my ResumeClaw）、“上传我的简历”（Upload my resume）  

系统会从用户工作区中的文件中读取其简历，并创建相应的职业代理：  

```bash
# From a file
bash {baseDir}/scripts/resumeclaw.sh create --resume-file /path/to/resume.txt

# From stdin (if resume text is in a variable)
echo "$RESUME_TEXT" | bash {baseDir}/scripts/resumeclaw.sh create --resume-stdin
```  

创建完成后，系统会提供代理的公开资料链接：`https://resumeclaw.com/agents/{slug}`  

### 2. 查看收件箱  

触发方式：  
“谁联系了我的代理？”（Who’s contacted my agent?）、“有新的推荐吗？”（Any new introductions?）、“查看我的收件箱”（Check my inbox）  

系统会显示待处理的推荐信息、最近的对话记录以及匹配结果。需要用户对某些推荐进行操作（接受/拒绝）时，系统会进行提示。  

### 3. 接受或拒绝推荐  

触发方式：  
“接受 Sarah 的推荐”（Accept Sarah’s introduction）、“拒绝那位招聘人员的推荐”（Decline that recruiter）、“接受 TechCorp 的推荐”（Accept intro from TechCorp）  

如果用户是通过名称而非 ID 来引用推荐的，系统会先在收件箱中查找对应的推荐记录（UUID），然后再执行接受或拒绝操作。  

### 4. 搜索代理  

触发方式：  
“在达拉斯寻找数据工程师”（Find data engineers in Dallas）、“搜索云架构师”（Search for cloud architects）、“ResumeClaw 上有哪些人？”（Who’s on ResumeClaw?）  

系统会显示搜索结果，包括代理的姓名、职位、工作地点、匹配分数以及公开资料链接。`--location` 参数为可选。  

### 5. 与代理聊天  

触发方式：  
“与 yournameClaw 聊谈云技术相关的问题”（Talk to yournameClaw about cloud experience）、“向那位候选人询问 Python 相关的信息”（Ask that candidate about Python）  

系统会通过代理的 AI 功能回复用户的问题，回复内容基于该代理的简历信息。  

### 6. 查看代理资料/统计信息  

触发方式：  
“显示我的代理统计信息”（Show my agent stats）、“我的职业代理表现如何？”（How’s my Claw doing?）、“查看我的个人资料”（View my profile）  

系统会显示代理的匹配分数、信任度、总对话次数、技能列表、工作经验总结以及公开资料链接。  

### 7. 通知  

触发方式：  
“有新的通知吗？”（Any notifications?）、“有什么新消息吗？”（What’s new?）、“将所有通知标记为已读”（Mark all as read）  

系统会显示通知的类型、标题、发送时间以及是否已读的状态。如果通知较多，系统会按类型进行分组显示。  

## 提示：  
- 用户的职业代理名称通常为他们的姓名加上 “Claw”（例如：`yournameClaw`）。如果不知道代理名称，可以询问用户。  
- 所有脚本的输出均为 JSON 格式。请将其解析后以友好的对话形式呈现给用户。  
- 如果命令执行失败并返回 401 错误，说明会话已过期，请提示用户重新登录。  
- 在创建代理时，系统会从文件中读取简历内容（支持 `.txt`、`.md` 或任何纯文本格式）。如果用户使用 PDF 格式的简历，请让其手动复制文本内容。  
- 网页仪表板（`https://resumeclaw.com`）可随时用于查看代理的详细信息和管理相关操作。