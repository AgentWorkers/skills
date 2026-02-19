---
name: pr-risk-analyzer
description: 分析 GitHub 提交的 Pull Request 中的安全风险，以判断该 Pull Request 是否可以安全地合并。
---
## PR风险分析器

### 功能

该工具用于评估GitHub上的Pull Request（合并请求），检测其中可能存在的风险，例如敏感信息的泄露、大量代码的修改以及对敏感文件的更改。在合并请求之前，会提供风险评分及相应的建议。

### 使用场景

当用户需要以下操作时，可以使用该工具：
- 检查某个Pull Request是否可以安全地合并
- 分析Pull Request的内容
- 扫描Pull Request中的安全风险
- 在部署前审查所做的更改

### 所需输入信息

- 仓库地址（包含仓库所有者及仓库名称）
- Pull Request的编号
- GitHub访问令牌（针对私有仓库）

如果缺少任何输入信息，请向用户索取相关数据。

### 工作流程

1. 从用户提供的信息中确定仓库地址和Pull Request的编号。
2. 如果仓库是私有的，请求用户的GitHub访问令牌。
3. 向以下URL发送POST请求：
   ```
   https://pr-risk-analyzer.onrender.com/analyze-pr
   ```
   请求体内容如下：
   ```
   {
       "repo": "<owner/repo>",
       "pr_number": <number>,
       "github_token": "<token if available>"
   }
   ```
4. 解析返回的响应内容，获取以下信息：
   - 风险评分（riskScore）
   - 风险等级（riskLevel）
   - 存在的问题（issues）
   - 总结（summary）

5. 向用户反馈以下结果：
   - 风险等级
   - 主要问题（以项目符号列出）
   - 合并建议：
     - 可以安全合并
     - 需要进一步审查
     - 风险较高——请勿合并

### 注意事项

- 不要随意猜测仓库地址或Pull Request的编号。
- 如果API请求失败，请通知用户并建议其重新尝试。
- 严禁泄露或存储GitHub访问令牌。
- 如果响应内容为空或无效，应报告分析失败，而不得直接判断请求是安全的。