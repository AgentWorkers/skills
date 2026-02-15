# Secret Scanner

在您的代码库中扫描泄露的秘密信息、API密钥和凭证，防止它们被部署到生产环境中。

## 快速入门

```bash
npx ai-secret-scan
```

## 功能介绍

- 扫描文件中硬编码的秘密信息和API密钥
- 识别常见的秘密模式（如AWS、Stripe、GitHub令牌等）
- 检查.env文件中是否存在敏感数据
- 警告git历史记录中存在的秘密信息
- 无需配置即可立即获取扫描结果

## 使用方法

```bash
# Scan current directory
npx ai-secret-scan

# Scan specific path
npx ai-secret-scan ./src
```

## 使用场景

- 在将代码推送到公共仓库之前
- 在进行安全审计时
- 在设置CI/CD管道时
- 在新团队成员入职时

## LXGIC开发工具包的一部分

LXGIC Studios提供的110多种免费开发者工具之一，无需付费，也无需注册。

**了解更多：**
- GitHub: https://github.com/lxgic-studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 许可证

MIT许可证。永久免费使用。