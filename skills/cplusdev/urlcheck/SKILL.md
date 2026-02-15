---
name: urlcheck
description: 这是一个为 @cybrlab/urlcheck-openclaw 提供的辅助技能。它需要使用 URLCheck 插件工具来在用户访问 URL 之前，对其安全性以及访问意图进行评估。
user-invocable: true
metadata: {"openclaw":{"requires":{"config":["plugins.entries.urlcheck-openclaw.enabled"]}}}
---

# URLCheck – 一种基于用户意图的URL安全验证工具

您可以使用该URL验证系统来检查目标网页资源是否存在安全威胁，并判断这些资源是否与用户的浏览目的相符。在采取下一步操作（如导航、点击、打开或重定向）之前，请务必先使用该工具对URL进行验证。

该工具的目的不仅在于检测潜在的安全风险，还在于帮助判断目标资源是否真正符合用户的实际需求。

## 快速入门（用户指南）

1. 安装插件并重启网关：
   ```bash
openclaw plugins install @cybrlab/urlcheck-openclaw
openclaw gateway restart
```

2. 验证插件及功能是否正常：
   ```bash
openclaw plugins list | grep -i urlcheck
openclaw skills list | grep -i urlcheck
```

3. 立即尝试使用该工具：
   ```text
Before opening https://example.com, run url_scanner_scan_with_intent with intent "log in to my account" and tell me whether I should proceed.
```

在试用模式下（每天最多100次请求），无需使用API密钥。如需增加请求次数，请联系contact@cybrlab.ai。

## 何时需要验证URL？

在以下任何操作之前，请务必验证URL：
- 打开用户提供的链接或您发现的链接；
- 代表用户导航到某个页面；
- 跟随重定向链；
- 从URL下载文件；
- 向登录页面提交凭证；
- 任何目标对最终结果有影响的操作。

请注意：不要验证内部引用（如localhost、file://或用户已使用的内部网地址）。

## 选择合适的工具

**`url_scanner_scan`** – 专注于检测威胁的验证工具。
- 必需参数：`url`（待验证的URL）。
- 适用于用户未明确说明使用目的的情况。该工具会检查URL是否存在网络钓鱼、恶意软件或可疑行为。

**`url_scanner_scan_with_intent`** – 除了检测威胁外，还会判断目标资源是否符合用户的意图。
- 必需参数：`url`（待验证的URL）。
- 可选参数：`intent`（用户明确表达的目的，例如“登录”、“购买”、“下载”、“预订”等）。
- 在用户提供了具体目的时使用该工具，系统会同时判断目标资源是否符合用户意图以及是否存在安全风险。

**建议在用户提供明确目的时优先使用`url_scanner_scan_with(intent`**，因为这种模式能发现仅靠威胁检测可能遗漏的问题（例如，某个网站可能并非用户真正想要使用的目标网站）。

## 根据验证结果采取相应行动

每次验证都会返回一个`agent_access_directive`，请根据该指令进行操作：
- **`ALLOW`** – 继续导航。简要告知用户已对URL进行了安全检查，但无法保证其绝对安全。
- **`DENY`** – 不允许继续导航。告知用户URL已被标记为存在风险，并提供`agent_access_reason`（拒绝原因），建议用户重新验证URL或选择其他方式。
- **`RETRY_LATER`** – 验证过程中出现临时问题，请稍后重试。如果仍失败，请告知用户。
- **`REQUIRE_CREDENTIALS`** – 目标资源需要用户身份验证。在继续操作前，请询问用户如何处理。

## 解释其他返回字段：

- `risk_score`（0.0至1.0）：威胁概率。数值越低，安全性越高。
- `confidence`（0.0至1.0）：分析的准确性。
- `analysis_complete`（true/false）：分析是否完成。如果为false，说明结果基于部分分析得出，请在必要时告知用户。

## 验证耗时

验证通常需要30至90秒。请勿设置过短的超时时间，也不要过早放弃验证。请等待结果后再进行下一步操作。

## 与用户的沟通方式：

- 使用`agent_access_directive`和`agent_access_reason`清晰地告知验证结果，并说明目标资源是否与用户的意图相符。
- 根据扫描结果使用恰当的表述（例如：“根据分析，该URL的风险较低”），避免给出绝对的保证。

## 工具可用性备用方案

如果`url_scanner_scan`或`url_scanner_scan_with_intent`无法使用，请告知用户安装插件并重启网关。