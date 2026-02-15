# IMA 技能

用于控制 **IMA (ima.copilot)** 桌面应用程序，实现 AI 搜索和私有知识检索功能。

## 工具

### ima_search
启动 IMA 并执行搜索操作。通过特殊标签支持“私有知识库”模式。

- **query**（必填）：搜索查询。使用 `@个人知识库` 或 `@知识` 作为前缀可搜索您的私有知识库（需要 `config.json` 配置文件）。
- **autoclose**（可选）：设置为 `true` 时，搜索完成后会自动关闭应用程序。默认值为 `false`。

**实现代码：**
```bash
/usr/bin/python3 /opt/homebrew/lib/node_modules/clawdbot/skills/ima/scripts/ima.py "{query}" --autoclose="{autoclose}"
```

## 配置

要启用私有知识库搜索功能，您需要提供您的 `knowledge_id`。
脚本会在以下位置查找配置文件：
1. `~/.clawd_ima_config.json`
2. `skills/ima/config.json`

**配置格式：**
```json
{
  "knowledge_id": "your_id_string"
}
```

## 示例

- **公共搜索：** `clawdbot ima_search query="DeepSeek 分析"`
- **私有搜索：** `clawdbot ima_search query="@知识 项目更新"`