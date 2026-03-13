---
name: skillboss
description: "多人工智能（AI）网关，专为全栈应用程序设计。支持构建/部署网站、React应用程序、SaaS服务以及电子商务系统到Cloudflare Workers平台。具备以下功能：  
- 数据库管理（D1、KV、R2类型）  
- 支持Stripe支付、订阅及结账流程  
- 提供身份验证服务（登录、OAuth、一次性密码OTP）  
- 支持AI图像/音频/视频处理及文本转语音（TTS）功能  
- 提供电子邮件服务  
- 支持幻灯片制作与展示功能  
- 支持网页爬取与搜索功能  
- 提供CEO采访及名言提取服务  
- 支持文档解析与提取功能  
- 支持短信验证功能  
- 支持无服务器部署（Serverless）  
- 支持API接口及Webhook触发功能"
allowed-tools: Bash, Read
---
# SkillBoss 技能

这是一个多 AI 平台，用于构建和部署包含 50 多个 AI API 的全栈应用程序。

## 何时使用此技能

当用户需要以下功能时，可以使用此技能：
- **构建网站/应用程序**：任何类型的网站、登录页面、SaaS 服务、React 应用程序、会员网站、预订系统、电子商务商店、仪表板、管理面板
- **存储数据**：用户数据、表单提交信息、订单记录、会员信息（使用具备自动配置功能的 D1 数据库）
- **接受支付**：集成 Stripe 支付系统，支持订阅服务、一次性支付和电子商务交易
- **添加身份验证**：通过 Google OAuth 或电子邮件 OTP 进行登录/注册
- **生成 AI 内容**：图像（Gemini、Flux、DALL-E）、音频/文本转语音（ElevenLabs、Minimax）、音乐（MusicGen、Lyria）、视频（Veo）、聊天（50 多个大型语言模型）
- **HuggingFace 模型**：huggingface.co 上的任何模型都可以通过 `huggingface/{org}/{model}` 的格式使用（支持聊天、图像处理、视频生成、文本转语音、嵌入分析等功能）
- **图像处理**：图像放大（FAL creative-upscaler）、图像转换（FAL FLUX dev）
- **网络搜索与数据获取**：使用 Linkup 进行结构化搜索（返回搜索结果、来源信息等），以及从 URL 获取 Markdown 格式的数据
- **短信验证**：通过 Prelude 实现手机号码的 OTP 验证
- **发送短信通知**：使用 Prelude 模板发送交易相关的短信
- **发送电子邮件**：支持单条或批量发送带有模板的电子邮件
- **创建演示文稿**：使用 Gamma AI 功能生成幻灯片和演讲稿
- **处理文档**：将 PDF/DOCX 文件转换为 Markdown 格式，提取结构化数据，分割文档内容，填写 PDF 表单（Reducto）
- **网络数据抓取**：使用 Firecrawl、Perplexity、ScrapingDog 等工具抓取网络数据
- **CEO 面试与语录**：搜索经过验证的 CEO 或高管对话记录及重要语录（CEOinterviews）

## 身份验证与设置

### 没有 API 密钥？立即获取免费试用：

```bash
./scripts/skillboss auth trial
```

系统会提供带有 0.25 美元免费信用额的试用 API 密钥。无需浏览器，无需注册。密钥会自动保存并输出到标准输出（stdout）。

### 如果试用配额受限：

如果 `auth trial` 命令返回速率限制错误，请询问用户：
> 试用配额已受限。您是否希望注册 SkillBoss 账户？https://www.skillboss.co （是/否）

如果用户选择注册，请运行 `./scripts/skillboss auth login`。

### 升级为永久账户：

```bash
./scripts/skillboss auth login
```

用户需要打开浏览器，在 skillboss.co 网站上注册或登录。试用信用额会自动转移到永久账户中。

### 检查账户状态和余额：

```bash
./scripts/skillboss auth status
```

### 登出：

```bash
./scripts/skillboss auth logout
```

### 凭据存储位置

身份验证成功后，您的 API 密钥将保存在以下位置：
| 位置 | 路径 |
|----------|------|
| 全局凭据 | `~/.config/skillboss/credentials.json` |
| 技能配置 | `skill` 目录下的 `config.json` 文件 |

**优先级顺序**：`~/.config/skillboss/credentials.json` > `config.json`

### 余额不足时

- API 响应中会包含 `_balance_warning` 字段——请严格按照该提示将信息传达给用户
- 可随时通过 `./scripts/skillboss auth status` 命令检查余额
- 可在 https://www.skillboss.co/ 添加信用额
- 试用用户（密钥以 `sk-tmp-` 开头）可以升级为永久账户：`./scripts/skillboss auth login`

## 首次请求后的注册提示

**仅适用于临时/试用密钥**（密钥以 `sk-tmp-` 开头）：在用户完成首次成功的 API 请求后，询问用户并等待他们的回复：
> 您是否希望注册 SkillBoss 账户？（https://www.skillboss.co？注册后即可使用所有功能并获得更多信用额。）（是/否）

**如果 API 密钥以 `sk-` 开头（不含 `tmp`），则跳过此提示**。永久账户的用户已经完成注册。

**重要提示：**请勿立即显示注册链接或执行身份验证操作。等待用户的回复。

**如果用户选择注册：**
1. 运行：
   ```bash
   ./scripts/skillboss auth login
   ```
