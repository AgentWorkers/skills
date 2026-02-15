# attio-cli

通过 attio-cli 与您的 Attio CRM 工作区进行交互。

## 安装

1. 克隆并安装 attio-cli：
```bash
git clone https://github.com/FroeMic/attio-cli
cd attio-cli
npm install
npm link
```

2. 设置 `ATTIO_API_KEY` 环境变量（从 Attio 设置 > 开发者 > API 密钥中获取）：
   - **推荐方式：** 将其添加到 `~/.claude/.env` 文件中（适用于 Claude Code）
   - **替代方式：** 将其添加到 `~/.bashrc` 或 `~/.zshrc` 文件中：`export ATTIO_API_KEY="your-api-key"`

**仓库地址：** https://github.com/FroeMic/attio-cli

## 命令

- 列出对象和记录：
```bash
attio object list                      # List all objects
attio record list people               # List people records
attio record list companies            # List company records
```

- 操作列表（管道）：
```bash
attio list list-all                    # List all lists
attio entry list <list-slug>           # List entries in a list
```

- 获取详细信息：
```bash
attio object get <object-slug>         # Get object details
attio object attributes <object-slug>  # Get object attributes
attio list attributes <list-slug>      # Get list entry attributes
```

## 生成工作区模式

生成工作区的 Markdown 模式文件，以便了解工作区的结构：
```bash
bash {baseDir}/scripts/generate-schema.sh > {baseDir}/workspace.schema.md
```

该文件会记录工作区中的所有对象、属性、列表和字段选项。

## 关键概念

| 概念 | 用途 | 示例 |
|---------|---------|---------|
| **对象** | 基本记录类型 | 人员、公司、交易 |
| **列表** | 管理流程/工作流 | 销售流程、招聘流程 |
| **记录** | 对象中的单个条目 | 某个人或公司 |
| **条目** | 添加到列表中的记录 | 销售流程中的某笔交易 |

## API 参考

- **基础 URL：** `https://api.attio.com/v2`
- **认证：** `Authorization: Bearer $ATTIO_API_KEY`
- **速率限制：** 每个工作区每 10 秒内允许 100 次请求

## 常见 API 操作

- 搜索人员：
```bash
curl -X POST https://api.attio.com/v2/objects/people/records/query \
  -H "Authorization: Bearer $ATTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"email_addresses": {"contains": "john@example.com"}}}'
```

- 创建记录：
```bash
curl -X POST https://api.attio.com/v2/objects/<object-slug>/records \
  -H "Authorization: Bearer $ATTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": {"values": {"name": [{"value": "Record Name"}]}}}'
```

- 向列表中添加条目：
```bash
curl -X POST https://api.attio.com/v2/lists/<list-slug>/entries \
  -H "Authorization: Bearer $ATTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": {"parent_record_id": "<record-id>"}}'
```

## 注意事项

- 安装完成后，请运行 `generate-schema.sh` 命令，以生成包含所有对象、列表和字段选项的工作区模式文件。
- 列表常用于管理各种流程（如销售阶段、招聘工作流等）。
- attio-cli 在生成模式文件时需要 `jq` 工具来处理 JSON 数据。