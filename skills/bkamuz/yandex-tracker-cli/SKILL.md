---
name: yandex-tracker-cli
description: Yandex Tracker 的命令行接口（CLI）：支持 bash 和 curl。功能包括管理任务队列、问题（issues）、评论（comments）、工作日志（worklogs）、附件（attachments），以及使用 YQL 进行数据查询。
homepage: https://github.com/bkamuz/yandex-tracker-cli
metadata:
  clawdbot:
    emoji: "📋"
    requires:
      env: ["TOKEN", "ORG_ID"]
      bins: ["curl", "jq"]
    primaryEnv: "TOKEN"
    files: ["yandex-tracker.sh"]
  openclaw:
    requires:
      env: ["TOKEN", "ORG_ID"]
      bins: ["curl", "jq"]
    primaryEnv: "TOKEN"
---
# Yandex Tracker CLI 工具

这是一个基于 bash 和 curl 的简单 CLI 工具，用于与 Yandex Tracker 进行交互。它通过带有正确请求头（`X-Org-Id`）的 API 直接进行通信，除了 `curl` 和 `jq` 之外，不依赖任何外部库。

## 安装

1. 将脚本复制到系统的 PATH 变量所包含的目录中：
```bash
mkdir -p ~/bin
cp yandex-tracker.sh ~/bin/yandex-tracker
chmod +x ~/bin/yandex-tracker
```

或者创建一个符号链接：
```bash
ln -s /path/to/skill/yandex-tracker.sh ~/bin/yandex-tracker
```

2. **配置凭据**：需要 `TOKEN` 和 `ORG_ID`——可以通过环境变量或配置文件来设置（只需选择一种方式）。如果环境变量中没有设置 `TOKEN/ORG_ID`，脚本会自动从配置文件中读取这些值。

**方法 A — 通过环境变量（推荐）：**
```bash
export TOKEN='y0__...'      # OAuth токен (Tracker UI → Settings → Applications → OAuth)
export ORG_ID='1234...'     # Org ID (DevTools → Network → X-Org-Id)
```
你可以将这些变量添加到 `~/.bashrc` 或 `~/.profile` 文件中。

**方法 B — 通过配置文件：**
创建一个名为 `~/.yandex-tracker-env` 的文件（脚本仅在环境变量中没有设置 `TOKEN/ORG_ID` 时才会读取该文件）。文件格式为 `KEY=value`（以 `#` 开头的注释会被忽略）。该文件仅被当作纯文本读取（仅提取 `TOKEN` 和 `ORG_ID` 的值），不会执行其中的任何代码：
```bash
TOKEN='y0__...'
ORG_ID='1234...'
```
建议使用环境变量来存储凭据。如果使用配置文件，请确保为其设置正确的权限（`chmod 600 ~/.yandex-tracker-env`）。

3. 确保已经安装了 `jq`：
```bash
sudo apt install jq   # Ubuntu/Debian
# или
brew install jq       # macOS
```

## 使用方法

### 常用命令

| 命令 | 功能 |
|---------|----------|
| `queues` | 显示所有队列的列表（格式：`key<TAB>name`） |
| `queue-get <key>` | 获取队列的详细信息（JSON 格式） |
| `queue-fields <key>` | 查看队列中的所有字段（包括自定义字段） |
| `issue-get <issue-id>` | 获取任务详情（格式：`BIMLAB-123`） |
| `issue-create <queue> <summary>` | 创建新任务（详细信息通过 stdin 提供，格式为 JSON） |
| `issue-update <issue-id>` | 更新任务信息（JSON 数据通过 stdin 提供） |
| `issue-delete <issue-id>` | 删除任务 |
| `issue-comment <issue-id> <text>` | 为任务添加评论 |
| `issue-comment-edit <issue-id> <comment-id> <new-text>` | 修改任务评论 |
| `issue-comment-delete <issue-id> <comment-id>` | 删除任务评论 |
| `issue-transitions <issue-id>` | 查看任务状态的变化历史 |
| `issue-close <issue-id> <resolution>` | 关闭任务（`resolution` 可选值：`fixed`, `wontFix`, `duplicate` 等） |
| `issue-worklog <issue-id> <duration> [comment]` | 为任务添加工作日志（`duration` 以 `PT1H30M` 等格式表示） |
| `issue-attachments <issue-id>` | 查看任务的附件列表（JSON 格式） |
| `attachment-download <issue-id> <fileId> [output]` | 下载附件（如果未指定 `output`，则输出到 stdout） |
| `attachment-upload <issue-id> <filepath> [comment]` | 上传文件到任务（可选，`comment` 用于记录上传信息） |
| `issues-search` | 通过 YQL 查询任务（示例请求：`{"query":"Queue = BIMLAB AND Status = Open","limit":50}`） |
| `projects-list` | 显示所有项目的列表（JSON 格式） |
| `project-get <project-id>` | 获取项目详情 |
| `project-issues <project-id>` | 查看项目下的所有任务 |
| `sprints-list` | 显示所有冲刺的列表 |
| `sprint-get <sprint-id>` | 获取冲刺的详细信息 |
| `sprint-issues <sprint-id>` | 查看冲刺中的任务 |
| `users-list` | 显示所有用户列表 |
| `statuses-list` | 显示所有任务的状态 |
| `resolutions-list` | 查看可用于关闭任务的解决方案类型 |
| `issue-types-list` | 显示任务类型（如 bug、task、improvement 等） |

