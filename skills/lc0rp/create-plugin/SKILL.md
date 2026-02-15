---
name: create-plugin
description: 根据用户的需求创建 OpenClaw 插件/扩展（TypeScript 模块）。具体使用场景包括：用户请求创建一个新的插件/扩展、添加一个新的命令（以斜杠开头），或要求开发某个特定功能的插件。触发命令包括：/create-plugin NAME WHAT-IT-DOES、/create-plugin GENERAL-PROMPT、"create extension that does ACTION" 等类似语句。
---

# 创建插件

**用户须知：** 根据权限设置的不同，OpenClaw 本身就可以创建插件。本教程将简化这一流程。插件可以改变 OpenClaw 的功能。它们会与网关在同一进程中运行，因此应将其视为可信代码。

## 参考资料

您可以使用以下资源作为参考，因为它们可能包含更最新的信息：
- [OpenClaw 插件文档](https://docs.openclaw.ai/plugins/)
- [OpenClaw 插件 > 代理工具](https://docs.openclaw.ai/plugins/agent-tools/)
- [仓库文档：插件](https://github.com/openclaw/openclaw/blob/main/docs/plugin.md)
- [仓库文档：代理工具](https://github.com/openclaw/openclaw/blob/main/docs/plugins/agent-tools.md)
- 如果有本地仓库：`<openclaw-repo>/docs/plugin.md` 和 `<openclaw-repo>/docs/plugins/agent-tools.md`

如果您能够访问这些链接，它们的内容可能会比本教程更最新。如有冲突，请以这些链接为准。否则，本教程将介绍截至 2026 年 2 月的 OpenClaw 插件创建方法。

## 概述

将用户请求转换为可运行的 OpenClaw 插件：选择一个插件 ID，生成基础文件（`openclaw.plugin.json`、`index.ts`，可选的 `package.json`），实现相应的命令/工具/服务，并记录如何启用或重启该插件。

## 工作流程

### 1) 解析请求 + 确认插件功能

- 确定插件的 ID 及其主要功能（自动回复命令、代理工具、命令行工具、频道、服务等）。
- 如果请求不明确，请询问以下信息：
  - 所需插件的 ID/名称
  - 触发该插件的条件（是什么命令或代理工具？）
  - 预期输出或副作用
  - 任何依赖项或外部二进制文件
  - 配置字段（API 密钥、标志、默认值）

### 2) 选择插件目录 + ID

选择一个插件根目录：
- **推荐目录（避免升级问题）：`~/.openclaw/extensions/<id>`
- 本地开发环境：`<workspace>/.openclaw/extensions/<id>`
- 自定义路径：需添加到 `plugins.loadpaths` 列表中

本地开发环境的安装选项：
- 复制安装：`openclaw plugins install /path/to/plugin`
- 创建符号链接安装：`openclaw plugins install -l /path/to/plugin`

插件 ID 应使用小写字母、连字符组成，长度不超过 64 个字符。

### 3) 创建所需文件

**必须包含插件配置文件**（`openclaw.plugin.json`）：
```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "description": "...",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```
注意：即使配置内容为空，`configSchema` 也是必需的。

**插件入口文件**（`index.ts`）：
```ts
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

export default function register(api: OpenClawPluginApi) {
  // registerCommand / registerTool / registerCli / registerService / etc.
}
```

**可选的 `package.json`（用于生成 npm 包元数据）：**
```json
{
  "name": "@openclaw/my-plugin",
  "version": "0.1.0",
  "type": "module",
  "openclaw": { "extensions": ["./index.ts"] }
}
```

### 4) 实现插件功能

务必为插件功能编写并运行测试用例。

**自动回复命令**（不涉及大型语言模型（LLM）的调用）：
```ts
api.registerCommand({
  name: "mycmd",
  description: "...",
  acceptsArgs: true,
  requireAuth: true,
  handler: async (ctx) => ({ text: "OK" }),
});
```
规则：
- 命令是全局的，不区分大小写，且不能覆盖保留的名称。
- `acceptsArgs: false` 表示 `/cmd args` 参数不会被解析。

**代理工具**（可被大型语言模型调用）：
```ts
import { Type } from "@sinclair/typebox";

api.registerTool({
  name: "my_tool",
  description: "Do a thing",
  parameters: Type.Object({ input: Type.String() }),
  async execute(_id, params) {
    return { content: [{ type: "text", text: params.input }] };
  },
});
```

可选工具（可选配置）：
```ts
api.registerTool({ ... }, { optional: true });
```
可以通过 `tools.allow` 或 `agents.list[].tools.allow` 来启用可选工具。

### 5) 启用插件 + 重启网关

如果您有权限执行命令，可以询问用户是否允许您执行以下操作；否则，请将这些操作作为说明提供给用户：
- 启用插件：`openclaw plugins enable <id>`（或设置 `plugins.entries.<id>.enabled = true`）
- 修改后重启网关：`openclaw plugins doctor`

## 输出结果

创建插件后，应生成以下内容：
- 插件文件结构
- `openclaw.plugin.json` 和 `index.ts` 的具体内容
- 所需的配置信息（`plugins.entries.<id>.config` 或工具允许列表）
- 关于如何启用插件、重启网关以及测试新功能的提示和说明