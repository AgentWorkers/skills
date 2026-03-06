---
name: ping-model
description: >
  **测量并显示 AI 模型的响应延迟**  
  当用户输入 `/ping` 或 `/ping` 后跟一个模型名称时，该功能可用于测试模型之间的往返时间（即从接收到命令到生成响应所需的时间）。系统能够精确记录这一时间，并以友好的格式（毫秒、秒或分钟）显示结果。此外，通过临时切换模型并测量其响应延迟，该功能还支持跨模型测试。
metadata: {"clawdbot":{"emoji":"🧪","requires":{"bins":["node"]}}}
---
# Ping模型

用于以统一的格式测量AI模型的响应延迟。

## 快速入门

### 简单Ping（当前模型）
```bash
bash command:"node {baseDir}/ping-model.js"
```

### 测量特定模型
```bash
bash command:"node {baseDir}/ping-model.js --model minimax"
```

### 比较多个模型
```bash
bash command:"node {baseDir}/ping-model.js --compare kimi,minimax,deepseek"
```

## 命令参考

| 命令 | 描述 |
|---------|-------------|
| `/ping` | 测量当前活跃模型的响应延迟 |
| `/ping kimi` | 切换到kimi模型，执行Ping操作并返回结果 |
| `/ping minimax` | 切换到minimax模型，执行Ping操作并返回结果 |
| `/ping deepseek` | 切换到deepseek模型，执行Ping操作并返回结果 |
| `/ping all` | 比较所有可用模型的响应延迟 |

## 输出格式

**必须使用以下格式：**

```
🧪 PING {model-name}

📤 Sent:     {HH:MM:SS.mmm}
📥 Received: {HH:MM:SS.mmm}
⏱️  Latency:  {formatted-duration}

🎯 Pong!
```

### 延迟显示规则

- **< 1秒**：显示为`XXXms`（例如：`847ms`）
- **≥ 1秒，< 60秒**：显示为`X.XXs`（例如：`1.23s`）
- **≥ 60秒**：显示为`X.XXmin`（例如：`2.5min`）

### 示例

**响应速度快（< 1秒）：**
```
🧪 PING kimi

📤 Sent:     09:34:15.123
📥 Received: 09:34:15.247
⏱️  Latency:  124ms

🎯 Pong!
```

**响应时间中等（1-60秒）：**
```
🧪 PING minimax

📤 Sent:     09:34:15.123
📥 Received: 09:34:16.456
⏱️  Latency:  1.33s

🎯 Pong!
```

**响应时间慢（> 60秒）：**
```
🧪 PING gemini

📤 Sent:     09:34:15.123
📥 Received: 09:35:25.456
⏱️  Latency:  1.17min

🎯 Pong!
```

## 跨模型测试

在测试非活跃模型时，请按照以下步骤操作：

1. 保存当前模型的状态。
2. 切换到目标模型。
3. 执行Ping操作。
4. 测量延迟。
5. 恢复到原始模型。
6. 显示测试结果。

**重要提示：** 测试完成后务必返回到原始模型。

## 比较模式

```bash
bash command:"node {baseDir}/ping-model.js --compare kimi,minimax,deepseek,gpt"
```

输出格式：
```
══════════════════════════════════════════════════
🧪 MODEL COMPARISON
══════════════════════════════════════════════════

🥇 kimi      124ms
🥈 minimax   1.33s
🥉 deepseek  2.45s
4️⃣  openai    5.67s

🏆 Fastest: kimi (124ms)
```

## 实现原理

Ping延迟的测量基于以下时间差：
- **T1**：代理接收到消息的时间。
- **T2**：模型准备好发送响应的时间。

该指标反映的是模型的内部处理时间，而非网络延迟。