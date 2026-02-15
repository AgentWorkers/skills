---
name: zentao
description: 使用 zentao CLI 登录并查询 ZenTao 产品及 bug 信息。ZENTAO_URL 通常包含 “/zentao” 这一部分。
homepage: https://www.npmjs.com/package/@leeguoo/zentao-mcp
metadata: {"openclaw":{"emoji":"🐞","install":[{"id":"node","kind":"node","package":"@leeguoo/zentao-mcp","bins":["zentao"],"label":"Install zentao CLI (node)"}]}}
---

# zentao (ZenTao CLI)

## 何时使用此技能

当用户需要执行以下操作时，请使用此技能：
- 通过 CLI 登录到 ZenTao
- 列出所有产品
- 查看某个产品的所有漏洞
- 查看漏洞的详细信息
- 查看用户自己的漏洞

## 安装（推荐）

使用 pnpm 进行全局安装：

```bash
pnpm i -g @leeguoo/zentao-mcp
```

如果未安装 pnpm，请按照以下步骤进行安装：

```bash
npm i -g pnpm
pnpm i -g @leeguoo/zentao-mcp
```

## 登录流程

1) 首次运行 `login` 命令：

```bash
zentao login \
  --zentao-url="https://zentao.example.com/zentao" \
  --zentao-account="leo" \
  --zentao-password="***"
```

2) 此命令会将登录凭据保存到以下文件中：
- `~/.config/zentao/config.toml`（或 `$XDG_CONFIG_HOME/zentao/config.toml`）

3) 验证登录是否成功：

```bash
zentao whoami
```

**重要提示：** `--zentao-url` 参数中必须包含 `/zentao`。如果登录时出现 404 错误，很可能是因为缺少 `/zentao` 这个路径。

## 命令说明

- **列出所有产品**（默认为简单列表）：
```bash
zentao products list
```

- **查看某个产品的漏洞**：
```bash
zentao bugs list --product 6
```

- **查看漏洞的详细信息**：
```bash
zentao bug get --id 1329
```

- **查看用户自己的漏洞（包含详细信息）**：
```bash
zentao bugs mine --status active --include-details
```

- **以 JSON 格式获取完整信息**：
  - `zentao products list --json`
  - `zentao bugs list --product 6 --json`
  - `zentao bug get --id 1329 --json`
  - `zentao bugs mine --include-details --json`