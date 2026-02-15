---
name: raiffeisen-elba
description: "使用 Playwright 自动化 Raiffeisen ELBA 在线银行操作：登录/登出、查看账户信息以及查询交易记录。"
summary: "Raiffeisen ELBA banking automation: login, accounts, transactions."
version: 1.3.2
homepage: https://github.com/odrobnik/raiffeisen-elba-skill
metadata:
  openclaw:
    emoji: "🏦"
    requires:
      bins: ["python3"]
      python: ["requests", "playwright"]
      env: ["RAIFFEISEN_ELBA_ID", "RAIFFEISEN_ELBA_PIN"]
---

# Raiffeisen ELBA 银行自动化

用于获取所有账户类型的当前账户余额、证券存管位置和交易记录，并以 JSON 格式输出，以便进行自动处理。该脚本利用 Playwright 工具实现 Raiffeisen ELBA 在线银行的自动化操作。

**入口文件：** `{baseDir}/scripts/elba.py`

## 设置

有关先决条件和设置说明，请参阅 [SETUP.md](SETUP.md)。

## 命令

```bash
python3 {baseDir}/scripts/elba.py login
python3 {baseDir}/scripts/elba.py logout
python3 {baseDir}/scripts/elba.py accounts
python3 {baseDir}/scripts/elba.py transactions --account <iban> --from YYYY-MM-DD --until YYYY-MM-DD
```

## 推荐的操作流程

```
login → accounts → transactions → portfolio → logout
```

完成所有操作后，请务必调用 `logout` 函数，以清除浏览器中存储的会话信息（cookie、本地存储数据以及 Playwright 的配置信息）。这样可以避免在磁盘上留下持久的认证状态。