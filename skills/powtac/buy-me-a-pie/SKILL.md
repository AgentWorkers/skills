---
name: buy-me-a-pie
description: >
  **读取和修改 Buy Me a Pie 列表的功能**  
  这是一个非官方的第三方技能（third-party skill），与 Buy Me a Pie 无任何关联。该功能主要用于管理列表、商品信息、购买状态、分享功能以及账户信息的查询。在使用该功能时，应优先通过 API 进行操作。浏览器仅用于注册、PIN 码重置、OAuth 验证、打印相关操作，或在 API 出现故障时作为备用方式。
homepage: https://app.buymeapie.com/
metadata:
  openclaw:
    skillKey: buy-me-a-pie
    summary: Unofficial skill to manage Buy Me a Pie lists and items.
    homepage: https://app.buymeapie.com/
    requires:
      bins:
        - python3
      env:
        - BUYMEAPIE_LOGIN
        - BUYMEAPIE_PIN
    install:
      - id: brew
        kind: brew
        formula: python
        bins:
          - python3
        label: Install Python 3 (brew)
---
# Buy Me A Pie

这是一个非官方的第三方技能（third-party skill），与 Buy Me a Pie 无关。

**API 使用说明：**

**设置凭据：**
- `BUYMEAPIE_LOGIN`
- `BUYMEAPIE_PIN`

**运行命令：**
- `{baseDir}/scripts/buymeapie.sh whoami`  查看当前用户信息
- `{baseDir}/scripts/buymeapie.sh lists`  查看商品列表
- `{baseDir}/scripts/buymeapie.sh items --list-id <id>`  查看指定商品的信息
- `{baseDir}/scripts/buymeapie.sh add-item --list-id <id> --title "Milk" --amount "2"`  添加商品（例如：购买牛奶）
- `{baseDir}/scripts/buymeapie.sh set-item-state --list-id <id> --item-id <id> --purchased true`  设置商品购买状态
- `{baseDir}/scripts/buymeapie.sh share-list --list-id <id> --email friend@example.com`  分享商品列表给指定邮箱

**使用规则：**
- 在执行写入操作前，必须先解析商品 ID。
- 除非用户明确要求替换分享邮箱，否则默认使用系统默认的分享邮箱。
- 如果遇到 `423` 错误，应尝试重试操作。
- 将 `401` 和 `422` 错误视为身份验证或状态相关的错误。
- 不允许对商品列表进行任何写入操作。
- 注册、重置 PIN 码、使用 OAuth、查看商品信息或处理 API 相关问题时，必须通过浏览器完成。

**仅在需要时阅读的文档：**
- `{baseDir}/references/api-surface.md`  API 使用指南
- `{baseDir}/references/architecture.md`  系统架构说明