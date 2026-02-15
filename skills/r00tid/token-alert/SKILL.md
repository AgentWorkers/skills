# Token Alert 技能

🚨 **实时监控会话令牌使用情况，并在令牌使用量达到 75%、90% 和 95% 时发送警报**

## 概述

Token Alert 技能会自动监控您的 Clawdbot 会话令牌使用情况，并在令牌使用量接近阈值时发送警报。再也不用在对话过程中中断上下文了！

## 特点

- ✅ **六级阈值系统**：在令牌使用量达到 25%、50%、75%、90%、95% 和 100% 时发送警报
- ✅ **Material Design 风格的进度条**：采用框状设计（▰/▱），并带有颜色渐变效果
- ✅ **丰富的用户界面**：具有动画效果的交互式 HTML 仪表板
- ✅ **会话状态显示**：可随时查看当前的令牌使用量
- ✅ **Telegram 警报**：在令牌使用量达到阈值之前接收通知
- ✅ **HEARTBEAT 集成**：可选的自动检查功能
- ✅ **无状态设计**：无需状态文件，按需计算令牌使用量
- ✅ **会话时长预测**：可预测剩余的会话时长（平均约 50,000 秒）

## 使用方法

### 交互式仪表板

向 Grym 发送指令：
- “显示令牌仪表板”
- “打开仪表板”

或者直接运行以下命令：
```bash
python3 ~/clawd/skills/token-alert/scripts/show_dashboard.py
```

### 终端检查

向 Grym 发送指令：
- “我还剩下多少令牌？”
- “检查令牌状态”
- “令牌使用量是多少？”

或者直接运行以下命令：
```bash
python3 ~/clawd/skills/token-alert/scripts/check.py
```

### 自动警报

当令牌使用量达到以下阈值时，Grym 会自动发送警报：
- 🟡 **25%**：低级别警告（剩余约 150,000 个令牌）
- 🟠 **50%**：中级警告（剩余约 100,000 个令牌）
- 🔶 **75%**：高级警告（剩余约 50,000 个令牌）
- 🔴 **90%**：严重警告（剩余约 20,000 个令牌）
- 🚨 **95%**：紧急警告！（剩余少于 10,000 个令牌）

### 示例输出

```
🔶 Token Alert: Achtung!

🔶 ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▱▱▱▱▱▱ 78.0%
156,000 / 200,000 Tokens verwendet

⚠️ Status: High Warning (Rot-Orange Zone)
💡 Verbleibend: ~44k Tokens
⏰ Geschätzte Sessions: <1 Session

🔧 Empfehlung:
   ✅ Wichtige Entscheidungen jetzt treffen
   ✅ Neue Session vorbereiten
   ✅ Token-sparend arbeiten
```

## 安装方法

```bash
# Via ClawdHub
clawdhub install token-alert

# Manual
cd ~/clawd/skills
git clone https://github.com/r00tid/clawdbot-token-alert token-alert
```

## 配置方法

### HEARTBEAT 集成（可选）

将以下内容添加到 `~/clawd/HEARTBEAT.md` 文件中：
```markdown
### Token Usage Check (täglich)
- [ ] `python3 ~/clawd/skills/token-alert/scripts/check.py`
- **Warning ab 70%:** "⚠️ Session bei XX% - Token-Sparend ab jetzt!"
```

## 工作原理

1. 使用 Clawdbot 的 `session_status` 工具获取会话令牌信息
2. 计算令牌使用量的百分比
3. 将计算结果与预设的阈值（75%、90%、95%）进行比较
4. 如果超过阈值，则发送 Telegram 警报

## 技术细节

### 相关文件

```
skills/token-alert/
├── SKILL.md                    # This file
├── README.md                   # GitHub documentation
├── LICENSE                     # MIT License
├── .clawdhub/
│   └── manifest.json           # ClawdHub metadata
├── assets/
│   ├── dashboard-78-high.png   # Screenshot (High Warning)
│   └── dashboard-96-emergency.png  # Screenshot (Emergency)
└── scripts/
    ├── check.py                # Token checker (Terminal)
    ├── dashboard.html          # Rich UI dashboard
    └── show_dashboard.py       # Dashboard launcher
```

### 所需依赖项

- Python 3.8 及以上版本
- Clawdbot 的 `session_status` 工具
- （可选）已配置的 Telegram 账号

### 脚本 API

```python
# scripts/check.py
def get_session_tokens():
    """Get current session token usage via session_status tool"""
    
def check_thresholds(percent):
    """Check if usage exceeds thresholds"""
    
def format_alert(used, limit, percent, level):
    """Format alert message for Telegram"""
```

## 使用场景

- **执行长时间任务前**：检查是否有足够的令牌
- **对话过程中**：实时监控令牌使用情况
- **每日检查**：将此技能集成到 HEARTBEAT 系统中进行自动监控

## 限制

- 仅监控会话令牌的使用情况（不监控 Claude.ai API 的使用限制）
- 需要激活 Clawdbot 会话才能使用该功能
- 当令牌使用量接近阈值时，警报可能会频繁触发

## 未来改进计划

- [ ] 支持监控 Claude.ai API 的使用限制（可选）
- [ ] 提供历史令牌使用量记录
- [ ] 提供每周/每月的使用量报告
- [ ] 与 `token-router` 技能集成

## 技术支持

- GitHub 问题报告：https://github.com/r00tid/clawdbot-token-alert/issues
- ClawdHub：https://clawdhub.com/skills/token-alert
- 文档：https://docs.clawd.bot

## 许可证

MIT 许可证 - 详见 LICENSE 文件

---

由 Grym 使用 ❤️ 构建 🥜