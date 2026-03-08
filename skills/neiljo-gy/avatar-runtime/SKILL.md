---
name: avatar-runtime
description: 使用 `avatar-runtime` npm 包嵌入并控制虚拟化身。该包支持 Live2D 渲染、VRM 3D 格式、矢量图作为备用方案，并通过一个与提供商无关的会话桥接机制来实现基于控制的表情/身体/场景动画。适用于用户请求虚拟化身、面部控制动画、Live2D 角色、化身小部件嵌入，或启动/停止化身会话的场景。
allowed-tools: Bash(node:*) Bash(curl:*) Bash(npm:*)
---
# 虚拟形象运行时技能（Avatar Runtime Skills）

## 运行时端点（Runtime Endpoint）

默认值：`http://127.0.0.1:3721`  
可覆盖：环境变量 `AVATAR_RUNTIME_URL`（如果未设置，则自动使用默认值）。

```bash
export AVATAR_RUNTIME_URL="${AVATAR_RUNTIME_URL:-http://127.0.0.1:3721}"
```

## 首次设置（First-time Setup）

### VRM 3D 虚拟形象（免费，无需账户）

```bash
# Run from the package root
bash scripts/ensure-default-vrm-sample.sh
```

从 `@pixiv/three-vrm` 下载 `VRM1_Constraint_Twist_Sample.vrm`（遵循 CC BY 4.0 许可协议，可自由使用，但需注明出处）。  
将其设置为 `assets/vrm/slot/default.vrm`，这样 `npm run dev:vrm-bridge` 即可自动加载该模型。

### Live2D 虚拟形象

Live2D 槽（`assets/live2d/slot/`）在 `live2d` 提供者进行渲染之前需要一个模型文件。

**选项 A — 使用您自己的模型**（推荐）：  
将您拥有的任何 Cubism 2（`.model.json`）或 Cubism 4（`.model3.json`）模型文件复制到 `assets/live2d/slot/`，并命名为 `default.model.json` 或 `default.model3.json`。

**选项 B — 仅用于本地开发**（请注意风险）：

```bash
# Run from the package root (where package.json lives)
bash scripts/ensure-default-live2d-sample.sh
```

