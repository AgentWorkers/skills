---
name: did-you-know
description: 该工具会从英文版的维基百科中获取“你知道吗？”（“Did you know?”）板块中的信息，将其缓存到本地，然后逐一展示给用户。使用该工具无需任何API密钥，也不会对维基百科的内容进行任何修改。
homepage: https://en.wikipedia.org/wiki/User:Jonathan_Deamer
metadata: {"openclaw":{"emoji":"❓","requires":{"bins":["python3"]}}}
---
# 你知道吗？

维基百科的[“你知道吗？”](https://en.wikipedia.org/wiki/Wikipedia:Did_you_know)板块精选了来自最新创建或扩展文章的、有可靠来源的事实。这些内容由志愿者定期（至少每天一次）进行整理和更新，为人们提供了源源不断的聊天话题！

## 运行

```bash
python3 {baseDir}/scripts/dyk.py
```

打印一条事实：

```
Did you know that the shortest war in history lasted 38 minutes?

https://en.wikipedia.org/wiki/Anglo-Zanzibar_War
```

如果没有新的钩子（hooks）可用：

```
No more facts to share today; check back tomorrow!
```

如果出现错误：

```
Something went wrong with the fact-fetching; please try again later.
```