---
name: context-guardian
version: 1.0.1
description: 通过智能的三级警报系统实现主动的上下文监控。在系统性能下降之前，及时了解何时需要重启设备。
author: brucey0017
tags: [monitoring, context, alerts, proactive, quality]
---
# Context Guardian 🛡️

**您的上下文守护者。在错误发生之前发出警报。**

通过主动监控上下文使用情况，在使用率达到60%、70%和85%时向您发出警告——在这些阶段，上下文污染可能会导致错误和系统异常（即“幻觉”现象）。

---

## 为什么需要它

**问题：**
- 长时间的对话会导致上下文污染
- 随着上下文数据的不断增加，系统性能会逐渐下降
- 您可能直到为时已晚才意识到需要重启系统
- 当使用率达到约70%后，错误和系统异常的现象会增多

**解决方案：**
- 持续监控上下文使用情况
- 智能的三级警报系统（⚠️ 60%、🟠 70%、🔴 85%）
- 每个警报级别都提供可操作的提示
- 防止重复警报

---

## 快速入门

### 对于代理（Agents）：集成心跳检测（Heartbeat Integration）

当您收到心跳检测请求时，请执行以下操作：
1. 调用 `session_status` 工具以获取当前的上下文使用情况
2. 从输出结果中解析上下文使用百分比
3. 与阈值（60% [警告]、70% [危险]、85% [严重]）进行比较
4. 如果超过阈值且不是重复警报，则显示相应的警报信息
5. 更新状态文件以记录警报历史

**实现方式：**
```
During heartbeat:
1. Get context usage from session_status
2. Check if usage >= 60%, 70%, or 85%
3. Load state from memory/context-guardian-state.json
4. Determine if alert should be sent (prevent duplicates)
5. If yes, display alert and update state
```

### 对于用户（Users）：在 `HEARTBEAT.md` 中启用该功能

在您的 `HEARTBEAT.md` 文件中添加以下内容：
```markdown
## Context Monitoring
- Check context usage
- Alert if thresholds exceeded (60%, 70%, 85%)
```

代理会自动处理其余的配置和逻辑。

---

## 工作原理

### 监控

该技能会调用 `session_status` 来检查当前的上下文使用百分比。

### 警报级别

**⚠️ 警告（60%）**
```
⚠️ Context: 60%
Getting full. Consider wrapping up or starting fresh soon.
```

**🟠 危险（70%）**
```
🟠 Context: 70%
Pollution risk rising. Recommend:
• Finish current task
• Start new session for next task
• Or compress with context-optimizer
```

**🔴 严重（85%）**
```
🔴 Context: 85% - CRITICAL
High error risk. STRONGLY recommend:
• Save work
• Start new session NOW
• Quality degradation likely
```

### 智能防止重复警报

该技能会记录警报历史，并仅在以下情况下发出警报：
1. 首次达到某个阈值时
2. 警报级别升级时（60% → 70% → 85%）
3. 使用率下降后又再次上升时

---

## 配置

编辑 `config/default.json` 或创建 `config/user.json` 文件：
```json
{
  "enabled": true,
  "checkInterval": "heartbeat",
  "thresholds": {
    "warning": 60,
    "danger": 70,
    "critical": 85
  },
  "alertMethod": "message",
  "alertStyle": "emoji",
  "preventDuplicates": true,
  "trackHistory": true,
  "suggestions": {
    "autoSuggest": true,
    "suggestCompression": true,
    "suggestRestart": true
  }
}
```

### 选项

**checkInterval:**
- `"heartbeat"`：在心跳检测期间进行检查（默认值）
- `"cron"`：独立的cron作业（未来版本）
- `number`：每隔 N 分钟检查一次（未来版本）

**thresholds:**
- 自定义警报级别（默认值：60%、70%、85%）

**alertMethod:**
- `"message"`：以消息形式发送警报（默认值）
- `"log"`：仅记录日志
- `"notification"`：系统通知（未来版本）

**alertStyle:**
- `"emoji"`：带表情符号的简洁文本（默认值）
- `"text"`：纯文本
- `"detailed"`：详细解释

---

## 手动检查

您可以手动检查上下文状态：
```bash
bash {baseDir}/scripts/check.sh
```

---

## 与其他技能的集成

### context-optimizer

