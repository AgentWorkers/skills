---
description: 使用 Signalgrid 将实时活动（Live-Activities）和持续通知（Ongoing-Notifications）发送到您的 iOS 或 Android 手机。
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
# Signalgrid实时活动功能

通过Signalgrid API将实时活动信息及持续进行的通知发送到您的手机上。

## 使用场景

当用户需要执行以下操作时，请使用此功能：
-   启动一个持续进行的通知
-   更新持续进行中的通知的进度
-   显示实时活动或实时进度
-   在某些操作（如部署、备份、导入、持续集成作业等）进行过程中保持通知的更新状态
-   结束/完成一个持续进行中的通知

### 参数

| 参数名称            | 类型    | 说明                                      |
|-----------------|--------|-----------------------------------------|
| title            | string   | 活动标题。默认值为“无标题”。                         |
| body            | string   | 活动正文内容。默认值为“无正文”。                         |
| type            | enum    | 活动阶段。常见值：`start`（开始）、`update`（更新）、`end`（结束）。默认值为`start`。 |
| severity        | string   | 对应的严重级别：`crit`（严重）、`warn`（警告）、`success`（成功）、`info`（信息）。详见备注。 |
| start_text      | string   | 开始状态的标签。默认值为“活动开始”。                     |
| end_text        | string   | 结束状态的标签。默认值为“活动结束”。                     |
| steps           | number   | 如果设置为5，则进度条将分为5个阶段。默认值为5。                 |
| progress        | number   | 当前进度值。默认值为10。                         |
| progress_legend | boolean | 是否显示进度条图例。默认值为`true`（以字符串形式传递）。         |
| token           | string   | 仅在更新和结束通知时使用，用于匹配相应的活动。                 |
| dismissal_delay | string   | 通知在发送结束消息后显示的延迟时间。仅适用于结束通知。         |

## 启动实时活动

使用提供的脚本：

```bash
node {baseDir}/skills/signalgrid-activity/signalgrid-activity.js \
  --type start \
  --title "OpenClaw" \
  --body "Starting…" \
  --severity info \
  --steps 1 \
  --progress 10 \
  --progress_legend "true" \
  --start_text "Activity Start" \
  --end_text "Activity End" \
```

## 更新实时活动

```bash
node {baseDir}/skills/signalgrid-activity/signalgrid-activity.js \
  --type update \
  --token "MX2L2K" \
  --title "OpenClaw" \
  --body "Step 3/6" \
  --severity warning \
  --steps 1 \
  --progress 50 \
  --progress_legend "true" \
  --start_text "Activity Start" \
  --end_text "Activity End" \
```

## 结束实时活动

```bash
node {baseDir}/skills/signalgrid-activity/signalgrid-activity.js \
  --type end \
  --token "MX2L2K" \
  --title "OpenClaw" \
  --body "Done" \
  --severity success \
  --steps 1 \
  --progress 100 \
  --progress_legend "true" \
  --start_text "Activity Start" \
  --end_text "Activity End" \
  --dismissal_delay 60
```

## 使用说明

在更新和结束通知时，如果未另行指定，需要从开始通知中获取以下参数并重新发送：
-   title（标题）
-   body（正文）
-   severity（严重级别）
-   steps（进度阶段）
-   progress_legend（进度条图例）
-   start_text（开始状态标签）
-   end_text（结束状态标签）

否则，活动的显示内容将会发生变化。虽然这种灵活性是允许的，但在大多数情况下并非必需。

## 备注

- 需要一个Signalgrid账户：https://web.signalgrid.co/
- 安装该功能的方法：
  ``` bash
  clawdhub --workdir ~/.openclaw install signalgrid-activity
  ```
  （请将`your_client_key_here`和`your_channel_name_here`替换为实际的客户端密钥和频道名称。）

- Signalgrid通知功能**不需要**手机号码或消息接收方信息。