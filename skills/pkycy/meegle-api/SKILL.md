---
name: meegle-api
description: Meegle Open API 技能索引。请先阅读相关认证信息；如果缺少认证凭据，请参阅 `meegle-api-credentials` 文件，并提示用户从何处获取这些凭据。
metadata: {"openclaw":{"requires":{"env":["MEEGLE_PLUGIN_ID","MEEGLE_PLUGIN_SECRET","MEEGLE_DOMAIN","MEEGLE_PROJECT_KEY","MEEGLE_USER_KEY"]}}}
---
# Meegle API（索引）

请先阅读 **meegle-api-credentials** 文件（其中包含域名、令牌、上下文信息以及请求头信息），然后再选择与您的任务相匹配的技能文档。可以使用 `read-file` 命令来读取相应的技能文档；`{baseDir}` 表示技能文档包的根目录。

| 序号 | 文件路径 | 读取时机 |
|-------|------|--------------|
| 1 | **{baseDir}/meegle-api-credentials/SKILL.md** | 域名、令牌、上下文信息、请求头信息 — 在进行任何 Meegle API 调用之前 |
| 2 | **{baseDir}/meegle-api-users/SKILL.md** | 用户相关 API（如用户组、用户信息等） |
| 3 | **{baseDir}/meegle-api-space/SKILL.md** | 项目空间相关操作 |
| 4 | **{baseDir}/meegle-api-work-items/SKILL.md** | 工作项的创建、读取、更新、删除（CRUD）操作以及列表、搜索功能 |
| 5 | **{baseDir}/meegle-api-setting/SKILL.md** | 设置相关功能（如设置类型、字段、处理流程等） |
| 6 | **{baseDir}/meegle-api-comments/SKILL.md** | 工作项的评论功能 |
| 7 | **{baseDir}/meegle-api-views-measurement/SKILL.md** | 数据视图相关功能（如看板、甘特图、图表等） |