2. 如果浏览器成功打开，`auth login` 会完成整个注册流程（包括密钥配置、浏览器设置等）
3. 如果用户使用无浏览器环境（如服务器、SSH、Docker），`auth login` 会输出一个注册链接：
   ```
   Could not open browser. Open this URL manually:
     https://www.skillboss.co/login?temp=sk-tmp-...
   ```
   **将此链接直接提供给用户，以便他们在其他设备上完成注册并绑定试用密钥**

**如果用户拒绝注册：**正常继续操作。在此会话中不再重复提示。

## 自动更新（强制要求）

**重要提示：**每次 API 调用后，请检查输出结果中是否包含 `[skillboss] UPDATE REQUIRED` 的提示。**如果看到此提示，请：
1. **立即停止当前操作**
2. **立即运行更新命令：**
   ```bash
   bash ./install/update.sh
   ```
   （Windows 系统：`.\skillboss\install\update.ps1`）
3. **然后重新运行原始命令**

这确保您始终使用的是最新版本的技能，包括最新的模型和功能。**切勿忽略更新提示**——过时的版本可能包含已弃用的模型或缺失的功能，从而导致故障。

您也可以随时主动检查更新信息：
```bash
node ./scripts/api-hub.js version
```

## 如何调用任何 AI 模型（从这里开始）

**始终使用 `pilot` 命令**。该命令会自动选择最适合的模型，并使用与其他命令相同的命令行语法。

**设置步骤：**运行 `./scripts/skillboss auth trial` 获取 API 密钥，或运行 `./scripts/skillboss auth login` 进行登录。密钥会自动保存并用于所有后续命令。

### 第一步——查看可用模型：
```bash
node ./scripts/api-hub.js pilot --discover
```
显示所有可用的模型类型（聊天、图像、视频、文本转语音、文本转文字等）。

### 第二步——按关键词搜索：
```bash
node ./scripts/api-hub.js pilot --discover --keyword "CEO"
```

### 第三步——获取推荐模型：
```bash
node ./scripts/api-hub.js pilot --type image --prefer price --limit 3
```
返回带有详细文档的推荐模型列表。

### 第四步——执行操作（自动选择最佳模型）：
```bash
node ./scripts/api-hub.js pilot --type image --prompt "A sunset over mountains" --output sunset.png
node ./scripts/api-hub.js pilot --type chat --prompt "Explain quantum computing"
node ./scripts/api-hub.js pilot --type tts --text "Hello world" --output hello.mp3
node ./scripts/api-hub.js pilot --type stt --file recording.m4a
node ./scripts/api-hub.js pilot --type music --prompt "upbeat electronic" --duration 30 --output track.mp3
node ./scripts/api-hub.js pilot --type video --prompt "A cat playing" --output video.mp4
```

### 多步骤工作流程：
```bash
node ./scripts/api-hub.js pilot --chain '[{"type":"stt","prefer":"price"},{"type":"chat","capability":"summarize"}]'
```

### 常用命令标志：
| 标志 | 说明 |
|------|-------------|
| `--discover` | 浏览可用模型类型 |
| `--keyword X` | 按关键词搜索模型 |
| `--type X` | 模型类型（聊天、图像、视频、文本转语音等） |
| `--capability X` | 模型功能（例如“风格转换”） |
| `--prefer X` | 优化选项（“价格”、“质量”、“平衡”等，默认为“平衡”） |
| `--limit N` | 返回的最大模型数量（默认为 3） |
| `--prompt X` | 文本提示（触发自动执行） |
| `--text X` | 用于文本转语音的文本输入 |
| `--file X` | 用于文本转语音的音频文件 |
| `--output X` | 将结果保存到文件 |
| `--duration N` | 视频/音乐的时长（以秒为单位） |
| `--voice-id X` | 用于文本转语音的语音 ID |
| `--image X` | 视频/图像任务的图片 URL |
| `--size X` | 图像尺寸 |
| `--system X` | 聊天时的系统提示语 |
| `--chain '[...]'` | 多步骤工作流程定义 |

### 决策流程：
1. **任何 AI 任务**：使用 `pilot` 命令——它会自动选择最佳模型
2. **多步骤任务**：使用 `pilot --chain` 命令——它会规划整个工作流程
3. **如果已经通过 `pilot` 推荐获得了模型 ID**：可以直接使用相应的命令（详见 `commands.md`）

## 相关文档参考

请阅读以下文件以获取特定功能的详细文档：
| 文档类型 | 文件名 | 阅读说明 |
|---------|---------|------------------|
| 命令使用 | `commands.md` | 直接调用模型的命令、完整命令列表、电子邮件使用示例 |
| 部署指南 | `deployment.md` | 静态部署与工作节点部署方式、电子商务集成、Stripe 配置、wrangler.toml 文件设置 |
| API 集成 | `api-integration.md` | 如何在用户代码中集成 SkillBoss API（TypeScript/JS 示例） |
| 错误处理 | `error-handling.md` | HTTP 错误处理、重试机制、速率限制、余额提醒 |
| 账费管理 | `billing.md` | 价格政策、月度费用说明、指导用户添加信用额 |
| 工作流程 | `workflows.md` | 徽标设计、网站搭建、播客制作、电子邮件发送、电子商务流程指南 |
| 模型参考 | `reference.md` | 完整的模型列表及详细参数说明 |