---
name: gen-paylink-govilo
description: >
  Upload files to Govilo and generate unlock links via Bot API. Use when:
  (1) Creating a Govilo unlock link from a ZIP, folder, or individual files,
  (2) Automating file upload to Govilo R2 storage with presigned URLs,
  (3) Managing Govilo Bot API interactions (presign → upload → create item).
  Requires GOVILO_API_KEY and SELLER_ADDRESS env vars.
  If missing, guides user to register at https://govilo.xyz/.
metadata:
  author: hau823823@gmail.com
  version: "1.0"
  openclaw:
    requires:
      env:
        - GOVILO_API_KEY
        - SELLER_ADDRESS
    primaryEnv: GOVILO_API_KEY
    homepage: https://github.com/hau823823/gen-paylink-govilo
---

# Govilo To Go

将任何文件转换为付费解锁链接——只需一个命令即可完成打包、上传并收集加密货币支付。实现从创建到盈利的自动化流程。

## 运行前须知

在执行 CLI 命令之前，务必向用户获取以下信息，切勿猜测或使用占位符：

1. **title**：产品名称是什么？
2. **price**：定价是多少（以 USDC 为单位）？
3. **description**：产品的简短描述（可选，但必须询问）。

## CLI 命令

> 需要 [uv](https://docs.astral.sh/uv/)。请参阅 [references/setup-guide.md](references/setup-guide.md) 以获取安装说明。

请从该技能的根目录运行命令。使用一个仅包含 `GOVILO_API_KEY`（以及可选的 `SELLER_ADDRESS`）的专用环境文件（`env` 文件）。切勿将 `--env-file` 指向包含无关敏感信息的项目 `.env` 文件。

```bash
cd <skill_base_directory>
uv run --env-file <path_to>/.env.govilo create-link \
  --input <path>         \
  --title "Product Name" \
  --price "5.00"         \
  --address "0x..."      \
  --description "optional"
```

如果不存在 `.env.govilo` 文件，请在运行前创建一个：

```dotenv
GOVILO_API_KEY=sk_live_xxx
SELLER_ADDRESS=0x...
```

`--input` 参数支持 ZIP 文件、文件夹或单个文件的上传（可重复使用）。非 ZIP 格式的文件会自动被打包。

所有输出结果均为 JSON 格式（`{"ok": true/false, ...}`），失败时退出代码为 1。

## 参数

| 参数                | 是否必填 | 来源                | 描述                          |
|------------------|--------|------------------|--------------------------------------------|
| `--input`           | 是      | CLI                | ZIP 文件、文件夹或文件的路径                |
| `--title`           | 是      | CLI                | 产品标题                        |
| `--price`           | 是      | CLI                | 价格（以 USDC 为单位）                   |
| `--address`          | 否      | 通过 `--env` 参数设置         | 卖家 EVM 钱包地址                   |
| `--description`       | 否      | CLI                | 产品描述                        |

## 工作流程

1. 验证配置信息（API 密钥和卖家地址）
2. 将输入文件打包成 ZIP 文件（如果尚未打包）
3. 发送请求 `POST /api/v1/bot/uploads/presign` 以获取上传链接（`upload_url`）和会话 ID（`session_id`）
4. 使用 `PUT upload_url` 将 ZIP 文件上传到 R2 服务器
5. 发送请求 `POST /api/v1/bot/items` 以获取解锁链接（`unlock_url`）

## 文件限制

- ZIP 文件最大大小：20 MB
- ZIP 文件中最多包含 20 个文件

## 设置要求

需要设置两个参数：

| 参数                | 是否必填 | 描述                          |
|------------------|--------|----------------------------------------|
| `GOVILO_API_KEY`       | 是      | 来自 [govilo.xyz](https://govilo.xyz/) 的机器人 API 密钥     |
| `SELLER_ADDRESS`     | 是*     | 卖家在 **Base 链** 上的 EVM 钱包地址         |

*`SELLER_ADDRESS` 也可以通过 `--address` CLI 参数传递。

请参阅 [references/setup-guide.md](references/setup-guide.md) 以获取详细的注册和钱包设置指南。

## API 参考

有关机器人 API 的端点和错误代码，请参阅 [references/bot-api-quick-ref.md](references/bot-api-quick-ref.md)。