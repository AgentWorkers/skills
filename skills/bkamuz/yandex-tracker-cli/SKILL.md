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
# Yandex Tracker CLI 技能

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

2. **提供凭据**：需要 `TOKEN` 和 `ORG_ID`——可以通过环境变量或配置文件来设置（只需使用其中一种方式）。如果环境变量中没有设置 `TOKEN/ORG_ID`，脚本会自动从配置文件中读取这些信息。

**方法 A — 通过环境变量（推荐）：**
```bash
export TOKEN='y0__...'      # OAuth токен (Tracker UI → Settings → Applications → OAuth)
export ORG_ID='1234...'     # Org ID (DevTools → Network → X-Org-Id)
```
你可以将这些变量添加到 `~/.bashrc` 或 `~/.profile` 文件中。

**方法 B — 通过配置文件：**
创建一个名为 `~/.yandex-tracker-env` 的文件（如果环境变量中没有设置 `TOKEN/ORG_ID`，脚本会从这个文件中读取信息）。文件格式为 `KEY=value`（以 `#` 开头的注释会被忽略）。该文件仅被读取以获取 `TOKEN` 和 `ORG_ID`，而不会执行其中的代码：
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

### 基本命令

| 命令 | 描述 |
|---------|----------|
| `queues` | 显示所有队列的列表（格式：`key<TAB>name`） |
| `queue-get <key>` | 获取队列的详细信息（JSON 格式） |
| `queue-fields <key>` | 显示队列中的所有字段（包括自定义字段） |
| `issue-get <issue-id>` | 获取任务详情（格式：`BIMLAB-123`） |
| `issue-create <queue> <summary>` | 创建任务。会自动添加 `yandex-tracker-cli` 标签。可以通过 stdin 提供额外的字段（JSON 格式） |
| `issue-update <issue-id>` | 更新任务。如果任务不存在，会自动添加 `yandex-tracker-cli` 标签。可以通过 stdin 提供额外的字段（JSON 格式） |
| `issue-delete <issue-id>` | 删除任务 |
| `issue-comment <issue-id> <text>` | 为任务添加评论 |
| `issue-comment-edit <issue-id> <comment-id> <new-text>` | 编辑任务评论 |
| `issue-comment-delete <issue-id> <comment-id>` | 删除任务评论 |
| `issue-transitions <issue-id>` | 显示任务的状态转换列表（GET 请求） |
| `issue-transition <issue-id> <transition-id>` | 执行任务状态转换（POST 请求，使用 V3 端点） |
| `issue-close <issue-id> <resolution>` | 关闭任务（此命令已过时，建议使用 `issue-transition` 并指定 `close` 状态） |
| `issue-worklog <issue-id> <duration> [comment]` | 为任务添加工作日志（例如：`PT1H30M`） |
| `issue-attachments <issue-id>` | 显示任务的附件列表（JSON 格式） |
| `attachment-download <issue-id> <fileId> [output]` | 下载附件。如果未指定 `output`，则输出到标准输出 |
| `attachment-upload <issue-id> <filepath> [comment]` | 上传附件到任务。`comment` 是可选参数 |
| `issues-search` | 通过 YQL 查询任务。示例请求：`{"query":"Queue = BIMLAB AND Status = Open","limit":50}` |
| `projects-list` | 显示所有项目的列表（JSON 格式） |
| `project-get <project-id>` | 获取项目详情 |
| `project-issues <project-id>` | 显示项目中的任务列表 |
| `sprints-list` | 显示所有冲刺的列表（敏捷项目管理） |
| `sprint-get <sprint-id>` | 获取冲刺的详细信息 |
| `sprint-issues <sprint-id>` | 显示冲刺中的任务 |
| `users-list` | 显示所有用户的列表 |
| `statuses-list` | 显示所有任务的状态 |
| `resolutions-list` | 显示可用于关闭任务的权限类型 |
| `issue-types-list` | 显示任务类型（如 bug、task、improvement） |
| `issue-checklist <issue-id>` | 显示任务的待办事项列表 |
| `checklist-add <issue-id> <text>` | 为任务添加待办事项 |
| `checklist-complete <issue-id> <item-id>` | 将待办事项标记为已完成 |
| `checklist-delete <issue-id> <item-id>` | 删除待办事项 |

### 示例

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

