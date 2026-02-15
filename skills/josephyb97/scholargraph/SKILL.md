{
  "name": "ScholarGraph",
  "description": "一个由人工智能驱动的工具包，可将学术文献转换为交互式的知识图谱，帮助研究人员发现知识之间的联系、追踪学术进展，并可视化研究领域的全貌。",
  "version": "1.0.0"
}

# ScholarGraph

ScholarGraph 是一个智能的学术研究辅助工具，可帮助您：

- **通过语义文献搜索发现相关论文**
- **从完整的 PDF 文档和摘要中提取关键见解**
- **利用动态知识图谱绘制知识关系**
- **通过自动化进度监控追踪研究趋势**
- **利用概念分析识别现有文献中的空白领域**

## 组件

- `literature-search`：在 arXiv、PubMed 和 Semantic Scholar 等数据库中查找论文
- `paper-analyzer`：从 PDF 文档中提取论文中的观点、方法和引用信息
- `knowledge-graph`：构建概念与论文之间的交互式网络
- `progress-tracker`：监控您所在领域的新出版物
- `concept-learner`：识别新兴的研究主题和空白领域

## 系统要求

- Python 3.9 或更高版本
- Node.js 18 或更高版本
- Semantic Scholar 或 arXiv 的 API 密钥（可选，但推荐使用）