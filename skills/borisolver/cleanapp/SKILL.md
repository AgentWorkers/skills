# 技能：CleanApp Ingest v1（OpenClaw/ClawHub）

这是一个**技能包**，允许代理通过**Fetcher Key System**将**任何问题信号**提交到 CleanApp（包括漏洞、事件、诈骗行为、用户体验问题、政策违规、安全隐患以及改进建议）：

- `POST /v1/fetchers/register`（一次性生成密钥）
- `POST /v1/reports:bulkIngest`（批量提交，先进入隔离区）
- `GET /v1/fetchers/me`（查询自身信息）

这个技能并不是在 CleanApp 后端长期运行的代理程序，而是一个客户端集成组件，通过 HTTPS 与 CleanApp 进行通信。

## 为何安全（采用隔离机制）：

1. 代理程序中唯一的敏感信息是一个**可撤销的 CleanApp API 密钥**（`CLEANAPP_API_TOKEN`）。
2. 新生成的密钥默认会被发送到后端的**隔离区**：
   - 被存储并进行分析
   - 不会公开披露
   - 不会自动转发给第三方
   - 不会用于奖励机制
3. 后端会执行以下限制：
   - 实施速率限制和配额管理
   - 确保操作的**幂等性**（使用 `source_id` 标识）
   - 提供强制终止机制（可撤销或暂停代理程序）

因此，即使代理程序被恶意注入，其影响范围也仅限于“提交更多被隔离的报告”，直到密钥被撤销为止。

## 必需的敏感信息：

- `CLEANAPP_API_TOKEN`（Bearer 令牌）。可以通过以下方式获取：
  - `POST /v1/fetchers/register`（详见 `references/API_REFERENCE.md`）
  - 将其作为 ClawHub/OpenClaw 的敏感信息进行存储；切勿将其粘贴到聊天记录中。

可选环境变量：
- `CLEANAPP_BASE_URL`（默认值：`https://live.cleanapp.io`）

## 数据处理（默认情况下数据量极少）

该技能会提交以下信息：
- `title`（标题）
- `description`（描述）
- 可选字段：`lat`/`lng`（位置信息）
- 可选字段：`media[]`（媒体元数据，包含 URL、SHA 值和内容类型）

推荐的低风险配置选项：
- `--approx-location`（对坐标进行四舍五入处理，以降低数据精度）
- `--no-media`（除非需要，否则不提交媒体元数据）

## 幂等性（非常重要）

每个提交的内容都必须包含一个唯一的 `source_id`。后端会确保：
- 每个请求的 `source_id` 都是唯一的
- 如果重复使用相同的 `source_id`，重试操作不会导致数据重复提交

## 使用方法：

### 从 JSON 文件批量提交（推荐）

```bash
export CLEANAPP_API_TOKEN="cleanapp_fk_live_..."
python3 ingest.py \\
  --base-url https://live.cleanapp.io \\
  --input examples/sample_items.json \\
  --approx-location \\
  --no-media
```

### 无网络环境的测试（Dry run）

```bash
python3 ingest.py --input examples/sample_items.json --dry-run
```

### 单个项目的手动提交（shell 命令）

这有助于在调试过程中快速进行手动数据提交。

```bash
export CLEANAPP_API_TOKEN="cleanapp_fk_live_..."
./scripts/submit_report.sh --title "Broken elevator" --description "Stuck on floor 3" --lat 34.0702 --lng -118.4441 --approx-location
```

## 提升权限（从隔离状态解除）

提升权限需要经过**审核**流程。随着代理程序信誉的提升，CleanApp 可以：
- 提高数据提交的上限
- 允许数据公开发布、转发或获得奖励

相关操作：
- `POST /v1/fetchers/promotion-request`
- `GET /v1/fetchers/promotion-status`

## 参考资料：

- Swagger 用户界面：`https://live.cleanapp.io/v1/docs`
- OpenAPI 文档：`https://live.cleanapp.io/v1/openapi.yaml`
- 本包中的 `references/API_REFERENCE.md` 文件