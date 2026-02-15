---
name: withings-health
description: 从 Withings API 获取健康数据，包括体重、身体成分（脂肪、肌肉、骨骼、水分）、活动量以及睡眠质量等信息。当用户询问他们的 Withings 设备数据（如体重记录、身体指标、每日步数、睡眠质量或任何健康测量结果）时，可以使用此功能。
version: 1.1.0
homepage: https://developer.withings.com/
metadata: {"clawdbot":{"emoji":"⚖️","requires":{"bins":["node"],"env":["WITHINGS_CLIENT_ID","WITHINGS_CLIENT_SECRET"]}}}
---

此技能允许您与用户的 Withings 账户进行交互，从而从 Withings 设备（智能体重秤、睡眠分析仪、活动追踪器等）中获取全面的健康数据。

## 何时使用此技能

当用户执行以下操作时，请使用此技能：
- 询问他们的体重或体重历史记录
- 希望查看他们的身体成分（脂肪百分比、肌肉质量、骨密度、水分含量）
- 请求查看他们的日常活动数据（步数、行走距离、消耗的卡路里）
- 询问他们的睡眠数据（睡眠时长、睡眠质量、深度睡眠时间、快速眼动睡眠阶段）
- 提到 “Withings” 或任何 Withings 设备（如 Body+、Sleep Analyzer、ScanWatch 等）
- 希望随时间跟踪自己的健康状况

## 设置：创建 Withings 开发者应用程序

在使用此技能之前，您需要创建一个免费的 Withings 开发者应用程序以获取 API 凭据。

### 第 1 步：创建 Withings 开发者账户

1. 访问 [Withings 开发者门户](https://developer.withings.com/)
2. 如果您已有 Withings 账户，请点击 **注册** 或 **登录**
3. 同意开发者服务条款

### 第 2 步：创建您的应用程序

1. 转到 **我的应用程序** → **创建应用程序**
2. 填写应用程序详细信息：
   - **应用程序名称**：选择一个名称（例如：“My Clawdbot Health”）
   - **描述**：简要说明您的使用场景
   - **联系邮箱**：您的电子邮件地址
   **回调 URL**：`http://localhost:8080`（OAuth 所需）
   - **应用程序类型**：选择 “个人使用” 或相应的类型
3. 提交应用程序申请

### 第 3 步：获取您的凭据

应用程序创建完成后：
1. 转到 **我的应用程序** 并选择您的应用程序
2. 您将看到：
   - **客户端 ID** → 设置为 `WITHINGS_CLIENT_ID` 环境变量
   - **客户端密钥** → 设置为 `WITHINGS_CLIENT_SECRET` 环境变量

### 第 4 步：配置环境变量

将这些凭据添加到您的 Clawdbot 环境中：
```bash
export WITHINGS_CLIENT_ID="your_client_id_here"
export WITHINGS_CLIENT_SECRET="your_client_secret_here"
```

或者在该技能目录下创建一个 `.env` 文件（此文件会被 git 忽略）：
```
WITHINGS_CLIENT_ID=your_client_id_here
WITHINGS_CLIENT_SECRET=your_client_secret_here
```

## 配置

该技能使用位于 `{baseDir}` 目录下的 `wrapper.js` 脚本。

在检索任何数据之前，请检查用户是否已登录。如果出现 “未找到令牌” 的错误，请引导用户完成初始认证流程。

## 可用的命令

### 1. 认证

- 首次设置时：生成 OAuth URL：
```bash
node {baseDir}/wrapper.js auth
```

用户访问该 URL 并获取授权码后：
```bash
node {baseDir}/wrapper.js auth YOUR_CODE_HERE
```

### 2. 获取体重

检索最新的体重测量数据：
```bash
node {baseDir}/wrapper.js weight
```

以 JSON 格式返回最近 5 次的体重记录。

**示例输出：**
```json
[
  { "date": "2026-01-17T08:30:00.000Z", "weight": "75.40 kg" },
  { "date": "2026-01-16T08:15:00.000Z", "weight": "75.65 kg" }
]
```

### 3. 获取身体成分

检索全面的身体指标（脂肪、肌肉、骨骼、水分、BMI）：
```bash
node {baseDir}/wrapper.js body
```

返回最近 5 次的身体成分测量数据。

**示例输出：**
```json
[
  {
    "date": "2026-01-17T08:30:00.000Z",
    "weight": "75.40 kg",
    "fat_percent": "18.5%",
    "fat_mass": "13.95 kg",
    "muscle_mass": "35.20 kg",
    "bone_mass": "3.10 kg",
    "hydration": "55.2%"
  }
]
```

### 4. 获取活动数据

检索日常活动数据（步数、行走距离、卡路里消耗）：
```bash
node {baseDir}/wrapper.js activity
```

可以选择要查询的天数（默认为 7 天）：
```bash
node {baseDir}/wrapper.js activity 30
```

**示例输出：**
```json
[
  {
    "date": "2026-01-17",
    "steps": 8542,
    "distance": "6.23 km",
    "calories": 2150,
    "active_calories": 450,
    "soft_activity": "45 min",
    "moderate_activity": "22 min",
    "intense_activity": "8 min"
  }
]
```

### 5. 获取睡眠数据

检索睡眠数据及睡眠质量：
```bash
node {baseDir}/wrapper.js sleep
```

可以选择要查询的天数（默认为 7 天）：
```bash
node {baseDir}/wrapper.js sleep 14
```

**示例输出：**
```json
[
  {
    "date": "2026-01-17",
    "start": "23:15",
    "end": "07:30",
    "duration": "8h 15min",
    "deep_sleep": "1h 45min",
    "light_sleep": "4h 30min",
    "rem_sleep": "1h 30min",
    "awake": "30min",
    "sleep_score": 82
  }
]
```

## 错误处理

常见错误及解决方法：

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| “未找到令牌” | 首次使用或未登录 | 运行 `node wrapper.js auth` 并按照 OAuth 流程进行认证 |
| “无法刷新令牌” | 令牌过期且刷新失败 | 使用 `node wrapper.js auth` 重新认证 |
| “API 错误状态：401” | 凭据无效或过期 | 检查您的 CLIENT_ID 和 CLIENT_SECRET，重新认证 |
| “API 错误状态：503” | Withings API 暂时不可用 | 稍后等待并重试 |
| 数据为空 | 请求期间没有测量数据 | 用户需要同步他们的 Withings 设备 |

## 注意事项

- 令牌会在过期后自动刷新
- 使用的 Withings API 权限范围：`user.metrics`、`user.activity`
- 数据的可用性取决于用户拥有的 Withings 设备类型
- 某些指标（如身体成分）需要兼容的智能体重秤才能获取