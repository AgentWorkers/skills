---
name: karakeep
description: 在 Karakeep 实例中管理书签和链接。当用户想要保存链接、查看最近的书签或搜索其收藏夹时，可以使用此功能。该功能会在用户输入类似 “保存这个链接”、“保存到 Karakeep” 或 “搜索我的书签” 等指令时被触发。
metadata: {"clawdbot":{"emoji":"📦","requires":{"bins":["uv"]}}}
---

# Karakeep 技能

在 Karakeep 实例中保存和搜索书签。

## 设置

首先，配置您的实例 URL 和 API 密钥：
```bash
uv run --with requests skills/karakeep/scripts/karakeep-cli.py login --url <instance_url> <api_key>
```

## 命令

### 保存链接
将一个 URL 添加到您的收藏夹中：
```bash
uv run --with requests skills/karakeep/scripts/karakeep-cli.py add <url>
```

### 列出书签
显示最新的书签：
```bash
uv run --with requests skills/karakeep/scripts/karakeep-cli.py list --limit 10
```

### 搜索书签
查找符合查询条件的书签。支持复杂语法，例如 `is:fav`、`title:word`、`#tag`、`after:YYYY-MM-DD` 等：
```bash
uv run --with requests skills/karakeep/scripts/karakeep-cli.py list --search "title:react is:fav"
```

## 故障排除
- 确保 `KARAKEEP_API_KEY`（或 `HOARDER_API_KEY`）已设置，或者运行 `login` 命令进行登录。
- 验证脚本或配置文件（`~/.config/karakeep/config.json`）中的实例 URL 是否正确。