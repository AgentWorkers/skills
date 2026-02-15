---
name: clawatar
description: 为您的人工智能代理提供一个具有3D VRM（Virtual Reality Modeling）模型的虚拟形象，该形象支持动画效果、面部表情、语音聊天以及唇形同步功能。当用户需要一个可视化的虚拟形象、VRM查看工具、虚拟形象伴侣，或是类似VTuber风格的3D角色（可以与用户进行对话）时，可以使用该服务。该服务会安装一个基于Web的查看器，该查看器可通过WebSocket进行远程控制。
---

# Clawatar — 3D VRM虚拟形象查看器

为您的AI代理添加一个虚拟身体。这是一个基于Web的VRM虚拟形象，支持162种动画效果、表情动作、TTS语音同步以及AI聊天功能。

## 安装与启动

```bash
# Clone and install
git clone https://github.com/Dongping-Chen/Clawatar.git ~/.openclaw/workspace/clawatar
cd ~/.openclaw/workspace/clawatar && npm install

# Start (Vite + WebSocket server)
npm run start
```

应用程序运行在 `http://localhost:3000`，并通过 `ws://localhost:8765` 进行WebSocket控制。

用户需要提供自己的VRM模型（可以通过拖放方式上传到页面，或通过 `clawatar.config.json` 文件设置 `model.url`）。

## WebSocket命令

向 `ws://localhost:8765` 发送JSON数据：

### play_action
```json
{"type": "play_action", "action_id": "161_Waving"}
```

### set_expression
```json
{"type": "set_expression", "name": "happy", "weight": 0.8}
```
可用表情：`happy`（开心）、`angry`（生气）、`sad`（悲伤）、`surprised`（惊讶）、`relaxed`（放松）

### speak（需要ElevenLabs API密钥）
```json
{"type": "speak", "text": "Hello!", "action_id": "161_Waving", "expression": "happy"}
```

### reset
```json
{"type": "reset"}
```

## 动画参考

| 情绪 | 动作ID |
|------|-----------|
| 问候 | `161_Waving` |
| 开心 | `116_Happy Hand Gesture` |
| 思考 | `88_Thinking` |
| 同意 | `118_Head Nod Yes` |
| 不同意 | `144_Shaking Head No` |
| 笑 | `125_Laughing` |
| 悲伤 | `142_Sad Idle` |
| 跳舞 | `105_Dancing`、`143_Samba Dancing`、`164_Ymca Dance` |
| 竖起大拇指 | `153_Standing Thumbs Up` |
| 闲置 | `119_Idle` |

完整动画列表：`publicAnimations/catalog.json`（共162种动画）

## 从代理端发送命令

```bash
cd ~/.openclaw/workspace/clawatar && node -e "
const W=require('ws'),s=new W('ws://localhost:8765');
s.on('open',()=>{s.send(JSON.stringify({type:'speak',text:'Hello!',action_id:'161_Waving',expression:'happy'}));setTimeout(()=>s.close(),1000)})
"
```

## 用户界面特性

- **触屏反应**：点击虚拟形象的头部或身体部位以触发相应动作
- **情绪栏**：提供 😊😢😠😮😌💃 等表情按钮
- **背景场景**：樱花园、夜空、咖啡馆、日落
- **相机预设**：面部、肖像、全身、电影模式
- **语音聊天**：用户输入语音 → AI生成回应 → 通过TTS实现语音同步

## 配置

编辑 `clawatar.config.json` 文件以配置端口、语音设置及模型URL。TTS功能需要ElevenLabs API密钥（环境变量 `ELEVENLABS_API_KEY`），或从 `~/.openclaw/openclaw.json` 文件的 `skills.entries.sag.apiKey` 中设置。

## 注意事项

- 动画素材来自 [Mixamo](https://www.mixamo.com/)，使用需注明出处，仅限非商业用途
- VRM模型需用户自行提供（BYOM：Bring Your Own Model）
- 该工具可独立运行（无需OpenClaw），AI聊天功能为可选选项