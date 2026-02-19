---
name: agent-media
description: 使用 `agent-media` CLI 从终端生成由 AI 提供支持的视频和图像。
homepage: https://github.com/gitroomhq/agent-media
metadata: {"clawdbot":{"emoji":"🌎","requires":{"bins":[],"env":[]}}}
---
**npm 发布：** https://www.npmjs.com/package/agent-media-cli  
**agent-media CLI 的 GitHub 仓库：** https://github.com/gitroomhq/agent-media  
**官方网站：** https://agent-media.ai  

# agent-media — 人工智能视频与图像生成工具  

使用 `agent-media` CLI 从终端生成由人工智能驱动的视频和图像。  

## 先决条件  

必须先安装并登录 `agent-media` CLI：  
```bash
npm install -g agent-media-cli
agent-media login
```  

使用 `agent-media whoami` 命令进行身份验证。如果未登录，请运行 `agent-media login` 并按照提示完成 OTP 验证流程。  

## 可用的模型  

| 模型名称 | 类型 | 特点 | 备注 |
|------|------|------|-------|  
| `kling3` | Kling 3.0 Pro | 视频 | 文本转视频/图像转视频，时长 5-10 秒，分辨率 1080p |
| `veo3` | Veo 3.1 | 视频 | 文本转视频/图像转视频，时长 4-8 秒，支持最高 4K 分辨率 |
| `sora2` | Sora 2 Pro | 视频 | 文本转视频/图像转视频，时长 4-25 秒，分辨率 1080p |
| `seedance1` | Seedance 1.0 Pro | 视频 | 文本转视频/图像转视频，时长 2-12 秒，分辨率 1080p |
| `flux2-pro` | Flux 2 Pro | 图像 | 文本转图像 |
| `flux2-flex` | Flux 2 Flex | 图像 | 文本转图像 |
| `grok-image` | Grok Imagine | 图像 | 文本转图像 |

## 核心命令  

### 生成媒体文件  

```bash
# Video generation
agent-media generate kling3 -p "A robot walking through a neon-lit city" --sync

# Image generation
agent-media generate flux2-pro -p "Cyberpunk samurai portrait" --sync

# Image-to-video (provide input image)
agent-media generate seedance1 -p "Make it dance" --input ./photo.jpg --sync

# With options
agent-media generate sora2 -p "Ocean waves at sunset" -d 10 -r 1080p --aspect-ratio 16:9 --sync
```  

**常用参数：**  
- `-p, --prompt` — 生成提示（必填）  
- `-d, --duration` — 视频时长（秒）  
- `-r, --resolution` — 输出分辨率（720p, 1080p）  
- `--aspect-ratio` — 长宽比（16:9, 9:16, 1:1 等）  
- `--input` — 图像转视频时的输入图像文件  
- `--sync, -s` — 等待生成完成并打印输出 URL  
- `--json` — 以 JSON 格式输出（便于后续处理）  

### 查看生成信息与状态  

```bash
# Credit balance
agent-media credits

# Current plan
agent-media plan

# Job status
agent-media status <job-id>

# List recent jobs
agent-media list
agent-media list --status completed --limit 5
```  

### 模型详情与价格信息  

```bash
# List all models
agent-media models

# Detailed pricing
agent-media pricing
agent-media pricing --model kling3
```  

### 任务管理  

```bash
# Download a completed job
agent-media download <job-id>

# Retry a failed job
agent-media retry <job-id>

# Cancel a running job
agent-media cancel <job-id>

# Delete a job
agent-media delete <job-id>
```  

### 账户管理  

```bash
agent-media whoami          # Current user
agent-media credits         # Credit balance
agent-media plan            # Current subscription
agent-media subscribe              # Interactive plan/credits menu (waits for confirmation)
agent-media subscribe --plan starter  # Subscribe to a plan directly
agent-media subscribe --credits 500   # Buy a credit pack directly
agent-media subscribe --manage        # Open Stripe billing portal
agent-media apikey list     # List API keys
agent-media apikey create   # Create new API key
```  

## 使用技巧：  
- 使用 `agent-media subscribe` 命令会在浏览器中打开 Stripe 结账页面，系统会等待最多 2 分钟以确认支付；成功后显示新的套餐信息/剩余信用额度。  
- 当需要等待生成结果并获取输出 URL 时，请务必使用 `--sync` 参数。  
- 如需程序化处理生成结果，请使用 `--json` 参数。  
- 在生成前请使用 `agent-media credits` 命令检查账户余额是否充足。  
- 视频的默认时长为 5 秒，分辨率默认为 720p（如未指定）。  
- 图像模型无需指定时长，只需提供文本提示及可选的分辨率即可。  
- 使用 `--sync` 参数会打印已完成媒体的公开 URL。