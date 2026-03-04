---
name: yuboto-omni-api
description: 实现、排查故障，并为 Yuboto Omni API（包括 SMS/Viber 消息端点、回调功能、联系人/黑名单管理以及费用/余额/账户相关方法）生成相应的集成方案。在根据 Yuboto API 文档编写代码或工作流程时，请特别注意：当 PDF 文档中的端点详情与实际运行的 Swagger 服务之间存在差异时，需要根据实际情况进行调整。
metadata:
  {
    "openclaw":
      {
        "emoji": "📨",
        "requires": { "bins": ["python3"], "env": ["OCTAPUSH_API_KEY"] },
        "primaryEnv": "OCTAPUSH_API_KEY",
      },
  }
---
# Yuboto Omni API

使用此技能可以安全、一致地与 Yuboto Omni API 进行交互。

**注意：** 此技能需要 `OCTAPUSH_API_KEY` 环境变量。

**入门步骤：** 您需要一个具有 API 访问权限的 Yuboto/Octapush 账户。请在 [octapush.yuboto.com](https://octapush.yuboto.com) 注册，并向客服申请 API 访问权限。

**OpenClaw 集成：** 该技能支持 OpenClaw 的原生凭证管理功能。将您的 API 密钥存储在 `openclaw.json` 文件中，以实现安全、集中化的凭证管理。

## 文档优先级顺序

1. `referencesswagger_v1.json`（实时端点契约）
2. `references/api_quick_reference.md`（人类可读的端点映射）
3. `references/omni_api_v1_10_raw.md`（旧版 PDF 文档）
4. `assets/OMNI_API DOCUMENTATION_V1_10.pdf`（原始 PDF 文件）

如果 PDF 文档与 Swagger 文档中的端点路径/字段存在冲突，请以 Swagger 为准。

## 快速工作流程

1. 确定使用场景（发送消息、获取消息送达状态、联系人列表、黑名单、费用/余额等）。
2. 查找相应的端点：
   - 阅读 `references/api_quick_reference.md`，
   - 或者运行：`python3 scripts/find_endpoints.py --q "<关键词>"`
3. 直接在 `referencesswagger_v1.json` 中验证请求格式：
   - 参数（路径、查询参数、请求头）
   - 请求体
   - 响应格式
4. 编写实现代码，包括：
   - 明确的认证头处理
   - 重试机制和超时设置
   - 结构化的错误处理
5. 对于高级的 Viber 功能，请先参考 Swagger 文档。

## 可用的命令（由 scripts/yuboto_cli.py 提供）

- `balance` — 获取账户余额
- `cost --channel sms --iso2 gr --phonenumber +30...` — 估算发送成本
- `send-sms --sender <approved_sender> --text "..." --to +30... --batch-size 200 --sms-encoding auto` — 发送短信（自动分批发送，支持 Unicode/GSM 编码）
- `dlr --id <messageGuid>` — 查询单条消息的送达状态
- `send-csv --file contacts.csv --phone-col phonenumber --text-col text --sender-col sender` — 从 CSV 文件批量发送短信
- `poll-pending` — 刷新所有待处理消息的状态
- `history --last 20` — 显示最近的发送记录
- `status` / `status --id <messageGuid>` — 查看消息的状态

## 输出要求

在生成代码或集成说明时，请包含以下内容：
- 确切的方法名称和路径
- 必需的认证头信息
- 最小的示例请求
- 预期的响应格式
- 一个失败案例及其处理方式

## 环境变量

### 必需的凭证
- `OCTAPUSH_API_KEY` — 您的 Yuboto/Octapush API 密钥（已由 Octapush 进行 Base64 编码）

**注意：** 这是唯一需要的凭证。

### 可选的变量（用于测试/覆盖）
- `TEST_PHONENUMBER` — 测试用电话号码（国际格式：+3069XXXXXXXX）
- `SMS_SENDER` — SMS 消息的默认发送者 ID（必须经过审核）
- `YUBOTO_BASE_URL` — API 基础 URL（默认：`https://api.yuboto.com`）

### 获取 API 密钥

要使用此技能，您需要一个 Yuboto/Octapush API 密钥：
1. 在 [octapush.yuboto.com](https://octapush.yuboto.com) 注册账户。
2. 联系 Yuboto 客服申请 API 访问权限。
3. 从 Octapush 仪表板或客服处获取 API 密钥。

API 密钥用于所有 Yuboto Omni API 端点的身份验证。

### 设置说明

#### 选项 1：OpenClaw 配置（✅ **推荐**）
将以下配置添加到您的 `openclaw.json` 文件中：
```json
"skills": {
  "entries": {
    "yuboto-omni-api": {
      "enabled": true,
      "env": {
        "OCTAPUSH_API_KEY": "your_base64_api_key_here"
      }
    }
  }
}
```

#### 选项 2：环境变量
```bash
export OCTAPUSH_API_KEY="your_base64_api_key_here"
```

**注意：** 不支持使用 `.env` 文件。建议使用 OpenClaw 配置文件进行安全、集中化的凭证管理。

## 安全与操作注意事项

- 将 API 密钥存储在 `OCTAPUSH_API_KEY` 环境变量中，不要保存在源代码文件中。
- 相比 CLI 的 `--api-key` 参数，使用环境变量更安全，可以避免在 shell 历史记录中泄露凭证。
- `poll-pending.sh` 命令仅从进程环境变量中读取 `OCTAPUSH_API_KEY`（不会读取 `.env` 文件）。
- 发送短信时必须使用经过审核的发送者 ID。如果发送者未通过审核，API 会返回 `108 - Sms Sender is not valid` 的错误代码。
- 批量发送的默认设置：
  - `send-sms` 的默认批量大小为 200 条（每次请求最多 1000 个接收者）
  - `send-sms` 的默认延迟时间为 250 毫秒
  - `send-csv` 的默认延迟时间为 100 毫秒
- 编码默认设置：
  - `--sms-encoding auto` 会自动检测非 GSM 格式的文本并转换为 Unicode 发送
  - 使用 `--sms-encoding unicode` 可强制使用 Unicode 编码（例如希腊语/阿拉伯语/中文）
  - 如有需要，可以使用 `--sms-encoding gsm` 强制使用 GSM 编码
- 默认情况下会保留本地状态：
  - 已发送的日志仅保留最后 5000 行（`YUBOTO_MAX_SENT_LOG_LINES`）
  - 跟踪的状态记录最多保留 5000 条（`YUBOTO_MAX_STATE_RECORDS`）
- 运行时数据存储位置默认在技能文件夹之外：
  - CLI 的状态数据存储路径为 `$XDG_STATE_HOME/openclaw/yuboto-omni-api`（备用路径：`~/.local/state/openclaw/yuboto-omni-api`）
- 日志/状态数据的存储遵循隐私保护原则：
  - 仅存储最小范围的元数据（如 messageGuid、时间戳、状态、接收者数量）
- 默认情况下不保存完整的消息内容/文本/接收者信息
- 如需保存完整数据，请通过 `YUBOTO_STORE_FULL_PAYLOAD=true` 启用该功能
- 运行时依赖项仅限于 Python 标准库（无需安装 `requests`）
- 辅助脚本也仅依赖标准库：`scripts/refresh_swagger.py` 使用 `urllib`（无需安装 `pip`）
- 即使在最小化模式下，也要将本地运行时日志/状态数据视为敏感信息

## 其他说明

- Swagger 文档地址：`https://api.yuboto.com/scalar/#description/introduction`
- Swagger JSON 文档地址：`https://api.yuboto.comswagger/v1swagger.json`
- 更多产品/账户信息：`https://messaging.yuboto.com`
- 生成的示例代码应保持语言中立性，除非用户特别要求使用希腊语/英语版本。