从 npm 包 `live2d-widget-model-chitose@1.0.5` 中下载 `chitose` 用于本地测试。  
⚠️ 原始模型受 [Live2D 免费材料许可协议](https://www.live2d.com/en/sdk/license/free-material/) 的约束，禁止重新分发和商业使用。**请勿** 使用该模型进行部署或分发。

## 启动服务器（Starting the Server）

```bash
# zero-config (mock provider — no API key required)
AVATAR_PROVIDER=mock npx avatar-runtime

# with Live2D local bridge
npm run dev:live2d-cubism-bridge          # terminal A — bridge on :3755
AVATAR_PROVIDER=live2d LIVE2D_ENDPOINT=http://127.0.0.1:3755 npx avatar-runtime  # terminal B

# with VRM 3D avatar (free models from https://hub.vroid.com — place .vrm in assets/vrm/slot/)
npm run dev:vrm-bridge                    # terminal A — asset server on :3756
AVATAR_PROVIDER=vrm npx avatar-runtime   # terminal B
```

## 会话 API（Session API）

```bash
# start session
curl -s -X POST "$AVATAR_RUNTIME_URL/v1/session/start" \
  -H "content-type: application/json" \
  -d '{"personaId":"{{slug}}","form":"image"}'

# send text to active session
curl -s -X POST "$AVATAR_RUNTIME_URL/v1/input/text" \
  -H "content-type: application/json" \
  -d '{"sessionId":"<sessionId>","text":"hello"}'

# query current state (includes control namespace for renderer)
curl -s "$AVATAR_RUNTIME_URL/v1/status"
```

## 虚拟形象控制 API（v0.2）（Avatar Control API, v0.2）

运行时使用统一的 `control` 命名空间，替代了旧的 `faceControl` 字段。

```bash
# Set face expression
curl -s -X POST "$AVATAR_RUNTIME_URL/v1/control/avatar/set" \
  -H "content-type: application/json" \
  -d '{
    "face": {
      "pose":  { "yaw": 0.2 },
      "mouth": { "smile": 0.7 }
    },
    "emotion": { "valence": 0.8, "arousal": 0.3, "label": "happy" }
  }'

# Set body pose (VRM only)
curl -s -X POST "$AVATAR_RUNTIME_URL/v1/control/avatar/set" \
  -H "content-type: application/json" \
  -d '{
    "body": {
      "preset": "wave",
      "skeleton": { "rightUpperArm": { "x": 0, "y": 0, "z": 60 } }
    }
  }'

# Set scene (VRM only)
curl -s -X POST "$AVATAR_RUNTIME_URL/v1/control/scene/set" \
  -H "content-type: application/json" \
  -d '{
    "camera": { "fov": 40, "position": { "x": 0, "y": 1.4, "z": 2.5 } },
    "world": { "ambientLight": 0.5, "keyLight": { "intensity": 1.2 } }
  }'

# Full control patch in one call
curl -s -X POST "$AVATAR_RUNTIME_URL/v1/control/set" \
  -H "content-type: application/json" \
  -d '{
    "avatar": {
      "face": { "mouth": { "smile": 0.5 } },
      "emotion": { "label": "neutral" }
    },
    "scene": { "world": { "background": "#001133" } }
  }'
```

**部分补丁（Partial Patches）：** 仅合并被修改的子对象。每个子域（`avatar.face`、`avatar.body`、`avatar.emotion`、`scene`）会独立合并——修改 `mouth.smile` 不会影响 `eyes` 的显示。

## 嵌入虚拟形象小部件（浏览器）（Embedding an Avatar Widget, Browser）

脚本标签使用量极少——供应商提供的脚本会自动加载：

```html
<script src="/packages/avatar-runtime/web/avatar-widget.js"></script>
<div id="avatar" style="width:360px;height:360px"></div>
<script>
  var widget = new AvatarWidget(document.getElementById('avatar'), {
    modelUrl: '/packages/avatar-runtime/assets/live2d/slot/default.model.json',
    stateUrl: 'http://127.0.0.1:3721/v1/status',   // polls control namespace
    pollMs:   500,
    // vendorBase: '/your/vendor-dist',              // required for Live2D in production
  });
  widget.ready().catch(function(e) { console.error(e); });
</script>
```

### VRM 3D 虚拟形象（VRM 3D Avatar）

```html
<script src="/packages/avatar-runtime/web/avatar-widget.js"></script>
<div id="avatar" style="width:360px;height:360px"></div>
<script>
  new AvatarWidget(document.getElementById('avatar'), {
    vrmUrl:   '/packages/avatar-runtime/assets/vrm/slot/default.vrm',
    stateUrl: 'http://127.0.0.1:3721/v1/status',
  });
</script>
```

如果没有模型（使用矢量替代方案——无需任何文件）：

```html
<script src="/packages/avatar-runtime/web/avatar-widget.js"></script>
<div id="avatar" style="width:360px;height:360px"></div>
<script>
  new AvatarWidget(document.getElementById('avatar'), {
    stateUrl: 'http://127.0.0.1:3721/v1/status'
  });
</script>
```

## 手动控制虚拟形象（Widget-based Avatar Control）

`update()` 方法接受一个包含 `control` 对象的 `mediaState` 参数。  
可以在 `ready()` 方法执行前调用该方法——数据会被缓冲并在页面加载完成后应用。

```js
widget.update({
  control: {
    avatar: {
      face: {
        pose:  { yaw: 0.2, pitch: 0.1, roll: 0 },
        eyes:  { blinkL: 0.9, blinkR: 0.9, gazeX: 0, gazeY: 0 },
        mouth: { jawOpen: 0.3, smile: 0.5 }
      },
      emotion: { valence: 0.7, arousal: 0.2, label: 'content', intensity: 0.6 }
    }
  }
});
```

## 从运行时状态控制虚拟形象（Controling the Avatar from Runtime State）

 `/v1/status` 响应中包含由当前使用的提供者生成的 `control` 数据，以及代理设置的值。  
`AvatarWidget` 会以 `pollMs` 为间隔自动请求这些数据。

### 手动请求数据（Manual Data Requesting）：

```bash
curl -s "$AVATAR_RUNTIME_URL/v1/status" | jq .control
```

## 提供者配置（Provider Configuration）

| 提供者 | 环境变量 | 备注 |
|----------|----------|-------|
| `mock` | — | 开发模式默认值，无需设置环境变量 |
| `heygen` | `HEYGEN_API_KEY` | 用于实时流式虚拟形象。`HEYGEN_STRICT=false` 时切换为模拟模式 |
| `live2d` | `LIVE2D_ENDPOINT` | 需要本地 Cubism 桥接器。`LIVE2D_STRICT=false` 时切换为模拟模式 |
| `vrm` | `VRM_BRIDGE_ENDPOINT` | 用于本地 3D 虚拟形象，支持客户端渲染。模型可从 [VRoid Hub](https://hub.vroid.com) 免费获取。无需 API 密钥 |
| `kusapics` | `KUSAPICS_API_KEY`, `KUSAPICS_BASE_URL` | 专注于动画的图像提供者 |

## 提供者的功能（Provider Features）

| 提供者 | faceRig | lipSync | gaze | blink | bodyMotion | streaming | bodyRig | sceneControl |
|----------|:-------:|:-------:|:----:|:-----:|:----------:|:---------:|:-------:|:------------:|
| `mock`     | ✓ | — | ✓ | ✓ | — | — | — | — |
| `heygen`   | ✓ | ✓ | — | — | ✓ | ✓ | — | — |
| `live2d`   | ✓ | ✓ | ✓ | ✓ | — | — | — | — |
| `vrm`      | ✓ | — | ✓ | ✓ | — | — | ✓ | ✓ |
| `kusapics` | — | — | — | — | — | — | — | — |

`bodyRig` 和 `sceneControl` 是 VRM 特有的功能——分别使用 `/v1/control/avatar/set` 和 `/v1/control/scene/set` 进行配置。

## 快速入门：VRM 3D 虚拟形象（无需 API 密钥）（Quick Start: VRM 3D Avatar, No API Key）

```bash
# Terminal A — Download sample VRM model + serve assets on :3756
cd packages/avatar-runtime
bash scripts/ensure-default-vrm-sample.sh   # one-time download (CC BY 4.0)
npm run dev:vrm-bridge                       # keeps running

# Terminal B — Start runtime pointing at the VRM bridge
AVATAR_PROVIDER=vrm npx avatar-runtime
```

测试面部和身体控制功能：

```bash
BASE=http://127.0.0.1:3721
SESSION=$(curl -s -X POST "$BASE/v1/session/start" \
  -H "content-type: application/json" \
  -d '{"personaId":"demo","form":"image"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['sessionId'])")

# Face expression
curl -s -X POST "$BASE/v1/control/avatar/set" \
  -H "content-type: application/json" \
  -d '{"face":{"pose":{"yaw":0.2},"mouth":{"smile":0.7}},"emotion":{"label":"happy","valence":0.8}}'

# Body pose (VRM only)
curl -s -X POST "$BASE/v1/control/avatar/set" \
  -H "content-type: application/json" \
  -d '{"body":{"preset":"wave","skeleton":{"rightUpperArm":{"x":0,"y":0,"z":60}}}}'

# Camera scene (VRM only)
curl -s -X POST "$BASE/v1/control/scene/set" \
  -H "content-type: application/json" \
  -d '{"camera":{"fov":35,"position":{"x":0,"y":1.5,"z":2.2}},"world":{"ambientLight":0.6}}'
```

将 VRM 查看器嵌入页面中：

```html
<script src="/packages/avatar-runtime/web/avatar-widget.js"></script>
<div id="avatar" style="width:400px;height:600px"></div>
<script>
  new AvatarWidget(document.getElementById('avatar'), {
    vrmUrl:   '/packages/avatar-runtime/assets/vrm/slot/default.vrm',
    stateUrl: 'http://127.0.0.1:3721/v1/status',
    pollMs:   400,
  });
</script>
```

## 快速入门：HeyGen 流式虚拟形象（Quick Start: HeyGen Streaming Avatar）

**前提条件：** 需要 HeyGen API 密钥以及您的 HeyGen 账户中的虚拟形象 ID。

```bash
export HEYGEN_API_KEY="your-key"
export HEYGEN_AVATAR_ID="your-avatar-id"   # from HeyGen dashboard

AVATAR_PROVIDER=heygen npx avatar-runtime
```

启动会话并流式播放语音片段：

```bash
BASE=http://127.0.0.1:3721
SESSION=$(curl -s -X POST "$BASE/v1/session/start" \
  -H "content-type: application/json" \
  -d '{"personaId":"demo","form":"video"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['sessionId'])")

curl -s -X POST "$BASE/v1/input/text" \
  -H "content-type: application/json" \
  -d "{\"sessionId\":\"$SESSION\",\"text\":\"Hello! I am your AI companion.\"}"

# Poll for a video URL in the response:
curl -s "$BASE/v1/status" | python3 -c "import sys,json; s=json.load(sys.stdin); print(s.get('avatarVideo','(pending)'))"
```

**优雅降级机制（Graceful Degradation）：** 当 `HEYGEN_STRICT` 未设置（默认值为 `false`）时，如果 API 密钥缺失或请求失败，运行时系统会自动切换到模拟模式——适用于无需密钥的本地开发环境。

## 备用方案（Fallback Strategy）

如果运行时系统不可用或返回错误：
- 继续以文本模式进行交互
- 通知用户当前虚拟形象功能不可用
- 不应声称渲染或语音播放成功

## 额外参考资料（Additional References）：
- [WEB-EMBEDDING.md](references/WEB-EMBEDDING.md) — 渲染器注册表、自定义渲染器实现、npm 使用方法