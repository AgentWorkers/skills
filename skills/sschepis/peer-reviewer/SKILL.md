---
name: peer-reviewer
description: 这款由人工智能驱动的学术论文评审工具采用多智能体系统（包括“Deconstructor”、“Devil's Advocate”和“Judge”三个智能体）来分析论文中的逻辑错误、矛盾之处以及实证研究的有效性。
version: 1.0.0
---

# 同行评审器（Peer Reviewer）

这是一个严谨的学术评审系统，它利用多个人工智能代理来分析、评估和评判科学论文。

## 使用场景

在以下情况下使用该工具：
- 当用户请求“评审这篇论文”或“找出其中的逻辑错误”时；
- 当你需要检查一篇学术论文是否与现有文献存在矛盾时；
- 当你希望获得类似“第二位评审者”（Reviewer 2）风格的批评意见时。

## 使用方法

通过 Node.js 命令行界面（CLI）在安装目录中运行该工具。

**目录示例：** `/Users/sschepis/Development/peer-reviewer`

### 命令

```bash
node dist/index.js "<path_to_paper_or_raw_text>"
```

### 参数

- `path_to_paper_or_raw_text`：论文或声明的文件路径（绝对路径或相对于包根目录的相对路径），或论文/声明的原始文本。

### 输出结果

该工具会以 JSON 格式输出一份“评审报告”，其中包含以下内容：
- `overallScore`（0-10 分）
- `defenseStrategy`（论文的辩护策略）
- `suggestions`（改进建议列表）
- `dimensions`（逻辑性、创新性等方面的评分）

## 示例

- **评审本地文件：**
  ```bash
cd /Users/sschepis/Development/peer-reviewer
node dist/index.js "/Users/sschepis/Desktop/research/draft_v1.txt"
```

- **评审原始声明：**
  ```bash
cd /Users/sschepis/Development/peer-reviewer
node dist/index.js "Claim: P=NP because I can solve Traveling Salesman in O(1) by guessing."
```

## 配置要求

确保根目录下存在 `google.json` 文件；或者如果在新的环境中运行，请设置 `GOOGLE_APPLICATION_CREDENTIALS` 环境变量。