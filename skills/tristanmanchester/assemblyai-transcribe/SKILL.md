---
name: assemblyai-transcribe
description: 使用 AssemblyAI 进行音频/视频的转录、录音、翻译、后期处理以及结构化处理。当用户需要 AssemblyAI 的特定功能时，例如从本地文件或 URL 中获取高质量的语音转文本服务、识别说话者身份、进行语言检测、添加字幕、提取段落或句子内容、分析主题/情感信息，或者希望获得适合 AI 工作流程的转录结果（格式为 Markdown 或标准化 JSON）时，可利用此技能。
compatibility: Requires Node.js 18+ with internet access and ASSEMBLYAI_API_KEY. Optional ASSEMBLYAI_BASE_URL / ASSEMBLYAI_LLM_BASE_URL for EU routing.
metadata:
  author: OpenAI
  version: "2.0.0"
  homepage: https://www.assemblyai.com/docs
  clawdbot:
    skillKey: assemblyai
    emoji: "🎙️"
    requires:
      bins:
        - node
      env:
        - ASSEMBLYAI_API_KEY
    primaryEnv: ASSEMBLYAI_API_KEY
---
# AssemblyAI转录、语音理解以及适用于智能代理的输出格式

当用户需要使用**AssemblyAI**而非通用转录服务时，或者当任务需要利用AssemblyAI的特定功能时（例如：  
- 在`universal-3-pro`和`universal-2`模型之间进行模型路由选择  
- 语言检测与代码切换  
- 语音记录功能以及**说话者名称/角色映射**  
- 翻译、自定义格式化或AssemblyAI说话者识别  
- 字幕、段落、句子的处理  
- 以Markdown或标准化JSON格式输出转录结果，便于其他智能代理使用），请使用此技能。  

该技能专为OpenClaw等AI代理设计，而不仅仅是终端用户。它提供了以下功能：  
1. 一个无依赖性的Node CLI工具（位于`scripts/assemblyai.mjs`文件中，以及相应的兼容性封装层`assemblyai.mjs`）  
2. 通过`models`和`languages`命令提供预打包的模型/语言信息  
3. 稳定的转录输出格式：  
  - 适用于智能代理的Markdown格式  
  - 标准化的JSON格式  
  - 便于下游自动化处理的文件包  
4. 说话者映射功能：  
  - 手动设置的说话者/频道映射  
  - AssemblyAI自动识别说话者  
  - 在Markdown和JSON中统一显示说话者名称  
5. 与AssemblyAI的LLM（大型语言模型）集成，实现从转录文本中提取结构化数据  

## 使用步骤：  

### 1) 判断用户是否需要AssemblyAI的特定功能  
如果用户仅需要“转录结果”，通用解决方案可能就足够了。当用户提及AssemblyAI、需要特定功能或更丰富的输出及后续处理时，使用此技能。  

### 2) 选择合适的入口命令  
- **新转录任务** → 使用`transcribe`  
- **已有转录ID** → 使用`get`或`wait`  
- **重新渲染已保存的JSON文件** → 使用`format`  
- **对现有转录内容进行后处理** → 使用`understand`  
- **通过LLM Gateway处理转录文本** → 使用`llm`  
- **在决策前快速查询功能** → 使用`models`或`languages`  

### 3) 优先选择适用于智能代理的默认设置  
对于大多数未知语言或混合语言的场景，建议使用默认设置：  
```bash
node {baseDir}/assemblyai.mjs transcribe INPUT   --bundle-dir ./assemblyai-out   --all-exports
```  

**原因：**  
- 当未指定模型时，CLI会自动选择最佳路由方式  
- 生成包含元数据的文件包，代理无需重新解析终端输出即可查看  
- 转录结果会立即以Markdown或JSON格式提供，便于后续操作  

## 快速入门示例：  

### 最通用默认设置  
当源语言未知或不在Universal-3-Pro支持的6种语言范围内时，使用此设置：  
```bash
node {baseDir}/assemblyai.mjs transcribe ./meeting.mp3   --bundle-dir ./out   --all-exports
```  
该设置会自动选择合适的模型并进行语言检测，除非用户已明确指定模型或语言。  

### 明确语言时的最佳设置  
如果语言已知且被Universal-3-Pro支持，建议明确指定模型：  
```bash
node {baseDir}/assemblyai.mjs transcribe ./meeting.mp3   --speech-model universal-3-pro   --language-code en_us   --bundle-dir ./out
```  

### 会议/面试场景中的标签处理  
```bash
node {baseDir}/assemblyai.mjs transcribe ./meeting.mp3   --speaker-labels   --bundle-dir ./out
```  

### 添加说话者名称或角色  
**手动映射方式：**  
```bash
node {baseDir}/assemblyai.mjs transcribe ./meeting.mp3   --speaker-labels   --speaker-map @assets/speaker-map.example.json   --bundle-dir ./out
```  

**使用AssemblyAI进行说话者识别：**  
```bash
node {baseDir}/assemblyai.mjs transcribe ./meeting.mp3   --speaker-labels   --speaker-type role   --known-speakers "host,guest"   --bundle-dir ./out
```  
**或对现有转录内容进行后处理：**  
```bash
node {baseDir}/assemblyai.mjs understand TRANSCRIPT_ID   --speaker-type name   --speaker-profiles @assets/speaker-profiles-name.example.json   --bundle-dir ./out
```  

### 翻译功能：  
```bash
node {baseDir}/assemblyai.mjs transcribe ./meeting.mp3   --translate-to de,fr   --match-original-utterance   --bundle-dir ./out
```  

