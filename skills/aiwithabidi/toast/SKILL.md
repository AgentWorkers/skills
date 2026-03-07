---
name: toast
description: "Toast — 一款用于餐厅的点餐系统，支持订单管理、菜单展示、员工管理、收入统计以及报表生成等功能。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🍞", "requires": {"env": ["TOAST_API_KEY", "TOAST_RESTAURANT_GUID"]}, "primaryEnv": "TOAST_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🍞 Toast

Toast 是一款用于餐厅管理的 POS（Point of Sale）系统，支持订单处理、菜单管理、员工管理、收入中心管理以及报表生成等功能。

## 必需配置项

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `TOAST_API_KEY` | ✅ | Toast API 密钥 |
| `TOAST_RESTAURANT_GUID` | ✅ | 餐厅的唯一标识符（GUID） |

## 快速入门

```bash
# List orders
python3 {{baseDir}}/scripts/toast.py list-orders --start-date <value> --end-date <value> --page-size "25"

# Get order details
python3 {{baseDir}}/scripts/toast.py get-order <id>

# List menus
python3 {{baseDir}}/scripts/toast.py list-menus

# Get menu details
python3 {{baseDir}}/scripts/toast.py get-menu <id>

# List menu items
python3 {{baseDir}}/scripts/toast.py list-menu-items --page-size "100"

# List employees
python3 {{baseDir}}/scripts/toast.py list-employees

# Get employee details
python3 {{baseDir}}/scripts/toast.py get-employee <id>

# List revenue centers
python3 {{baseDir}}/scripts/toast.py list-revenue-centers

# List tables
python3 {{baseDir}}/scripts/toast.py list-tables

# List dining options
python3 {{baseDir}}/scripts/toast.py list-dining-options

# Get restaurant info
python3 {{baseDir}}/scripts/toast.py get-restaurant --guid <value>
```

## 输出格式

所有命令默认以 JSON 格式输出结果。

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/toast.py` | 主要的 CLI 工具，包含所有命令 |

## 致谢

该项目由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 共同开发。  
相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 查看，代码仓库位于 [GitHub](https://github.com/aiwithabidi)。  
Toast 是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理系统设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)