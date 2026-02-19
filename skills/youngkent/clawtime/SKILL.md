---
name: clawtime
description: 操作 ClawTime：包括网页聊天小部件、任务面板以及头像创建功能。
---
# ClawTime 技能

ClawTime 是 OpenClaw 的一个 Webchat 接口，提供了操作参考。

## 安装

首次设置（克隆、配置、部署）请参考 **[INSTALL.md](./INSTALL.md)**。

---

## 操作

```bash
# Status & logs
systemctl --user status clawtime
journalctl --user -u clawtime -f

# Restart after config changes  
systemctl --user restart clawtime

# Get current tunnel URL
journalctl --user -u clawtime-tunnel | grep trycloudflare | tail -1
```

## 小部件

ClawTime 支持交互式小部件，以增强用户体验。在响应中包含小部件的标记，它们会作为 UI 组件进行渲染。

### 小部件语法

```
[[WIDGET:{"widget":"TYPE","id":"UNIQUE_ID",...properties}]]
```

这些标记会从显示的消息中提取出来，并渲染成交互式的 UI 元素。

### 可用的小部件

#### 按钮
```
[[WIDGET:{"widget":"buttons","id":"choice1","label":"Pick a color:","options":["Red","Green","Blue"]}]]
```
- `label` — 按钮上方的提示文本
- `options` — 按钮标签的数组

#### 确认
```
[[WIDGET:{"widget":"confirm","id":"delete1","title":"Delete file?","message":"This cannot be undone."}]]
```
- `title` — 加粗的标题文本
- `message` — 描述文本
- 会显示“取消”和“确认”按钮

#### 进度条
```
[[WIDGET:{"widget":"progress","id":"upload1","label":"Uploading...","value":65}]]
```
- `label` — 描述文本
- `value` — 进度百分比（0-100）

#### 代码
```
[[WIDGET:{"widget":"code","id":"snippet1","filename":"example.py","code":"print('Hello')","language":"python"}]]
```
- `filename` — 标题中的文件名
- `code` — 代码内容
- `language` — 代码高亮提示
- 包含“复制”按钮

#### 表单
```
[[WIDGET:{"widget":"form","id":"survey1","label":"Quick Survey","fields":[{"name":"email","label":"Email","type":"text"},{"name":"rating","label":"Rating","type":"text"}]}]]
```
- `label` — 表单标题
- `fields` — `{name, label, type}` 的数组

#### 日期选择器
```
[[WIDGET:{"widget":"datepicker","id":"date1","label":"Select date:"}]]
```
- `label` — 提示文本

### 小部件响应

当用户与小部件交互时：
```
[WIDGET_RESPONSE:{"id":"choice1","widget":"buttons","value":"Red","action":"submit"}]
```

### 最佳实践

1. **始终使用唯一的 ID** — 每个小部件都需要一个唯一的 `id`
2. **保持选项简洁** — 按钮标签应简短明了
3. **使用小部件进行结构化输入** — 比直接输入“1、2 或 3”更好
4. **确认用户的操作** — 显示用户选择了什么

## 任务面板

ClawTime 包含一个任务面板，用于跟踪工作进度。**请将其作为标准任务列表使用。**

### 文件格式

任务以 markdown 格式存储在 `~/.clawtime/tasks.json` 文件中：

```markdown
# Tasks

## Active
- 🟡 Task you're working on right now

## Blocked
- ⏳ Task waiting on someone else

## Backlog
- Task to do later

## Done
- ✅ Completed task
```

### 各部分的意义

| 部分 | 含义 |
|---------|---------|
| **活动中的** | 当前正在处理的任务 |
| **阻塞中** | 等待输入或依赖项 |
| **待办事项** | 以后会处理的任务 |
| **已完成** | 已完成任务（在 UI 中隐藏） |

### 任务图标

