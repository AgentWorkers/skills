---
name: wordpress
description: OpenClaw 提供了一项技能（skill），该技能通过普通的 HTTP 协议为 WordPress 提供 REST API 命令行界面（CLI），用于操作文章（posts）、页面（pages）、分类（categories）、标签（tags）、用户（users）以及执行自定义请求（custom requests）。
---

# WordPress REST API 技能（高级）

## 目的  
提供一个适用于生产环境的命令行工具（CLI），用于自动化 WordPress REST API 的操作。该工具主要支持内容管理工作流（如文章/页面）、分类系统（类别/标签）、用户权限管理以及无需外部 HTTP 库的安全自定义请求。

## 适用场景  
- 需要一个稳定的 CLI 来实现自动化操作和机器人流程。  
- 数据传输需要采用 JSON 格式。  
- 偏好使用简单的 HTTP 协议，且不依赖额外的库或工具。  

## 不适用场景  
- 需要处理 OAuth 流程或复杂的基于浏览器的身份验证机制。  
- 需要支持高级的媒体上传功能（如多部分数据流）。  

## 系统要求  
- Node.js 18 及以上版本（以支持原生的 `fetch` API）。  

## 一次性设置步骤  
1. 启用 WordPress REST API（在现代版本的 WordPress 中默认已启用）。  
2. 为 WordPress 用户创建一个专用密码（称为“应用程序密码”）。  
3. 确认用户具有相应的权限（例如编辑者/管理员权限）。  

## 安装  
```bash
cd wordpress
npm install
```  

## 运行  
```bash
node scripts/wp-cli.js help
node scripts/wp-cli.js posts:list --query per_page=5
node scripts/wp-cli.js posts:create '@post.json'
```  

您也可以使用 npm 来安装该工具：  
```bash
npm run wp -- posts:list --query per_page=5
```  

## 认证方式  
支持以下认证方式（优先选择第一个匹配的选项）：  
- 基本认证令牌：`WP_BASIC_TOKEN`（用户密码的 Base64 编码形式）  
- 用户名 + 应用程序密码：`WP_USER` + `WP_APP_PASSWORD`  
- JWT 令牌：`WP_JWT_TOKEN`  

## 必需的环境变量  
- `WP_BASE_URL`（示例：`https://example.com`）  

## 输入格式  
- 数据可以以 JSON 格式直接输入，也可以通过 `@path` 从文件中读取。  
- 查询参数使用 `--query key=value`（可重复使用）或 `--query key1=value1,key2=value2` 的格式。  

## 命令列表（高级功能）  
- 文章相关操作：`posts:list`、`posts:get`、`posts:create`、`posts:update`、`posts:delete`  
- 页面相关操作：`pages:list`、`pages:get`、`pages:create`、`pages:update`、`pages:delete`  
- 分类系统相关操作：`categories:list`、`categories:create`、`tags:list`、`tags:create`  
- 用户相关操作：`users:list`、`users:get`  
- 高级功能：`request`（用于自定义请求）  

## 操作指南  
- 对于只读列表查询，建议使用 `context:view` 方法。  
- 在测试环境中发布内容时，可以使用 `status=draft` 参数。  
- 在自动化脚本中，应对 `429` 错误和短暂的 `5xx` 错误进行重试处理。  

## 预期输出  
- 成功执行时，输出结果以 JSON 格式显示到标准输出（stdout）；遇到错误时，程序会返回非零退出码。  

## 安全注意事项  
- 严禁记录或提交任何认证令牌或应用程序密码。  
- 尽可能使用权限较低的 WordPress 用户账户来执行这些操作。