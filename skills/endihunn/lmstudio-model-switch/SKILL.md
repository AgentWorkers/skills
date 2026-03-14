# lmstudio-model-switch

**在 LM Studio 本地模型与 Kimi API 之间快速切换模型**

通过一个简单的命令，您可以实时在本地（LM Studio）和云端（Kimi API）的 AI 模型之间切换代理的模型。

---

## 安装

```bash
# Clone to your OpenClaw skills directory
git clone https://github.com/yourusername/lmstudio-model-switch \
  ~/.openclaw/workspace/skills/lmstudio-model-switch

# Or manually copy
cp -r lmstudio-model-switch ~/.openclaw/workspace/skills/
```

---

## 使用方法

### 命令

| 命令 | 描述 |
|---------|-------------|
| `/switch-model status` | 显示当前模型及可用的提供者 |
| `/switch-model local` | 切换到 LM Studio（默认模型：Qwen 3.5 9B） |
| `/switch-model local <model>` | 切换到特定的本地模型 |
| `/switch-model api` | 切换到 Kimi K2.5 API |
| `/switch-model kimi` | 是 `/switch-model api` 的别名 |

### 示例

```bash
# Check current status
/switch-model status

# Switch to local LM Studio
/switch-model local

# Switch to specific model
/switch-model local mistral-small-24b

# Switch to Kimi API
/switch-model api
```

---

## 配置

将以下配置添加到您的 `openclaw.json` 文件中：

```json
{
  "skills": {
    "lmstudio-model-switch": {
      "enabled": true,
      "config": {
        "local": {
          "baseUrl": "http://127.0.0.1:1234/v1",
          "defaultModel": "qwen/qwen3.5-9b"
        },
        "api": {
          "provider": "kimi-coding",
          "model": "k2p5"
        }
      }
    }
  }
}
```

---

## 工作原理

1. **备份**：创建 `openclaw.json` 的带时间戳的备份文件。
2. **修改**：更新 `agents.defaults` 文件中的 “primary” 模型设置。
3. **验证**：检查 JSON 语法是否正确。
4. **重启**：重新启动 OpenClaw 代理服务。
5. **确认**：显示新的活动模型。

---

## 使用场景

### 优先考虑隐私的场景
在处理以下内容时，使用 **本地模型**：
- 认证令牌
- 密码或凭证
- 敏感个人信息
- 专有代码

### 优先考虑质量的场景
在需要以下功能时，使用 **API 模型**：
- 最高的推理能力
- 非常长的上下文（超过 100,000 个令牌）
- 一流的性能
- 云服务的可靠性

### VRAM 管理
在以下情况下，切换到 **API 模型**：
- GPU 内存不足（剩余空间 < 6GB）
- 正在运行其他占用大量 GPU 资源的任务
- LM Studio 正在重启

---

## 系统要求

- OpenClaw 版本需大于或等于 2026.3.12
- LM Studio 需运行在端口 1234 上（用于本地模式）
- 需配置 Kimi API 密钥（用于 API 模式）
- 需要 systemd 系统来管理服务的重启

---

## 故障排除

### “LM Studio 无响应”
```bash
# Check if LM Studio is running
curl http://127.0.0.1:1234/api/v0/models

# Restart LM Studio if needed
killall lmstudio; sleep 2; lmstudio &
```

### “切换失败”
- 检查 JSON 语法：`python3 -m json.tool ~/.openclaw/openclaw.json`
- 从备份文件中恢复数据：`cp ~/.openclaw/openclaw.json.bak.* ~/.openclaw/openclaw.json`

### “代理服务无法重启”
```bash
# Check service status
systemctl --user status openclaw-gateway

# Manual restart
systemctl --user restart openclaw-gateway
```

---

## 作者

**WarMech** - OpenClaw 社区成员

## 许可证

MIT 许可证

---

## 更新日志

**2026-03-14** - v1.0.0
- 首次发布
- 支持本地模型与 API 之间的切换
- 引入了备份/恢复功能
- 集成了 systemd 系统用于服务管理