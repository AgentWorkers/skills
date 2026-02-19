---
name: geepers-corpus
description: 查询 COCA（当代美国英语语料库）的语言学 API，以获取单词频率、搭配使用情况、共现关系以及历史使用趋势。该 API 可用于语言学研究、写作辅助，或了解单词在美国英语中的实际使用方式。
---
# Dreamer Corpus

您可以通过以下地址访问 COCA 语料库 API：`https://api.dr.eamer.dev`。

COCA 包含了超过 10 亿个单词，这些单词来自当代美国英语的口语、小说、杂志、报纸和学术文献。

## 认证

```bash
export DREAMER_API_KEY=your_key_here
```

## 端点（Endpoints）

### 单词搜索 / 词频统计（Word Search / Concordance）
```
GET https://api.dr.eamer.dev/v1/corpus/search?word=serendipity&limit=20
```
返回关键词-in-context (KWIC) 的示例，展示该单词在实际使用中的用法。

### 搭配词（Collocations）
```
GET https://api.dr.eamer.dev/v1/corpus/collocations?word=run&pos=verb&limit=20
```
返回与目标单词在统计上频繁共现的单词（包括共现频率 MI 和出现次数）。

### 单词频率（Frequency）
```
GET https://api.dr.eamer.dev/v1/corpus/frequency?word=algorithm&genre=academic
```
返回每百万单词中的单词出现频率，支持按类型过滤：`spoken`（口语）、`fiction`（小说）、`magazine`（杂志）、`newspaper`（报纸）或 `academic`（学术文献）。

## 使用场景
- 检查某个单词在现代美国英语中的正式程度或使用频率
- 查找有助于写作的自然搭配词
- 进行关于单词使用模式的语言学研究
- 分析几十年来的单词使用频率趋势

## 不适用场景
- 当您需要非英语语料库时
- 当您需要非当代美国英语的语料库时（COCA 的数据范围是 1990 年至今）