### 使用示例

```bash
# Список очередей
yandex-tracker queues

# Создать задачу с дополнительными полями
echo '{"priority":"critical","description":"Подробности"}' | yandex-tracker issue-create BIMLAB "Новая задача"

# Добавить комментарий
yandex-tracker issue-comment BIMLAB-266 "Работаю над этим"

# Добавить spent time
yandex-tracker issue-worklog BIMLAB-266 PT2H "Исследование"

# Получить возможные переходы (чтобы понять, как закрыть)
yandex-tracker issue-transitions BIMLAB-266 | jq .

# Обновить задачу (перевести в другую очередь, например)
echo '{"queue":"RAZRABOTKA"}' | yandex-tracker issue-update BIMLAB-266

# Поиск задач через YQL
echo '{"query":"Queue = BIMLAB AND Status = Open","limit":20}' | yandex-tracker issues-search | jq .

# Список проектов
yandex-tracker projects-list | jq .

# Задачи проекта
yandex-tracker project-issues 104 | jq .

# Вложения (Attachments)
# Список вложений
yandex-tracker issue-attachments BIMLAB-266 | jq .
# Скачать файл (fileId из списка вложений) в указанный путь
yandex-tracker attachment-download BIMLAB-266 abc123 /tmp/downloaded.pdf
# Загрузить файл в задачу (с комментарием)
yandex-tracker attachment-upload BIMLAB-266 /path/to/file.pdf "Служебная записка"

# Спринты (Agile)
yandex-tracker sprints-list | jq .
yandex-tracker sprint-issues 42 | jq .

# Справочники
yandex-tracker users-list | jq .
yandex-tracker statuses-list | jq .
yandex-tracker resolutions-list | jq .
yandex-tracker issue-types-list | jq .

# Редактирование и удаление комментариев
yandex-tracker issue-comment-edit BIMLAB-266 12345 "Обновлённый текст"
yandex-tracker issue-comment-delete BIMLAB-266 12345
```

## 注意事项

- **对于本地部署的 Yandex Tracker**：请在 DevTools 的 Tracker → Network → 任意请求中查找 `X-Org-Id` 这个头部信息。
- **对于云端的 Yandex Tracker**，需要将脚本中的 `X-Org-Id` 替换为 `X-Cloud-Org-Id`。
- 可以在 Tracker 的用户界面（Settings → Applications → OAuth → Generate new token）中生成 `TOKEN`。
- 所有命令都会通过 `jq` 将结果转换为 JSON 格式，以便于进一步处理。

## 文件结构

```
skills/yandex-tracker-cli/
├── yandex-tracker        # Исполняемый скрипт
├── SKILL.md              # Эта документация
└── ~/.yandex-tracker-env # (опционально, не в репо) Конфиг с TOKEN и ORG_ID
```

## 限制

- 不支持分页（仅显示前 100 条记录）
- 不提供高级搜索功能（可以通过扩展 `issues-find` 命令来实现）
- 对参数的验证较为简单

## 许可证

MIT 许可证