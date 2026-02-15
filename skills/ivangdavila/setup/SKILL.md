---
name: Setup
description: 配置 OpenClaw 安装，包括优化设置、频道设置、安全加固以及生产环境下的使用建议。
---

## 快速参考

| 任务 | 对应文件 |
|------|------|
| 消息通道（Telegram、WhatsApp、Discord等） | `channels.md` |
| 代理设置、模型、工作区 | `agents.md` |
| 安全性、认证、私信策略、白名单 | `security.md` |
| 工具：执行命令、浏览器、网页界面、媒体处理 | `tools.md` |
| 定时任务（Cron）、钩子（hooks）、心跳检测（heartbeats）、自动化 | `automation.md` |
| 基于使用场景的建议 | `recommendations.md` |
| 内存搜索、嵌入技术（embeddings）、QMD | `memory.md` |
| 网关配置：端口、TLS协议、Tailscale连接、远程访问 | `gateway.md` |

---

## 首次设置检查清单

在进行任何配置之前，请运行以下命令：
```bash
openclaw onboard --install-daemon  # Full wizard
openclaw doctor                    # Check issues
```

**最低限度的可用配置：**
- [ ] 至少连接了一个消息通道（建议使用Telegram进行测试）
- [ ] 配置了模型（Anthropic Claude或OpenAI）
- [ ] 设置了工作区路径（`agents.defaults_workspace`）
- [ ] 配置了所有者白名单（在`channels.*.allowFrom`文件中指定您的用户ID）

---

## 配置文件的位置

| 文件名 | 用途 |
|------|---------|
| `~/.openclaw/openclaw.json` | 主配置文件 |
| `~/.openclaw/.env` | 环境变量 |
| `~/.openclaw/workspace/` | 默认工作区 |
| `~/.openclaw/sessions/` | 会话存储目录 |

**热重启：** 大多数配置更改会立即生效。但网关配置（如端口、TLS设置）需要重启后才能生效。

---

## 常见错误及避免方法

1. **未设置白名单就启用私信功能** → 任何人都可能向您的机器人发送消息
2. **远程网关未配置认证令牌** → 会导致系统暴露在互联网上
3. **模型未设置备用方案** → 会导致系统出现单点故障
4. **心跳检测未指定发送目标** → 会导致主动发送的消息丢失
5. **在群组中设置`exec.security: "full"` | 会允许用户执行危险命令

---

## 完成设置后

```bash
openclaw doctor       # Verify config
openclaw status       # Check runtime
openclaw health       # Gateway health
```