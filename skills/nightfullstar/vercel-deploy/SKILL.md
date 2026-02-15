---
name: vercel-deploy
description: 部署和管理 Vercel 项目。适用于将应用程序部署到 Vercel、管理环境变量、检查部署状态、查看日志或执行 Vercel 相关操作。支持生产环境部署和预览部署。这属于实际的基础设施管理操作——并非依赖“AI 自动构建应用程序”的方式。
---

# Vercel 部署与管理

部署和管理 Vercel 项目。这里没有“AI 会为你构建应用程序”这类花言巧语，只有实用的 Vercel 操作指南。

## 配置

### Vercel 设置

**获取令牌：**
1. 访问 https://vercel.com/account/tokens
2. 创建一个令牌（命名为“OpenClaw”）
3. 将令牌设置到环境变量中：

```bash
export VERCEL_TOKEN="your-token-here"
```

或者将其存储在 `.env` 文件中：
```
VERCEL_TOKEN=your-token-here
```

## Vercel 操作

### 部署项目

```bash
# Deploy to preview
scripts/vercel_deploy.sh --project bountylock --preview

# Deploy to production
scripts/vercel_deploy.sh --project bountylock --production
```

### 管理环境变量

```bash
# List env vars
scripts/vercel_env.sh --project bountylock --list

# Set env var
scripts/vercel_env.sh --project bountylock --set \
  --key NEXT_PUBLIC_RPC_URL \
  --value "https://sepolia.base.org" \
  --env production

# Delete env var
scripts/vercel_env.sh --project bountylock --delete \
  --key OLD_VAR \
  --env production
```

### 检查部署状态

```bash
# Get latest deployment
scripts/vercel_status.sh --project bountylock

# Get specific deployment
scripts/vercel_status.sh --deployment dpl_abc123
```

### 查看日志

```bash
# Get deployment logs
scripts/vercel_logs.sh --deployment dpl_abc123

# Get runtime logs
scripts/vercel_logs.sh --project bountylock --function api/bounties
```

## 常见工作流程

### 初始测试网部署

1. **设置环境变量：**
```bash
# Contract addresses (after deploying to Sepolia)
scripts/vercel_env.sh --project bountylock --set \
  --key NEXT_PUBLIC_CONTRACT_ADDRESS \
  --value "0x..." \
  --env production

# RPC URL
scripts/vercel_env.sh --project bountylock --set \
  --key NEXT_PUBLIC_RPC_URL \
  --value "https://sepolia.base.org" \
  --env production

# Chain ID
scripts/vercel_env.sh --project bountylock --set \
  --key NEXT_PUBLIC_CHAIN_ID \
  --value "84532" \
  --env production
```

2. **部署：**
```bash
scripts/vercel_deploy.sh --project bountylock --production
```

3. **检查状态：**
```bash
scripts/vercel_status.sh --project bountylock
```

### 更新环境变量

```bash
# Update contract address after redeployment
scripts/vercel_env.sh --project bountylock --set \
  --key NEXT_PUBLIC_CONTRACT_ADDRESS \
  --value "0xNEW_ADDRESS" \
  --env production

# Trigger new deployment to use updated vars
scripts/vercel_deploy.sh --project bountylock --production
```

### 调试部署问题

```bash
# Get latest deployment info
scripts/vercel_status.sh --project bountylock

# Get build logs
scripts/vercel_logs.sh --deployment dpl_abc123

# Check environment variables
scripts/vercel_env.sh --project bountylock --list
```

## 安全最佳实践

1. **令牌范围：** 尽可能使用项目级令牌
2. **令牌轮换：** 定期更换令牌
3. **审计：** 定期审查部署日志
4. **机密信息：** 绝不要将令牌提交到 Git 中

## 故障排除

**“身份验证失败”**
- 确保令牌设置正确
- 验证令牌是否过期

**“项目未找到”**
- 确认项目名称与 Vercel 项目名称一致
- 检查账户是否具有访问该项目的权限

**“部署失败”**
- 查看构建日志：`scripts/vercel_logs.sh --deployment dpl_xxx`
- 确认环境变量设置正确
- 检查代码中是否存在构建错误

## 参考文件

- **Vercel API 参考：** 请参阅 [vercel-api.md](references/vercel-api.md) 以获取完整的 API 文档
- **部署模式：** 请参阅 [deployment-patterns.md](references/deployment-patterns.md) 以了解常见的部署工作流程