当上下文使用率达到70%时，该技能会建议使用 `context-optimizer` 来压缩上下文数据，而不是直接重启系统。

### context-recovery

在上下文数据恢复后，该技能会自动恢复监控。

---

## 代理的实现指南

### 分步流程

**1. 获取上下文使用情况**

调用 `session_status` 工具并解析输出结果：
```
Example output: "Context: 54k/200k (27%)"
Extract: 27
```

**2. 确定警报级别**

```javascript
if (usage >= 85) level = "critical"
else if (usage >= 70) level = "danger"
else if (usage >= 60) level = "warning"
else level = null
```

**3. 加载状态**

读取 `{workspace}/memory/context-guardian-state.json` 文件：
```json
{
  "lastCheck": 1709452800,
  "lastUsage": 54,
  "lastAlertLevel": "warning",
  "lastAlertTime": 1709452500,
  "history": [...]
}
```

**4. 判断是否需要发出警报**

防止重复警报：
```javascript
shouldAlert = false

// First time reaching threshold
if (!lastAlertLevel && level) shouldAlert = true

// Level upgrade (warning → danger → critical)
if (levelNum[level] > levelNum[lastAlertLevel]) shouldAlert = true

// Usage dropped below threshold and rose again
if (lastUsage < threshold - 5 && usage >= threshold) shouldAlert = true
```

**5. 发送警报**

如果需要发出警报，则显示相应的信息：
```
⚠️ Context: 60%
Getting full. Consider wrapping up or starting fresh soon.
```

**6. 更新状态**

将新的状态信息保存到 `memory/context-guardian-state.json` 文件中：
```json
{
  "lastCheck": <current_timestamp>,
  "lastUsage": <current_usage>,
  "lastAlertLevel": <level_if_alerted>,
  "lastAlertTime": <timestamp_if_alerted>,
  "history": [..., {"timestamp": <now>, "usage": <usage>}]
}
```

### 警报信息

**警告（60%）：**
```
⚠️ Context: 60%
Getting full. Consider wrapping up or starting fresh soon.
```

**危险（70%）：**
```
🟠 Context: 70%
Pollution risk rising. Recommend:
• Finish current task
• Start new session for next task
• Or compress with context-optimizer
```

**严重（85%）：**
```
🔴 Context: 85% - CRITICAL
High error risk. STRONGLY recommend:
• Save work
• Start new session NOW
• Quality degradation likely
```

---

## 状态管理

状态信息存储在 `{workspace}/memory/context-guardian-state.json` 文件中：
```json
{
  "lastCheck": 1709452800,
  "lastUsage": 54,
  "lastAlertLevel": null,
  "lastAlertTime": null,
  "history": [
    {"timestamp": 1709452800, "usage": 54}
  ]
}
```

---

## 故障排除

**没有警报出现：**
- 确保 `HEARTBEAT.md` 文件中包含了上下文监控代码
- 验证心跳检测功能是否正在运行
- 检查状态文件是否有错误

**警报过多：**
- 在配置文件中提高阈值
- 确认 `preventDuplicates` 选项是否已启用

**警报不准确：**
- 验证 `session_status` 工具是否正常工作
- 检查与 OpenClaw 的版本兼容性

---

## 示例

### 集成心跳检测

在 `HEARTBEAT.md` 文件中添加以下内容：
```markdown
## Context Monitoring
- Check context usage
- Alert if thresholds exceeded
```

### 自定义阈值

创建 `config/user.json` 文件：
```json
{
  "thresholds": {
    "warning": 50,
    "danger": 65,
    "critical": 80
  }
}
```

---

## 技术细节

**依赖项：**
- OpenClaw 2026.2.0 或更高版本
- `session_status` 工具
- Bash 解释器

**性能：**
- 无额外开销（仅在心跳检测期间进行检测）
- 最小的状态存储需求（约1KB）

**隐私保护：**
- 所有数据均存储在本地
- 无外部数据调用
- 无数据传输

---

## 开发计划

**v1.1.0：**
- 历史趋势跟踪
- 使用量预测功能
- 独立的 cron 检测模式

**v1.2.0：**
- 自动触发 `context-optimizer` 功能
- 可视化趋势图表
- 支持多会话监控

---

## 贡献方式

发现错误或有建议？请在 GitHub 上提交问题或 pull request。

---

## 许可证

MIT 许可证