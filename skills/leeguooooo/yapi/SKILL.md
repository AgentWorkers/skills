---
name: yapi
description: 查询和同步 YApi 接口文档。当用户提及“yapi 接口文档”或请求请求/响应的详细信息时，或者需要同步文档时，系统会执行此操作。此外，当用户粘贴的 YApi URL 与配置的 `base_url` 匹配时，系统也会触发该操作。
---

# YApi接口文档

## URL检测

当用户提供一个URL时，需要检查该URL是否与配置的YApi实例匹配：

1. 读取配置文件以获取`base_url`：
```bash
cat ~/.yapi/config.toml | grep base_url
```

2. 如果URL的源地址与`base_url`相同，使用`yapi` CLI来执行操作：
   - 从URL路径中提取`project_id`（例如：`/project/123/...` → `project_id=123`
   - 从URL路径中提取`api_id`（例如：`.../api/456` → `api_id=456`
   - 使用`yapi --path /api/interface/get --query id=<api_id>`来获取详细信息

3. 示例URL模式：
   - `https://yapi.example.com/project/123/interface/api/456` → `project=123, api=456`
   - `https://yapi.example.com/project/123/interface/api/cat_789` → `project=123, category=789`

## 先决条件

### 检查是否已安装`yapi` CLI
```bash
yapi --version
```

### 如果未安装，请提示用户全局安装`yapi` CLI
```bash
npm install -g @leeguoo/yapi-mcp
# or
pnpm add -g @leeguoo/yapi-mcp
```

### 检查登录状态
```bash
yapi whoami
```

### 如果未登录，请进行交互式登录
```bash
yapi login
```
登录时需要提供：
- YApi的基地址（例如：`https://yapi.example.com`
- 电子邮件
- 密码

配置文件保存在`~/.yapi/config.toml`中。

## 工作流程
1. 如果用户提供了YApi的URL，检查该URL是否与`~/.yapi/config.toml`中配置的`base_url`匹配。
2. 确保已安装`yapi` CLI（如果未安装，请提示用户全局安装）。
3. 使用`yapi whoami`检查登录状态；如果未登录，请运行`yapi login`。
4. 从`~/.yapi/config.toml`中加载配置信息（包括`base_url`、`auth_mode`、`email/password`或`token`，`project_id`为可选）。
5. 根据ID、URL或关键词识别目标接口；如有需要，可以询问项目/类别ID。
6. 使用CLI调用YApi的端点以获取原始JSON数据。
7. 提供方法、路径、请求头、查询参数/响应数据结构以及示例信息。

## CLI使用方法
- 配置文件位置：`~/.yapi/config.toml`
- 认证缓存文件：`~/.yapi-mcp/auth-*.json`

### 常用命令
```bash
# Check version
yapi --version

# Show help
yapi -h

# Check current user
yapi whoami

# Login (interactive)
yapi login

# Search interfaces
yapi search --q keyword

# Get interface by ID
yapi --path /api/interface/get --query id=123

# List interfaces in category
yapi --path /api/interface/list_cat --query catid=123
```

## 文档同步
- 使用`yapi docs-sync bind add --name <binding> --dir <path> --project-id <id> --catid <id>`将本地文档绑定到YApi的相应类别（结果保存在`.yapi/docs-sync.json`文件中）。
- 使用`yapi docs-sync --binding <binding>`同步文档，或使用`yapi docs-sync`同步所有绑定。
- 默认情况下仅同步已更改的文件；使用`--force`选项可同步所有文件。
- Mermaid渲染功能依赖于`mmdc`插件（如果可能的话会自动安装；即使安装失败也不会阻止同步过程）。
- 如需完整的Markdown格式渲染，请安装`pandoc`插件（需手动安装）。
- 在文档同步后生成的额外文件：
  - `.yapi/docs-sync-links.json`：本地文档与YApi文档URL的映射关系。
  - `.yapi/docs-sync.projects.json`：缓存的项目元数据和环境信息。
  - `.yapi/docs-sync.deployments.json`：本地文档与部署后的URL的映射关系。

## 接口创建提示
- 在创建接口时，务必设置`req_body_type`（建议使用`json`格式），并提供`res_body`（建议使用JSON Schema格式）。如果这些字段为空，可能会导致`/api/interface/add`操作失败。
- 将请求和响应的结构保存在`req_*`和`res_body`字段中，而不是直接写入`desc`或`markdown`内容中。