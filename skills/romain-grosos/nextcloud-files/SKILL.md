---
name: nextcloud
description: "通过 WebDAV 和 OCS API 进行 Nextcloud 文件及文件夹管理。适用场景包括：  
(1) 创建、读取、写入、重命名、移动、复制或删除文件/文件夹；  
(2) 列出或搜索目录内容；  
(3) 设置文件为收藏夹或管理系统标签；  
(4) 查看存储空间使用情况。  
**不适用场景**：  
- Nextcloud 的通话功能（使用 CalDAV）；  
- 日历/联系人管理（使用 CalDAV）；  
- 应用程序管理（需要管理员权限）；  
- 大型二进制文件的传输；  
- 创建共享链接（默认不支持共享功能——详见 README 文件）。"
homepage: https://github.com/rwx-g/openclaw-skill-nextcloud
compatibility: Python 3.9+ · no external dependencies · network access to Nextcloud instance
metadata:
  {
    "openclaw": {
      "emoji": "☁️",
      "requires": { "env": ["NC_URL", "NC_USER", "NC_APP_KEY"] },
      "primaryEnv": "NC_APP_KEY"
    }
  }
ontology:
  reads: [files, folders, user, quota, capabilities]
  writes: [files, folders, tags, favorites]
---
# Nextcloud 技能

该技能提供了完整的 Nextcloud 客户端功能：支持 WebDAV（文件/文件夹操作）和 OCS（标签、用户信息管理）。完全不依赖外部库，仅使用标准库（如 urllib）。

**凭据存储位置：** `~/.openclaw/secrets/nextcloud_creds`  
**配置文件：** `~/.openclaw/config/nextcloud/config.json`

## 触发语句

当用户说出以下命令时，立即执行此技能：
- “将文件上传/保存/写入 Nextcloud”  
- “在 Nextcloud 中创建文件夹”  
- “列出/浏览/显示 [文件夹] 中的内容”  
- “在 Nextcloud 中搜索 [文件]”  
- “从 Nextcloud 读取/下载 [文件]”  
- “重命名/移动/复制 [文件]”  
- “查看我的存储空间使用情况”  
- “为文件添加标签”/“将文件标记为收藏”

## 快速入门

```bash
python3 scripts/nextcloud.py config    # verify credentials + active config
python3 scripts/nextcloud.py quota     # test connection + show storage
python3 scripts/nextcloud.py ls /      # list root directory
```

## 设置

```bash
python3 scripts/setup.py       # interactive: credentials + permissions + connection test
python3 scripts/init.py        # validate all configured permissions against live instance
```

`init.py` 仅在 `allow_write` 和 `allow_delete` 都设置为 `true` 时执行写入/删除操作。如果 `allow_delete` 设置为 `false`，则跳过写入测试，不会生成任何测试结果。

**手动配置：**  
`~/.openclaw/secrets/nextcloud_creds` 文件的权限需设置为 `chmod 600`。  
**应用程序密码：** 通过 Nextcloud 的 “设置” → “安全” → “应用程序密码” 进行设置。

**config.json** 文件中的配置选项：
| 参数 | 默认值 | 功能说明 |
|------|---------|--------|
| `base_path` | `"/"` | 限制代理的访问范围（例如，仅访问 `/Jarvis` 目录） |
| `allow_write` | `false` | 禁止写入、重命名和复制操作（需显式启用） |
| `allow_delete` | `false` | 禁止删除文件和文件夹（需显式启用） |
| `readonly_mode` | `false` | 即使允许写入，也会阻止所有修改操作 |

**安全建议：** 默认情况下，`allow_write` 和 `allow_delete` 都被设置为 `false`。仅在需要时才启用这些选项，并通过 `base_path` 限制代理的访问范围（例如，仅访问 `/Jarvis`）。  
**共享功能** 默认是关闭的。如需启用，请参阅 README 文件中的说明。

## 存储与凭据管理

