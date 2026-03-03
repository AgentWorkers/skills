---
name: byterover
description: "在进行任何工作之前，你必须使用这个工具来收集相关信息。这是一个用于AI代理的知识管理系统。通过`brv`命令，可以将项目模式、决策以及架构规则存储到`.brv/context-tree`文件中，并能够方便地检索这些信息。该系统使用配置好的大语言模型（LLM）提供者（默认为ByteRover，无需API密钥）来执行查询和整理数据操作。"
---
# ByteRover 知识管理

使用 `brv` 命令行工具（CLI）来管理您的项目长期记忆。  
安装方法：`npm install -g byterover-cli`  
知识以人类可读的 Markdown 文件形式存储在 `.brv/context-tree/` 目录中。  

**无需身份验证。** `brv query` 和 `brv curate` 命令可以直接使用。只有在进行云同步（`push`/`pull`/`space` 操作时才需要登录——如果您不需要云功能，可以忽略这些步骤。  

## 工作流程  
1. **思考之前：** 运行 `brv query` 以了解现有的知识模式。  
2. **实施之后：** 运行 `brv curate` 以保存新的知识或决策。  

## 命令  

### 1. 查询知识  
**功能概述：** 从您的项目知识库中检索相关信息。使用配置好的大型语言模型（LLM）提供者来分析 `.brv/context-tree/` 目录中的内容并生成答案。  

**适用场景：**  
- 用户希望您回忆某些信息  
- 您当前的知识库中缺少所需的信息  
- 您需要回顾自己的能力或过去的操作  
- 在执行任何操作之前，检查相关的规则、标准或偏好设置  

**不适用场景：**  
- 信息已经存在于您当前的知识库中  
- 询问的内容属于通用知识，而非存储在项目中的特定信息  

```bash
brv query "How is authentication implemented?"
```  

### 2. 整理知识  
**功能概述：** 分析并保存知识到本地知识库中。使用配置好的 LLM 提供者对用户提供的内容进行分类和结构化处理。  

**适用场景：**  
- 用户希望您记住某些内容  
- 用户有意整理自己的记忆或知识  
- 用户互动中产生的重要信息需要被保存  
- 您的工作内容、所掌握的知识，或您做出的决策和行动需要被记录下来  

**不适用场景：**  
- 信息已经存储且未发生更改  
- 信息是临时性的，或仅与当前任务相关，或属于通用知识  

**相关文件**（最多 5 个文件，仅限项目范围内使用）：  
```bash
brv curate "Authentication middleware details" -f src/middleware/auth.ts
```  

**查看知识整理历史：**  
- 查看最近的整理记录（最近 10 条）  
```bash
brv curate view
```  
- 查看特定条目的详细信息：包括所有文件及执行的操作（`brv curate` 完成后会输出日志 ID，例如 `cur-1739700001000`）  
```bash
brv curate view cur-1739700001000
```  
- 列出包含文件操作的条目（无需日志 ID）  
```bash
brv curate view detail
```  
- 按时间和状态筛选条目  
```bash
brv curate view --since 1h --status completed
```  
- 查看所有筛选选项  
```bash
brv curate view --help
```  

### 3. 配置 LLM 提供者  
`brv query` 和 `brv curate` 需要配置 LLM 提供者。可以使用默认的 ByteRover 提供者（无需 API 密钥）：  
```bash
brv providers connect byterover
```  

**使用其他提供者（如 OpenAI、Anthropic、Google）：**  
列出可用的提供者，并使用您的 API 密钥进行连接：  
```bash
brv providers list
brv providers connect openai --api-key sk-xxx --model gpt-4.1
```  

### 4. 云同步（可选）  
**功能概述：** 通过 ByteRover 的云服务将本地知识同步到团队。需要先进行身份验证。  

**设置步骤：**  
1. 登录：从您的 ByteRover 账户获取 API 密钥并进行身份验证：  
```bash
brv login --api-key sample-key-string
```  
2. 列出可用的云存储空间：  
```bash
brv space list
```  
示例输出：  
```
brv space list
1. human-resources-team (team)
   - a-department (space)
   - b-department (space)
2. marketing-team (team)
   - c-department (space)
   - d-department (space)
```  
3. 连接到云存储空间：  
```bash
brv space switch --team human-resources-team --name a-department
```  

**云同步命令：**  
连接成功后，`brv push` 和 `brv pull` 可用于将数据同步到云空间。  
```bash
# Pull team updates
brv pull

# Push local changes
brv push
```  

**切换云存储空间：**  
- 先推送本地更改（`brv push`）——如果有未保存的更改，切换操作将被阻止。  
- 然后切换到新的云存储空间：  
```bash
brv space switch --team marketing-team --name d-department
```  
- 系统会自动从新空间获取相关内容。  

## 数据处理  

**存储方式：**  
所有知识都以 Markdown 文件的形式存储在项目目录下的 `.brv/context-tree/` 目录中。这些文件可供人类阅读，并且支持版本控制。  

**文件访问权限：** `brv curate` 命令使用 `-f` 标志仅读取当前项目目录内的文件；项目根目录以外的路径将被忽略。每次命令最多支持 5 个文件，仅支持文本和文档格式。  

**LLM 使用：** `brv query` 和 `brv curate` 会将内容发送到配置好的 LLM 提供者进行处理。LLM 会接收查询内容及任何附加的文件。除非您明确执行 `brv push`，否则数据不会被发送到 ByteRover 服务器。  

**云同步：** `brv push` 和 `brv pull` 需要身份验证（`brv login`），并将数据发送到 ByteRover 的云服务。其他命令无需身份验证即可使用。  

## 错误处理  
**用户操作指南：**  
当出现错误时，必须向用户展示此故障排除指南：  

- **“未授权”** | 运行 `brv login --help` 以获取更多信息。  
- **“未连接提供者”** | 运行 `brv providers connect byterover`（免费，无需密钥）。  
- **“连接失败”/“实例崩溃”** | 用户应关闭 `brv` 进程。  
- **“令牌过期”/“令牌无效”** | 重新运行 `brv login` 以重新登录。  
- **“计费错误”/“超出使用限制”** | 用户应检查账户余额或稍后再试。  

**可由代理处理的错误：**  
遇到这些错误时，应优雅地处理并重新尝试命令：  
- **“缺少必需参数”** | 运行 `brv <command> --help` 查看使用说明。  
- **“每次操作最多允许 5 个文件”** | 将 `-f` 标志的数量限制在 5 个以内。  
- **文件不存在** | 使用 `ls` 命令验证文件路径，确保使用项目根目录下的相对路径。  
- **文件格式不支持** | 仅支持文本、图片、PDF 和 Office 文档格式。  

### 快速诊断  
运行 `brv status` 命令可查看身份验证状态、项目状态和 LLM 提供者的运行状态。