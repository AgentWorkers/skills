---
name: whoop
description: **WHOOP晨间签到（恢复/睡眠/压力情况）及建议**
metadata:
  clawdbot:
    config:
      requiredEnv:
        - WHOOP_CLIENT_ID
        - WHOOP_CLIENT_SECRET
        - WHOOP_REFRESH_TOKEN
---

# whoop

## 每日早晨的WHOOP检查：
- 获取您的最新WHOOP数据（恢复情况、睡眠质量、周期/压力水平）
- 生成当天的建议

### 快速入门（用户 + 机器人）

### 用户需要执行的操作（只需一次）：
1. 创建一个WHOOP应用程序并获取凭证：
   - `WHOOP_CLIENT_ID`
   - `WHOOP_CLIENT_SECRET`

2. 在WHOOP开发者控制台中设置回调URL：
   - `https://localhost:3000/callback`

3. 将凭证添加到`~/.clawdbot/.env`文件中：

```bash
WHOOP_CLIENT_ID=...
WHOOP_CLIENT_SECRET=...
```

4. 进行一次授权（获取刷新令牌）：

```bash
node /home/claw/clawd/skills/whoop/bin/whoop-auth --redirect-uri https://localhost:3000/callback
```

- 在手机或浏览器中打开生成的回调URL
- 点击“允许/授权”
- 复制回调URL中的`code`，然后粘贴回去

这样会自动将`WHOOP_REFRESH_TOKEN=...`写入`~/.clawdbot/.env`文件中。

### 机器人需要执行的操作（每次运行时）：
执行以下命令：

```bash
node /home/claw/clawd/skills/whoop/bin/whoop-morning
```

然后将结果发送给用户。

### 自动化（每日执行）：
建议使用Gateway的cron任务进行每日自动执行：
- 命令：`node /home/claw/clawd/skills/whoop/bin/whoop-morning`
- 机器人应将执行结果以消息的形式发送给用户。

## 注意事项：
- OAuth接口地址：
  - 认证：`https://api.prod.whoop.com/oauth/oauth2/auth`
  - 令牌：`https://api.prod.whoop.com/oauth/oauth2/token`
- 需要`offline`权限才能获取刷新令牌。
- WHOOP会定期更新刷新令牌；必须保存最新的刷新令牌。