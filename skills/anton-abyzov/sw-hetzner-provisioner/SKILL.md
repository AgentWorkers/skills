---
name: hetzner-provisioner
description: 使用 Terraform/Pulumi 在 Hetzner Cloud 上搭建基础设施。为 CX11/CX21/CX31 实例生成基础设施即代码（IaC）代码，配置 Postgres 数据库管理、SSL 设置以及 Docker 部署。支持在 Hetzner Cloud 上进行部署，提供经济实惠的托管服务（每月仅需 10 美元）。
---

# Hetzner Cloud 配置工具

这是一个自动化基础设施配置工具，专为 Hetzner Cloud 设计——它是 Vercel 和 AWS 的经济实惠的替代方案。

## 使用目的

该工具用于生成和部署适用于 Hetzner Cloud 的基础设施即代码（Infrastructure-as-Code，IaC）资源，使得每月只需花费 10-15 美元的成本即可实现 SaaS 应用程序的部署，而其他平台的成本通常在 50-100 美元之间。

## 使用场景

当用户提及以下关键词时，该工具会被激活：
- “在 Hetzner 上部署”
- “Hetzner Cloud”
- “经济型部署”
- “低成本托管”
- “每月 10 美元的部署方案”
- “高性价比的基础设施”

## 功能概述

1. **分析需求**：
   - 应用程序类型（NextJS、Node.js、Python 等）
   - 数据库需求（Postgres、MySQL、Redis）
   - 预计的流量/用户数量
   - 预算限制

2. **生成基础设施即代码**：
   - 为 Hetzner Cloud 生成 Terraform 配置文件
   - 或者使用 Pulumi（适用于 TypeScript 项目的基础设施即代码管理）
   - 选择合适的服务器实例（CX11、CX21、CX31）
   - 管理型数据库（Postgres、MySQL）
   - 对象存储（如需要）
   - 网络配置（防火墙规则、浮动 IP）

3. **配置生产环境**：
   - Docker 容器化
   - SSL 证书（使用 Let’s Encrypt）
   - DNS 配置（Cloudflare 或 Hetzner 自带 DNS 服务）
   - 配置 GitHub Actions 进行持续集成/持续部署（CI/CD）
   - 监控系统（Uptime Kuma，自行部署）
   - 自动化备份

4. **提供部署指南**：
   - 详细的部署步骤
   - 成本明细
   - 监控地址
   - 故障排除指南

---

## ⚠️ 重要提示：必须提供秘钥

**在生成 Terraform/Pulumi 代码之前，请务必检查 Hetzner API 令牌是否存在。**

### 第一步：检查令牌是否存在

```bash
# Check .env file
if [ -f .env ] && grep -q "HETZNER_API_TOKEN" .env; then
  echo "✅ Hetzner API token found"
else
  # Token NOT found - STOP and prompt user
fi
```

### 第二步：如果令牌缺失，请停止操作并显示此提示信息

```
🔐 **Hetzner API Token Required**

I need your Hetzner API token to provision infrastructure.

**How to get it**:
1. Go to: https://console.hetzner.cloud/
2. Click on your project (or create one)
3. Navigate to: Security → API Tokens
4. Click "Generate API Token"
5. Give it a name (e.g., "specweave-deployment")
6. Permissions: **Read & Write**
7. Click "Generate"
8. **Copy the token immediately** (you can't see it again!)

**Where I'll save it**:
- File: `.env` (gitignored, secure)
- Format: `HETZNER_API_TOKEN=your-token-here`

**Security**:
✅ .env is in .gitignore (never committed to git)
✅ Token is 64 characters, alphanumeric
✅ Stored locally only (not in source code)

Please paste your Hetzner API token:
```

### 第三步：验证令牌格式

```bash
# Hetzner tokens are 64 alphanumeric characters
if [[ ! "$HETZNER_API_TOKEN" =~ ^[a-zA-Z0-9]{64}$ ]]; then
  echo "⚠️  Warning: Token format unexpected"
  echo "Expected: 64 alphanumeric characters"
  echo "Got: ${#HETZNER_API_TOKEN} characters"
  echo ""
  echo "This might not be a valid Hetzner API token."
  echo "Continue anyway? (yes/no)"
fi
```

### 第四步：安全存储令牌

