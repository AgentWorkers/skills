---
name: grok-image-cli
description: 通过 Grok API 从命令行生成和编辑图像。支持 xAI API 密钥的跨平台安全存储，具备批量生成、调整画面比例以及图像风格转换等功能。
metadata: {"clawdbot":{"emoji":"🎨","os":["macos","windows","linux"],"requires":{"bins":["grok-img","node"],"env":{"XAI_API_KEY":{"required":false,"description":"xAI API key (fallback when no credential store entry exists)"}}},"credentials":[{"id":"xai-api-key","label":"xAI API key","storage":"cross-keychain","service":"grok-image-cli","account":"api-key","env_fallback":"XAI_API_KEY"}],"install":[{"id":"npm","kind":"shell","command":"npm install -g grok-image-cli","bins":["grok-img"],"label":"Install grok-image-cli via npm"},{"id":"source","kind":"shell","command":"git clone https://github.com/cyberash-dev/grok-image-cli.git && cd grok-image-cli && npm install && npm run build && npm link","bins":["grok-img"],"label":"Install from source (audit before running)"}],"source":"https://github.com/cyberash-dev/grok-image-cli"}}
---
# grok-image-cli

这是一个用于生成和编辑图像的命令行工具（CLI），它通过 xAI 的 Grok API 来实现这些功能。支持多种模型：`grok-imagine-image`（默认）、`grok-imagine-image-pro`、`grok-2-image-1212`。该工具由官方的 `@ai-sdk/xai` SDK 提供支持。用户凭据通过 `cross-keychain` 机制存储在操作系统的本地凭据存储库中（macOS 的 Keychain、Windows 的 Credential Manager、Linux 的 Secret Service）。

## 安装

需要 Node.js 版本 >= 20.19.0。支持 macOS、Windows 和 Linux 系统。该软件包完全开源，遵循 MIT 许可证：https://github.com/cyberash-dev/grok-image-cli

```bash
npm install -g grok-image-cli
```

该 npm 包在发布时会附带来源信息的验证，通过 GitHub Actions 将每个版本与其对应的源代码提交关联起来。您可以在安装前验证已发布的代码内容：
```bash
npm pack grok-image-cli --dry-run
```

如果您希望在安装前审核代码，也可以选择从源代码进行安装：
```bash
git clone https://github.com/cyberash-dev/grok-image-cli.git
cd grok-image-cli
npm install && npm run build && npm link
```

安装完成后，`grok-image` 命令将在全局范围内可用。

## 快速入门

```bash
grok-img auth login                                                      # Interactive prompt: enter xAI API key
grok-img generate "A futuristic city skyline at night"                   # Generate with default model
grok-img generate "A futuristic city skyline at night" -m grok-imagine-image-pro  # Use pro model
grok-img edit "Make it a watercolor painting" -i ./photo.jpg             # Edit an existing image
```

## API 密钥管理

**交互式提示：** 输入 API 密钥以进行存储：
```bash
grok-img auth login
```

**查看已存储的密钥（部分信息被屏蔽）及其来源：**
```bash
grok-img auth status
```

**从凭据存储库中删除密钥：**
```bash
grok-img auth logout
```

当找不到凭据存储条目时，该 CLI 也会使用环境变量 `XAI_API_KEY` 作为备用方案。

## 图像生成

```bash
grok-img generate "A collage of London landmarks in street-art style"
grok-img generate "Mountain landscape at sunrise" -n 4 -a 16:9
grok-img generate "A serene Japanese garden" -o ./my-images
grok-img generate "Photorealistic portrait" -m grok-imagine-image-pro
grok-img generate "Abstract art" -m grok-2-image-1212
```

## 图像编辑

您可以编辑本地文件或远程 URL 中的图像：
```bash
grok-img edit "Change the landmarks to New York City" -i ./landmarks.jpg
grok-img edit "Render as a pencil sketch" -i https://example.com/portrait.jpg
grok-img edit "Add a vintage film grain effect" -i ./photo.jpg -a 3:2 -o ./edited
```

## 常用参数说明

### `generate` 命令参数

| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `-m, --model <model>` | 使用的模型（grok-imagine-image、grok-imagine-image-pro、grok-2-image-1212） | grok-imagine-image |
| `-a, --aspect-ratio <ratio>` | 纵横比（1:1、16:9、9:16、4:3、3:4、3:2、2:3、2:1、1:2、19.5:9、9:19.5、20:9、9:20、auto） | auto |
| `-n, --count <number>` | 生成图像的数量（1-10） | 1 |
| `-o, --output <dir>` | 输出目录 | ./grok-images |

### `edit` 命令参数

| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `-i, --image <path>` | 源图像文件路径或 URL | **必需** |
| `-m, --model <model>` | 使用的模型（grok-imagine-image、grok-imagine-image-pro、grok-2-image-1212） | grok-imagine-image |
| `-a, --aspect-ratio <ratio>` | 纵横比 | auto |
| `-o, --output <dir>` | 输出目录 | ./grok-images |

## 安全性与数据存储

以下安全特性已在源代码中得到实现：

- **xAI API 密钥**：通过 `cross-keychain` 机制存储在操作系统的本地凭据存储库中（macOS 的 Keychain、Windows 的 Credential Manager、Linux 的 Secret Service；服务名称：`grok-image-cli`，账户名称：`api-key`）。根据设计，该密钥绝不会以明文形式保存到磁盘上。如果找不到凭据存储条目，CLI 会使用环境变量 `XAI_API_KEY` 作为替代方案。具体实现细节请参见 [`src/infrastructure/adapters/credential-store.adapter.ts`](https://github.com/cyberash-dev/grok-image-cli/blob/main/src/infrastructure/adapters/credential-store.adapter.ts)。
- **无配置文件**：所有设置都通过 CLI 参数传递；除了凭据存储条目外，没有任何数据会被保存到磁盘上。
- **网络通信**：API 密钥仅通过官方的 `@ai-sdk/xai` SDK 通过 HTTPS 协议发送到 `api.x.ai`。在编辑远程 URL 中的图像时（使用 `-i https://...`），SDK 会额外发起一个 HTTPS 请求来获取源图像。CLI 本身不会进行其他网络请求（安装过程中的 npm/git 请求属于标准包管理器的行为）。具体实现细节请参见 [`src/infrastructure/adapters/grok-api.adapter.ts`](https://github.com/cyberash-dev/grok-image-cli/blob/main/src/infrastructure/adapters/grok-api.adapter.ts)。
- **生成的图像**：保存在本地输出目录（默认为 `./grok-images`）。生成的图像不会被缓存或上传到其他地方。

## API 参考

该 CLI 通过 Vercel AI SDK 调用 xAI 的图像生成 API：
- 生成图像：`POST /v1/images/generations`
- 编辑图像：`POST /v1/images/edits`

更多文档请参考：https://docs.x.ai/docs/guides/image-generation