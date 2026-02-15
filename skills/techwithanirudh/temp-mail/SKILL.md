---
name: temp-mail
description: 这是一个由 Vortex (vortex.email) 提供的临时电子邮件辅助工具。当需要在注册流程中使用一次性邮箱地址时，可以借助该工具来创建一个邮箱（包含随机的本地部分域名），定期检查是否有新邮件，并在收到邮件后及时清理这些邮箱。
homepage: https://vortex.skyfall.dev
metadata: {"clawdis":{"emoji":"✉️","requires":{"bins":["curl"]}}}
---

# temp-mail 技能

该技能提供了一个 Python 命令行接口（CLI）脚本，用于与托管的 Vortex API 进行交互（支持 GET /emails/{email} 和 DELETE /emails/{email}/clear 请求）。

**使用示例**（脚本位于 `scripts/` 目录下）：
- `create`：为指定的域名生成一个随机的 `localpart`（邮件地址的一部分），并打印出完整的邮件地址。
- `fetch`：查询 Vortex HTTP API，列出该地址下的所有邮件。
- `poll`：等待新邮件到达，或达到超时时间。
- `clear`：删除该地址下的所有邮件。

**运行方式**：使用 `uv` 命令运行脚本：`uv run {baseDir}/scripts/temp_mail.py`（脚本包含 shebang 语句和元数据头，与 `hn` 技能类似）。

**示例代码**（请参考 ````bash
# generate a random address
uv run {baseDir}/scripts/temp_mail.py create

# fetch messages for an address
uv run {baseDir}/scripts/temp_mail.py fetch alice@dash.dino.icu

# poll until messages arrive (timeout 60s)
uv run {baseDir}/scripts/temp_mail.py poll alice@dash.dino.icu --timeout 60

# clear mailbox
uv run {baseDir}/scripts/temp_mail.py clear alice@dash.dino.icu
````）：

**默认配置**：
- `VORTEX_URL`：`https://vtx-api.skyfall.dev`
- `default_domain`：`skyfall.dev`（可通过 `VORTEX_DOMAIN` 环境变量进行覆盖）

**安装说明**（请参考 ````bash
# create a venv and install deps (unix)
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r scripts/requirements.txt

# or using uv which creates an ephemeral venv for you, e.g.
uv run {baseDir}/scripts/temp_mail.py create
````）：

**注意事项**：
- 脚本使用 `httpx` 库进行网络请求；`rich` 库是可选的，因此在依赖项中未包含。
- 随机用户名的生成方式与前端系统的行为一致（仅包含小写字母和数字）。
- 托管实例支持多个域名（例如 `dash.dino.icu`、`skyfall.dev` 等）。在创建邮件地址时，可以从这些域名中选择一个，或者让脚本使用默认域名。