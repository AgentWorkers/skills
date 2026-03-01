---
name: yuboto-omni-api
description: 实现、排查故障，并为 Yuboto Omni API（包括 SMS/Viber 消息端点、回调功能、联系人/黑名单管理以及费用/余额/账户相关方法）生成相应的集成方案。在基于 Yuboto API 文档开发代码或工作流程时，请务必参考这些内容，尤其是当 PDF 文档中的端点详情与实际运行的 Swagger 服务存在差异时。
---
# Yuboto Omni API

使用此技能可以安全、一致地与 Yuboto Omni API 进行交互。

## 优先级顺序

1. `referencesswagger_v1.json`（实时端点契约）
2. `references/api_quick_reference.md`（人类可读的端点映射）
3. `references/omni_api_v1_10_raw.md`（旧版 PDF 文档）
4. `assets/OMNI_API DOCUMENTATION_V1_10.pdf`（原始 PDF 文件）

如果 PDF 文档与 Swagger 文档中的端点路径或字段信息存在冲突，请以 Swagger 的内容为准。

## 快速工作流程

1. 确定需要执行的操作（发送消息、查询消息状态、获取联系人信息、管理黑名单、查询费用/余额等）。
2. 查找相应的端点：
   - 阅读 `references/api_quick_reference.md`，
   - 或者运行命令：`python3 scripts/find_endpoints.py --q "<关键词>"`
3. 直接在 `referencesswagger_v1.json` 中验证请求格式：
   - 请求参数（路径、查询参数、请求头）
   - 请求体
   - 响应格式
4. 编写实现代码，确保包含以下功能：
   - 正确处理认证请求头
   - 实现重试机制和超时设置
   - 优雅地处理错误情况
5. 对于高级的 Viber 功能，请先参考 Swagger 文档。

## 可用的命令（由 `scripts/yuboto_cli.py` 提供）

- `balance` — 获取账户余额
- `cost --channel sms --iso2 gr --phonenumber +30...` — 估算短信发送费用
- `send-sms --sender <approved_sender> --text "..." --to +30...` — 发送短信
- `dlr --id <messageGuid>` — 查询单条消息的发送状态
- `send-csv --file contacts.csv --phone-col phonenumber --text-col text --sender-col sender` — 从 CSV 文件批量发送短信
- `poll-pending` — 刷新所有待处理消息的状态
- `history --last 20` — 显示最近的发送记录
- `status` / `status --id <messageGuid>` — 查看消息的发送状态

## 代码生成与集成说明要求

- 明确指定方法名称和端点路径。
- 提供必要的认证请求头信息。
- 提供一个简单的示例请求。
- 描述预期的响应格式。
- 提供一个失败场景及其处理方法。

## 安全性与运维注意事项

- 将 API 密钥存储在环境变量 `OCTAPUSH_API_KEY` 中，切勿将其放在源代码文件中。
- 优先使用环境变量而非命令行参数 `--api-key`，以避免在 shell 历史记录中泄露敏感信息。
- 仅使用经过审核的发送者 ID（例如，官方认可的短信发送者名称）。
- 将本地运行时的日志和状态数据视为敏感信息（如电话号码、消息预览内容、消息状态数据）。
- 在发布技能包时，确保将运行时数据单独存放，不要包含在技能包内。

## 其他注意事项

- Swagger 文档地址：`https://api.yuboto.com/scalar/#description/introduction`
- Swagger JSON 文件地址：`https://api.yuboto.comswagger/v1swagger.json`
- 生成的示例代码应保持语言中立性，除非用户特别要求提供俄文或英文版本。