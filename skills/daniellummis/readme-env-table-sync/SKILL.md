---
name: readme-env-table-sync
description: 使用 marker 块从 `.env.example` 文件生成并同步一个 README 文件中的环境变量表，并实现持续集成（CI）过程中的漂移检测功能。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# README 环境变量文档同步

使用此技能可确保 README 文件中的环境变量文档与实际的 `.env.example` 文件保持一致。

## 功能说明
- 从 `.env.example` 文件（或其他环境变量模板文件）中解析环境变量键值对
- 生成一个包含键值对的 Markdown 表格
- 通过将生成的表格与 README 文件中的标记块进行比较来检测文档是否发生变动
- 可选地直接将更新内容应用到 README 文件中

## 输入参数
可选参数：
- `ENV_FILE`（默认值：`.env.example`）
- `README_FILE`（默认值：`README.md`）
- `SYNC_MODE`（`report` 或 `apply`，默认值：`report`）
- `TABLE_START-marker`（默认值：`<!-- ENV_TABLE_START -->`）
- `TABLE_END-marker`（默认值：`<!-- ENV_TABLE_END -->`）

## 使用方法
- **生成报告**：
  ```bash
ENV_FILE=.env.example \
README_FILE=README.md \
bash skills/readme-env-table-sync/scripts/sync-readme-env-table.sh
```

- **应用更新**：
  ```bash
ENV_FILE=.env.example \
README_FILE=README.md \
SYNC_MODE=apply \
bash skills/readme-env-table-sync/scripts/sync-readme-env-table.sh
```

- **针对包含的测试用例运行同步操作**：
  ```bash
ENV_FILE=skills/readme-env-table-sync/fixtures/.env.sample \
README_FILE=skills/readme-env-table-sync/fixtures/README.sample.md \
SYNC_MODE=apply \
bash skills/readme-env-table-sync/scripts/sync-readme-env-table.sh
```

## 输出结果
- 如果表格已同步或更新已应用，程序退出状态码 `0`
- 如果输入无效、缺少标记、解析错误或在报告模式下检测到文档变动，程序退出状态码 `1`
- 程序会输出包含键值对数量和操作模式的简要总结