```bash
# Save to .env
echo "HETZNER_API_TOKEN=$HETZNER_API_TOKEN" >> .env

# Ensure .env is gitignored
if ! grep -q "^\.env$" .gitignore; then
  echo ".env" >> .gitignore
fi

# Create .env.example for team
cat > .env.example << 'EOF'
# Hetzner Cloud API Token
# Get from: https://console.hetzner.cloud/ → Security → API Tokens
HETZNER_API_TOKEN=your-hetzner-token-here
EOF

echo "✅ Token saved to .env (gitignored)"
echo "✅ Created .env.example for team (commit this)"
```

### 第五步：在 Terraform 中使用令牌

```hcl
# terraform/variables.tf
variable "hetzner_token" {
  description = "Hetzner Cloud API Token"
  type        = string
  sensitive   = true
}

# terraform/provider.tf
provider "hcloud" {
  token = var.hetzner_token
}

# Run Terraform
# export TF_VAR_hetzner_token=$HETZNER_API_TOKEN
# terraform apply
```

---

## 使用示例

**用户**：“我希望以最低的成本在 Hetzner 上部署我的 NextJS 应用程序，并使用 Postgres 数据库。”

**hetzner-provisioner**：
```markdown
I'll provision your NextJS app on Hetzner Cloud for ~$12/month.

Infrastructure:
- CX11 instance (2 vCPU, 2GB RAM): $5.83/month
- Managed Postgres (2GB): $5.00/month
- 20GB storage: $0.50/month
- SSL (Let's Encrypt): Free
- Total: ~$11.33/month

Creating Terraform configuration...

✅ Generated files:
- terraform/main.tf
- terraform/variables.tf
- terraform/outputs.tf
- .github/workflows/deploy.yml

Next steps:
1. Set HETZNER_API_TOKEN in GitHub secrets
2. Push to GitHub
3. GitHub Actions will deploy automatically

Deployment URL: https://your-app.yourdomain.com (after DNS configured)
```

## 配置选项

支持多种服务器实例类型：
- **CX11**（1 个 vCPU，2GB 内存）：每月 5.83 美元——适用于小型应用程序，支持 100-1000 名用户
- **CX21**（2 个 vCPU，4GB 内存）：每月 6.90 美元——适用于中型应用程序，支持 1000-10000 名用户
- **CX31**（2 个 vCPU，8GB 内存）：每月 14.28 美元——适用于大型应用程序，支持 10000 名以上用户

数据库选项：
- 管理型 Postgres（2GB 内存）：每月 5 美元
- 管理型 MySQL（2GB 内存）：每月 5 美元
- 自行托管数据库（包含在实例费用中）

## 成本对比

| 平台 | 小型应用 | 中型应用 | 大型应用 |
|------|--------|---------|---------|
| **Hetzner** | 12 美元/月 | 15 美元/月 | 25 美元/月 |
| Vercel | 60 美元/月 | 120 美元/月 | 240 美元/月 |
| AWS | 25 美元/月 | 80 美元/月 | 200 美元/月 |
| Railway | 20 美元/月 | 50 美元/月 | 100 美元/月 |

**成本节省**：相比其他方案可节省 50-80% 的费用

## 技术细节

- **Terraform 提供者**：`hetznercloud/hcloud`
- **API**：Hetzner Cloud API v1
- **可用区域**：纽伦堡、福尔肯施泰因、赫尔辛基（德国/芬兰）
- **部署方式**：使用 Docker 和 GitHub Actions
- **监控系统**：Uptime Kuma（自行部署，免费）

## 集成能力**

- 与 `cost-optimizer` 集成：在预算有限的情况下推荐使用 Hetzner
- 与 `devops-agent` 集成：用于战略性的基础设施规划
- 与 `nextjs-agent` 集成：专门用于 NextJS 应用程序的部署
- 支持多种后端框架（Node.js、Python、Go 等）

## 限制条件

- 仅支持欧盟地区的数据中心（符合 GDPR 规范）
- 需要拥有 Hetzner Cloud 账户
- 需要手动配置 DNS
- 不支持跨区域部署（如需跨区域部署，请使用 AWS/GCP）

## 未来计划

- 将支持 Kubernetes（在 Hetzner 上部署 Kubernetes 集群）
- 提供负载均衡器配置功能
- 支持多区域部署
- 加强灾难恢复机制