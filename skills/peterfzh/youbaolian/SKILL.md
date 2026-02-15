---
name: youbaolian
description: 用于管理用户表单（youbaolian）、订单（orders）以及用户（users）的 REST API。
homepage: https://cxv3-new.youbaolian.top
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["jq","curl"],"env":["YBL_URL","YBL_CRYPTION"]}}}
---

# Youbaolian 技能

## 设置

1. 在 `credentials.json` 文件中配置您的 ybl 服务器：
```json
{
    "name": "Server Ybl",
    "url": "https://cxv3-new.youbaolian.top",
    "account": {
        "encryption": "1W2VGiJLPZUQkBiPsbkwiT+fW9hD3IMKlrA9dhYKakG0shYmRHVYNpO3SKzbqwf6Iw8x067uaqXa2o+VTUrc9RpFeX5YJ5Y5jphtNWm00WhYjP3K5c3gkV+j/kqY2AP3WXF5IvKNFoNEiQkl71P9o8RLDoRzym+GFJMjE70psXEfM="
    }
}
```

2. 设置环境变量：
   ```bash
   export YBL_URL="https://cxv3-new.youbaolian.top"
   export YBL_ENCRYPTION="1W2VGiJLPZUQkBiPsbkwiT+fW9hD3IMKlrA9dhYKakG0shYmRHVYNpO3SKzbqwf6Iw8x067uaqXa2o+VTUrc9RpFeX5YJ5Y5jphtNWm00WhYjP3K5c3gkV+j/kqY2AP3WXF5IvKNFoNEiQkl71P9o8RLDoRzym+GFJMjE70psXEfM="
   ```

3. 获取认证令牌：
   ```bash
   export TB_TOKEN=$(curl -s -X POST "$YBL_URL/insapi/v3/union/unionLoginEncryptionPortal" \
    -H "Content-Type: application/json" \
    -d "{\"encryption\":\"$YBL_ENCRYPTION\"}" | jq -r '.data.token')
   ```

## 使用方法

所有命令均使用 `curl` 来与 Youbaolian REST API 进行交互。

### 认证

**登录并获取令牌：**
```bash
curl -s -X POST "$YBL_URL/insapi/v3/union/unionLoginEncryptionPortal" \
  -H "Content-Type: application/json" \
  -d "{\"encryption\":\"$YBL_ENCRYPTION\"}" | jq -r '.data.token'
```