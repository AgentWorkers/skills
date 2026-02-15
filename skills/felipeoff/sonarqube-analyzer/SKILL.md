# SonarQube 分析器技能

该技能用于分析自托管的 SonarQube 项目，自动检测问题并提供建议的解决方案。

## 注册的工具

### `sonar_get_issues`
用于获取 SonarQube 项目中所有问题或合并请求（Pull Requests, PRs）的列表。

**参数：**
- `projectKey` (string, 必填): 项目键
- `pullRequest` (string, 可选): 需要分析的合并请求编号
- `severities` (string[], 可选): 需要过滤的严重性级别（BLOCKER, CRITICAL, MAJOR, MINOR, INFO）
- `status` (string, 可选): 问题的状态（OPEN, CONFIRMED, FALSE_POSITIVE 等）
- `limit` (number, 可选): 问题数量限制（默认值：100）

**示例：**
```json
{
  "projectKey": "openclaw-panel",
  "pullRequest": "5",
  "severities": ["CRITICAL", "MAJOR"],
  "limit": 50
}
```

### `sonar_analyze_and_suggest`
根据 SonarQube 的规则分析问题并提供建议的解决方案。

**参数：**
- `projectKey` (string, 必填): 项目键
- `pullRequest` (string, 可选): 合并请求编号
- `autoFix` (boolean, 可选): 是否尝试自动应用修复（默认值：false）

**示例：**
```json
{
  "projectKey": "openclaw-panel",
  "pullRequest": "5",
  "autoFix": false
}
```

### `sonar_quality_gate`
用于检查项目的质量检查（Quality Gate）状态。

**参数：**
- `projectKey` (string, 必填): 项目键
- `pullRequest` (string, 可选): 合并请求编号

**示例：**
```json
{
  "projectKey": "openclaw-panel",
  "pullRequest": "5"
}
```

## 配置

该技能使用以下环境配置：

```bash
SONAR_HOST_URL=http://127.0.0.1:9000  # URL do SonarQube
SONAR_TOKEN=admin                      # Token de autenticação
```

## 使用方法

### 分析特定的合并请求：
```bash
node scripts/analyze.js --project=my-project --pr=5
```

### 生成问题报告：
```bash
node scripts/report.js --project=my-project --format=markdown
```

### 检查质量检查状态：
```bash
node scripts/quality-gate.js --project=my-project --pr=5
```

## 响应结构

### `sonar_get_issues`
```json
{
  "total": 12,
  "issues": [
    {
      "key": "...",
      "severity": "MAJOR",
      "component": "apps/web/src/ui/App.tsx",
      "line": 346,
      "message": "Extract this nested ternary...",
      "rule": "typescript:S3358",
      "status": "OPEN",
      "solution": "Extract nested ternary into a separate function..."
    }
  ],
  "summary": {
    "BLOCKER": 0,
    "CRITICAL": 0,
    "MAJOR": 2,
    "MINOR": 10,
    "INFO": 0
  }
}
```

### `sonar_analyze_and_suggest`
```json
{
  "projectKey": "openclaw-panel",
  "analysis": {
    "totalIssues": 12,
    "fixableAutomatically": 8,
    "requiresManualFix": 4
  },
  "suggestions": [
    {
      "file": "apps/web/src/ui/App.tsx",
      "line": 346,
      "issue": "Nested ternary operation",
      "suggestion": "Extract into independent component",
      "codeExample": "...",
      "autoFixable": false
    }
  ],
  "nextSteps": [
    "Run lint:fix for auto-fixable issues",
    "Refactor nested ternaries in App.tsx",
    "Replace || with ?? operators"
  ]
}
```

## 可用的自动修复方案

| 规则 | 问题 | 自动修复方案 |
|-------|----------|-------------------|
| S6606 | 使用 `|\|\|` 替代 `??` | ✅ 将 `??` 替换为 `|\|\|` |
| S3358 | 嵌套的三元表达式 | ❌ 需要手动重构 |
| S6749 | 代码片段冗余 | ✅ 删除冗余代码片段 |
| S6759 | 属性未设置为只读 | ✅ 为属性添加 `readonly` 属性 |
| S3776 | 认知复杂性过高 | ❌ 需要提取相关组件 |
| S6571 | 联合类型中的 `any` 关键字 | ✅ 删除冗余部分 |

## 系统要求

- Node.js 18 及以上版本
- 具备访问 SonarQube 的权限（默认地址：localhost:9000）
- 已配置认证令牌

## 与工作流集成

示例：在 GitHub Actions 中的使用方法：
```yaml
- name: Analyze with SonarQube Skill
  run: |
    npm install -g @felipeoff/sonarqube-analyzer
    sonarqube-analyzer \
      --project=my-project \
      --pr=${{ github.event.pull_request.number }} \
      --suggest-fixes
```