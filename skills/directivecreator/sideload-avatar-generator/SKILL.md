---
name: sideload-avatar-generator
description: 通过 Sideload.gg，可以根据文本提示或图片生成 3D 虚拟形象（格式为 VRM、GLB 或 MML）。支持按使用量付费，支持使用任何 x402 钱包进行支付（基础货币为 USDC）。
metadata: {"openclaw":{"emoji":"🎭","requires":{"bins":["node"]}}}
---

# Sideload头像生成器

使用 [Sideload.gg](https://sideload.gg) 根据文本描述或参考图片生成3D头像。支持按使用次数计费的支付方式，通过 [x402协议](https://x402.org) 支付——基础套餐下每次生成费用为2美元（USDC）。

**支持任何x402钱包**。请携带您自己的钱包和私钥，无需使用任何专有钱包。

## 生成结果

每次生成会生成四种格式的文件：

| 格式 | 文件类型 | 用途 |
|--------|------|----------|
| **GLB** | `.glb` | 通用3D格式——适用于Three.js、Unity、Unreal及网页浏览器 |
| **VRM** | `.vrm` | 头像标准格式——适用于VRChat、VTubing及社交应用 |
| **MML** | URL | 元宇宙标记语言（Metaverse Markup Language）格式——适用于支持MML的虚拟世界 |
| **PNG** | `.png` | 用于头像生成的参考图片 |

## 🎭 使用 @pixiv/three-vrm 渲染头像

VRM格式的输出文件专为与 [@pixiv/three-vrm](https://github.com/pixiv/three-vrm) 配合使用而设计，该库是用于加载、显示和动画化VRM头像的标准Three.js库。如果您已经在使用Three.js进行开发，生成的头像可以无缝集成，并支持完整的骨骼结构：

```javascript
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { VRMLoaderPlugin } from '@pixiv/three-vrm';

const loader = new GLTFLoader();
loader.register((parser) => new VRMLoaderPlugin(parser));

loader.load('https://aiml.sideload.gg/models/avt-xxx.vrm', (gltf) => {
  const vrm = gltf.userData.vrm;
  scene.add(vrm.scene);

  // Animate bone transforms, look-at, etc.
});
```

这使得您可以使用Sideload轻松生成头像，并立即将其应用于任何Three.js场景中——无论是游戏、社交应用还是虚拟世界。

有关在元宇宙中构建交互式3D体验的更多信息，请参阅 [awesome-mml](https://github.com/DirectiveCreator/awesome-mml)——这是一个精选的MML（元宇宙标记语言）资源列表。

## 先决条件

- **Node.js 18+**  
- **x402支付令牌**：使用您自己的钱包/签名工具进行支付，并通过 `--x402-token` 参数传递令牌。本工具不会处理私钥信息。

  ```bash
  # Check the cost first
  node scripts/generate.js --probe

  # Generate with your x402 token
  node scripts/generate.js --prompt "..." --x402-token <base64-encoded-payment>
  ```

  您可以使用任何兼容x402的客户端来获取支付令牌：[Coinbase x402 SDK](https://github.com/coinbase/x402)、[Thirdweb x402](https://portal.thirdweb.com/payments/x402) 或您自己的支付流程。

## 设置

```bash
npm install
```

## 使用方法

### 根据文本描述生成头像

```bash
node scripts/generate.js --prompt "A cyberpunk samurai with glowing red armor" --x402-token <token>
```

### 根据图片URL生成头像

```bash
node scripts/generate.js --image https://example.com/character.png --x402-token <token>
```

### 根据本地图片生成头像

```bash
node scripts/generate.js --image /path/to/photo.jpg --x402-token <token>
```

### 查看费用（无需支付）

```bash
node scripts/generate.js --probe
```

### 查看任务状态

```bash
node scripts/status.js avt-a1b2c3d4
```

### 配置选项

| 选项 | 说明 |
|------|-------------|
| `--prompt "text"` | 头像的文本描述 |
| `--image <url-or-path>` | 参考图片的URL或本地文件路径 |
| `--x402-token <token>` | x402支付令牌（生成头像时必需） |
| `--probe` | 仅查看费用，不进行生成 |
| `--output <name>` | 下载文件的自定义文件名 |
| `--no-download` | 跳过下载结果文件 |

## API参考

请参阅 [SIDELOAD-API.md](./SIDELOAD-API.md) 以获取完整的API文档，或访问 [sideload.gg/agents/raw](https://sideload.gg/agents/raw)。

### 快速参考

**生成命令：**
```
POST https://sideload.gg/api/agent/generate
Headers: Content-Type: application/json, x-payment: <x402_token>
```

**文本描述：**
```json
{
  "type": "text",
  "prompt": "描述头像的详细信息"
}
```

**图片描述：**
```json
{
  "type": "image",
  "imageUrl": "https://..."
}
```

**查询任务状态：**
```bash
GET https://sideload.gg/api/agent/generate/{jobId}/status
```
（无需认证）

## 提示技巧

- 在描述头像时请具体说明：
  - **外观**：服装、颜色、配饰
  - **风格**：写实、动漫、卡通、赛博朋克
  - **特殊元素**：盔甲、武器、发型、翅膀

**示例提示：**
- “一位穿着皮制工具带、配备铜制机械臂的蒸汽朋克工程师”
- “一位拥有长银发、发光紫色眼睛、手持华丽金色法杖的动漫风格女巫”
- “一位身穿蓝白相间动力装甲、带有发光能量护盾的未来主义士兵”

## 图片要求：

- 图片格式：PNG、JPG或WebP
- 最佳图片为正面肖像或全身照
- 图像轮廓清晰，服装和特征明显
- 分辨率越高，生成效果越好

## 使用限制与费用

- 每次生成费用为2美元（USDC，基于x402协议，链ID 8453）
- 每个钱包每30分钟最多生成10次
- 如收到429状态码的响应，请检查 `Retry-After` 头部信息以重试请求

## 链接资源

- [Sideload.gg](https://sideload.gg)
- [API文档](https://sideload.gg/agents/raw)
- [@pixiv/three-vrm](https://github.com/pixiv/three-vrm) — 用于加载VRM头像的Three.js库
- [awesome-mml](https://github.com/DirectiveCreator/awesome-mml) — 元宇宙标记语言（MML）资源库
- [x402协议](https://x402.org)
- [Coinbase x402 SDK](https://github.com/coinbase/x402)
- [VRM规范](https://vrm.dev/en/)
- [MML（元宇宙标记语言）](https://mml.io)