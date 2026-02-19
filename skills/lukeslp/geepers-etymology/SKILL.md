---
name: geepers-etymology
description: 通过 dr.eamer.dev 的词源学和历时语言学 API，可以查询单词的词源、历史音变、语言家族树以及单词的演变过程。该 API 可用于语言历史研究、写作，或探索单词随时间的变化情况。
---
# Dreamer 的词源查询功能

您可以通过 `https://api.dr.eamer.dev` 访问词源查询和历史语言学数据。

## 认证

```bash
export DREAMER_API_KEY=your_key_here
```

## 终端点（Endpoints）

### 单词词源查询（Word Etymology）
```
GET https://api.dr.eamer.dev/v1/etymology/word?word=serendipity
```
返回单词的原始语言、词根、历史形态以及首次出现的记录。

### 探索单词历史（Explore Word History）
```
GET https://api.dr.eamer.dev/v1/etymology/explore?word=knight&lang=en
```
返回单词的完整词源链、相关词汇以及所属语言家族的信息。

### 音变规则（Diachronica）
```
GET https://api.dr.eamer.dev/v1/etymology/sound-changes?from=proto-indo-european&to=english
```
展示原始语言与其后代语言之间的语音变化记录。

## 使用场景：
- 研究单词的起源及其历史意义的变化
- 了解不同语言中的同源词
- 探索数百年来发音的变化情况
- 在需要深入词源分析的写作中使用该功能

## 不适用场景：
- 当您需要标准词典定义时（请使用词典 API）
- 当您需要查询非常新的词汇时（该数据主要针对已记录的历史形态）