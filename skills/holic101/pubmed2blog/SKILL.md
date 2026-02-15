---
name: pubmed2blog
description: 将 PubMed 论文转换为适合搜索引擎优化的医疗博客文章
bins:
  - pubmed2blog
install: npm install -g pubmed2blog
requires: []
---
# pubmed2blog 技能

该技能提供了对 `pubmed2blog` 命令行工具的访问权限，该工具可用于将 PubMed 论文转换为博客文章。

## 命令

### discover
在 PubMed 中搜索相关研究，并根据其适合用于博客的程度进行排序。
```
pubmed2blog discover "cardiovascular prevention"
pubmed2blog discover "sleep quality" --days 30 --tier tier1,tier2
```

### extract
从 PubMed 获取论文的完整详细信息。
```
pubmed2blog extract 39847521
pubmed2blog extract 39847521 --json
```

### generate
根据 PubMed 论文生成博客文章。
```
pubmed2blog generate 39847521 --type research-explainer
pubmed2blog generate 39847521 --type patient-facing --lang en,de --save
```

### pipeline
完整流程：discover + extract + generate。
```
pubmed2blog pipeline "sleep quality" --top 3 --save
```

### init
交互式设置 API 密钥和偏好设置。
```
pubmed2blog init
```

## 文章类型

- **research-explainer**：面向普通读者的研究结果解释
- **patient-facing**：通俗易懂，无专业术语
- **differentiation**：解释“为什么我们不提供 X 服务”
- **service-connection**：将研究结果与相关服务进行关联

## 作为代理的使用方法

当使用此技能作为代理时：

1. 运行 `pubmed2blog discover <关键词>` 来查找相关论文
2. 使用 `pubmed2blog extract <pmid>` 获取论文的完整详细信息
3. 使用 `pubmed2blog generate <pmid> --type <类型> --save` 生成博客文章
4. 将结果通过聊天方式发送给用户
5. 通过 cron 安排定期生成内容

## 设置

```bash
npm install -g pubmed2blog
pubmed2blog init
```

支持 Anthropic、OpenAI 和 Z.AI 提供商。