### 通过LLM Gateway提取结构化数据  
```bash
node {baseDir}/assemblyai.mjs llm TRANSCRIPT_ID   --prompt @assets/example-prompt.txt   --schema @assets/llm-json-schema.example.json   --out ./summary.json
```  

## 命令使用指南：  

### `transcribe`  
- 用于处理本地文件或远程URL。  
  - 先上传本地文件，或直接将远程URL发送给AssemblyAI。  
  - 默认情况下会等待处理结果后再输出。  
  - 对于较长的转录内容，建议使用`--bundle-dir`参数。  

### `get` / `wait`  
- 当您已有转录ID时使用。`wait`会等待处理完成；`get`会立即获取结果（除非添加`--wait`参数）。  

### `format`  
- 当您已保存以下文件时使用：  
  - 来自AssemblyAI的原始JSON转录内容  
  - 由该技能生成的标准化JSON格式  
  - 此命令可用于应用新的说话者映射、重新生成Markdown格式或无需重新转录即可生成新的文件包。  

### `understand`  
- 当您需要对现有转录内容进行语音理解时使用：  
  - 翻译  
  - 说话者识别  
  - 自定义格式化  
  - 该命令会获取转录内容，合并处理后的结果，并生成更新后的Markdown、JSON或文件包。  

### `llm`  
- 当用户需要以下功能时使用：  
  - 摘要提取  
  - 结构化数据提取  
  - 对转录内容进行进一步处理（如通过LLM推理）  
  - 建议在后续步骤中使用`--schema`参数以实现自动化。  

## 输出策略：  
### 适用于智能代理的最佳默认设置：**文件包模式**  
使用`--bundle-dir`参数生成包含以下内容的目录：  
- Markdown格式的转录结果  
- 适用于智能代理的JSON格式  
- 原始JSON格式  
- 可选的段落、句子、字幕  
- 机器可读的元数据文件  

**常见输出格式：**  
使用`--export`参数选择主要输出格式：  
- `markdown`（默认）  
- `agent-json`  
- `json` / `raw-json`  
- `text`  
- `paragraphs`  
- `sentences`  
- `srt`  
- `vtt`  
- `manifest`  

### 额外输出文件：  
您还可以通过以下参数请求额外文件：  
- `--markdown-out`  
- `--agent-json-out`  
- `--raw-json-out`  
- `--paragraphs-out`  
- `--sentences-out`  
- `--srt-out`  
- `--vtt-out`  
- `--understanding-json-out`  

## 说话者名称显示规则：  
说话者名称的显示顺序如下：  
1. 手动设置的`--speaker-map`  
2. AssemblyAI自动识别的说话者名称  
3. 默认的通用名称（如“Speaker A”或“Channel 1”）  

**示例手动映射文件：** `assets/speaker-map.example.json`  

### 模型与语言查询：  
在选择参数前，请查看预打包的参考数据：  
```bash
node {baseDir}/assemblyai.mjs models
node {baseDir}/assemblyai.mjs models --format json
node {baseDir}/assemblyai.mjs languages --model universal-3-pro
node {baseDir}/assemblyai.mjs languages --model universal-2 --codes --format json
```  
预打包的数据位于以下文件中：  
- `assets/model-capabilities.json`  
- `assets/language-codes.json`  

## 重要操作注意事项：  
- 请勿在聊天记录中泄露API密钥，应通过环境变量传递。  
- 如用户明确需要欧盟地区的处理服务，请使用**EU**版本的AssemblyAI API地址。  
- 上传文件和生成转录内容时必须使用同一AssemblyAI项目的API密钥。  
- 对于较长的输出文件，建议使用`--bundle-dir`或`--out`参数。  
- 该CLI工具是非交互式的，会将诊断信息输出到标准错误流（stderr），便于代理脚本化使用。  
- 如需使用该技能尚未提供的新参数，请使用`--config`或`--request`参数。  

## 参考资料：  
如需深入了解相关内容，请查阅以下文档：  
- [功能介绍](references/capabilities.md)  
- [工作流程与使用指南](references/workflows.md)  
- [输出格式规范](references/output-formats.md)  
- [说话者映射规则](references/speaker-mapping.md)  
- [LLM Gateway使用说明](references/llm-gateway.md)  
- [故障排除指南](references/troubleshooting.md)  

## 关键文件：  
- `assemblyai.mjs`：与原始技能兼容的封装层  
- `scripts/assemblyai.mjs`：主要CLI工具  
- `assets/speaker-map.example.json`：说话者映射配置文件  
- `assets/speaker-profiles-name.example.json`：说话者信息文件  
- `assets/speaker-profiles-role.example.json`：说话者角色信息文件  
- `assets/custom-spelling.example.json`：自定义拼写规则文件  
- `assets/llm-json-schema.example.json`：LLM输出格式文件  
- `assets/transcript-agent-json-schema.json`：转录结果格式文件  

## 完成任务前的检查：  
- 是否选择了正确的区域（`api.assemblyai.com`或`api.eu.assemblyai.com`）？  
- 选择的模型策略是否适合当前语言环境？  
- 如果说话者名称很重要，是否启用了语音记录功能并提供了说话者映射信息？  
- 如果结果将用于其他智能代理，是否生成了Markdown或JSON格式的输出（而不仅仅是原始文本）？  
- 如果转录内容将被机器处理，是否生成了必要的元数据文件或文件名？