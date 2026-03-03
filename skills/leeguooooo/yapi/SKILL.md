---
name: yapi
description: 查询并同步 YApi 接口文档。当用户提及“yapi 接口文档”、“YAPI 文档”或请求请求/响应的详细信息时，应使用此功能；同时，当用户粘贴的 YApi URL 与配置的 `base_url` 匹配时，该功能也会被触发。
---
# YApi接口文档

## 命令使用规范

优先使用`yapi`命令。如果`yapi`命令不可用，可以回退到使用`npx`命令（无需全局安装）：

```bash
yapi -h
# fallback:
npx -y @leeguoo/yapi-mcp -h
```

在以下命令示例中，`yapi`可以被替换为`npx -y @leeguoo/yapi-mcp`。

## 快速工作流程
1. 如果用户提供了YApi的URL，首先验证该URL是否属于已配置的`base_url`。
2. 确认用户身份（使用`yapi whoami`），仅在需要时执行`yapi login`。
3. 根据`api_id`、关键词或类别来查找目标接口。
4. 首先获取原始的JSON数据，然后对其进行整理：包括方法、路径、请求头、参数、请求体以及响应数据的结构/示例。
5. 在执行文档同步任务时，先使用`--dry-run`模式进行测试，然后再进行正式的同步。

## URL检测
1. 从`~/.yapi/config.toml`文件中读取已配置的`base_url`。
```bash
rg -n "^base_url\\s*=" ~/.yapi/config.toml
```
2. 如果URL的路径部分与`base_url`匹配，从中提取接口的ID：
   - `/project/123/...` -> `project_id=123`
   - `.../api/456` -> `api_id=456`
   - `.../api/cat_789` -> `catid=789`
3. 如果`api_id`存在，优先直接通过`api_id`来查找接口：
```bash
yapi --path /api/interface/get --query id=<api_id>
```

## 常用命令
```bash
# version/help
yapi --version
yapi -h

# auth
yapi whoami
yapi login

# search / fetch
yapi search --q keyword --project-id 310
yapi --path /api/interface/get --query id=123
yapi --path /api/interface/list_cat --query catid=123
```

配置缓存位置：
- 配置文件：`~/.yapi/config.toml`
- 身份验证缓存：`~/.yapi-mcp/auth-*.json`

## 文档同步
推荐的绑定模式：
```bash
yapi docs-sync bind add --name projectA --dir docs/release-notes --project-id 267 --catid 3667
yapi docs-sync --binding projectA --dry-run
yapi docs-sync --binding projectA
```

注意事项：
- 绑定文件：`.yapi/docs-sync.json`
- 映射输出文件：
  - `.yapi/docs-sync-links.json`
  - `.yapi/docs-sync.projects.json`
  - `.yapi/docs-sync.deployments.json`
- 默认情况下，仅同步发生变化的文件；使用`--force`选项可进行全量同步。
- 如果配置文件为`.yapi.json`，系统也会使用该文件（但不支持绑定功能）。
- 文档的渲染格式（Mermaid/PlantUML/Graphviz/D2）取决于本地是否安装了相应的工具；缺少这些工具不会影响基本的同步功能。

## 接口创建规则
- 在创建或更新接口时，务必设置`req_body_type`（不确定时使用`json`），并提供`res_body`（建议使用JSON格式）。
- 将结构化的请求/响应字段放入`req_*`或`res_body`中，而不要仅使用纯文本的`desc`或`markdown`格式。