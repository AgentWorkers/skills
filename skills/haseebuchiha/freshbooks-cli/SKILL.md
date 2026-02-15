---
name: freshbooks-cli
description: FreshBooks CLI 用于管理发票、客户和账单。当用户提到 FreshBooks、开票、计费、客户或会计相关内容时，请使用该工具。
metadata: {"openclaw":{"emoji":"💰","requires":{"bins":["freshbooks"]},"install":[{"id":"npm","kind":"node","package":"@haseebuchiha/freshbooks-cli","bins":["freshbooks"],"label":"Install freshbooks-cli (npm)"}]}}
---

# freshbooks-cli

这是一个用于管理FreshBooks发票、客户和账单的命令行工具（CLI），它使用了官方的`@freshbooks/api` SDK。

## 安装

```bash
npm install -g @haseebuchiha/freshbooks-cli
```

安装此工具需要`.npmrc`文件，并在其中添加以下仓库地址：`@haseebuchiha:registry=https://npm.pkg.github.com`（用于从GitHub仓库下载依赖项）。

## 设置（只需一次）

使用FreshBooks的OAuth2认证。必须使用`--manual`标志进行手动认证（因为使用`localhost`作为回调地址在FreshBooks中无法正常工作）。

```bash
freshbooks auth login \
  --client-id "<FRESHBOOKS_CLIENT_ID>" \
  --client-secret "<FRESHBOOKS_CLIENT_SECRET>" \
  --manual
```

1. 打开浏览器，使用FreshBooks的OAuth2认证流程进行登录。
2. 认证成功后，将页面上显示的授权代码复制到命令行工具中。
3. 授权信息会被保存在`~/.config/freshbooks-cli/config.json`文件中（文件权限设置为0600），并在令牌过期前自动刷新。

验证认证状态：`freshbooks auth status`

## 认证相关命令

- `freshbooks auth login --client-id <id> --client-secret <secret> --manual`：通过OAuth2 OOB（Out-of-Browser）流程登录
- `freshbooks auth logout`：清除存储的令牌和凭据
- `freshbooks auth status`：显示账户ID、令牌过期时间和认证状态
- `freshbooks auth refresh`：手动刷新访问令牌

## 客户相关命令

- `freshbooks clients list [-p <page>] [--per-page <n>] [-s <search>]`：列出所有客户或按组织名称搜索客户
- `freshbooks clients get <id>`：根据ID获取单个客户信息
- `freshbooks clients create [--fname <name>] [--lname <name>] [--email <email>] [--organization <org>]`：创建新客户
- `freshbooks clients create --data '<json>'`：使用JSON数据创建客户
- `freshbooks clients update <id> --data '<json>'`：更新客户信息

示例：`freshbooks clients create --fname "Taha" --organization "abcg.io"`

## 发票相关命令

- `freshbooks invoices list [-p <page>] [--per-page <n>]`：列出所有发票
- `freshbooks invoices get <id>`：根据ID获取单个发票
- `freshbooks invoices create --client-id <id> --lines '<json>']`：创建包含明细项目的发票
- `freshbooks invoices create --data '<json>'`：使用JSON数据创建发票
- `freshbooks invoices update <id> --data '<json>'`：更新发票信息
- `freshbooks invoices archive <id>`：将发票归档（FreshBooks不支持永久删除）
- `freshbooks invoices share-link <id>`：获取发票的共享链接

### 发票明细项格式

发票明细项是一个JSON数组，每个明细项包含`name`（名称）、`qty`（数量）和`unitCost`（单价，单位为货币）：

```json
[
  {"name": "Web Services", "qty": 1, "unitCost": {"amount": "15000.00", "code": "USD"}},
  {"name": "App Services", "qty": 1, "unitCost": {"amount": "15000.00", "code": "USD"}}
]
```

示例（完整的发票创建命令）：

```bash
freshbooks invoices create --client-id 818183 \
  --lines '[{"name":"Web Services","qty":1,"unitCost":{"amount":"15000.00","code":"USD"}},{"name":"App Services","qty":1,"unitCost":{"amount":"15000.00","code":"USD"}}]'
```

## 工作流程

### 新客户的添加及发票的开具

1. 使用`freshbooks clients create --fname "Name" --organization "Company"`创建新客户，并记录返回的`id`。
2. 使用`freshbooks invoices create --client-id <id> --lines '[...]'`创建发票。
3. 使用`freshbooks invoices share-link <invoice-id>`获取发票的共享链接。

### 客户账单信息的查询

1. 使用`freshbooks clients list -s "company name"`查找客户ID。
2. 使用`freshbooks invoices list`列出所有属于该客户的发票。
3. 使用`freshbooks invoices get <id>`获取详细的发票信息。

## 注意事项

- 所有输出结果都是JSON格式，可以直接输出到标准输出（stdout）或通过`jq`进行过滤，例如：`freshbooks clients list | jq '.clients[].organization'`。
- 货币值的格式为`{"amount": "string", "code": "USD"`，其中`amount`始终为字符串类型（例如`"30000.00"`），切勿使用`parseFloat`函数进行转换。
- 使用`archive`命令会将发票状态设置为`1`（表示已归档）。FreshBooks不支持永久删除发票。
- 令牌会自动刷新；如果刷新失败，请重新执行`freshbooks auth login --client-id <id> --client-secret <secret> --manual`命令进行登录。
- 客户信息也可以从环境变量`FRESHBOOKS_CLIENT_ID`和`FRESHBOOKS_CLIENT_SECRET`中读取（这些环境变量的优先级高于配置文件中的设置）。
- 在创建发票或修改账单信息之前，请务必获得用户的确认。