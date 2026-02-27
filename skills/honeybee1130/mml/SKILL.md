---
name: mml
description: "使用 MML（Metaverse Markup Language）为 Otherside 元宇宙及其他兼容 MML 的环境构建 3D 场景和交互式体验。该技术适用于创建 3D 对象、世界、交互元素、动画、模型、角色、音频/视频、标签、基于碰撞的交互功能、位置跟踪、聊天集成等功能。相关触发条件包括：MML、元宇宙标记语言（metaverse markup）、3D 场景构建（3D scene building）、Otherside 世界构建（Otherside world building）、m-cube、m-model、m-character、m-group、m-frame、m-attr-anim 等。"
---
# MML（元宇宙标记语言）

> **完整编译参考文档：** `/home/ubuntu/.openclaw/workspace/research/mml-reference.md`  
> 来源：mml.io + DashBODK Studio (dashbodk.vercel.app/docs)  
> 包含所有元素、属性、事件和碰撞检测模式。

MML 是一种类似于 HTML 的标记语言，用于构建 3D 场景。文档通过 WebSocket 传输，并由客户端（如 Web/Three.js 或 Unreal Engine）进行渲染。MML 支持通过内嵌的 `<script>` 标签进行脚本编写（使用标准的 DOM API）。

## 关键概念

- **单位**：位置以米为单位，旋转以度为单位，字体大小以厘米为单位  
- **坐标系**：x（右侧），y（上方），z（前方）  
- **常见属性**：所有可见元素都具有 `x`, `y`, `z`, `rx`, `ry`, `rz`, `sx`, `sy`, `sz`, `visible`, `id`, `class` 等属性  
- **碰撞检测系统**：为元素设置 `collision-interval`（以毫秒为单位），可接收 `collisionstart`, `collisionmove`, `collisionend` 事件  
- **文档时间**：动画和媒体使用文档的生命周期时间（从文档开始计算的毫秒数）  
- **脚本编写**：通过 `<script>` 标签进行标准的 DOM 操作，例如 `document.getElementById()`, `addEventListener()`, `setAttribute()` 等。

## 元素快速参考

| 元素          | 用途                                      | 关键属性                                      |
|-----------------|----------------------------------------|----------------------------------------|
| `m-group`       | 容器，将子元素按单位进行变换                        | （仅支持 `transform` 属性）                        |
| `m-cube`       | 3D 立方体                                      | `width`, `height`, `depth`, `color`, `opacity`                   |
| `m-sphere`       | 3D 球体                                      | `radius`, `color`, `opacity`                   |
| `m-cylinder`       | 3D 圆柱体                                      | `radius`, `height`, `color`, `opacity`                   |
| `m-plane`       | 平面                                      | `width`, `height`, `color`, `opacity`                   |
| `m-model`       | 加载 3D 模型（GLTF/OBJ/FBX 格式）                     | `src`, `anim-src`, `anim-loop`, `anim-enabled`, `start-time`, `pause-time`       |
| `m-character`     | 3D 字符（可与 `m-model` 的子元素组合使用）                | `src`, `anim-src`, `anim-loop`, `anim-enabled`, `start-time`, `pause-time`       |
| `m-light`       | 点光源或聚光灯                                  | `type`, `intensity`, `distance`, `angle`, `enabled`, `cast-shadows`, `color`     |
| `m-image`       | 在 3D 环境中显示图像                             | `src`, `width`, `height`, `emissive`, `opacity`                   |
| `m-video`       | 在 3D 环境中播放视频（支持 WHEP 流媒体）                   | `src`, `width`, `height`, `emissive`, `loop`, `enabled`, `volume`, `start-time`, `pause-time` |
| `m-audio`       | 空间音频                                      | `src`, `loop`, `loop-duration`, `enabled`, `volume`, `cone-angle`, `cone-falloff-angle`, `start-time`, `pause-time` |
| `m-label`       | 平面上的文本标签                                  | `content`, `width`, `height`, `font-size`, `font-color`, `padding`, `alignment`, `color`, `emissive` |
| `m-frame`       | 嵌入另一个 MML 文档                               | `src`, `min-x`, `max-x`, `min-y`, `max-y`, `min-z`, `max-z`, `load-range`, `unload-range`     |
| `m-link`       | 可点击链接（无视觉提示）                               | `href`, `target`                             |
| `m-prompt`       | 点击时显示的用户输入框                               | `message`, `placeholder`, `prefill`, `onprompt`                 |
| `m-interaction`    | 在空间中的交互动作                              | `range`, `in-focus`, `line-of-sight`, `priority`, `oninteract`           |
| `m-position-probe`    | 跟踪用户位置                                  | `range`, `onpositionenter`, `onpositionmove`, `onpositionleave`          |
| `m-chat-probe`    | 接收聊天消息                                  | `range`, `onchat`                             |
| `m-attr-anim`     | 关键帧动画（与文档时间同步）                         | `attr`, `start`, `end`, `start-time`, `pause-time`, `duration`, `loop`, `easing`       |
| `m-attr-lerp`     | 属性值的平滑过渡                               | `attr`, `duration`, `easing`                         |

## 常见用法示例

