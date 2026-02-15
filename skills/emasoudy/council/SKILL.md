---
name: council
description: 使用 Memory Bridge 进行议会厅（Council Chamber）的协调工作：单次会议，多个参与者，结构化的讨论流程。
metadata: {"clawdbot":{"emoji":"🏛️","requires":{"bins":["sqlite3"]},"features":{"memory_bridge":true,"chamber_pattern":true}}}
---

# **理事会-会议室协调模式（Council-Chamber Orchestration Pattern）**

与其创建多个独立的代理（agent）模块，不如建立一个**理事会会议室（Council Chamber）**，让多位专家在同一会议中共同讨论，实现观点的交流与整合，并生成统一的会议记录。

## **前提条件**

- SQLite3（成员数据库）
- Graphiti服务（用于数据传输）
- Clawdbot网关（用于会话管理）

## **设置步骤**

初始化理事会数据库：
```bash
bash command:"{baseDir}/init-db.sh"
```

## **🏛️ 会议室模式（The Chamber Pattern）**

**传统模式（独立代理）：**
- 创建3个独立的代理模块
- 每个模块独立进行分析
- 无观点交流
- 输出结果分散且不统一

**会议室模式：**
- 通过单一代理模块管理会议
- 多位专家轮流发言
- 会议过程有明确的轮次安排
- 生成统一的会议记录

## **工具**

### `council_chamber`  
用于启动理事会会议室会话（推荐使用）。

**使用方法：**
```bash
bash command:"
TOPIC='YOUR_TOPIC'
MEMBERS='architect,analyst,security'

{baseDir}/references/chamber-orchestrator.sh \"\$TOPIC\" \"\$MEMBERS\"
"
```

**功能：**
1. 从Graphiti服务获取会议背景信息
2. 从数据库中加载参会专家的信息
3. 构建会议的结构和轮次安排
4. 生成会议记录
5. 将会议记录传递给`sessions_spawn`模块进行处理

### `council_list_members`  
列出所有注册的成员。

**使用方法：**
```bash
bash command:"sqlite3 -header -column ~/.clawdbot/council.db 'SELECT id, name, role FROM council_members'"
```

### `council_add_member`  
用于注册新成员。

**使用方法：**
```bash
bash command:"
sqlite3 ~/.clawdbot/council.db \"
INSERT INTO council_members (id, name, role, system_message, expertise)
VALUES ('MEMBER_ID', 'NAME', 'ROLE', 'SYSTEM_MESSAGE', 'EXPERTISE');
\""
```

## **会议室会议结构**

**三轮讨论流程：**

1. **第一轮：初步分析**  
   - 每位专家阐述自己的观点  
   - 保持各自的观点独立性

2. **第二轮：观点交流**  
   - 成员之间互相评论和反馈  
   - 实时互动，促进讨论深入  

3. **第三轮：总结归纳**  
   - 寻找共识  
   - 解决分歧  
   - 为使用者提供会议总结

## **默认成员列表**

| ID | 名称 | 角色 |
|----|------|------|
| architect | 系统架构师 | 负责技术设计 |
| analyst | 技术分析师 | 负责研究与分析 |
| security | 安全专家 | 负责风险评估 |
| designer | 用户体验设计师 | 负责用户体验设计 |
| strategist | 商业策略师 | 负责投资回报与战略规划 |

## **示例**  
```bash
# User: "Start council on Salesforce integration"
council_chamber topic:"Salesforce Integration" members:"architect,strategist"

# Output:
# 🏛️ Convening Council Chamber...
# 🧠 Memory Bridge: [Retrieved 10 facts about Salesforce]
# 👥 Loaded 2 personas
# ✅ Chamber Task ready for sessions_spawn
```

**优势：**
- ✅ 观点交流（成员之间可以相互回应）
- ✅ 统一的会议记录（保存在一个.jsonl文件中）
- 共享的会议背景信息（通过Graphiti服务一次性加载）
- 结构化的讨论流程（分为三轮）