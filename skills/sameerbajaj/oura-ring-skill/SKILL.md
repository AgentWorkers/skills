---
name: oura-ring
description: 通过 Oura Cloud API V2 获取 Oura Ring 的设备状态（是否已准备好使用）以及 7 天内的状态变化趋势，并生成一份每日设备状态报告（Morning Readiness Brief）。
---

# Oura Ring (V1)

本技能提供了一个小型、公开可用的参考实现，用于从 **Oura V2 API** (`/v2/usercollection/*`) 中获取 **健康状况（Readiness）**、**睡眠质量（Sleep）** 以及 **7天健康趋势（7-day Readiness trends）** 数据。

## 快速参考

- **命令行界面（CLI，获取原始数据）**：
  - `python3 skills/oura-ring/cli.py --format json --pretty readiness`
  - `python3 skills/oura-ring/cli.py --format json --pretty sleep`
  - `python3 skills/oura-ring/cli.py --format json --pretty trends`
  - `python3 skills/oura-ring/cli.py --format json --pretty resilience`
  - `python3 skills/oura-ring/cli.py --format json --pretty stress`

- **晨间健康报告（格式化输出）**：
  - `./skills/oura-ring/scripts/morning_brief.sh`

## 功能特点

- **晨间健康报告**：基于最新数据提供战术性建议。
- **趋势分析**：展示过去7天内各项指标的变化情况。
- **韧性跟踪**：实时监控系统容量，帮助进行压力管理。

## 设置

### 1) 安装依赖项（建议使用虚拟环境（venv）**

在 macOS 或 Homebrew 环境中，Python 通常会阻止系统级别的 `pip install` 操作（遵循 PEP 668 规范），因此建议使用虚拟环境：

```bash
python3 -m venv skills/oura-ring/.venv
source skills/oura-ring/.venv/bin/activate
python -m pip install -r skills/oura-ring/requirements.txt
```

### 2) 创建 `.env` 文件

在 `skills/oura-ring` 目录下创建 `.env` 文件：

```bash
cp skills/oura-ring/.env.example skills/oura-ring/.env
# then edit skills/oura-ring/.env
```

CLI 需要读取以下环境变量：
- `OURA_TOKEN`（必填）
- `OURA_BASE_URL`（可选；默认值为 `https://api.ouraring.com/v2/usercollection`）

## 获取 Oura API 令牌（OAuth2）

Oura V2 使用 OAuth2 令牌进行身份验证：

1. 创建一个 Oura API 应用程序：
   - 访问：https://cloud.ouraring.com/oauth/applications
2. 设置重定向 URI（用于本地测试，例如 `http://localhost:8080/callback`）。
3. 打开授权页面，并填写以下信息：
   - `CLIENT_ID`
   - `REDIRECT_URI`
   - `scope`

```text
https://cloud.ouraring.com/oauth/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT_URI&scope=readiness%20sleep
```

4. 审批通过后，系统会将您重定向到指定的重定向 URI，并在 URL 中附加 `code=...` 的查询参数。
5. 使用该代码获取访问令牌：

```bash
curl -X POST https://api.ouraring.com/oauth/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d grant_type=authorization_code \
  -d client_id=CLIENT_ID \
  -d client_secret=CLIENT_SECRET \
  -d redirect_uri=REDIRECT_URI \
  -d code=AUTH_CODE
```

6. 将获取到的访问令牌保存到 `skills/oura-ring/.env` 文件中，格式为 `OURA_TOKEN=...`。

**注意**：
- 访问令牌可能会过期，您可能需要使用 `refresh_token` 来刷新令牌。
- **请勿** 将 `.env` 文件提交到版本控制系统中。

## 使用方法

### 健康状况（Readiness）

```bash
python3 skills/oura-ring/cli.py --env-file skills/oura-ring/.env --format json --pretty readiness
```

### 睡眠质量（Sleep）

```bash
python3 skills/oura-ring/cli.py --env-file skills/oura-ring/.env --format json --pretty sleep
```

### 7天健康趋势（分页显示）

```bash
python3 skills/oura-ring/cli.py --env-file skills/oura-ring/.env --format json --pretty trends
```

## 晨间健康报告的实现方式

```bash
./skills/oura-ring/scripts/morning_brief.sh
```

**修改环境变量文件的位置**：

```bash
OURA_ENV_FILE=/path/to/.env ./skills/oura-ring/scripts/morning_brief.sh
```

**以模拟模式运行（无需令牌）**：

```bash
OURA_MOCK=1 ./skills/oura-ring/scripts/morning_brief.sh
```

**无需令牌的验证方式**：

```bash
python3 skills/oura-ring/cli.py --mock readiness --format json
python3 skills/oura-ring/cli.py --mock sleep --format json
python3 skills/oura-ring/cli.py --mock trends --format json
```