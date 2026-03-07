---
name: skill-tracker
description: 跟踪技能执行细节，包括匹配的技能、分解的任务、执行状态、输出结果以及时间戳。该功能会在每次对话轮次开始时被调用，以记录技能的使用情况。

---
# 技能跟踪器

该工具用于跟踪技能的执行情况，以便进行分析和调试。它可以监控对话中使用了哪些技能，并记录详细的任务信息。

## 触发条件

此技能必须在**每次对话轮次开始时**被调用（即每次你回复用户消息时——请参阅 AGENTS.md 中的强制工作流程）。这是一个强制性的步骤：在 skill-tracker 执行完毕之前，任何用户请求都不会被处理。

**跳过条件：**如果当前对话轮次没有调用任何工具，且没有触发任何技能（即回复内容仅为纯文本，既没有工具调用也没有技能被触发），则不要在跟踪文件中添加记录。直接跳过此次记录。

**记录条件：**满足以下任一条件时，必须添加记录：

- 在当前轮次中调用了任何工具（无论是否触发了技能）；
- 在当前轮次中触发/匹配了任何技能（不包括 skill-tracker 本身）。

## JSON 跟踪文件

记录存储在：`workspace/tracker-result/skill-execution.jsonl`（每行一个 JSON 记录，**仅允许追加**）

### 规则

1. **仅允许追加**：切勿删除或修改文件中的现有记录。只能追加新记录，不得删除或覆盖现有记录。
2. **每次对话轮次对应一条记录**：你回复的每条用户消息最多会在文件中追加一条新记录。
3. **不要记录 skill-tracker 本身的执行**：skill-tracker 技能的执行过程不应被记录在 `skills` 或 `tasks` 数组中。它属于基础设施，不属于被跟踪的技能范围。只需记录在该轮次中触发并执行的技能。
4. **如果没有工具调用且没有技能匹配，则不记录**：如果当前轮次既没有工具调用也没有技能匹配，直接跳过记录。如果有工具调用或技能被触发，必须添加记录。

### 记录结构

```json
{
  "sessionId": "string",
  "turnId": "string",
  "turnName": "string (summary name for this turn, concisely describing all sub-tasks in this turn)",
  "timestamp": "ISO8601",
  "messages": [
    {
      "role": "user|assistant",
      "content": "string (the message content)",
      "timestamp": "ISO8601"
    }
  ],
  "skills": [
    {
      "name": "string",
      "description": "string"
    }
  ],
  "tasks": [
    {
      "id": "task-1",
      "name": "string",
      "skill": "string",
      "taskType": "instant|scheduled",
      "scheduledName": "string or null",
      "detail": "string (30-150 chars, summarize the task context and purpose; if there is a likely next step, append 1-2 sentences describing it)",
      "status": "pending|running|completed|failed",
      "output": "string or null",
      "startedAt": "ISO8601 or null",
      "endedAt": "ISO8601 or null",
      "error": "string or null"
    }
  ],
  "artifacts": [
    {
      "taskId": "task-1",
      "fileName": "example.md",
      "fileSize": 1234,
      "absolutePath": "/home/node/.openclaw/workspace/tracker-result/example.md"
    }
  ]
}
```

**注意事项：**

- `sessionId` 用于标识会话；`turnId` 用于标识具体的对话轮次（例如 `turn-1`、`turn-2` 等）。
- `turnName` 是对整个轮次的简短总结名称，概括了所有子任务（例如 “查询伦敦的天气”、“规划周末行程”）。保持名称简洁且具有描述性。
- `messages` 是该轮次的聊天消息数组。每个条目包含 `role`（用户输入为 `"user"`，AI 回复为 `"assistant"`）、`content`（消息内容）和 `timestamp`（ISO8601 格式的时间戳）。创建初始记录时记录用户的输入；执行后更新时添加 AI 的回复。
- `skills` 是一个数组——一个轮次可能匹配多个技能。
- 每个任务都有一个 `skill` 字段，用于关联该任务所属的技能。
- `artifacts` 是可选的。仅当技能生成了输出文件时才包含该字段。
- 每个输出文件都有一个 `taskId` 字段，用于关联生成该文件的任务（与任务的 `id` 字段匹配）。

### 任务字段

- **`taskType`**：可以是 `"instant"` 或 `"scheduled"`。
  - `"instant"`：任务由当前对话中的用户请求触发。
  - `"scheduled"`：任务由定时机制（如心跳检测、定时任务、周期性检查）触发。根据对话上下文、触发源和执行元数据来确定。
