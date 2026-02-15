# EchoDecks 技能

该技能与 EchoDecks 外部 API 集成，用于管理闪卡、利用人工智能生成内容以及进行音频学习。

## 配置要求
需要设置 `ECHODECKS_API_KEY` 环境变量。

## 可用工具

### `echodecks_get_user`
获取用户信息、剩余信用额度以及全局学习统计数据。

### `echodecks_list_decks`
列出您账户中的所有闪卡集。
- `id`（可选）：通过 ID 查找特定的闪卡集。

### `echodecks_create_deck`
创建一个新的闪卡集。
- `title`（必填）：闪卡集的名称。
- `description`（可选）：简短描述。

### `echodecks_list_cards`
列出特定闪卡集中的所有卡片。
- `deck_id`（必填）：目标闪卡集的 ID。

### `echodecks_generate_cards`
使用人工智能生成新的闪卡。
- `deck_id`（必填）：目标闪卡集的 ID。
- `topic`（可选）：主题字符串。
- `text`（可选）：详细的来源文本。
*费用：10 信用点。*

### `echodecks_generate_podcast`
根据闪卡集内容合成音频播客。
- `deck_id`（必填）：源闪卡集的 ID。
- `style`（可选）：“summary” 或 “conversation”（默认值：“summary”）。
*费用：50 信用点。*

### `echodecks_podcast_status`
查看播客的生成进度。
- `id`（必填）：播客的 ID。

### `echodecks_get_study_link`
获取基于网页的学习会话的直接链接。
- `deck_id`（必填）：用于学习的闪卡集的 ID。

### `echodecks_submit_review`
为某张卡片提交间隔重复学习记录。
- `card_id`（必填）：卡片的 ID。
- `quality`（必填）：0（再次学习），1（困难），2（中等），3（简单）。

## 实现方式
所有工具均通过 `scripts/echodecks_client.py` 命令行接口（CLI）进行调用。