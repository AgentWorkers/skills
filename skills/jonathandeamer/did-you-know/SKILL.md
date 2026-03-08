---
name: did-you-know
description: 该工具会从英文维基百科的“你知道吗？”（“Did you know?”）板块中获取相关内容，将其缓存在本地，并以单条信息的形式展示给用户。使用该工具无需任何API密钥，同时也不会对维基百科的内容进行任何修改。
homepage: https://en.wikipedia.org/wiki/User:Jonathan_Deamer
metadata: {"openclaw":{"emoji":"❓","requires":{"bins":["python3"]}}}
---
# 你知道吗？

维基百科的[“你知道吗？”](https://en.wikipedia.org/wiki/Wikipedia:Did_you_know)板块精选了来自最近创建或更新的文章中的、来源可靠的事实。这些内容由志愿者们每天至少更新一次，为你提供了源源不断的聊天话题！

## 运行方式

### 打印一条事实：
```bash
```bash
python3 {baseDir}/scripts/dyk.py
```
```

### 如果没有新的事实可显示：
```bash
```
Did you know that heavy-metal guitarist Kiki Wong played drums for Taylor Swift before joining the Smashing Pumpkins?

https://en.wikipedia.org/wiki/Kiki_Wong
```
```

### 如果出现错误：
```bash
```
Something went wrong with the fact-fetching; please try again later.
```
```