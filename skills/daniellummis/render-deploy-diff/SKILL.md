---
name: render-deploy-diff
description: 在部署之前，检测所需的本地环境变量（local env keys）与 Render 服务之间的配置差异；如果远程环境中缺少某些必需的变量，则检测失败。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","curl","python3"],"env":["RENDER_API_KEY"]}}}
---
# **Render Deploy Diff**

在部署之前使用此技能，以比较所需的环境配置键与Render服务当前的实际配置。

## **该技能的功能：**
- 根据 `RENDER_SERVICE_ID` 或 `RENDER_SERVICE_NAME` 查找目标Render服务。
- 从 `REQUIRED_ENV_KEYS` 或本地环境模板文件中读取所需的环境配置键。
- 从Render API中获取已配置的环境配置键。
- 输出两组差异信息：
  - 在Render上存在但本地缺失的配置键。
  - 在Render上存在但在本地不需要的配置键。
- 如果Render上缺少任何所需的配置键，则返回非零的退出码。

## **输入参数：**
- `RENDER_API_KEY`（必需，除非使用模拟的JSON数据）。
- 以下参数之一：
  - `RENDER_SERVICE_ID`
  - `RENDER_SERVICE_NAME`
- 可选参数：
  - `RENDER_API_BASE_URL`（默认值：`https://api.render.com/v1`）
  - `REQUIRED_ENV_KEYS`（用逗号分隔的必需配置键列表）
  - `REQUIRED_ENV FILES`（用逗号分隔的文件路径，用于解析环境配置文件，默认值为`.env.example`和`.env.production`）
  - `RENDER_ENV_VARS_JSON_PATH`（保存的Render环境变量API JSON文件的路径，用于离线测试）

## **执行方式：**
```bash
bash scripts/render-deploy-diff.sh
```

**使用明确指定的所需配置键执行：**
```bash
RENDER_SERVICE_NAME=my-service \
REQUIRED_ENV_KEYS="DATABASE_URL,DIRECT_URL,SHADOW_DATABASE_URL,NEXT_PUBLIC_APP_URL" \
bash scripts/render-deploy-diff.sh
```

**使用保存的API响应进行离线测试：**
```bash
REQUIRED_ENV_KEYS="DATABASE_URL,NEXT_PUBLIC_APP_URL" \
RENDER_ENV_VARS_JSON_PATH=./fixtures/render-env-vars.json \
bash scripts/render-deploy-diff.sh
```

## **输出结果：**
- 输出服务标识、所需配置键的数量、远程服务器上的配置键数量以及差异总结。
- 如果Render上所有所需的配置键都存在，则返回退出码`0`。
- 如果缺少所需的配置键或输入参数无效，则返回退出码`1`。