该技能会读取和写入以下路径中的数据。所有操作都是经过设计并记录在文档中的：
- `~/.openclaw/secrets/nextcloud_creds`：存储 Nextcloud 的凭据（NC_URL、NC_USER、NC_APP_KEY）。该文件的权限设置为 `chmod 600`，且不会被提交到版本控制系统。  
- `~/.openclaw/config/nextcloud/config.json`：包含行为限制配置（如访问路径、写入权限等）。该文件不包含敏感信息，且会在 ClawHub 更新后仍然保留。

**替代方案：** 凭据也可以通过环境变量（`NC_URL`、`NC_USER`、`NC_APP_KEY`）传递给该技能。技能会优先使用环境变量中的值。

**卸载时的清理操作：** 使用 `clawhub uninstall nextcloud-files` 命令可删除该技能的相关文件。若需同时清除凭据和配置信息，请执行相应操作。

## 模块使用方法

```python
from scripts.nextcloud import NextcloudClient
nc = NextcloudClient()
nc.write_file("/Jarvis/notes.md", "# Notes\n...")
nc.mkdir("/Jarvis/Articles")
items = nc.list_dir("/Jarvis")
```

## 命令行接口（CLI）参考

```bash
# Files & folders
python3 scripts/nextcloud.py mkdir /path/folder
python3 scripts/nextcloud.py write /path/file.md --content "# Title"
python3 scripts/nextcloud.py write /path/file.md --file local.md
python3 scripts/nextcloud.py write /path/file.md --content "new entry" --append
python3 scripts/nextcloud.py read  /path/file.md
python3 scripts/nextcloud.py rename /old /new
python3 scripts/nextcloud.py copy   /src /dst
python3 scripts/nextcloud.py delete /path
python3 scripts/nextcloud.py exists /path          # exit 0/1

# Listing & search
python3 scripts/nextcloud.py ls /path --depth 2 --json
python3 scripts/nextcloud.py search "keyword" --path /folder --limit 20

# Favorites & tags
python3 scripts/nextcloud.py favorite /path/file.md
python3 scripts/nextcloud.py tags
python3 scripts/nextcloud.py tag-create "research"
python3 scripts/nextcloud.py tag-assign <file_id> <tag_id>

# Account
python3 scripts/nextcloud.py quota
python3 scripts/nextcloud.py config
```

## 模板示例

- **结构化工作空间设置**  
- **将日志追加到正在运行的日志文件中**  
- **读取并更新 JSON 列表**  
- **文件创建后自动添加标签**  

## 其他扩展方式

- 可通过设置 `base_path`（例如 `/Jarvis`）来限制代理的访问范围，确保其仅能操作指定目录。  
- 可将生成的 Markdown 文件存储在 Nextcloud 中，并在回复中自动提供只读链接。  
- 使用 `append_to_file` 功能记录日志或变更日志。  
- 通过 `write_json` 和 `read_json` 实现会话间的数据持久化。  
- 可根据文件类型（如研究/草稿/已发布）自动为文件添加标签。

## 与其他技能的结合使用示例：

| 技能 | 工作流程 | 说明 |
|-------|----------|--------|
| **ghost** | 发布文章 → 将 Markdown 草稿保存到 Nextcloud → 通过 Ghost 发布文章 |
| **summarize** | 收集 URL 的摘要 → 将摘要保存为 `.md` 文件到 Nextcloud |
| **gmail** | 接收附件 → 将附件保存到 Nextcloud 以供归档 |
| **obsidian** | 将 Obsidian 的笔记同步到 Nextcloud 进行远程备份 |
| **self-improving-agent** | 将代理的学习内容记录到 Nextcloud，以便长期保存和查询 |

## API 参考

有关 WebDAV/OCS 的详细信息、PROPFIND 属性及错误代码，请参阅 `references/api.md`。

## 故障排除

有关常见问题的解决方法，请参阅 `references/troubleshooting.md`。