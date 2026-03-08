---
description: 使用 Signalgrid 向您的 iOS 或 Android 手机发送推送通知。
  Signalgrid.
homepage: "https://web.signalgrid.co"
metadata:
  clawdbot:
    emoji: 📲
    primaryEnv: SIGNALGRID_CLIENT_KEY
    requires:
      bins:
      - node
      env:
      - SIGNALGRID_CLIENT_KEY
      - SIGNALGRID_CHANNEL
name: signalgrid-push
---
# Signalgrid 推送通知

通过 Signalgrid API 向您的手机发送推送通知。

## 示例

发送一条简单的通知：

``` bash
node {baseDir}/skills/signalgrid-push/signalgrid-push.js --title "OpenClaw" --body "来自 OpenClaw 的问候" --type INFO
```
  
Send a deployment notification:

```
node {baseDir}/skills/signalgrid-push/signalgrid-push.js --title "部署完成" --body "构建成功" --type INFO
```
    
Send a critical notification:

```
node {baseDir}/skills/signalgrid-push/signalgrid-push.js --title "注意" --body "这是一个紧急通知" --type INFO --critical true
```

## Options

-   `--title <title>`: Notification title (required)
-   `--body <body>`: Main message (required)
-   `--type <type>`: Notification type --- `crit`, `warn`, `success`,
    `info`
-   `--critical <bool>`: Emergency bypass flag (optional)

## When to use

Use this skill when the user asks to:  
&nbsp;  
&nbsp;o   &nbsp;send a notification  
&nbsp;o   &nbsp;notify me  
&nbsp;o   &nbsp;send a push  
&nbsp;o   &nbsp;push a message  
&nbsp;o   &nbsp;alert me  
&nbsp;o   &nbsp;send a signalgrid notification  
&nbsp;o   &nbsp;notify my phone

## Notes

-   Requires a Signalgrid account: https://web.signalgrid.co/
&nbsp;  
&nbsp;  
-   Install the skill:

```
clawdhub --workdir ~/.openclaw install signalgrid-push
```

-   And ensure your OpenClaw **Tool Profile** is set to `full`  ( Config -> Tools -> Tool Profile )  
&nbsp;  
-   Configure environment variables ( Config -> Environment -> Environment Variables Overrides + Add Entry):

```
SIGNALGRID_CLIENT_KEY=your_client_key_here
SIGNALGRID_CHANNEL=your_channel_name_here
```

- Signalgrid 通知**不需要**提供手机号码或消息接收者信息。