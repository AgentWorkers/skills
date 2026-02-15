---
name: pscale-service-token
description: 创建、列出并管理服务令牌，用于 CI/CD（持续集成/持续部署）认证。这些令牌适用于设置自动化部署、配置 CI/CD 管道（如 GitHub Actions、GitLab CI、CircleCI 等）、实现非交互式认证，或轮换 CI/CD 凭据。在生产环境中的自动化场景中，建议优先使用服务令牌而非密码。服务令牌可用于触发 CI/CD 流程、实现自动化认证等功能。
---

# pscale service-token

用于创建、列出和管理用于持续集成/持续部署（CI/CD）及自动化流程的服务令牌。

## 常用命令

```bash
# Create service token
pscale service-token create --org <org>

# List service tokens
pscale service-token list --org <org>

# Delete service token
pscale service-token delete <token-id> --org <org>
```

## 工作流程

### 持续集成/持续部署设置（GitHub Actions）

```bash
# 1. Create service token
pscale service-token create --org my-org

# Returns:
#   TOKEN_ID: xxxxx
#   TOKEN: yyyyy

# 2. Add to GitHub Secrets
#   PLANETSCALE_SERVICE_TOKEN_ID = xxxxx
#   PLANETSCALE_SERVICE_TOKEN = yyyyy

# 3. Use in workflow
# .github/workflows/deploy.yml
# env:
#   PLANETSCALE_SERVICE_TOKEN_ID: ${{ secrets.PLANETSCALE_SERVICE_TOKEN_ID }}
#   PLANETSCALE_SERVICE_TOKEN: ${{ secrets.PLANETSCALE_SERVICE_TOKEN }}
# run: |
#   pscale deploy-request deploy my-db my-branch
```

### 持续集成/持续部署管道集成

```bash
# 1. Create service token
pscale service-token create --org my-org

# 2. Add to your CI/CD secrets/variables
#   PLANETSCALE_SERVICE_TOKEN_ID
#   PLANETSCALE_SERVICE_TOKEN

# 3. Use in your pipeline config (.github/workflows, .gitlab-ci.yml, etc.)
# deploy:
#   script:
#     - pscale deploy-request create $DATABASE $BRANCH_NAME
```

### 令牌轮换

```bash
# 1. List existing tokens
pscale service-token list --org my-org

# 2. Create new token
pscale service-token create --org my-org

# 3. Update CI/CD secrets

# 4. Delete old token
pscale service-token delete <old-token-id> --org my-org
```

## 故障排除

### 令牌认证失败

**错误信息：** `401 Unauthorized`

**解决方法：**
- 确保 `TOKEN_ID` 和 `TOKEN` 都设置正确
- 检查令牌是否已被删除：`pscale service-token list`
- 确保令牌具有所需的权限
- 尝试创建新的令牌（旧令牌可能已过期）

### 令牌未显示在列表中

**原因：** 令牌是组织级（organization-scoped）的

**解决方法：**
```bash
# Ensure correct org
pscale org show

# List tokens for specific org
pscale service-token list --org <correct-org>
```

## 安全最佳实践

1. **定期轮换令牌**（建议每90天轮换一次）
2. **为不同的CI/CD系统使用不同的令牌**
3. **立即删除未使用的令牌**
4. **切勿将令牌提交到版本控制系统中**
5. **使用秘密管理工具**（如GitHub Secrets、环境变量或加密存储系统）
6. **如果可能的话，限制令牌的权限范围**（这将在未来的PlanetScale更新中实现）

## 相关技能

- **pscale-auth** - 交互式认证（开发用途）
- **pscale-deploy-request** - 通过令牌进行自动化部署
- **gitlab-cli-skills** - GitLab持续集成集成
- **github** - GitHub Actions集成

## 参考资料

有关完整命令的参考信息，请参阅 `references/commands.md`。