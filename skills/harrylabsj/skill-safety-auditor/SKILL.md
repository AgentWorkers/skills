---
name: skill-safety-auditor
description: 对技能（skills）进行全面的安全审计，以识别漏洞、不安全的编程模式以及合规性问题。此步骤适用于对技能进行安全审查时，检查是否存在硬编码的敏感信息（hardcoded secrets）、注入攻击的风险（injection risks），或在技能发布之前进行安全验证。
---
# 技能安全审计器（Skill Safety Auditor）

## 概述

`skill-safety-auditor` 工具可以对技能（skills）进行全面的安全审计，以识别漏洞、不安全的代码模式、权限问题以及合规性违规。它有助于确保技能在发布或部署前符合安全标准。

## 使用场景

- 在技能开发过程中进行早期问题检测
- 在新技能发布到生产环境之前
- 作为发布审批流程的一部分
- 当用户请求对技能进行“审计”或“安全检查”时
- 在定期进行安全审查时
- 在审查第三方技能时

## 核心概念

### 审计类型

| 类型 | 描述 | 速度 |
|------|-------------|-------|
| `quick-scan` | 快速的表面级检查 | 约1秒 |
| `audit` | 全面分析 | 约5-10秒 |
| `report` | 带有JSON输出的完整审计报告 | 约10秒 |

### 漏洞类别

| 类别 | 检查内容 | 严重程度 |
|----------|------------|----------|
| `secrets` | 硬编码的API密钥、密码、令牌 | 严重 |
| `injection` | 命令注入、路径遍历 | 高风险 |
| `permissions` | 不安全的文件权限 | 中等风险 |
| `dependencies` | 已知的漏洞依赖项 | 高风险 |
| `network` | 不安全的HTTP连接 | 低风险 |

### 严重程度等级

- **严重**：立即存在安全风险，必须在发布前修复
- **高风险**：存在显著风险，强烈建议修复
- **中等**：存在中等风险，应予以处理
- **低风险**：属于次要问题，可考虑修复
- **信息提示**：仅提供信息参考，非强制修复

## 输入参数

- 技能目录的路径
- 审计类型
- 输出格式偏好
- 漏洞类型筛选条件

## 输出结果

- 包含审计结果的控制台输出
- JSON格式的审计报告
- 统计摘要
- 审计通过/失败状态

## 工作流程

### 快速安全检查

1. 对目标技能执行快速扫描
2. 查看并处理任何立即需要解决的问题
3. 修复严重或高风险的问题

### 全面审计

1. 执行包含详细输出的全面审计
2. 按严重程度查看所有审计结果
3. 生成JSON格式的报告
4. 按优先级处理审计结果
5. 重新执行审计以验证修复情况

### 发布前审计

1. 启用所有审计功能对技能进行审计
2. 生成正式的报告
3. 与团队一起审查报告
4. 修复所有严重或高风险的问题
5. 记录被接受的低风险问题

## 命令说明

### 快速扫描
```bash
./scripts/quick-scan.sh /path/to/skill
```

### 全面审计
```bash
./scripts/audit-skill.sh /path/to/skill --verbose
```

### 生成报告
```bash
./scripts/audit-skill.sh /path/to/skill --output report.json
```

### 按类型筛选审计结果
```bash
./scripts/audit-skill.sh /path/to/skill --types secrets,injection
```

### 查看历史审计记录
```bash
./scripts/list-audits.sh [--skill <name>] [--since 2024-01-01]
```

## 输出格式

### 控制台输出
```
🔍 Starting security audit: my-skill
================================
✅ SKILL.md exists
Scanning for secrets...
Scanning for injection vulnerabilities...
[high] injection: eval() detected
  File: src/utils.js:15
  Recommendation: Avoid eval(), use safer alternatives

================================
Validation complete:
  Errors: 0
  Warnings: 1
❌ Validation FAILED
```

### JSON报告
```json
{
  "audit_id": "AUDIT-20240313-001",
  "skill": "my-skill",
  "timestamp": "2024-03-13T10:30:00Z",
  "summary": {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "info": 1
  },
  "findings": [
    {
      "id": "SEC-001",
      "severity": "high",
      "type": "injection",
      "file": "src/utils.js",
      "line": 15,
      "description": "eval() detected - potential code injection",
      "recommendation": "Avoid eval(), use safer alternatives"
    }
  ],
  "passed": false,
  "recommendations": [
    "Remove eval() from src/utils.js:15",
    "Add input validation to all user inputs"
  ]
}
```

## 审计内容

### 保密信息检测

- API密钥和令牌
- 数据库密码
- 私钥
- 访问凭证
- 环境变量中的敏感信息

### 代码安全性检查

- `eval()` 函数的使用
- 函数构造函数
- 使用字符串设置 `setTimeout/setInterval`
- 子进程的执行
- 动态代码的执行

### 文件权限检查

- 具有世界写入权限的文件
- 数据文件的执行权限
- 敏感文件的访问权限

### 依赖项检查

- 已知的CVE漏洞
- 已弃用的包
- 可能存在危险的包

### 网络安全检查

- HTTP与HTTPS URL的使用
- 不安全的API端点
- 证书验证缺失

## 质量要求

- 在技能发布前必须执行审计
- 修复所有严重或高风险的问题
- 记录被接受的风险
- 修复问题后重新进行审计
- 保留审计历史记录

## 常见使用示例

- “对这项技能进行安全问题审计”
- “发布前进行安全检查”
- “扫描硬编码的保密信息”
- “检查是否存在注入漏洞”
- “对技能X进行安全审计”

## 限制

- 仅进行静态分析，无法检测运行时漏洞
- 可能会误判合法代码为漏洞
- 无法验证外部服务的安全性
- 不会测试实际的运行时行为
- 仅针对已知的漏洞模式进行检查

## 资源文件

### 脚本

- `audit-skill.sh`：全面安全审计
- `quick-scan.sh`：快速安全检查
- `list-audits.sh`：查看审计历史记录
- `test.sh`：测试技能功能

### 参考资料

- 安全最佳实践
- 常见漏洞模式
- OWASP安全指南