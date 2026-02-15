---
name: withings-family
description: 从 Withings API 中获取多名家庭成员的健康数据，包括体重、身体成分（脂肪、肌肉、骨骼、水分）、活动量以及睡眠状况。当用户询问自己或家人的 Withings 设备数据（如体重变化、身体指标、每日步数、睡眠质量或任何健康测量结果）时，可以使用此功能。
version: 1.1.1
homepage: https://github.com/odrobnik/withings-family-skill
metadata: {"openclaw": {"emoji": "⚖️", "requires": {"bins": ["python3"], "env": ["WITHINGS_CLIENT_ID", "WITHINGS_CLIENT_SECRET"]}}}
---

此技能允许您与多位家庭成员的 Withings 账户进行交互，从而从 Withings 设备（智能体重秤、睡眠分析仪、活动追踪器等）中获取全面的健康数据。

## 多用户支持

该技能原生支持多用户，并为每位用户提供单独的令牌文件：

```
tokens-alice.json
tokens-bob.json
tokens-charlie.json
```

每位家庭成员只需通过 OAuth 进行一次身份验证。他们的令牌会单独存储并自动更新。无需复制或切换令牌——只需将用户 ID 作为第一个参数传递即可。

```bash
python3 scripts/withings.py alice weight
python3 scripts/withings.py bob sleep
python3 scripts/withings.py charlie activity
```

## 何时使用此技能

当用户需要执行以下操作时，请使用此技能：
- 询问自己的体重或体重历史记录
- 查看自己的身体成分（脂肪百分比、肌肉质量、骨骼质量、水分含量）
- 获取每日活动数据（步数、行走距离、消耗的卡路里）
- 了解自己的睡眠数据（睡眠时长、睡眠质量、深度睡眠时间、快速眼动睡眠阶段）
- 提到 “Withings” 或任何 Withings 设备（如 Body+、Sleep Analyzer、ScanWatch 等）
- 希望跟踪自己或家人的健康状况变化

## 设置：创建 Withings 开发者应用程序

在使用此技能之前，您需要创建一个免费的 Withings 开发者应用程序以获取 API 凭据。

### 第 1 步：创建 Withings 开发者账户

