---
name: searxng
description: >
  这是一个用于 OpenClaw 代理的自托管网页搜索聚合器。您可以使用此技能来：  
  (1) 在虚拟私有服务器（VPS）或服务器上安装 SearXNG，以便代理无需 API 密钥即可进行网页搜索；  
  (2) 使用现有的本地 SearXNG 实例来执行网页搜索。  
  文档内容包括安装步骤、配置方法、search.py 命令行工具（CLI）的使用说明，以及故障排查时的应对策略。  
  当代理需要网页搜索功能、在设置新的 OpenClaw 实例时，或诊断搜索故障时，都可以参考本文档。
---
# SearXNG

SearXNG 是一个自托管的搜索聚合器，可以同时查询 Google、Bing、Brave、Startpage、DuckDuckGo 和 Wikipedia 的搜索结果。无需使用 API 密钥。搜索结果以 JSON 格式返回。

## 快速入门（已安装）

```bash
python3 scripts/search.py "your query"             # human-readable
python3 scripts/search.py "your query" --json      # JSON (for parsing)
python3 scripts/search.py "query" --count 5 --json # limit + JSON
```

将 `search.py` 文件放置在方便访问的位置——通常建议将其放在工作区的 `tools` 目录下，例如 `tools/search.py`。

有关详细的使用方法和服务管理信息，请参阅 `references/usage.md`。

## 安装（新实例）

在 Ubuntu 22.04/24.04 上以 root 用户身份运行以下命令：

```bash
bash scripts/install_searxng.sh
```

此命令会安装 SearXNG，创建一个名为 `searxng` 的系统用户，生成 `/etc/searxng/settings.yml` 配置文件，并在 `http://127.0.0.1:8888` 端口上启动一个 systemd 服务。

验证安装是否成功：

```bash
curl 'http://127.0.0.1:8888/search?q=test&format=json' | python3 -m json.tool | head -20
systemctl status searxng
```

## 将 `search.py` 与服务器连接

`search.py` 默认会连接到 `http://127.0.0.1:8888`。如果端口地址不同，请更新脚本顶部的 `SEARXNG_URL` 变量。

## 备用方案

当 SearXNG 无法正常工作时，`search.py` 会自动切换到使用 Wikipedia 和 GitHub 的 API 进行搜索。此时无需进行任何操作，搜索结果仍然会返回，只是来源会减少。

## 故障排除

| 故障现象 | 解决方法 |
|---------|-----|
| 在标准错误输出（stderr）中显示 “[SearXNG unavailable]” | 使用 `systemctl restart searxng` 重启服务 |
| 端口 8888 被占用 | 修改 `/etc/searxng/settings.yml` 文件中的 `port:` 配置值，并更新脚本中的 `SEARXNG_URL` |
| 所有搜索引擎均返回空结果 | 检查 `/etc/searxng/settings.yml` 文件中的搜索引擎配置，然后重启服务 |
| 连接失败 | 服务未运行——使用 `systemctl start searxng` 启动服务 |