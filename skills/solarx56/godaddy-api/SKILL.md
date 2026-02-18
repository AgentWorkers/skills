---
name: godaddy
description: 通过Shell脚本和MCP服务器，全面掌握GoDaddy API的功能，涵盖域名管理、DNS设置、证书处理、购物车功能、订阅服务、协议管理、国家信息以及售后商品列表等各个方面。
homepage: https://developer.godaddy.com/doc
metadata: {"openclaw": {"emoji": "🌐", "requires": {"bins": ["bash", "curl", "jq", "node", "npm"]}}}
---
# GoDaddy API

## 设置

```bash
export GODADDY_API_BASE_URL="https://api.godaddy.com"  # or https://api.ote-godaddy.com
export GODADDY_API_KEY="your-key"
export GODADDY_API_SECRET="your-secret"
```

密钥获取地址：<https://developer.godaddy.com/keys>

## Shell 脚本

- `scripts/gd-domains.sh` — 列出/获取域名信息、检查域名可用性、验证购买信息、购买域名、续费域名、转移域名、更新域名信息、删除域名、设置域名隐私选项、获取/接受域名协议
- `scripts/gd-dns.sh` — 获取所有 DNS 信息、更改 DNS 类型/名称、批量添加 DNS 设置、删除特定类型的 DNS 设置
- `scripts/gd-certs.sh` — 创建/验证证书信息、获取证书、执行证书相关操作（下载、续费、重新发放、撤销、验证域名控制权）
- `scripts/gd-shoppers.sh` — 获取/更新/删除用户账户信息
- `scripts/gd-subscriptions.sh` — 列出/取消订阅服务
- `scripts/gd-agreements.sh` — 列出所有法律协议
- `scripts/gd-countries.sh` — 列出所有国家/地区信息
- `scripts/gd-aftermarket.sh` — 列出域名在二级市场的销售信息

执行破坏性或涉及财务操作的脚本前需要用户确认。

## MCP 服务器

路径：`scripts/mcp-server/`

```bash
cd scripts/mcp-server
npm install
npm run build
node dist/index.js
```

MCP 服务器提供了用于管理所有域名相关服务的工具（域名、DNS、证书、用户账户、订阅服务、法律协议、国家/地区信息、二级市场交易等）。

MCP 服务器的配置示例：

```json
{
  "mcpServers": {
    "godaddy": {
      "command": "node",
      "args": ["path/to/mcp-server/dist/index.js"],
      "env": {
        "GODADDY_API_BASE_URL": "https://api.godaddy.com",
        "GODADDY_API_KEY": "",
        "GODADDY_API_SECRET": ""
      }
    }
  }
}
```

## 参考资料

- `references/endpoints.md` — 完整的 API 端点映射
- `references/auth-and-env.md` — 用户认证和环境配置相关资料
- `references/request-bodies.md` — 请求数据格式示例
- `references/error-handling.md` — 错误处理指南
- `references/safety-playbook.md` — 安全操作规范