### 带有变换的基本场景  
```html
<m-group x="0" y="1" z="-5">
  <m-cube color="red" width="2" height="0.5" depth="2"></m-cube>
  <m-sphere color="blue" radius="0.3" y="1"></m-sphere>
</m-group>
```  

### 循环旋转动画  
```html
<m-cube color="green" y="2">
  <m-attr-anim attr="ry" start="0" end="360" duration="3000" loop="true"></m-attr-anim>
</m-cube>
```  

### 属性变化时的平滑过渡  
```html
<m-cube id="box" color="red" y="1">
  <m-attr-lerp attr="x,y,z" duration="500" easing="easeInOutQuad"></m-attr-lerp>
</m-cube>
```  

### 点击交互  
```html
<m-cube id="btn" color="blue" onclick="
  this.setAttribute('color', this.getAttribute('color') === 'blue' ? 'red' : 'blue');
"></m-cube>
```  

### 碰撞检测  
```html
<m-cube id="platform" width="5" height="0.2" depth="5" color="green" collision-interval="100">
</m-cube>
<script>
  const platform = document.getElementById("platform");
  platform.addEventListener("collisionstart", (e) => {
    platform.setAttribute("color", "yellow");
  });
  platform.addEventListener("collisionend", (e) => {
    platform.setAttribute("color", "green");
  });
</script>
```  

### 位置跟踪  
```html
<m-position-probe id="probe" range="20" interval="500"></m-position-probe>
<m-label id="info" content="Waiting..." y="3" width="3" height="1"></m-label>
<script>
  const probe = document.getElementById("probe");
  const info = document.getElementById("info");
  probe.addEventListener("positionenter", (e) => {
    info.setAttribute("content", `User ${e.detail.connectionId} entered`);
  });
</script>
```  

### 加载带动画的 3D 模型  
```html
<m-model src="https://example.com/character.glb" 
         anim-src="https://example.com/dance.glb"
         anim-loop="true" y="0" sx="1" sy="1" sz="1">
</m-model>
```  

### 使用 `m-frame` 组合多个文档  
```html
<m-frame src="https://example.com/other-scene.html" 
         x="10" y="0" z="0"
         min-x="-5" max-x="5" min-y="0" max-y="10" min-z="-5" max-z="5">
</m-frame>
```  

### 空间音频  
```html
<m-audio src="https://example.com/music.mp3" 
         loop="true" volume="0.5" 
         x="0" y="2" z="0">
</m-audio>
```  

### 与聊天功能交互的元素  
```html
<m-chat-probe id="chat" range="10"></m-chat-probe>
<m-label id="msg" content="" y="3" width="4" height="1"></m-label>
<script>
  document.getElementById("chat").addEventListener("chat", (e) => {
    document.getElementById("msg").setAttribute("content", e.detail.message);
  });
</script>
```  

## 缓动函数

`m-attr-anim` 和 `m-attr-lerp` 支持以下缓动函数：  
`easeInQuad`, `easeOutQuad`, `easeInOutQuad`, `easeInCubic`, `easeOutCubic`, `easeInQuart`, `easeOutQuart`, `easeInQuint`, `easeOutQuint`, `easeInSine`, `easeOutSine`, `easeInExpo`, `easeOutExpo`, `easeInCirc`, `easeOutCirc`, `easeInElastic`, `easeOutElastic`, `easeInBack`, `easeOutBack`, `easeInBounce`, `easeOutBounce`, `easeInOutBounce`  
（线性插值不支持缓动效果。）

## 事件参考

| 事件          | 来源                                      | 关键属性                                      |
|-----------------|--------|--------------------------------|
| `click`       | 任何可点击元素                              | `detail.connectionId`, `detail.position`                   |
| `collisionstart`    | 具有 `collision-interval` 的元素                   | `detail.connectionId`, `detail.position`                   |
| `collisionmove`    | 具有 `collision-interval` 的元素                   | `detail.connectionId`, `detail.position`                   |
| `collisionend`    | 具有 `collision-interval` 的元素                   | `detail.connectionId`                   |
| `positionenter`    | `m-position-probe`                             | `detail.connectionId`, `detail.position`, `detail.rotation`           |
| `positionmove`    | `m-position-probe`                             | `detail.connectionId`, `detail.position`, `detail.rotation`           |
| `positionleave`    | `m-position-probe`                             | `detail.connectionId`                   |
| `chat`       | `m-chat-probe`                             | `detail.message`, `detail.connectionId`                   |
| `interact`      | `m-interaction`                             | `detail.connectionId`                         |
| `prompt`       | `m-prompt`                             | `detail.value`, `detail.connectionId`                   |
| `connected`/`disconnected` | 文档级别事件                               | `detail.connectionId`                         |

## 平台支持

大多数元素在 Web 和 Unreal Engine 中均可用。但有以下例外：  
- `m-link`：仅支持 Web 平台  
- `m-attr-lerp`：仅支持 Web 平台  
- `m-frame` 的边界和加载范围：仅支持 Web 平台  
- `socket` 属性：仅支持 Web 平台  

## 全部元素文档

有关每个元素的详细属性列表，请参阅 [references/elements.md](references/elements.md)。