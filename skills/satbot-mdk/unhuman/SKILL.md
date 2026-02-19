---
name: unhuman
description: 通过 unhuman.domains 进行域名搜索、注册和管理。使用 agent-wallet 以比特币进行支付。适用于用户需要查找可用域名、注册新域名、管理 DNS 记录、更新域名服务器或续订域名的场景。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["npx"] },
        "install":
          [
            {
              "id": "unhuman-npm",
              "kind": "node",
              "package": "unhuman",
              "bins": ["unhuman"],
              "label": "Install unhuman CLI (npm)",
            },
          ],
      },
  }
---
# unhuman — 域名管理命令行工具（Domain Management CLI）

您可以在 [unhuman.domains](https://unhuman.domains) 注册和管理域名，支付方式支持通过 Lightning Network 使用比特币。

- **npm 包**: [unhuman](https://www.npmjs.com/package/unhuman)（由 moneydevkit 发布）
- **来源**: unhuman.domains 的域名注册 API

## 命令

### 搜索域名

```bash
npx unhuman domains search myproject
npx unhuman domains search myproject --tld com,dev,xyz
npx unhuman domains search myproject --json
```

### 注册域名

```bash
# Manual payment (prints Lightning invoice, waits for preimage)
npx unhuman domains register mysite.xyz --email recovery@example.com

# Auto-pay with agent-wallet (requires explicit --wallet flag)
npx unhuman domains register mysite.xyz --wallet --email recovery@example.com
```

- `--email` 参数用于设置恢复邮箱（推荐使用）
- 注册成功后，管理令牌会保存在 `~/.unhuman/tokens.json` 文件中

### 域名信息

```bash
npx unhuman domains info mysite.xyz
```

### DNS 记录

```bash
npx unhuman domains dns mysite.xyz
npx unhuman domains dns set mysite.xyz --records '[{"type":"A","name":"@","value":"1.2.3.4","ttl":3600}]'
```

### 更新域名解析服务器

```bash
npx unhuman domains nameservers mysite.xyz ns1.example.com ns2.example.com
```

### 续订域名

```bash
npx unhuman domains renew mysite.xyz
npx unhuman domains renew mysite.xyz --wallet --period 2
```

### 恢复管理令牌

```bash
npx unhuman domains recover mysite.xyz --email recovery@example.com
npx unhuman domains recover mysite.xyz --email recovery@example.com --code 123456
```

### 列出已保存的令牌

```bash
npx unhuman domains tokens
```

## 使用 `--wallet` 标志进行支付

`--wallet` 标志允许通过 `@moneydevkit/agent-wallet` 自动完成支付。**仅当用户明确要求自动支付时使用此标志。**

**注意事项**：
- 需要运行 `npx @moneydevkit/agent-wallet start` 命令来启动 agent-wallet 守护进程。
- 确保钱包中有足够的余额。

**支付流程**：
- 提交请求 → 收到包含 Lightning Network 发票的 402 错误响应 → agent-wallet 执行支付 → 使用预签名数据（preimage）重新尝试支付。

**⚠️ 使用 `--wallet` 之前务必征得用户同意。** 此标志会触发实际的比特币支付。如果不使用 `--wallet`，CLI 会显示发票供用户手动支付。

## 凭据与存储

- **管理令牌**：注册成功后保存在 `~/.unhuman/tokens.json` 文件中。这些令牌用于 DNS、域名解析服务器设置和续订操作。请保护该文件的安全。
- **无需 API 密钥**：域名搜索是免费的；注册和续订操作采用 MDK 402 支付协议（按使用次数通过 Lightning Network 发票支付）。
- **agent-wallet**：如果使用 `--wallet`，请确保 wallet 守护进程已启动并运行。钱包的助记词和密钥由 `~/.agent-wallet/` 目录下的 agent-wallet 独立管理。

## 其他说明

- 所有命令都支持 `--json` 选项，以生成机器可读的输出格式。
- 价格以美元计价，按当前比特币汇率支付。
- 恢复邮箱是可选的，但强烈建议设置，以便在需要时恢复管理权限。