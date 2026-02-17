---
name: browser-research-lite
description: >
  无需API密钥，即可通过内置的浏览器工具进行在线研究。  
  当由于缺少API密钥导致网络搜索失败，但您仍需要网络上的证据时，请使用此功能。
---
# Browser Research Lite

**目标：** 在无需使用 Brave/Tavily/Serper API 密钥的情况下，实现可靠的网页检索功能。

## 使用场景**

- 当 `web_search` 报告密钥或配置错误时（例如：`missing_brave_api_key`）。
- 需要查找事实性信息、定义、定理陈述或参考页面时。
- 在基准测试任务中需要外部证据，但远程搜索 API 不可用时。

## 核心原则**

- 对于可计算的问题，优先使用本地计算工具。
- 如果需要在线检索，直接使用内置的 `browser` 工具。
- 优先选择可信的来源（官方文档、教科书、大学网站；Wikipedia 作为备用）。
- 对于非显而易见的结论，至少核对两个来源。

## 浏览器使用流程**

1. 首先运行浏览器可用性检查：

```bash
python3 skills/browser-research-lite/scripts/browser_guard.py
```

2. 如果 `browser_available` 为 `False`，停止浏览器重试并切换到本地工具：
   - 如果 `browser_running` 为 `False` 或 `browser_cdp_ready` 为 `False`，手动启动浏览器：
     - 在安装了 OpenClaw 扩展程序的 Chrome 浏览器中打开任意页面，
     - 单击 OpenClaw 扩展程序图标以附加当前标签页，
     - 重新运行 `browser_guard.py`。
3. 如果 `browser_available` 为 `True`，使用简洁的查询词打开搜索页面。
4. 浏览搜索结果，选择 2-3 个高质量的来源。
5. 仅提取回答问题所需的最基本信息。
6. 如果页面内容杂乱无章，使用更精确的关键词重新查询。
7. 以简洁的理由给出最终答案；避免复制长段落。

## 备用方案**

- 如果浏览受到限制或需要频繁输入验证码，切换到其他域名并使用更简洁的查询词。
- 如果浏览器节点不可用，避免在同一问题中重复调用浏览器。
- 如果浏览器仍然无法使用，切换到 `skills/web-fetch-research-lite/SKILL.md`，并通过 `web_fetch` 进行 URL 基本的检索。
- 如果无法快速找到可靠的信息来源，返回尽力得出的答案，并标明不确定性。

## 记录改进事项**

当该功能有助于提升基准测试成绩时，记录以下内容：
- 触发该功能的信号（trigger signal）；
- 来源的质量及检索步骤；
- 对基准测试分数/准确性的实际影响。