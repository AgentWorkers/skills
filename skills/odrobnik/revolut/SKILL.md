---
name: revolut
description: "通过 Playwright 实现 Revolut 的 Web 自动化：登录/登出、查看账户信息以及获取交易记录。"
summary: "Revolut banking automation: login, accounts, transactions, portfolio."
version: 1.3.1
homepage: "https://github.com/odrobnik/revolut-skill"
metadata:
  openclaw:
    emoji: "💳"
    requires:
      bins: ["python3", "playwright"]
      python: ["playwright"]
---

# Revolut 银行业务自动化

以 JSON 格式获取所有钱包货币和存款的当前账户余额、投资组合持仓及交易记录。使用 Playwright 来自动化 Revolut 网上银行操作。

**入口文件：** `{baseDir}/scripts/revolut.py`

## 设置

有关先决条件和设置说明，请参阅 [SETUP.md](SETUP.md)。

## 命令

```bash
python3 {baseDir}/scripts/revolut.py --user oliver login
python3 {baseDir}/scripts/revolut.py --user oliver accounts
python3 {baseDir}/scripts/revolut.py --user oliver transactions --from YYYY-MM-DD --until YYYY-MM-DD
python3 {baseDir}/scripts/revolut.py --user sylvia portfolio
python3 {baseDir}/scripts/revolut.py --user oliver invest-transactions --from YYYY-MM-DD --until YYYY-MM-DD
```

## 推荐的操作流程

```
login → accounts → transactions → portfolio → logout
```

完成所有操作后，请务必调用 `logout` 以删除存储的浏览器会话。

## 注意事项：
- 每个用户的状态数据存储在 `{workspace}/revolut/` 目录中（通过 `logout` 命令删除）。
- 输出文件路径（`--out` 参数）会被保存在工作区或 `/tmp` 目录中。
- 不会加载 `.env` 文件——所有凭据信息仅存储在 `config.json` 文件中。