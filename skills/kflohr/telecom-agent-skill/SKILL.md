---
name: "Telecom Agent Skill"
description: "将您的人工智能代理转变为电信运营商：支持批量呼叫、聊天操作（ChatOps）以及现场监控（Field Monitoring）功能。"
version: "1.2.0"
---

# 📡 电信代理技能 v1.2

**为您的 MoltBot / OpenClaw 代理赋予电信运营商的功能。**

此技能将您的代理连接到 **电信运营商控制台**，使其能够管理营销活动、处理审批请求，并安全地操作公共电话网络。

## ✨ 功能

### 🚀 营销活动队列（批量呼叫） *新功能*
*   **批量拨号**：上传包含 10,000 个以上电话号码的列表。系统会自动处理速率限制问题。
*   **ChatOps**：“机器人，为‘周五潜在客户’列表创建一个营销活动。”
*   **监控**：代理可以使用 `--json` 命令查询状态，以便精确跟踪进度。

### 🗣️ 语音与语音合成
*   **拨打电话**：可以拨打任何全球电话号码。
*   **语音播放**：支持动态的“文本转语音”问候语。
*   **录音**：自动录制音频以进行质量监控。

### 📱 现场操作（Telegram）
*   **远程管理**：通过 Telegram 机器人监控系统状态。
*   **审批**：通过手机按钮批准/拒绝高风险操作。

### 🧠 操作日志
*   **通话记录**：代理可以查看完整的通话记录（“电信代理日志”）。
* **数据持久化**：所有日志都会保存到安全的运营商控制台中。

---

## 代理快速入门

### 1. 安装
```bash
/install https://github.com/kflohr/telecom-agent-skill
```

### 2. 设置
```bash
telecom onboard
# Follow the wizard to link your Twilio account.
```

### 3. 使用示例

**批量营销活动**：
```bash
telecom campaign create "Outreach" --file leads.csv
telecom campaign status <id> --json
```

**单次呼叫**：
```bash
telecom agent call +14155550100 --intro "Hello from the AI team."
```

**日志查询**：
```bash
telecom agent memory <CallSid>
```