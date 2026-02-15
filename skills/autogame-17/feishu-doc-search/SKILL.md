# Feishu 文档搜索

在 Feishu（Lark）驱动器中搜索文档。

## 使用方法

```bash
node skills/feishu-doc-search/index.js --query "keyword"
```

## 输出结果

返回一个包含找到的文档的 JSON 数组，其中包含文档的标识符（token）和文档的 URL。