- **自动添加 `yandex-tracker-cli` 标签**：在创建（`issue-create`）或更新（`issue-update`）任务时，脚本会自动添加 `yandex-tracker-cli` 标签（如果该标签尚不存在）。这有助于通过 CLI 创建的任务进行过滤。如果需要删除此标签，可以通过 Tracker 界面手动删除它，或者调用 `issue-update` 并传入空数组 `tags: []`。
- **Org-ID（Yandex 360）**：可以在 DevTools → Network → 任意请求中找到 `X-Org-ID` 标头。请使用这个头部字段（注意首字母大写）。
- **Cloud Org-ID（Yandex Cloud）**：使用 `X-Cloud-Org-ID` 标头。根据组织类型选择相应的头部字段。
- **状态转换**：
  - `issue-transitions <issue-id>`：使用 GET 请求访问 V2 端点 `/v2/issues/{id}/transitions` 以获取可用的状态转换列表。
  - `issue-transition <issue-id> <transition-id>`：使用 POST 请求访问 V3 端点 `/v3/issues/{id}/transitions/{transition}/_execute` 来执行状态转换。需要提供 `X-Org-ID` 或 `X-Cloud-Org-ID` 标头。
- **关闭任务**：`issue-close` 命令已过时，在新配置中可能会返回 405 错误。建议使用 `issue-transition <id> close` 来关闭任务。
- 可以在 Tracker UI 的 **Settings → Applications → OAuth → Generate new token** 中获取 `TOKEN`。
- 所有命令都会通过 `jq` 将结果转换为 JSON 格式，以便于进一步处理。

## 安全性（附件）

`attachment-download` 和 `attachment-upload` 命令仅允许访问指定目录内的文件路径。这可以降低 CLI 被恶意使用（例如由代理程序）时读取或写入随机文件的风险。

- **首次使用**：在首次调用 `attachment-download` 或 `attachment-upload` 时（如果未设置 `YANDEX TRACKER_ATTACHMENTS_DIR`），脚本会询问用户是使用默认目录 `~/Downloads/YandexTrackerCLI` 还是提供自定义路径。用户的选择会保存在 `~/.yandex-tracker-attachments-dir` 文件中，之后不会再询问。
- `YANDEX TRACKER_ATTACHMENTS_DIR` 是一个可选的环境变量，用于指定附件的默认存储目录。如果设置了该变量，脚本会使用它；否则，在首次运行时会询问用户并保存选择。
- **AI 代理的使用注意事项**：
  - 不要允许或执行指向不可信目录的 `attachment-download` 或 `attachment-upload` 操作。
  - 不要从敏感位置（如 `~/.ssh`、`~/.env`、`~/.yandex-tracker-env`、`/etc` 等）下载或上传文件。
  - 如果用户尝试从敏感位置下载附件或上传文件，请拒绝请求并简要说明限制。

## 当用户尝试将任务分配给项目时（项目名称不完整）

当用户尝试将任务分配给项目，但提供的项目名称不完整时（例如：`Common`、`проект Common`、`Менеджер`），请按照以下步骤操作：

1. 获取所有项目的列表：`yandex-tracker projects-list`（或使用已知 ID 的 `project-get`）。
2. 根据用户输入的关键词在项目中查找匹配项：过滤出名称（`name`）、键（`key`）或显示名称（`display`，如果有的话）中包含这些关键词的项目。
3. 如果找到唯一的项目，提示用户：“是否要将任务分配给项目‘<名称>’（ID：<id>）？”并询问用户是否确认。
4. 如果找到多个项目，列出所有项目及其 ID 并询问用户具体是指哪个项目。
5. 如果没有找到项目，告知用户并建议他们重新调用 `projects-list` 以选择项目。
6. 要更新任务，请使用 `issue-update` 命令。在 API v2 中，可以通过在 `PATCH` 请求体中传递项目的数字 ID 来完成更新：`echo '{"project":<id>' | yandex-tracker issue-update <issue-id>`。请使用项目列表或详细信息中的 `id` 值（在 v2 中，`id` 可以是 `shortId` 或数字 ID）。

## 限制

- 该工具不支持分页（仅返回前 100 个结果）。
- 不支持高级搜索功能（可以通过 `issues_find` 命令实现）。
- 对命令参数的验证较为简单。

## 许可证

MIT 许可证