---
name: dexcom
description: 通过Dexcom G7/G6连续血糖监测仪（CGM）监测血糖水平
homepage: https://www.dexcom.com
metadata: {"clawdbot":{"emoji":"🩸","requires":{"bins":["uv"],"env":["DEXCOM_USER","DEXCOM_PASSWORD"]},"primaryEnv":"DEXCOM_USER","install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# Dexcom CGM

通过Dexcom G6/G7连续血糖监测仪实现实时血糖监测。

## 设置

设置环境变量：
```bash
export DEXCOM_USER="your@email.com"
export DEXCOM_PASSWORD="your-password"
export DEXCOM_REGION="ous"  # or "us" (optional, defaults to "ous")
```

或在`~/.clawdbot/clawdbot.json`中配置：
```json5
{
  skills: {
    "dexcom": {
      env: {
        DEXCOM_USER: "your@email.com",
        DEXCOM_PASSWORD: "your-password",
        DEXCOM_REGION: "ous"
      }
    }
  }
}
```

## 使用方法

**格式化后的报告：**
```bash
uv run {baseDir}/scripts/glucose.py now
```

**原始JSON数据：**
```bash
uv run {baseDir}/scripts/glucose.py json
```

## 示例输出**

```
🩸 Glucose: 100 mg/dL (5.6 mmol/L)
📈 Trend: steady ➡️
🎯 Status: 🟢 In range
⏰ 2026-01-18 09:30:00
```

## 系统要求

- 需要启用Share功能的Dexcom G6或G7血糖监测仪
- 安装uv（Python包管理工具）
- 拥有有效的Dexcom Share登录凭据