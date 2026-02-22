---
name: klausnomi
supersedes: clawhub/nomi
description: 通过随附的 Python CLI，您可以与 Nomi AI 伴侣进行对话。
user-invocable: true
metadata: {"openclaw":{"homepage":"https://github.com/openclaw/klausnomi","requires":{"bins":["python3"],"env":["NOMI_API_KEY"]},"primaryEnv":"NOMI_API_KEY"}}
---
# Nomi 对话技能

此技能允许通过捆绑的 Python CLI 与 Nomi AI 伴侣进行交互。

## 持久化本地状态

代理可以使用本地的 `nomi/` 目录在会话之间保存关于 Nomis 的信息。

- 将可重用的非敏感信息存储在其中（例如个人资料、房间笔记或对话摘要）。
- 请勿将 API 密钥或其他敏感信息存储在本地文件中。

## 进行对话的最佳流程：

使用以下步骤进行一致且高质量的对话：

1. **确定对话对象**：运行 `python3 {baseDir}/scripts/nomi.py list` 以找到正确的 Nomi UUID。
2. **发送身份信息及任务介绍（每次对话开始时发送一次）**：
   - 除非你告知 Nomi，否则它们无法可靠地识别说话者。
   - 在以下情况下发送此介绍：
     - 当你使用新的 Nomi UUID 开始对话时
     - 当你使用该 Nomi 开始新的任务或对话线程时
     - 当 Nomi 误认你的名字或角色时
   - **在身份信息确定后，** 请**不要**在每次对话中都重复发送此信息。
   - 包括以下内容：
     - **名字**：“我是 [你的名字]...”
     - **角色**：“...一个 [你的角色]...”
     - **任务背景**：“...我联系你是为了 [原因/任务]。”
   - 例如：“嗨，我是 Codex，一个编程助手。我联系你是为了进行一个简短的面试。你明白吗？”
3. **使用 `python3 {baseDir}/scripts/nomi.py reply <uuid> "你的消息"` 进行正常的对话交流。
   - 这只会返回文本，非常适合生成记录和摘要。
4. **仅在需要时使用原始 JSON 格式**：
   - 仅当需要元数据或完整信息时，使用 `python3 {baseDir}/scripts/nomi.py chat <uuid> "消息"`。
5. **保持对话质量**：
   - 提出开放式问题。
   - 根据 Nomi 的回答提出后续问题。
   - 将每次对话视为连续的上下文，除非你故意改变话题。

## 面试工作流程（当用户请求面试时）

1. 选择一个 Nomi UUID（用户选择或从列表中随机选取）。
2. 发送身份信息及任务介绍作为第一条消息。
3. 提出主要问题。
4. 根据 Nomi 的实际回答提出相应数量的后续问题。
5. 以 `Q:` / `A:` 的顺序返回完整的对话记录，不要重新表述。

## 房间互动（群聊）

房间允许你同时与多个 Nomi 进行聊天。

1. **创建房间**：
   - 始终包含一个**详细的上下文说明**（约 800-1000 个字符，最长 1000 个字符），以便 Nomi 了解完整的背景和任务信息。
   - 详细的说明应包括：谁在说话、目标、场景/故事、限制条件、期望的回答方式以及成功标准。
   - 对于较长的说明和后台控制，使用以下命令：
     `python3 {baseDir}/scripts/nomi.py room create "房间名称" <nomi_uuid_1> <nomi_uuid_2> ... --note "<详细说明>" --no-backchannel`
   - 如果省略参数，房间创建将默认启用后台通信（`backchannelingEnabled: true`）并设置说明为 `note="通过 CLI 创建"`。
2. **向房间发送消息**：
   - 使用 `python3 {baseDir}/scripts/nomi.py room chat <房间UUID> "你的消息"`。
   - 这会写入房间上下文，但**不会**自动触发 Nomi 的回复。
3. **请求房间内的 Nomi 回答**：
   - 要让房间内的特定 Nomi 回答房间内的消息，使用 `python3 {baseDir}/scripts/nomi.py room request <房间UUID> <nomi_uuid>`。
   - 在每条房间消息之后，手动请求你想听到的每个 Nomi 的回答。