1. 访问 [Withings 开发者门户](https://developer.withings.com/)
2. 如果您已有 Withings 账户，请点击 **注册** 或 **登录**
3. 同意开发者服务条款

### 第 2 步：创建您的应用程序

1. 转到 **我的应用程序** → **创建应用程序**
2. 填写应用程序详细信息：
   - **应用程序名称**：选择一个名称（例如：“My Moltbot Health”）
   - **描述**：简要说明您的使用场景
   - **联系邮箱**：您的电子邮件地址
   - **回调 URL**：`http://localhost:18081`（OAuth 所需）
   - **应用程序类型**：选择 “个人使用” 或相应的类型
3. 提交应用程序

### 第 3 步：获取您的凭据

应用程序创建完成后：
1. 转到 **我的应用程序** 并选择您的应用程序
2. 您将看到：
   - **客户端 ID** → 设置为 `WITHINGS_CLIENT_ID` 环境变量
   - **客户端密钥** → 设置为 `WITHINGS_CLIENT_SECRET` 环境变量

### 第 4 步：配置环境变量

将这些变量添加到您的 Moltbot 环境中：
```bash
export WITHINGS_CLIENT_ID="your_client_id_here"
export WITHINGS_CLIENT_SECRET="your_client_secret_here"
```

或者，在 `~/.openclaw/withings-family/.env` 文件中创建一个 `.env` 文件（旧版本：`~/.moltbot/withings-family/.env`）：
```
WITHINGS_CLIENT_ID=your_client_id_here
WITHINGS_CLIENT_SECRET=your_client_secret_here
```

## 配置

该技能提供了两个脚本（位于 `scripts/` 目录下）：
- **`scripts/withings.oauth_local.py`** — 使用本地回调服务器进行自动 OAuth（推荐）
- **`scripts/withings.py`** — 主 CLI 代码 + 手动 OAuth

**凭据存放位置：** `~/.openclaw/withings-family/`（旧版本：`~/.moltbot/withings-family/`）
- `.env` 文件：客户端 ID/密钥（可选，也可以使用环境变量）
- `tokens-<userId>.json`：每位用户的 OAuth 令牌（有效期 600 小时）

在获取任何数据之前，请检查用户是否已通过身份验证。如果出现 “未找到令牌” 的错误，请引导用户完成该用户的初始身份验证流程。

## 身份验证方法

### 方法 A：自动 OAuth（推荐）

使用本地回调服务器自动捕获授权码：

```bash
python3 {baseDir}/scripts/withings_oauth_local.py <userId>
```

示例：
```bash
python3 {baseDir}/scripts/withings_oauth_local.py alice
```

脚本将：
1. 显示授权 URL
2. 在本地主机（localhost:18081）上启动一个服务器
3. 等待重定向
4. 自动捕获授权码并将其转换为令牌
5. 将令牌保存到 `tokens-<userId>.json` 文件中

### 方法 B：手动 OAuth

传统的两步验证流程（详见下面的 “Authentication” 命令）

## 可用命令

所有命令均遵循以下格式：
```bash
python3 {baseDir}/scripts/withings.py <userId> <command> [options]
```

### 1. 身份验证

首次使用时，生成 OAuth URL：
```bash
python3 {baseDir}/scripts/withings.py alice auth
```

用户访问该 URL 并获取授权码后：
```bash
python3 {baseDir}/scripts/withings.py alice auth YOUR_CODE_HERE
```

对于需要访问权限的每位家庭成员，重复此步骤。

### 2. 获取体重

检索最新的体重测量数据：
```bash
python3 {baseDir}/scripts/withings.py alice weight
```

以 JSON 格式返回最近的 5 条体重记录。

**示例输出：**
```json
[
  { "date": "2026-01-17T08:30:00.000Z", "weight": "75.40 kg" },
  { "date": "2026-01-16T08:15:00.000Z", "weight": "75.65 kg" }
]
```

### 3. 获取身体成分

检索全面的身体指标（脂肪、肌肉、骨骼、水分含量）：
```bash
python3 {baseDir}/scripts/withings.py alice body
```

返回最近的 5 次身体成分测量数据。

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

检索每日活动数据（步数、行走距离、消耗的卡路里）：
```bash
python3 {baseDir}/scripts/withings.py alice activity
```

可选地指定天数（默认值：7 天）：
```bash
python3 {baseDir}/scripts/withings.py alice activity 30
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
python3 {baseDir}/scripts/withings.py alice sleep
```

可选地指定天数（默认值：7 天）：
```bash
python3 {baseDir}/scripts/withings.py alice sleep 14
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

常见错误及其解决方法：

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| “未找到令牌” | 用户未通过身份验证 | 运行 `python3 scripts/withings.py <userId> auth` 并按照 OAuth 流程进行身份验证 |
| “令牌刷新失败” | 令牌过期且刷新失败 | 重新使用 `python3 scripts/withings.py <userId> auth` 进行身份验证 |
| “API 错误状态：401” | 凭据无效或过期 | 检查您的客户端 ID 和客户端密钥，然后重新进行身份验证 |
| “API 错误状态：503” | Withings API 暂时不可用 | 稍后等待并重试 |
| 数据为空 | 请求的时间段内没有测量数据 | 用户需要同步他们的 Withings 设备 |

## 注意事项

- **多用户**：每位家庭成员都有自己的令牌文件（`tokens-{userId}.json`）
- **令牌刷新**：令牌在过期后会自动更新
- **权限范围**：使用的 Withings API 权限范围为 `user.metrics` 和 `user.activity`
- **设备支持**：可获取的数据取决于用户拥有的 Withings 设备类型
- **身体成分**：需要使用兼容的智能体重秤（例如 Body+、Body Comp）