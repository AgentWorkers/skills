---
name: apple-photos
description: macOS上的Apple Photos.app集成功能：可以列出相册、浏览照片、按日期/人物/内容进行搜索以及导出照片。
metadata: {"clawdbot":{"emoji":"📷","os":["darwin"]}}
---

# Apple Photos

可以通过 SQLite 查询来访问 Photos.app。脚本的执行路径为：`cd {baseDir}`

## 使用要求
- 终端需要具有完整的磁盘访问权限（系统设置 → 隐私 → 完整磁盘访问）

## 命令

| 命令 | 用法 |
|---------|-------|
| 获取库统计信息 | `scripts/photos-count.sh` |
| 列出相册 | `scripts/photos-list-albums.sh` |
| 查看最近的照片 | `scripts/photos-recent.sh [count]` |
| 列出人物信息 | `scripts/photos-list-people.sh` |
| 按人物名称搜索照片 | `scripts/photos-search-person.sh <name> [limit]` |
| 按照片内容搜索 | `scripts/photos-search-content.sh <query> [limit]` |
| 按日期搜索照片 | `scripts/photos-search-date.sh <start> [end] [limit]` |
| 查看照片详情 | `scripts/photos-info.sh <uuid>` |
| 导出照片 | `scripts/photos-export.sh <uuid> [output_path]` |

## 输出格式

- 最近的照片/搜索结果：`文件名 | 日期 | 类型 | UUID`
- 人物信息：`ID | 名称 | 照片数量`
- 默认导出路径：`/tmp/photo_export.jpg`

## 工作流程：
1. 查看最近的照片：`scripts/photos-recent.sh 1`
2. 导出照片：`scripts/photos-export.sh "UUID"`
3. 在 `/tmp/photo_export.jpg` 中查看导出的照片

## 注意事项：
- 日期格式：`YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM`
- 内容搜索使用机器学习算法，速度较慢（约 5-10 秒），而按日期/人物名称搜索速度较快（约 100 毫秒）
- HEIC 格式的照片在导出时会自动转换为 JPEG 格式
- 名称搜索不区分大小写，支持部分匹配