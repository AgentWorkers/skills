---
name: pinchtab
description: 通过 Pinchtab 的 HTTP API 来控制无头或有头的 Chrome 浏览器。该 API 可用于网页自动化、数据抓取、表单填写、导航以及多标签页操作。Pinchtab 会将浏览器的可访问性树（accessibility tree）以结构化的 JSON 格式提供，其中包含稳定的引用信息，非常适合人工智能代理使用（低请求成本、快速响应）。适用于以下场景：浏览网站、填写表单、点击按钮、提取页面文本、截图，或任何基于浏览器的自动化任务。使用前需确保 Pinchtab 服务已启动（需要运行其 Go 语言编写的二进制程序）。
homepage: https://pinchtab.com
metadata:
  openclaw:
    emoji: "🦀"
    requires:
      bins: ["pinchtab"]
      env:
        - name: BRIDGE_TOKEN
          secret: true
          optional: true
          description: "Bearer auth token for Pinchtab API"
        - name: BRIDGE_PORT
          optional: true
          description: "HTTP port (default: 9867)"
        - name: BRIDGE_HEADLESS
          optional: true
          description: "Run Chrome headless (true/false)"
---
# Pinchtab

这是一个专为AI代理设计的快速、轻量级的浏览器控制工具，通过HTTP协议和页面的可访问性树（accessibility tree）来实现交互。

**安全提示：** Pinchtab在您的控制下运行一个本地的Chrome浏览器。它不会访问您的凭据、泄露数据或连接到外部服务。所有操作都仅在本地进行，除非您明确地导航到外部网站。Pinchtab的二进制文件通过[GitHub发布](https://github.com/pinchtab/pinchtab/releases)进行分发，并附带校验和（checksum）。有关完整的安全模型和VirusTotal标志说明，请参阅[TRUST.md]。

## 快速入门（代理工作流程）

浏览器任务的30秒操作流程如下：

```bash
# 1. Start Pinchtab (runs forever, local on :9867)
pinchtab &

# 2. In your agent, follow this loop:
#    a) Navigate to a URL
#    b) Snapshot the page (get refs like e0, e5, e12)
#    c) Act on a ref (click e5, type e12 "search text")
#    d) Snapshot again to see the result
#    e) Repeat step c-d until done
```

**就这么简单。** 所有的引用（refs）都是稳定的，无需在每次操作前都重新生成快照。只有在页面发生显著变化时才需要重新生成快照。

## 设置

```bash
# Headless (default) — no visible window
pinchtab &

# Headed — visible Chrome window for human debugging
BRIDGE_HEADLESS=false pinchtab &

# With auth token
BRIDGE_TOKEN="your-secret-token" pinchtab &

# Custom port
BRIDGE_PORT=8080 pinchtab &

# Dashboard/orchestrator — profile manager + tab launcher
pinchtab dashboard &
```

默认设置：端口9867，无需身份验证（仅限本地使用）。如需远程访问，请设置`BRIDGE_TOKEN`。

有关高级设置的详细信息，请参阅[references/profiles.md](references/profiles.md)和[references/env.md](references/env.md)。

## 快照的生成方式

调用 `/snapshot` 后，您会得到页面的可访问性树数据，以JSON格式返回——这是一个包含元素及其引用信息的扁平列表：

```json
{
  "refs": [
    {"id": "e0", "role": "link", "text": "Sign In", "selector": "a[href='/login']"},
    {"id": "e1", "role": "textbox", "label": "Email", "selector": "input[name='email']"},
    {"id": "e2", "role": "button", "text": "Submit", "selector": "button[type='submit']"}
  ],
  "text": "... readable text version of page ...",
  "title": "Login Page"
}
```

然后您可以根据这些引用执行相应的操作：`click e0`（点击元素e0）、`type e1 "user@example.com"`（在元素e1中输入文本“user@example.com”）、`press e2 Enter`（按Enter键）。

## 核心工作流程

典型的代理工作流程包括：
1. **导航** 到目标URL
2. **生成页面的可访问性树快照**（获取引用信息）
3. **根据引用信息执行操作**（如点击、输入文本、按键）
4. **再次生成快照** 以查看操作结果

每次生成快照后，引用信息（如`e0`、`e5`、`e12`）会保存在对应的标签页中——除非页面发生显著变化，否则无需在每次操作前都重新生成快照。

### 示例代码

有关完整的HTTP API接口（包括curl请求示例、文件下载/上传、cookie处理、批量操作等功能），请参阅[references/api.md](references/api.md)。

## 令牌使用指南

| 方法                | 通常需要的令牌数量 | 使用场景                |
|------------------|------------------|----------------------|
| `/text`            | 约800个令牌        | 读取页面内容              |
| `/snapshot?filter=interactive` | 约3,600个令牌        | 查找可点击的按钮/链接          |
| `/snapshot?diff=true`     | 令牌数量因操作而异     | 多步骤操作（仅获取变化部分）         |
| `/snapshot?format=compact` | 减少约56-64%的令牌消耗 | 每个节点仅输出一行信息，效率最高       |
| `/snapshot`          | 约10,500个令牌        | 获取页面的完整信息            |
| `/screenshot`        | 约2,000个令牌        | 用于页面的视觉验证            |

**使用建议：**  
- 首先使用`?filter=interactive&format=compact`进行快照生成；  
- 对于后续操作，可以使用`?diff=true`来获取仅有的变化部分；  
- 仅当需要获取可读内容时，才使用`/text`方法；  
- 仅在必要时才使用完整的`/snapshot`方法。

## 代理优化

**2026年2月验证结果：** 通过AI代理的测试发现了一种能够提高令牌使用效率的优化方法。

**查看完整指南：** [docs/agent-optimization.md](../../docs/agent-optimization.md)

### 总结

**3秒操作流程：** 在导航后等待一段时间再生成快照：

```bash
curl -X POST http://localhost:9867/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' && \
sleep 3 && \
curl http://localhost:9867/snapshot | jq '.nodes[] | select(.name | length > 15) | .name'
```

**令牌节省效果：** 与探索式代理方法相比，使用这种优化方案可以节省93%的令牌消耗（从3,842个令牌减少到272个令牌）。

有关详细优化策略、系统提示模板以及特定网站的注意事项，请参阅[docs/agent-optimization.md](../../docs/agent-optimization.md)。

## 使用技巧：
- 在处理多个标签页时，务必明确传递`tabId`参数。
- 快照生成后，引用信息是稳定的，因此点击操作前无需重新生成快照。
- 在导航或页面发生重大变化后，需要重新生成快照以获取最新的引用信息。
- Pinchtab会保留会话状态——重启后标签页的内容仍然保留（可通过`BRIDGE_NO_RESTORE=true`禁用此功能）。
- Chrome的配置文件会持续保存——cookie和登录信息会在多次运行之间保持一致。
- 对于以读取为主的操作，可以使用`BRIDGE_BLOCK IMAGES=true`或`"blockImages": true`来禁用图片显示。
- **导航后至少等待3秒再生成快照**：Chrome需要时间来渲染页面上的2000多个可访问性树节点。