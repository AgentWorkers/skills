---
name: whoop-morning
description: 每天早上检查 WHOOP 系统的恢复情况、睡眠状态以及系统负载（strain），并给出相应的建议。
metadata:
  clawdbot:
    config:
      requiredEnv:
        - WHOOP_CLIENT_ID
        - WHOOP_CLIENT_SECRET
        - WHOOP_REFRESH_TOKEN
---

# whoop-morning

**早晨的WHOOP检查：**  
- 获取您最新的WHOOP数据（恢复情况、睡眠质量、训练强度等）  
- 生成当天的一些建议  

## 设置  

### 1) 创建WHOOP OAuth凭据  

您已经拥有以下信息：  
- `WHOOP_CLIENT_ID`  
- `WHOOP_CLIENT_SECRET`  

将这些信息保存到`~/.clawdbot/.env`文件中。  

### 2) 进行一次授权（获取刷新令牌）  

运行以下命令：  
```bash
/home/claw/clawd/skills/whoop-morning/bin/whoop-auth --scopes offline read:recovery read:sleep read:cycles read:profile
```  

该命令会生成一个授权URL。  
在浏览器中打开该URL，完成授权流程后，将返回的`code`粘贴回终端中。  
脚本会使用该`code`获取刷新令牌，并将`WHOOP_REFRESH_TOKEN=...`写入`~/.clawdbot/.env`文件中。  

### 3) 运行早晨报告  

运行以下命令：  
```bash
/home/claw/clawd/skills/whoop-morning/bin/whoop-morning
```  

## 自动化  

建议使用Gateway的cron任务（每天早晨自动执行）。  
cron任务应运行`whoop-morning`脚本，并将其输出结果作为消息发送出去。  

## 注意事项：**  
- 本脚本使用WHOOP的OAuth2认证机制：  
  - 认证URL：`https://api.prod.whoop.com/oauth/oauth2/auth`  
  - 令牌URL：`https://api.prod.whoop.com/oauth/oauth2/token`  
- WHOOP会定期更新刷新令牌；请避免同时执行多次刷新操作。  
- API的可用性或字段可能会发生变化；如果刷新令牌时出现401/400错误，请重新运行`whoop-auth`命令。