| 图标 | 含义 |
|------|---------|
| 🟡 | 活动中/等待中 |
| ⏳ | 被阻塞/等待中 |
| ✅ | 已完成 |
| `- [x]` | 也标记为已完成 |

## 头像创建

ClawTime 使用 **Three.js 体素头像** — 由简单形状组成的 3D 角色，会根据状态进行动画展示。

### 头像模板

在 `~/.clawtime/avatars/<name>.js` 文件中创建头像：

```javascript
/* AVATAR_META {"name":"MyAgent","emoji":"🤖","description":"Custom 3D avatar","color":"4f46e5"} */
(function() {
  'use strict';
  
  var scene, camera, renderer, character;
  var head, leftEye, rightEye, mouth;
  var clock = new THREE.Clock();
  var currentState = 'idle';
  var isInitialized = false;

  // ─── Required: Initialize the 3D scene ───
  window.initAvatarScene = function() {
    if (isInitialized) return;
    
    var container = document.getElementById('avatarCanvas');
    if (!container) return;
    
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f1318);
    
    var w = container.clientWidth, h = container.clientHeight;
    camera = new THREE.PerspectiveCamera(40, w / h, 0.1, 100);
    camera.position.set(0, 2, 8);
    camera.lookAt(0, 0, 0);
    
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(w, h);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);
    
    // Lighting
    scene.add(new THREE.AmbientLight(0x606080, 1.5));
    var light = new THREE.DirectionalLight(0xffffff, 2.0);
    light.position.set(4, 10, 6);
    scene.add(light);
    
    // Build your character
    character = new THREE.Group();
    buildCharacter();
    scene.add(character);
    
    isInitialized = true;
    animate();
  };
  
  function buildCharacter() {
    var bodyMat = new THREE.MeshLambertMaterial({ color: 0x4f46e5 });
    var body = new THREE.Mesh(new THREE.BoxGeometry(1.5, 2, 1), bodyMat);
    body.position.y = 0;
    character.add(body);
    
    var headMat = new THREE.MeshLambertMaterial({ color: 0x4f46e5 });
    head = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1), headMat);
    head.position.y = 1.8;
    character.add(head);
    
    var eyeMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    leftEye = new THREE.Mesh(new THREE.SphereGeometry(0.15), eyeMat);
    leftEye.position.set(-0.25, 1.9, 0.5);
    character.add(leftEye);
    
    rightEye = new THREE.Mesh(new THREE.SphereGeometry(0.15), eyeMat);
    rightEye.position.set(0.25, 1.9, 0.5);
    character.add(rightEye);
    
    var pupilMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
    mouth = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.1, 0.1), pupilMat);
    mouth.position.set(0, 1.5, 0.5);
    character.add(mouth);
  }
  
  function animate() {
    requestAnimationFrame(animate);
    var t = clock.getElapsedTime();
    
    if (character) {
      character.position.y = Math.sin(t * 2) * 0.05;
    }
    
    if (currentState === 'thinking') {
      head.rotation.z = Math.sin(t * 3) * 0.1;
    } else if (currentState === 'talking') {
      mouth.scale.y = 1 + Math.sin(t * 15) * 0.5;
    } else {
      head.rotation.z = 0;
      mouth.scale.y = 1;
    }
    
    renderer.render(scene, camera);
  }
  
  // ─── Required: Handle state changes ───
  window.setAvatarState = function(state) {
    currentState = state;
  };
  
  // ─── Required: Handle connection state ───
  window.setConnectionState = function(state) {
    // state: 'online', 'connecting', 'offline'
  };
  
  // ─── Required: Handle resize ───
  window.adjustAvatarCamera = function() {
    if (!renderer) return;
    var container = document.getElementById('avatarCanvas');
    var w = container.clientWidth, h = container.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  };
})();
```

### 设置为默认头像

在 `~/.clawtime/config.json` 中创建或更新配置：

```json
{
  "selectedAvatar": "<name>"
}
```

