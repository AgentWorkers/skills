# 工作区技能条目

该文件为尝试从工作区根目录读取 `SKILL.md` 的代理程序提供了一个稳定的入口点。

## 技能的实际存储位置

- 根目录索引：`skills/README.md`
- Calibre 仅读模式：`skills/calibre-catalog-read/SKILL.md`
- Calibre 元数据编辑：`skills/calibre-metadata-apply/SKILL.md`

## Calibre 路由规则（硬性规定）

- 读取/搜索/列出/获取 ID 的操作 -> `calibre-catalog-read`
- 元数据编辑/修复/更新（标题/作者/系列/系列索引/标签/出版商/发布日期/语言）的操作 -> `calibre-metadata-apply`
- 绝不要通过聊天流程启动 `calibre-server`。请连接到已运行的 Content 服务器。