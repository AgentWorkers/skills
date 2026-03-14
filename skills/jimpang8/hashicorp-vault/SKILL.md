---
name: hashicorp-vault
description: 使用 `vault` CLI 与 HashiCorp Vault 进行身份验证检查、键值对（KV）秘密的读写操作、路径列表的查询、秘密引擎的启用与调优、策略检查、令牌查找以及操作故障排除。当任务中提到 HashiCorp Vault、Vault KV、秘密路径（如 `secret/` 或 `kv/`）、`VAULT_ADDR`、`VAULT_TOKEN`、AppRole、策略、挂载（mounts）或 `vault` 命令时，请使用该工具。
metadata:
  {
    "openclaw":
      {
        "emoji": "🏦",
        "requires": { "bins": ["vault"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "hashicorp/tap/vault",
              "bins": ["vault"],
              "label": "Install HashiCorp Vault CLI (brew)",
            },
            {
              "id": "apt",
              "kind": "apt",
              "package": "vault",
              "bins": ["vault"],
              "label": "Install HashiCorp Vault CLI (apt)",
            },
            {
              "id": "manual-download",
              "kind": "manual",
              "url": "https://releases.hashicorp.com/vault/",
              "label": "Download Vault CLI from HashiCorp releases",
            },
          ],
      },
  }
---
# HashiCorp Vault CLI

使用 `vault` CLI 来管理 Vault 的各项功能。建议先进行只读检查，确认无误后再执行写入密钥、更改认证方式、启用新的加密引擎或编辑策略等操作。

## 快速检查

```bash
vault version
vault status
vault auth list
vault secrets list
vault token lookup
```

如果 `VAULT_ADDR` 未设置，请先进行配置：

```bash
export VAULT_ADDR='https://vault.example.com'
```

对于 Jim 的本地 Vault，可以使用经过测试的本地端点：

```bash
export VAULT_ADDR='http://192.168.1.106:8200'
vault status
curl -s "$VAULT_ADDR/v1/sys/health"
```

关于本地环境的注意事项：
- `http://192.168.1.106:8200` 的响应正常。
- `https://192.168.1.106:8200` 返回了 TLS 版本不匹配的错误，因此该端点使用的是 HTTP 协议，而非 HTTPS。
- 从当前运行环境中无法解析 `vault.jimcom2.local`，因此除非修复了本地 DNS/mDNS 设置，否则应优先使用 IP 地址。

在假设某个路径不存在之前，请先验证相应的认证是否有效：

```bash
vault token lookup
vault kv get secret/my-app
```

## 读取密钥

对于 KV v2 格式的密钥，应使用 `vault kv` 命令，而非原始的 API 格式路径。

```bash
vault kv get secret/my-app
vault kv get -field=password secret/my-app
vault kv list secret/
```

如果输出结果不明确，请将其转换为 JSON 格式：

```bash
vault kv get -format=json secret/my-app
vault secrets list -format=json
```

## 写入密钥

在覆盖或删除任何数据之前，请务必先进行确认。

```bash
vault kv put secret/my-app username=app password='s3cr3t'
vault kv patch secret/my-app password='rotated'
```

在更新 KV v2 中的部分密钥时，建议使用 `patch` 命令。

## 策略与挂载

在使用新策略或挂载点之前，请先进行详细检查：

```bash
vault policy list
vault policy read my-policy
vault secrets list -detailed
```

只有在明确用户需求的情况下，才允许进行更改：

```bash
vault policy write my-policy ./policy.hcl
vault secrets enable -path=secret kv-v2
vault secrets tune -max-versions=10 secret/
```

## 认证辅助工具

常见的登录流程如下：

```bash
vault login
vault login -method=userpass username=<user>
vault write auth/approle/login role_id=<role_id> secret_id=<secret_id>
```

在排查认证问题时，首先检查已启用的认证后端以及令牌的详细信息：

```bash
vault auth list -detailed
vault token lookup
```

## 故障排除流程

1. 检查 `vault status` 和 `VAULT_ADDR` 的配置。
2. 使用 `vault token lookup` 或相应的登录流程来验证认证是否正常。
3. 使用 `vault secrets list` 命令确认挂载点的名称。
4. 在执行相关操作前，先确认所使用的加密引擎是 KV v1 还是 KV v2。
5. 当输出结果需要被解析或比较时，建议使用 `-format=json` 格式。
6. 可以参考 `references/kv-and-troubleshooting.md` 以获取命令使用规范及常见故障处理方法。