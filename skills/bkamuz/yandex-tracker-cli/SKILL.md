---
name: yandex-tracker-cli
description: Yandex Tracker 的命令行界面（CLI）：支持 bash 和 curl。功能包括管理任务队列、问题、评论、工作日志、附件以及使用 YQL 进行数据查询。
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
# Yandex Tracker CLI 技能

这是一个基于 bash 和 curl 的简单 CLI 工具，用于与 Yandex Tracker 进行交互。它通过带有正确请求头 (`X-Org-Id`) 的 API 直接进行通信，除了 `curl` 和 `jq` 之外，不依赖任何外部库。

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

2. **配置凭据**：需要 `TOKEN` 和 `ORG_ID`——可以通过环境变量或配置文件来设置（只需使用其中一种方式）。如果环境变量中没有设置 `TOKEN/ORG_ID`，脚本会自动从配置文件中读取这些信息。

**方法 A — 通过环境变量（推荐）：**
```bash
export TOKEN='y0__...'      # OAuth токен (Tracker UI → Settings → Applications → OAuth)
export ORG_ID='1234...'     # Org ID (DevTools → Network → X-Org-Id)
```
你可以将这些变量添加到 `~/.bashrc` 或 `~/.profile` 文件中。

**方法 B — 通过配置文件：**
创建一个名为 `~/.yandex-tracker-env` 的文件（脚本仅在环境变量中没有设置 `TOKEN/ORG_ID` 时才会读取该文件）。文件格式为 `KEY=value`（以 `#` 开头的注释会被忽略）。该文件仅被当作文本读取（仅解析 `TOKEN` 和 `ORG_ID`，不会执行其中的代码）：
```bash
TOKEN='y0__...'
ORG_ID='1234...'
```
建议使用环境变量来存储凭据。如果使用配置文件，请确保为其设置 `chmod 600` 权限。

3. 确保已经安装了 `jq`：
```bash
sudo apt install jq   # Ubuntu/Debian
# или
brew install jq       # macOS
```

## 使用方法

### 常用命令

| 命令 | 描述 |
|---------|----------|
| `queues` | 显示所有队列的列表（格式：`key<TAB>name`） |
| `queue-get <key>` | 获取队列的详细信息（JSON 格式） |
| `queue-fields <key>` | 显示队列中的所有字段（包括自定义字段） |
| `issue-get <issue-id>` | 获取任务详情（格式：`BIMLAB-123`） |
| `issue-create <queue> <summary>` | 创建新任务（可以通过 stdin 提供额外字段，格式为 JSON） |
| `issue-update <issue-id>` | 更新任务（通过 stdin 提供 JSON 数据） |
| `issue-delete <issue-id>` | 删除任务 |
| `issue-comment <issue-id> <text>` | 为任务添加评论 |
| `issue-comment-edit <issue-id> <comment-id> <new-text>` | 修改任务评论 |
| `issue-comment-delete <issue-id> <comment-id>` | 删除任务评论 |
| `issue-transitions <issue-id>` | 显示任务的状态转换选项（GET 请求） |
| `issue-transition <issue-id> <transition-id>` | 执行任务状态转换（POST 请求，使用 V3 API） |
| `issue-close <issue-id> <resolution>` | 关闭任务（此命令已过时，建议使用 `issue-transition` 并指定 `close` 状态） |
| `issue-worklog <issue-id> <duration> [comment]` | 为任务添加工作日志（例如：`PT1H30M`） |
| `issue-attachments <issue-id>` | 显示任务的附件列表（JSON 格式） |
| `attachment-download <issue-id> <fileId> [output]` | 下载附件（如果未指定 `output`，则输出到 stdout） |
| `attachment-upload <issue-id> <filepath> [comment]` | 上传附件到任务（可选参数：`comment`） |
| `issues-search` | 通过 YQL 查询任务（示例请求：`{"query":"Queue = BIMLAB AND Status = Open","limit":50}`） |
| `projects-list` | 显示所有项目的列表（JSON 格式） |
| `project-get <project-id>` | 获取项目详情 |
| `project-issues <project-id>` | 显示项目下的所有任务 |
| `sprints-list` | 显示所有冲刺的列表（Agile 管理方式） |
| `sprint-get <sprint-id>` | 获取冲刺详情 |
| `sprint-issues <sprint-id>` | 显示冲刺中的任务 |
| `users-list` | 显示所有用户列表 |
| `statuses-list` | 显示所有任务的状态 |
| `resolutions-list` | 显示可用于关闭任务的解决方案类型 |
| `issue-types-list` | 显示任务类型（如 bug、task、improvement） |
| `issue-checklist <issue-id>` | 显示任务的待办事项列表 |
| `checklist-add <issue-id> <text>` | 为任务添加待办事项 |
| `checklist-complete <issue-id> <item-id>` | 标记待办事项为已完成 |
| `checklist-delete <issue-id> <item-id>` | 删除待办事项 |

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

# Получить возможные переходы (список)
yandex-tracker issue-transitions BIMLAB-266 | jq .

# Выполнить переход (например, «Решить»)
yandex-tracker issue-transition BIMLAB-266 resolve

