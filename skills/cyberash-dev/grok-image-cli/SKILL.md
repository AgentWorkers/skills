---
name: grok-image-cli
description: 通过 Grok API 从命令行生成和编辑图像。使用 macOS 的 Keychain 来安全存储 xAI API 密钥。支持批量生成、调整图像的宽高比以及应用图像样式转换（style transfer）。
metadata: {"clawdbot":{"emoji":"🎨","os":["macos"],"requires":{"bins":["grok-img","node"],"env":{"XAI_API_KEY":{"required":false,"description":"xAI API key (fallback when no Keychain entry exists)"}}},"credentials":[{"id":"xai-api-key","label":"xAI API key","storage":"macos-keychain","service":"grok-image-cli","account":"api-key","env_fallback":"XAI_API_KEY"}],"install":[{"id":"npm","kind":"shell","command":"npm install -g grok-image-cli","bins":["grok-img"],"label":"Install grok-image-cli via npm"},{"id":"source","kind":"shell","command":"git clone https://github.com/cyberash-dev/grok-image-cli.git && cd grok-image-cli && npm install && npm run build && npm link","bins":["grok-img"],"label":"Install from source (audit before running)"}],"source":"https://github.com/cyberash-dev/grok-image-cli"}}
---

# grok-image-cli

这是一个命令行工具（CLI），用于使用 xAI 的 Grok API (`grok-imagine-image` 模型) 生成和编辑图像。该工具由官方的 `@ai-sdk/xai` SDK 提供支持，用户凭据存储在 macOS 的 Keychain 中。

## 安装

需要 Node.js >= 20.19.0 和 macOS 环境。该软件包完全开源，遵循 MIT 许可证：https://github.com/cyberash-dev/grok-image-cli

```bash
npm install -g grok-image-cli
```

该 npm 包会附带来源信息的验证信息，通过 GitHub Actions 将每个版本与其对应的源代码提交关联起来。您可以在安装前验证已发布的代码内容：
```bash
npm pack grok-image-cli --dry-run
```

如果您希望在安装前审查代码，也可以选择从源代码进行安装：
```bash
git clone https://github.com/cyberash-dev/grok-image-cli.git
cd grok-image-cli
npm install && npm run build && npm link
```

安装完成后，`grok-image` 命令将在全局环境中可用。

## 快速入门

```bash
grok-img auth login                                          # Interactive prompt: enter xAI API key
grok-img generate "A futuristic city skyline at night"       # Generate an image
grok-img edit "Make it a watercolor painting" -i ./photo.jpg # Edit an existing image
```

## API 密钥管理

**存储 API 密钥**（交互式提示）：
```bash
grok-img auth login
```

**查看已存储的密钥（部分信息已屏蔽）及来源代码**：
```bash
grok-img auth status
```

**从 Keychain 中删除密钥**：
```bash
grok-img auth logout
```

当找不到 Keychain 中的密钥时，该 CLI 也会支持使用 `XAI_API_KEY` 环境变量作为备用方案。

## 图像生成

```bash
grok-img generate "A collage of London landmarks in street-art style"
grok-img generate "Mountain landscape at sunrise" -n 4 -a 16:9
grok-img generate "A serene Japanese garden" -o ./my-images
```

## 图像编辑

您可以编辑本地文件或远程 URL 对应的图像：
```bash
grok-img edit "Change the landmarks to New York City" -i ./landmarks.jpg
grok-img edit "Render as a pencil sketch" -i https://example.com/portrait.jpg
grok-img edit "Add a vintage film grain effect" -i ./photo.jpg -a 3:2 -o ./edited
```

## 标志说明

### `generate` 命令参数

| 标志 | 说明 | 默认值 |
|------|-------------|---------|
| `-a, --aspect-ratio <比例>` | 纵横比（1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 2:1, 1:2, 19.5:9, 9:19.5, 20:9, 9:20, auto） | auto |
| `-n, --count <数量>` | 生成图像的数量（1-10） | 1 |
| `-o, --output <输出目录>` | 输出目录 | ./grok-images |

### `edit` 命令参数

| 标志 | 说明 | 默认值 |
|------|-------------|---------|
| `-i, --image <路径>` | 源图像文件路径或 URL | **必需** |
| `-a, --aspect-ratio <比例>` | 纵横比 | auto |
| `-o, --output <输出目录>` | 输出目录 | ./grok-images |

## 安全性与数据存储

以下安全特性已在源代码中明确说明：

- **xAI API 密钥**：存储在 macOS 的 Keychain 中（服务：`grok-image-cli`，账户：`api-key`）。根据设计，密钥不会以明文形式保存到磁盘上。如果 Keychain 中没有相应的密钥条目，CLI 会使用 `XAI_API_KEY` 环境变量。具体实现细节请参阅 [`src/infrastructure/adapters/keychain.adapter.ts`](https://github.com/cyberash-dev/grok-image-cli/blob/main/src/infrastructure/adapters/keychain.adapter.ts)。
- **无配置文件**：所有设置均通过 CLI 参数传递；除了 Keychain 中的密钥信息外，没有任何数据会保存到磁盘上。
- **网络通信**：API 密钥仅通过官方的 `@ai-sdk/xai` SDK 通过 HTTPS 协议发送到 `api.x.ai`。在编辑远程 URL 对应的图像时（使用 `-i` 参数），SDK 会额外发起一个 HTTPS 请求来获取源图像。CLI 本身不会进行其他网络请求（安装过程中 npm 的 git 获取操作属于标准包管理器的行为）。具体实现详情请参阅 [`src/infrastructure/adapters/grok-api.adapter.ts`](https://github.com/cyberash-dev/grok-image-cli/blob/main/src/infrastructure/adapters/grok-api.adapter.ts)。
- **生成的图像**：保存在本地指定的输出目录（默认为 `./grok-images`）。生成的图像不会被缓存或上传到其他地方。

## API 参考

该 CLI 通过 Vercel AI SDK 调用 xAI 的图像生成 API：
- 生成图像：`POST /v1/images/generations`
- 编辑图像：`POST /v1/images/edits`

更多文档请参考：https://docs.x.ai/docs/guides/image-generation