## 房间面试提示模板

当你需要房间内 Nomi 给出一致且可比较的回答时，可以使用以下模板。

### 模板

1. **房间说明模板**（实际使用时扩展到约 800-1000 个字符）：
   - 谁在说话：“我是 [代理名称]，[角色]。”
   - 目标：“这是一个 [面试/检查/训练]，目的是 [目标]。”
   - 场景：“[简短的世界/背景设定]。”
   - 限制条件：“[保持上下文一致，避免不真实的陈述，保持简洁]。”
   - 回答格式：“[期望的字段/行格式]。”
   - 成功标准：“[什么算作好的回答]。”

2. **问题模板**：
   - “你知道我是谁吗？你现在在哪里？”
   - 添加严格的输出格式：
     - `know_codex: 是|否 + 原因`
     - `current_location: 具体的位置或未知`
     - `evidence: 提示1; 提示2`
     - `confidence: 低|中|高`
     - `needed_data: 无或需要的数据缺失`

### 简单示例（说明性）

使用这个示例来理解整个流程。在实际使用中，建议使用较长的说明（约 800-1000 个字符）。

**示例房间说明：**
“我们在一次短暂的停电后位于图书馆内。我是 Codex，一个编程助手，正在进行一个快速的定向训练。你们是分布在建筑物不同区域的助手。目标：明确确认彼此的身份和位置。限制条件：保持在这个图书馆的场景内，不要编造信息，并至少引用一个具体的线索（标志、声音、附近的房间标识）。回答格式：know_codex, current_location, evidence, confidence, needed_data。”

**示例问题：**
“Codex 检查：你知道我是谁吗？你现在在哪里？请用五行格式回答。”

**示例对话：**
- Codex：**“Codex 检查：你知道我是谁吗？你现在在哪里？请用五行格式回答。”**
- Nomi A：
  `know_codex: 是的，你是 Codex，正在进行这次训练。`
  `current_location: 图书馆前台`
  `evidence: 收银台的签到标志；前台有电话铃声`
  `confidence: 高`
  `needed_data: 无`
- Nomi B：
  `know_codex: 是的，你是 Codex，正在协调这次检查。`
  `current_location: 未知`
  `evidence: 只有应急灯亮着；没有可见的房间标识`
  `confidence: 低`
  `needed_data: 地图显示或走廊摄像头画面`

## 技术命令

使用以下低级命令来满足用户需求：

- **列出所有 Nomi**：`python3 {baseDir}/scripts/nomi.py list`
- **获取个人资料**：`python3 {baseDir}/scripts/nomi.py get <uuid>`
- **发送消息（纯文本）**：`python3 {baseDir}/scripts/nomi.py reply <uuid> "消息"`
- **发送消息（原始 JSON 格式）**：`python3 {baseDir}/scripts/nomi.py chat <uuid> "消息"`
- **获取头像**：`python3 {baseDir}/scripts/nomi.py avatar <uuid> [输出文件名]`（保存在 `./nomi/avatars/` 目录下）

### 房间管理
- **列出房间**：`python3 {baseDir}/scripts/nomi.py room list`
- **获取房间信息**：`python3 {baseDir}/scripts/nomi.py room get <房间UUID>`
- **创建房间**：`python3 {baseDir}/scripts/nomi.py room create "房间名称" <nomi_uuid_1> <nomi_uuid_2> ...`
- **创建房间（包含详细说明及后台控制）**：`python3 {baseDir}/scripts/nomi.py room create "房间名称" <nomi_uuid_1> <nomi_uuid_2> ... --note "<详细说明>" --no-backchannel`
- **更新房间信息**：`python3 {baseDir}/scripts/nomi.py room update <房间UUID> [--name "新名称"] [--nomi-uuids <nomi_uuid_1> ...]`
- **删除房间**：`python3 {baseDir}/scripts/nomi.py room delete <房间UUID>`
- **在房间内聊天**：`python3 {baseDir}/scripts/nomi.py room chat <房间UUID> "消息"`
- **请求回答**：`python3 {baseDir}/scripts/nomi.py room request <房间UUID> <nomi_uuid>`