# 🎨 Pollinations 图像生成技能

这是一个由 [Pollinations.ai](https://pollinations.ai) 提供的、简洁、模块化且用户友好的图像生成工具。

## ✨ 主要功能

- 🎁 每月可免费使用 5,000 张图片（通过“pollen”奖励机制）
- 🔄 **模型切换简单**——随时可更换模型
- 💾 **持久化设置**——记住您的偏好设置
- 📊 **清晰的模型对比**——包括质量、速度和成本
- 🔧 **模块化设计**——易于扩展

## 🚀 快速入门

### 首次设置

```bash
# 1. Clone or copy the skill
cd pollinations-image/

# 2. (Optional) Configure your API key
cp .env.example .env
# Edit .env and add your key from https://enter.pollinations.ai

# 3. (Optional) Set your default model  
cp .user.conf.example .user.conf
# Edit .user.conf to change DEFAULT_IMAGE_MODEL

# 4. List all available models
./generate.sh models

# 5. Generate your first image
./generate.sh "a cute purple cat"
```

### 已经配置好了？

```bash
# List all available models
./generate.sh models

# Set your default model (optional)
./generate.sh set-model flux

# Generate an image
./generate.sh generate --prompt "a cute purple cat"

# Or use the shortcut
./generate.sh "a cute purple cat"
```

## 📋 可用模型

| 模型 | 类型 | 速度 | 质量 | 成本 |
|-------|------|-------|---------|------|
| `flux` | 🎁 免费 | ⚡⚡ | ⭐⭐⭐⭐⭐ | 约 0.0002 枚“pollen”奖励 |
| `zimage` | 🎁 免费 | ⚡ | ⭐⭐⭐⭐ | 约 0.0002 枚“pollen”奖励 |
| `klein` | 付费 | ⚡⚡ | ⭐⭐⭐⭐⭐ | 约 0.008 枚“pollen”奖励 |
| `klein-large` | 付费 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 约 0.012 枚“pollen”奖励 |
| `gptimage` | 付费 | ⚡⚡ | ⭐⭐⭐⭐⭐ | 每张图片 2.0–8.0 枚“pollen”奖励 |

## 📖 命令

### `generate`（或 `g`）
根据您的提示生成图片。

```bash
# Full command
./generate.sh generate --prompt "a sunset over mountains" --model flux --width 1024 --height 1024

# Short options
./generate.sh g -p "a sunset" -m zimage -w 512 -h 512

# Even shorter (prompt only)
./generate.sh "a cute cat"
```

**可选参数：**
- `--prompt, -p` - 图片描述（必填）
- `--model, -m` - 使用的模型（会覆盖默认设置）
- `--width, -w` - 图片宽度（默认：1024）
- `--height, -h` - 图片高度（默认：1024）
- `--seed, -s` - 用于生成可重复结果的随机种子
- `--filename, -f` - 自定义输出文件名
- `--nologo` - 移除 Pollinations 的水印
- `--enhance` - 让 AI 改进您的提示内容

### `models`（或 `m`）
显示所有可用模型及其评分。

```bash
./generate.sh models
```

### `model MODEL_NAME`
显示特定模型的详细信息。

```bash
./generate.sh model klein-large
```

### `set-model MODEL_NAME`
将当前模型设置为所有后续生成的默认模型。

```bash
./generate.sh set-model zimage
```

**注意：**此设置会保存在 `.user.conf` 文件中，并在会话之间保持一致。

### `config`
显示当前的配置信息。

```bash
./generate.sh config
```

### `help`
显示帮助信息。

```bash
./generate.sh help
```

## ⚙️ 配置

用户偏好设置存储在 `.user.conf` 文件中：

```bash
# Example .user.conf
DEFAULT_IMAGE_MODEL=flux
```

API 密钥存储在 `.env` 文件中（不包含在 Git 代码库中）：

```bash
# Example .env
POLLINATIONS_API_KEY=your_key_here
```

## 📁 文件结构

```
pollinations-image/
├── generate.sh        # Main entry point
├── lib/
│   └── models.sh      # Model registry and metadata
├── .env               # API keys (private)
├── .user.conf         # User preferences
└── SKILL.md           # This documentation
```

## 🎯 推荐的工作流程

### 草稿 → 优化 → 最终版本

```bash
# 1. Quick draft with fast model
./generate.sh g -p "concept sketch of a dragon" -m zimage -w 512

# 2. Refine with better model
./generate.sh g -p "detailed dragon in a castle" -m flux -w 1024

# 3. Final high-quality render
./generate.sh g -p "masterpiece, highly detailed dragon..." -m klein-large
```

### 日常使用流程

```bash
# Set fast model for daily use
./generate.sh set-model zimage

# All future generations use zimage by default
./generate.sh "quick concept"

# Override for special occasion
./generate.sh "important artwork" --model klein-large
```

## 🔑 获取 API 密钥

1. 访问 [enter.pollinations.ai](https://enter.pollinations.ai)
2. 创建账户
3. 申请“pollen”奖励（免费 tier：每月 5,000 张图片）
4. 生成 API 密钥
5. 将密钥保存到 `.env` 文件中：`POLLINATIONS_API_KEY=your_key`

## 🤝 贡献与分享

这个技能旨在供大家共同使用！

### 需要包含的文件

在分享此技能时，请包含以下文件：
- ✅ `generate.sh` — 主脚本
- ✅ `lib/models.sh` — 模型注册文件
- ✅ `.env.example` — 示例 API 密钥文件
- ✅ `.user.conf.example` — 示例用户配置文件
- ✅ `SKILL.md` — 文档文件

### 不应分享的文件（包含个人数据）

请勿分享以下文件：
- ❌ `.env` — 您的私人 API 密钥
- ❌ `.user.conf` — 您的个人偏好设置
- ❌ `.first-run-complete` — 用于标记首次使用的文件

### 添加新模型

1. 编辑 `lib/models.sh`
2. 按照以下格式将新模型添加到 `MODELS_LIST` 中：
   ```
   model_id|Display Name|type|cost|speed|quality|Description
   ```
3. 使用 `./generate.sh model your_model_id` 进行测试

### 首次使用体验

当用户首次运行此技能时（如果没有配置文件），系统会显示欢迎信息并指导他们完成设置。该技能会使用默认设置直接使用：
- **默认模型：`flux`（免费，高质量）**
- **API 密钥：** 可选（支持公共 API 端点）

## 📝 许可证

MIT 许可证——您可以自由使用、修改和分享此技能！

---

本技能专为 OpenClaw 社区制作。