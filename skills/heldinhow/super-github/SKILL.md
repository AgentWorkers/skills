# Super GitHub

**终极的GitHub自动化框架。**整合了GitHub在处理问题（issues）、Pull Request（PRs）、发布版本（releases）等方面的最佳功能。

---

## 为什么选择这个工具？

这个工具提供了全面的GitHub管理功能：问题管理、Pull Request处理、版本发布以及自动化操作，所有这些功能都集中在一个工具中。

---

## 核心特性

### 1. 问题自动化
- 创建问题（可添加标签、指定负责人）
- 查看问题列表（按状态、标签筛选）
- 更新问题内容（标题、正文、标签）
- 自动分类问题并提供标签建议

### 2. Pull Request审核辅助
- 提供Pull Request的摘要分析
- 统计文件变更情况
- 生成审核检查清单
- 检测代码冲突

### 3. 版本发布自动化
- 自动创建版本发布记录
- 自动生成变更日志
- 管理版本标签

### 4. 仓库管理
- 列出所有仓库
- 获取/设置仓库的秘密信息（security secrets）
- 管理仓库的工作流程

---

## 使用方法

### 创建问题
```
gh issue create --title "Bug in login" --body "Description" --label bug
```

### 审核Pull Request
```
gh pr review --summary --stats --checklist
```

### 创建版本发布
```
gh release create v1.0.0 --generate-notes
```

---

## 其他类似工具的评分

| 工具名称 | 评分 |
|---------|------|
| openclaw-github-assistant | 3.470 |
| github-automation-pro | 3.266 |
| github-mcp | 3.180 |

---

## 版本信息

v1.0.0 - 初始版本