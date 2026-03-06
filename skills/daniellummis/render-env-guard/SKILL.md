---
name: render-env-guard
description: >
  **预检功能：**  
  在部署之前，该功能会检查渲染服务的环境变量，确保所有必要的键值对都已正确设置。同时，它会检测是否存在缺失的键或占位符/模板值，这些问题常常会导致生产环境中的部署失败。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["curl","python3"],"env":["RENDER_API_KEY"]}}}
---
# Render Env Guard

当部署失败时（可能是由于环境变量缺失、模板中泄露了占位符值，或者服务选择不明确），请使用此技能。

## 该技能的功能：
- 通过ID或名称查找Render服务
- 通过Render API获取服务的环境变量
- 验证所需的关键值是否存在且非空
- 标记可疑的值（如模板占位符、本地主机数据库URL、未展开的 `${VAR}` 引用）
- 如果遇到任何阻碍性问题，会返回非零退出码，以便CI/部署脚本能够快速终止

## 适用场景：
- 在执行 `render deploy` 或 `render blueprint` 更新之前
- 在新环境上线之后
- 当运行时出现与配置相关的5xx错误时

## 输入参数：
- `RENDER_API_KEY`（必填）
- 以下选项之一：
  - `RENDER_SERVICE_ID`
  - `RENDER_SERVICE_NAME`
- 可选参数：
  - `RENDER_API_BASE_URL`（默认值：`https://api.render.com/v1`）
  - `REQUIRED_ENV_KEYS`（以逗号分隔，默认值：`DATABASE_URL,DIRECT_URL,SHADOW_DATABASE_URL,NEXT_PUBLIC_APP_URL`）

## 执行方式：
```bash
bash scripts/check-render-env.sh
```

或者使用具体的值执行：
```bash
RENDER_SERVICE_NAME=my-service \
REQUIRED_ENV_KEYS="DATABASE_URL,NEXT_PUBLIC_APP_URL,STRIPE_SECRET_KEY" \
bash scripts/check-render-env.sh
```

## 输出结果：
- 打印包含 `PASS`/`FAIL` 状态的简短报告
- 如果所有所需的关键值都有效，返回退出码 `0`
- 如果有任何关键值缺失/无效或服务查找失败，返回退出码 `1`

## 注意事项：
- 该检查工具的设计较为严格，旨在防止错误的部署发生。
- 它验证的是服务层面的数据（即Render在运行时实际注入的数据），而非本地的 `.env` 文件内容。