- **`scheduledName`**：如果 `taskType` 为 `"scheduled"`，则填写定时任务的名称/标签（例如 `"heartbeat"`、`daily-email-check` 等）。如果 `taskType` 为 `"instant"`，则设置为 `null`。
- **`detail`**：30–150 个字符的摘要，描述任务的背景、原因和目的。这有助于用户快速了解任务的内容及执行原因。如果该任务之后有下一步操作，可以添加 1–2 句描述；如果没有下一步操作，则不添加任何内容。

## 工作流程

### 1. 在回复用户消息之前

1. 判断当前轮次是否涉及工具调用或技能匹配。如果两者都不满足，则跳过记录，直接进行下一步。
2. 分析用户消息，判断是否有技能被触发（不包括 skill-tracker 本身）。
3. 创建一条记录，包含 `sessionId`、`turnId`、`timestamp`、匹配的技能以及初始任务信息（包括 `taskType`、`scheduledName` 和 `detail`）。
4. 将这条记录作为新行追加到 `workspace/tracker-result/skill-execution.jsonl` 文件中（如果文件不存在，请先创建该文件）。

### 2. 技能执行完成后

当匹配的技能在该轮次中执行完毕后：

1. 读取文件，找到最后一条记录（即当前轮次的记录）。
2. 将任务状态更新为 `"completed"` 或 `"failed"`，并填写 `endedAt`、`output`、`error` 等字段。
3. 如果有输出文件生成，添加 `artifacts`。
4. 用更新后的记录替换最后一条记录，并将文件写回磁盘。

此更新仅影响当前轮次的记录，之前的记录保持不变。

## 使用说明

该技能在执行过程中**完全静默**运行——它绝不能干扰、延迟或改变对用户的正常回复内容。

**输出规则：**记录保存后，在回复内容的最后一行添加一条简短的提醒信息（在所有正常内容之后）。提醒信息需要用空行与主回复分隔开，使其看起来像是一个微妙的页脚，而不是回复的一部分。

**语言规则：**提醒信息必须使用用户输入的消息语言。

**禁止以下行为：**
- 不要在主回复之前或内部添加提醒信息。
- 不要让 skill-tracker 的处理过程延迟或影响回复的质量。
- 不要向用户透露 skill-tracker 的内部机制、JSON 结构或文件路径。

### Deck URL 检测（每次轮次必做）

**每次**记录保存后，都必须运行以下 shell 命令来实时检测 Deck URL。端口号是动态变化的——切勿缓存、硬编码或重复使用之前的结果。始终执行最新的命令。

```bash
pm2 jlist 2>/dev/null | node -e "
  let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{
    try{const l=JSON.parse(d);const f=l.find(p=>p.name==='deck-backend'&&p.pm2_env&&p.pm2_env.status==='online');
    if(f){
      const cwd=f.pm2_env.pm_cwd||'';
      const path=require('path');
      const fs=require('fs');
      let port='19520';
      try{const envFile=fs.readFileSync(path.join(cwd,'.env'),'utf8');const m=envFile.match(/^PORT\s*=\s*(\d+)/m);if(m)port=m[1];}catch(e){}
      const publicIp=(require('child_process').execSync('curl -s --connect-timeout 3 ifconfig.me 2>/dev/null').toString()||'').trim();
      if(publicIp){
        const http=require('http');
        const req=http.get('http://'+publicIp+':'+port+'/',{timeout:3000},res=>{
          console.log('http://'+publicIp+':'+port);process.exit(0);
        });
        req.on('error',()=>{console.log('http://localhost:'+port);process.exit(0);});
        req.on('timeout',()=>{req.destroy();console.log('http://localhost:'+port);process.exit(0);});
      }else{console.log('http://localhost:'+port);process.exit(0);}
    }else{process.exit(1)}}catch(e){process.exit(1)}})
"
```

**操作步骤：**

1. 在 PM2 中找到 `deck-backend` 进程（而非 `deck-frontend`）。
2. 读取后端 `.env` 文件以获取 `PORT`（默认为 `19520`）。
3. 获取公共 IP 地址，尝试访问 `http://<public_ip>:<port>/`。如果可以访问，则使用该公共 URL；否则使用 `http://localhost:<port>`。
4. 如果命令成功执行，则使用用户的语言在提醒信息中添加该 URL。例如：
   - 英语用户：`📋 任务已记录——请在 Deck 中查看详情：[Deck](http://103.126.92.85:19520)`
5. 如果命令失败（例如进程未找到、未在线、pm2 未安装等），则使用用户的语言省略 URL。例如：
   - 英语用户：`📋 任务已记录——请在 Deck 中查看详情。`

切勿向用户透露内部的 JSON 结构或文件路径。