### 头像状态

每种状态都应有明显的视觉区别和对应的动作/指示器。用户应能立即识别头像所处的状态。

| 状态 | 含义 | 设计思路 |
|-------|---------|--------------|
| `空闲` | 默认状态，等待中 | 呼吸、四处张望、展示姿势、偶尔眨眼 |
| `思考中` | 处理请求 | 头部倾斜、眼睛向上、思维泡泡（❓）、轻敲脚或翅膀 |
| `说话中` | 发送响应 | 嘴部动画、语音泡泡、音符（🎵）、手势 |
| **倾听中** | 用户正在说话 | 向前倾、眼睛睁得大大的、耳朵/头顶竖起 |
| **工作中** | 进行长时间的任务 | 可看到笔记本电脑/工具、打字动作、专注地眯眼 |
| **快乐** | 结果积极 | 跳跃、爱心符号（❤️）、眯着笑的眼睛（^_^）、摇尾巴 |
| **庆祝** | 取得重大成功 | 跳跃、旋转、五彩纸屑（⭐）、充满活力 |
| **睡眠中** | 未活动/超时 | 眼睛闭合、Z 字形符号（💤）、蜷缩着、呼吸缓慢 |
| **错误** | 出现问题 | 颤抖、感叹符号（❗）、羽毛凌乱、带有红色色调 |
| **反思中** | 沉思中 | 电灯泡（💡）、向上凝视、平静的姿势、一只手举起 |

### 状态设计原则

1. **视觉指示器很重要** — 根据状态添加不同的浮动符号（❓❤️💡❗💤⭐）
2. **肢体语言很重要** — 每种状态都需要独特的姿势、动作速度和能量水平
3. **眼睛很重要** — 眼睛的大小、开闭程度、眯眼或睁大的程度都很重要
4. **动作节奏要有所区别** — 快速/活泼表示快乐，缓慢/轻柔表示睡眠，颤抖表示错误
5. **道具能增加清晰度** — 例如：笔记本电脑表示工作状态，Z 字形符号表示睡眠状态，五彩纸屑表示庆祝状态
6. **像动画师一样思考** — 这个状态下皮克斯角色会怎么做？

### 创意示例

**鹦鹉头像：**
- **思考中** → 用脚抓头，疑问符号出现
- **说话中** → 嘴张开/闭合，音符飘浮
- **错误** → 羽毛飞散，发出惊叫声，翅膀张开
- **庆祝中** — 鹦鹉旋转，周围飘满五彩纸屑

**蝾螈头像：**
- **思考中** — 火焰闪烁得更亮，一只脚轻敲
- **睡眠中** — 火焰变成微小的余烬，蜷缩着
- **错误** — 火焰变红，全身颤抖
- **反思中** | 出现电灯泡，一只爪子思考地举起

### 头像设计提示

- 查看 `~/.clawtime/avatars/` 文件中的完整示例
- 使用体素风格（立方体、球体）—— 与 ClawTime 的设计风格相匹配
- 确保所有状态都有独特的视觉表现
- 添加连接状态指示器（平台上的光环/发光效果）
- 在桌面和移动设备上进行测试
- 保持多边形数量适中，以优化移动设备的性能
- 根据状态显示或隐藏指示器对象（避免每一帧都创建/销毁）

## 关键文件

| 路径 | 用途 |
|------|---------|
| `~/.clawtime/.env` | 隐私设置和配置 |
| `~/.clawtime/config.json` | 头像选择、偏好设置 |
| `~/.clawtime/credentials.json` | 密钥数据 |
| `~/.clawtime/sessions.json` | 活动中的会话 |
| `~/.clawtime/avatars/` | 自定义头像 |
| `~/.clawtime/tasks.json` | 任务列表 |

## 故障排除

有关常见问题的解决方法，请参阅 **[INSTALL.md → 故障排除](./INSTALL.md#troubleshooting)**。