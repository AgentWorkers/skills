# Gork Legacy Skill  
在 OpenClaw 中实现 “Gork” 助手的功能。  

## 功能  
- **任务管理**：从笔记和 Slack 中自动提取任务信息（由 AI 支持）。  
- **每日笔记自动化**：自动处理未完成的任务，并生成相应的模板。  
- **同步集成**：  
  - **Slack**：将私信和提及内容同步到本地数据库。  
  - **Strava**：同步用户的健身活动数据和心率区间数据。  
  - **Harvest**：启动/停止计时器，并统计可计费的工时。  

## 配置（见 `TOOLS.md` 文件）  
请将以下配置添加到您的 `TOOLS.md` 文件中：  
```markdown
### Gork Skill
- SLACK_USER_TOKEN: xoxp-...
- STRAVA_CLIENT_ID: ...
- STRAVA_CLIENT_SECRET: ...
- STRAVA_REFRESH_TOKEN: ...
- HARVEST_ACCESS_TOKEN: ...
- HARVEST_ACCOUNT_ID: ...
- OBSIDIAN_VAULT_PATH: /home/adam/.openclaw/workspace/vault
```  

## 数据库架构（SQL）  
该技能使用一个名为 `gork.db` 的本地 SQLite 数据库，其中包含以下表格：  
- `tasks`：用于存储任务的中央数据库。  
- `strava_activities`：记录用户的健身活动数据。  
- `note_processing_log`：记录数据库变更的审计日志。  

## 逻辑实现  
### 任务处理  
OpenClaw 代理不通过 shell 脚本直接修改文件，而是使用 `read` 和 `write` 工具来执行以下操作：  
1. 查找前一天的每日笔记。  
2. 提取包含 `[- [ ]` 标签的行，并将其添加到当天的笔记中的 “Overdue”（逾期）部分。  

### 同步逻辑  
- **Slack**：通过 `web_fetch` 或专门的 Python 脚本定期从 Slack 获取数据。  
- **Strava/Harvest**：通过 REST API 获取数据并更新本地数据库。  

## 文件冲突解决机制  
为避免 Obsidian 数据库同步时产生的冲突：  
1. **原子性写入**：在写入文件之前，始终先读取当前文件的内容。  
2. **临时缓冲区**：用户的数据会先写入到一个临时缓冲区；只有当处理成功并提交后，这些数据才会被写入数据库。  
3. **外部数据库备份**：任务数据会同步到 SQLite 数据库中，以确保在同步失败时数据不会丢失。