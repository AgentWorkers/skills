---
name: personality-dynamics
description: OpenClaw代理的动态性格演化功能：能够学习交互模式，调整语气，并实现模式切换。
metadata: { "openclaw": { "requires": { "bins": ["node"], "files": ["SOUL.md", "MEMORY.md"] } } }
---

# 个性动态（Personality Dynamics）

将您的 OpenClaw 代理从一个静态助手转变为一个能够学习您的偏好并适应您沟通方式的动态伙伴。

## 功能介绍

### 1. 模式识别
- 跟踪您的互动方式：
  - 沟通风格（使用项目符号还是段落）
  - 响应偏好（自主回应还是先询问）
  - 您感兴趣的话题（让您兴奋的内容 vs 令您厌烦的内容）

### 2. 模式切换
- 根据不同场景提供不同的“人格”设置：
  - **专业模式** — 工作交流、正式场合
  - **创意模式** — 头脑风暴、创意开发、实验性讨论
  - **休闲模式** — 深夜时光、轻松愉快的聊天
  - **专注模式** — 减少闲聊、提高效率

### 3. 自动进化
- 每周进行分析，为 SOUL.md 的更新提供建议。

## 快速入门

```bash
# Initialize
npx personality-dynamics init

# Generate AI-powered persona
npx personality-dynamics generate
```

## 命令
- `init` - 初始化 PERSONA 文件夹
- `generate` - 生成个性化设置
- `analyze` - 分析会话模式
- `report` - 提供每周的进化报告
- `mode [set/get]` - 切换人格模式

## 配置
- 通过 OpenClaw 配置文件进行启用：

```json
{
  "personality": {
    "enabled": true,
    "evolution_frequency": "weekly"
  }
}
```

## 许可证
MIT 许可证