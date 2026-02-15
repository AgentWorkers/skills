---
name: telegram-bot-manager
description: 管理和配置 OpenClaw 的 Telegram 机器人。适用于设置 Telegram 集成、排查机器人连接问题、配置机器人令牌，以及管理 Telegram 频道/Webhook 设置。该工具负责处理机器人的注册、令牌验证，以及与 apiTelegram.org 的网络连接检查。
---

# Telegram机器人管理器

## 快速入门

### 创建新的Telegram机器人

1. **通过BotFather创建机器人**
   - 在Telegram中给@BotFather发送消息
   - 使用`/newbot`命令
   - 按照提示设置机器人名称和用户名
   - 复制机器人令牌（格式：`1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`）

2. **在OpenClaw中进行配置**
   - 将令牌添加到OpenClaw配置中
   - 启用Telegram插件
   - 设置私信访问的配对模式

### 验证机器人配置

```bash
# Test Telegram API connectivity
curl -I https://api.telegram.org

# Check bot token validity
curl -s "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
```

## 常见工作流程

### 解决连接问题

当apiTelegram.org无法访问时：

1. **检查网络连接**
   ```bash
   curl -I -m 10 https://api.telegram.org
   ```

2. **验证DNS解析**
   ```bash
   nslookup api.telegram.org
   ```

3. **测试备用端点**
   ```bash
   curl -I https://telegram.org
   ```

### 配置OpenClaw与Telegram的集成

详细配置步骤请参阅[OPENCLAW_CONFIG.md](references/OPENCLAW_CONFIG.md)。

### 机器人令牌的安全性

- **切勿将机器人令牌提交到版本控制系统中**
- **将令牌存储在环境变量或安全的配置文件中**
- **如果令牌被泄露，请更换令牌**
- **为不同的环境（开发/生产）使用不同的令牌**

## 机器人命令参考

BotFather的常见Telegram机器人命令：

- `/newbot` - 创建新的机器人
- `/mybots` - 管理你的机器人
- `/setdescription` - 设置机器人描述
- `/setabouttext` - 设置关于文本
- `/setuserpic` - 设置机器人头像
- `/setcommands` - 设置机器人命令
- `/token` - 生成新的令牌
- `/revoke` - 取消当前令牌
- `/setprivacy` - 配置隐私设置

## Webhook与轮询

### Webhook（推荐用于生产环境）
- 机器人通过HTTP POST接收更新
- 需要一个公开的HTTPS端点
- 适用于处理大量消息的机器人

### 轮询（适合开发环境）
- 机器人持续检查更新
- 设置简单，不需要公开端点
- 便于在本地进行调试

Webhook的配置方法请参阅[WEBHOOK_setup.md](references/WEBHOOK_SETUP.md)。

## 错误处理

### 常见错误及解决方法

**“连接超时”**
- 检查防火墙规则
- 验证代理配置
- 使用不同的网络进行测试

**“令牌无效”**
- 验证令牌格式（应包含冒号）
- 检查是否有多余的空白字符
- 如有必要，重新生成令牌

**“机器人无响应”**
- 验证机器人是否被屏蔽
- 检查机器人的隐私设置
- 确保机器人具有适当的权限

## 测试你的机器人

### 手动测试
1. 在Telegram中搜索你的机器人用户名
2. 使用`/start`开始对话
3. 测试基本命令

### 自动化测试
使用`scripts/test_bot.py`中的测试脚本来进行自动化验证。

## 参考资料

- [Telegram机器人API文档](https://core.telegram.org/bots/api)
- [BotFather文档](https://core.telegram.org/bots#6-botfather)
- [OpenClaw配置指南](references/OPENCLAW_CONFIG.md)