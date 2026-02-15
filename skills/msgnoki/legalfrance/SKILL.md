---
name: legalfrance
description: "法国法律辅助工具 RAG，专注于法典和综合法律（LEGI/DILA）。可用于查询法国法律问题、查找相关条文、解释法律文本，并提供可核实的法律条文引用及法律综述。"
---

# LegalFrance

这是一个基于混合检索技术（FTS + 向量方法）的法语法律辅助工具，能够提供相关文章的引用。

## 首次使用 — 初始化数据库

如果索引文件缺失（`data/chroma_db` 或 `data/fts_index.db` 不存在），**在执行操作前请先获取用户的确认**：

```bash
python scripts/ingest.py
```

⚠️ 此步骤会下载 HuggingFace 提供的 LEGI 数据集以及 BGE-M3 嵌入模型（总大小约为 2 Go），并将索引文件写入磁盘。根据网络连接速度，预计耗时 20–40 分钟。

提示：*“初始化操作将下载约 2 Go 的数据（法律语料库 + 模型）。是否确认？”*

## 使用方法

- 提出法律问题：

```bash
python scripts/one_shot.py "<question>"
```

- 以结构化 JSON 格式输入问题：

```bash
python scripts/one_shot.py "<question>" --json
```

- 对法律条文进行直接搜索：

```bash
python scripts/search.py "<requête>" 5
```

## 回答规则：

- 仅引用在索引中找到的来源资料；
- 绝不允许编造任何文章或法律判决的内容；
- 如果找不到足够的参考资料，必须明确说明；
- 建议的回答格式为：**原则 → 适用情况 → 限制条件 → 参考来源**；
- 回答末尾必须添加免责声明（仅提供一般性信息，不提供个性化法律建议）。

## 法律判例模块（可选）

`search_jurisprudence` 模块（包含最高法院/国务委员会的判例数据）为可选配置。
如果该模块未安装，该工具将仅针对法律条文提供查询服务。