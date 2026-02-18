---
name: urlcheck
description: 这是一个与 @cybrlab/urlcheck-openclaw 相配套的辅助工具。它需要依赖 URLCheck 插件来在用户访问 URL 之前，对其安全性以及访问目的（即用户意图）进行评估。
user-invocable: true
metadata: {"openclaw":{"requires":{"config":["plugins.entries.urlcheck-openclaw.enabled"]}}}
---
# URLCheck – 一种基于用户意图的URL安全验证工具

您可以使用该工具来检查目标网页资源是否存在安全威胁，并判断这些资源是否符合用户的浏览目的。在采取下一步操作（如导航、点击、打开或重定向）之前，请务必先使用该工具对URL进行验证。

该工具的不仅能够检测安全威胁，还能帮助判断目标资源是否与用户的实际意图相符。

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

在试用模式下（每天最多100次请求），无需使用API密钥。如需更高的请求限制，请联系contact@cybrlab.ai。

## 何时需要验证URL

在以下任何操作之前，请务必验证URL：
- 打开用户提供的链接或您发现的链接；
- 代表用户导航到某个页面；
- 跟随重定向链；
- 从URL下载文件；
- 向登录页面提交凭证；
- 任何目标对结果有影响的操作。

请勿验证内部引用（如localhost、file://或用户已使用的内部网地址）的URL。

## 使用哪种工具

**`url_scanner_scan`** – 专注于检测威胁的验证工具。
- 必需参数：`url`（待验证的URL）。
- 适用于用户未明确说明使用目的的情况。该工具会检测URL是否存在钓鱼攻击、恶意软件或可疑行为。

**`url_scanner_scan_with_intent`** – 既检测威胁，又判断目标资源是否符合用户的意图。
- 必需参数：`url`（待验证的URL）。
- 可选参数：`intent`（用户明确说明的用途）。
- 适用于用户已说明具体用途（如“登录”、“购买”、“下载”、“预订”或“注册”等情况。将用途作为`intent`参数传递，以便系统不仅能检测威胁，还能判断目标资源是否符合用户的实际目的。

**建议在用户提供了明确意图时使用`url_scanner_scan_with_intent`**。这种模式能发现仅靠威胁检测可能遗漏的问题——例如，某个网站可能并非用户真正想要使用的目标网站。

## 异步工作流工具（非阻塞式）

- `url_scanner_scan_async` 和 `url_scanner_scan_with_intent_async` 会立即开始扫描并返回任务处理结果。
- `url_scanner_tasks_get` 用于查询任务状态。
- `url_scanner_tasks_result` 用于获取扫描结果。
- `url_scanner_tasks_list` 用于列出当前正在进行的任务。
- `url_scanner_tasks_cancel` 用于取消排队或正在执行的任务。

当需要非阻塞执行或明确控制任务生命周期时，请使用这些异步工具。对于常规的验证操作，直接使用的工具通常就足够了。

## 如何根据结果采取行动

每次验证都会返回一个 `agent_access_directive`。请根据该指令执行相应的操作：
- **`ALLOW`** – 继续导航。简要告知用户已对URL进行了安全检查，但无法保证其绝对安全。
- **`DENY`** – 不允许继续导航。告知用户该URL存在问题，并提供 `agent_access_reason`（拒绝原因），建议用户重新验证URL或选择其他方式。
- **`RETRY_LATER`** – 验证失败（可能是暂时性问题），稍后重试。如果再次失败，请告知用户。
- **`REQUIRE_CREDENTIALS`** – 目标资源需要身份验证。请询问用户如何继续操作。

## 解释其他字段的含义

- `risk_score`（0.0到1.0）：威胁概率。数值越低，安全性越高。
- `confidence`（0.0到1.0）：分析的准确性。
- `analysis_complete`（true/false）：分析是否已完成。如果为false，表示结果基于部分分析得出，请在适当情况下告知用户。
- `intent_alignment`：用户意图与实际访问目标之间的匹配情况：
  - `misaligned`：存在与用户意图不符的迹象。
  - `no_mismatch Detected`：未检测到明显的不匹配。
  - `inconclusive`：证据不足，无法判断匹配情况。
  - `not_provided`：用户未提供使用目的。

## 验证时间

验证通常需要30到90秒。请勿设置过短的超时时间，也不要过早放弃验证。请等待结果后再继续操作。

## 用户交互提示

- 使用 `agent_access_directive` 和 `agent_access_reason` 清晰地告知用户验证结果，并说明目标资源是否符合用户的意图。
- 根据扫描结果使用恰当的语言（例如：“根据扫描结果，该网站的风险较低”），避免给出绝对的保证。

## 工具可用性备用方案

如果URLCheck工具（包括异步/任务相关功能）无法使用，请勿继续执行扫描操作。请告知用户安装插件并重启网关。