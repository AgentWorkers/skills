---
name: kagi
description: 当您需要比Brave/Google更高质量的结果，或者Brave Search受到速率限制时，可以使用Kagi API（搜索API + FastGPT）进行网络搜索。触发命令包括：“search with Kagi”、“Kagi search”、“use FastGPT”、“Kagi FastGPT”、“Kagi summarize”，或者当您希望通过Kagi的API令牌进行程序化网络搜索时。
---

# Kagi（API）

可以使用随附的Python脚本从OpenClaw主机调用Kagi的API。

## 快速入门

1) 在https://kagi.com/settings/api创建一个令牌。
2) 将该令牌导出到您的shell或会话中：

```bash
export KAGI_API_TOKEN='…'
```

3) 运行搜索：

```bash
python3 scripts/kagi_search.py "haaps glass" --limit 10 --json
```

4) 或者使用FastGPT（大型语言模型 + 网页搜索）：

```bash
python3 scripts/kagi_fastgpt.py "Summarize the latest Haaps glass mentions" --json
```

## 任务

### 1) 网页搜索（Kagi搜索API）

当您需要一个常规的排名结果列表（URL/标题/片段）时，请使用此API。

命令：

```bash
python3 scripts/kagi_search.py "<query>" [--limit N] [--json]
```

注意：
- 默认情况下会输出易于阅读的摘要；使用`--json`选项可获取原始API输出。
- 脚本会自动设置`Authorization: Bot <token>`。

### 2) 基于网页结果提供答案/总结（FastGPT）

当您希望获得包含引用URL的简短答案时，请使用此API。

命令：

```bash
python3 scripts/kagi_fastgpt.py "<question>" [--cache true|false] [--json]
```

### 3) 将Kagi作为网页搜索的替代方案

如果Brave Search受到速率限制（429错误），或者您希望获得更好的搜索结果：
- 使用`scripts/kagi_search.py`来获取结果。
- 然后使用主代理模型根据返回的URL/片段进行合成或总结。

## 文件

- API参考文档：`references/kagi-api.md`
- Python客户端及命令行工具：`scripts/kagi_client.py`, `scripts/kagi_search.py`, `scripts/kagi_fastgpt.py`