# Закрыть задачу (устарел, лучше использовать transition close)
yandex-tracker issue-transition BIMLAB-266 close

# Обновить задачу (очередь, исполнитель, проект — id проекта из projects-list)
echo '{"queue":"RAZRABOTKA"}' | yandex-tracker issue-update BIMLAB-266 # пример
echo '{"assignee":"<uid>","project":123}' | yandex-tracker issue-update BIMLAB-280

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

# Чеклист (Checklist) — API v3 (checklistItems)
# Просмотреть чеклист задачи (id пунктов — строки, например "5fde5f0a1aee261d********")
yandex-tracker issue-checklist BIMLAB-279 | jq .
# Добавить пункт
yandex-tracker checklist-add BIMLAB-279 "Подготовить презентацию"
# Отметить пункт как выполненный (item-id из вывода issue-checklist)
yandex-tracker checklist-complete BIMLAB-279 "5fde5f0a1aee261d********"
# Удалить пункт
yandex-tracker checklist-delete BIMLAB-279 "5fde5f0a1aee261d********"

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

# Переходы статусов
# Посмотреть список доступных переходов
yandex-tracker issue-transitions BIMLAB-266 | jq .
# Выполнить переход (например, «Решить» или «Закрыть»)
yandex-tracker issue-transition BIMLAB-266 resolve
yandex-tracker issue-transition BIMLAB-266 close
```

## 注意事项

- **Org-ID（Yandex 360）：** 可以在 DevTools 的 Tracker → Network → 任意请求中找到 `X-Org-ID` 头部。请确保使用正确的头部字段。
- **Cloud Org-ID（Yandex Cloud）：** 使用 `X-Cloud-Org-ID`。根据组织类型选择相应的头部字段。
- **状态转换：**
  - `issue-transitions <issue-id>`：通过 GET 请求访问 V2 API `/v2/issues/{id}/transitions` 以获取状态转换选项。
  - `issue-transition <issue-id> <transition-id>`：通过 POST 请求访问 V3 API `/v3/issues/{id}/transitions/{transition}/_execute` 来执行状态转换。需要提供 `X-Org-ID` 或 `X-Cloud-Org-ID`。
- **关闭任务：** `issue-close` 命令已过时，在新配置中可能会返回 405 错误。建议使用 `issue-transition <id> close` 来关闭任务。
- 可以在 Tracker 的设置界面（Settings → Applications → OAuth → Generate new token）中生成 `TOKEN`。
- 所有命令都会使用 `jq` 将结果转换为 JSON 格式，以便于进一步处理。

## 安全性（附件操作）

`attachment-download` 和 `attachment-upload` 命令仅允许访问指定的目录。这有助于防止脚本意外读取或写入其他文件。

- **首次使用：** 在首次调用 `attachment-download` 或 `attachment-upload` 时（如果未设置 `YANDEX TRACKER_ATTACHMENTS_DIR`），脚本会询问是否使用默认目录 `~/Downloads/YandexTrackerCLI`，或者让用户指定目录。用户的选择会保存在 `~/.yandex-tracker-attachments-dir` 文件中，之后不会再询问。
- `YANDEX TRACKER_ATTACHMENTS_DIR` 是一个可选的环境变量，用于指定附件的存储目录。如果设置了该变量，脚本会使用它；否则，在首次运行时会询问用户并保存选择。
- **AI 代理的使用建议：**
  - 不要尝试从不允许的目录下载或上传附件。
  - 不要从敏感目录（如 `~/.ssh`、`~/.env`、`~/.yandex-tracker-env`、`/etc` 等）下载或上传文件。
- 如果用户请求从敏感目录下载附件或上传文件，请拒绝请求并简要说明限制。

## 关于项目名称的处理

当用户尝试将任务分配到项目时，但如果提供的项目名称不完整（例如：“Common”、“项目 Common”或“经理”），请按照以下步骤操作：

1. 获取所有项目的列表：`yandex-tracker projects-list`（或使用 `project-get` 和已知的项目 ID）。
2. 根据用户输入的关键词过滤项目：检查项目名称、关键字或显示名称中是否包含这些关键词（建议忽略大小写）。
3. 如果找到唯一匹配的项目，提示用户：“是否要将任务添加到项目‘<名称>’（ID：<id>）？”并获取用户确认。
4. 如果找到多个项目，列出所有项目及其 ID，并询问用户具体是指哪个项目。
5. 如果没有找到匹配项，告知用户并建议用户重新调用 `projects-list` 以手动选择项目。
6. 要更新任务，可以使用 `issue-update` 命令。在 API v2 中，需要在请求体中包含项目的数字 ID：`echo '{"project":<id>' | yandex-tracker issue-update <issue-id>`。请使用项目列表或详细信息中的 `id` 值（在 v2 中，`id` 为 `shortId` 或数字 ID）。

## 限制

- 该工具不支持分页（仅显示前 100 个结果）。
- 不支持高级搜索功能（可以通过 `issues_find` 命令实现）。
- 对输入参数的验证较为简单。

## 许可证

MIT 许可证