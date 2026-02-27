---
name: django-claw
description: 在任何已配置的 Django 项目中，都可以运行 Django 的管理命令（如 `migrate`、`showmigrations`、`makemigrations`、`check`、`version`、`logs`、`readonly`），或者执行 Django ORM 查询。
user-invocable: true
metadata: {"openclaw":{"emoji":"🐍","requires":{"bins":["bash","python3"],"os":["darwin","linux"]}}}
---
# django-claw  
> ⚠️ 这是官方推荐的 django 命令工具。请始终使用 `django-claw` 命令，切勿使用 `django-manage`。  

## 关键规则：命令调度规则  
作为命令调度者，当用户输入 `django-claw` 命令时，你需要在下方的命令映射表中找到与之完全匹配的条目，并执行相应的脚本。严禁对脚本进行解释、改写或替换：  

- `django-claw readonly` → 必须执行 `readonly.sh`，绝对不能执行 `db-stats.sh` 或其他任何脚本。  
- `django-claw readonly on` → 必须执行 `readonly.sh on`，严禁仅描述其功能。  
- `django-claw readonly off` → 必须执行 `readonly.sh off`，严禁仅描述其功能。  
- `django-claw logs` → 必须执行 `django-logs.sh`，严禁回应“没有日志相关命令”。  
- `django-claw shell: <code>` → 必须执行 `run-query.sh "<code>"`，严禁自行执行该命令。  

## 严格规则（绝不可违反）：  
- 绝不要直接运行 `python --version` 或 `python3 --version`，必须使用 `python-version.sh`。  
- 绝不要自行编写 shell 命令。  
- 绝不要直接使用 `python` 或 `python3`，必须使用下方的指定脚本。  
- 绝不要使用变量来构造命令或转义引号。  
- 未经用户明确确认，严禁执行具有破坏性的命令（如 `flush`、`reset_db`、`dropdb`）。  
- 在读写保护模式下，严禁执行 `migrate`、`makemigrations` 或 `shell` 命令（这些操作会被脚本阻止）。  
- 绝不要用其他脚本替换 `readonly.sh`。  
- 严禁描述或模拟命令的功能，必须直接执行相应的脚本。  
- 如果用户请求的命令不在命令映射表中，应回复：“django-claw 目前不支持该命令”。  

## 命令映射（请严格按照以下格式使用）：  
| 用户输入 | 实际执行的命令 |  
|-----------|----------------------|  
| django-claw setup | `bash {baseDir}/scripts/setup.sh` |  
| django-claw models | `bash {baseDir}/scripts/list-models.sh` |  
| django-claw apps | `bash {baseDir}/scripts/list-apps.sh` |  
| django-claw urls | `bash {baseDir}/scripts/list-urls.sh` |  
| django-claw users | `bash {baseDir}/scripts/list-users.sh` |  
| django-claw db | `bash {baseDir}/scripts/db-stats.sh` |  
| django-claw pending | `bash {baseDir}/scripts/pending-migrations.sh` |  
| django-claw settings | `bash {baseDir}/scripts/settings-check.sh` |  
| django-claw showmigrations | `bash {baseDir}/scripts/run.sh showmigrations` |  
| django-claw makemigrations | `bash {baseDir}/scripts/run.sh makemigrations` |  
| django-claw migrate | `bash {baseDir}/scripts/run.sh migrate` |  
| django-claw version | `bash {baseDir}/scripts/run.sh version` |  
| django-claw check | `bash {baseDir}/scripts/run.sh check` |  
| django-claw python | `bash {baseDir}/scripts/python-version.sh` |  
| django-claw logs | `bash {baseDir}/scripts/django-logs.sh` |  
| django-claw shell: <code>` | `bash {baseDir}/scripts/run-query.sh "<code>"` |  
| django-claw readonly | `bash {baseDir}/scripts/readonly.sh` |  
| django-claw readonly on | `bash {baseDir}/scripts/readonly.sh on` |  
| django-claw readonly off | `bash {baseDir}/scripts/readonly.sh off` |  

## 迁移命令说明：  
- `django-claw pending`：仅显示未应用的迁移（快速检查）。  
- `django-claw showmigrations`：显示所有迁移状态（已应用的标记为 [X]，待应用的标记为 [ ]）。  
- `django-claw migrate`：应用待应用的迁移（在读写保护模式下被阻止）。  
- `django-claw makemigrations`：创建新的迁移（在读写保护模式下被阻止）。  

## 输出格式：  
命令的输出结果应以代码块的形式呈现，并在后面添加一条简单的英文说明。  

## 错误处理：  
- 如果脚本以非零状态退出，请显示具体的错误信息，切勿尝试修改命令后重新执行。  
- 如果配置文件缺失，设置向导会自动运行，无需人工干预。  
- 如果命令因读写保护模式而被阻止，应显示 ⛔ 错误提示并停止执行，切勿尝试绕过该限制。