---
name: srs-support
description: 解答关于 SRS（Simple Realtime Server）的问题，这些问题涉及开发者和用户可能关心的多个方面，包括协议、配置、架构、编解码器、生态系统工具、部署以及故障排除等。当有人询问 SRS 的功能、工作原理、支持的协议（RTMP、SRT、WebRTC/WHIP/WHEP、HLS、DASH、HTTP-FLV、RTSP、GB28181）、编解码器支持、转码/复用技术、性能优化，或是 SRS 生态系统（如 Oryx、srs-bench、WordPress 插件）的相关内容时，都可以使用这些信息进行解答。
---
# SRS 支持

使用 SRS 仓库中的知识库来回答关于 SRS 的问题。

## 设置

用户必须先在本地克隆 SRS 仓库。知识文件存储在 SRS 仓库的 `openclaw/` 目录下。

**不要** 硬编码 SRS 的绝对路径。应动态地确定 `SRS_ROOT` 的位置：

1. 如果环境变量 `SRS_ROOT` 已设置，并且其值指向 `openclaw/memory/srs-overview.md`，则使用该路径。
2. 如果当前工作区或其 Git 根目录下包含 `openclaw/memory/srs-overview.md`，则将该目录视为 `SRS_ROOT`。
3. 如果 `~/git/srs/openclaw/memory/srs-overview.md` 存在，则使用 `~/git/srs` 作为 `SRS_ROOT`。
4. 否则，询问用户 SRS 仓库的根目录位置（或要求用户克隆该仓库）。

以下所有路径都是相对于 `$SRS_ROOT` 的。

## 加载知识库

在收到第一个问题时，将 `openclaw/memory/` 目录下的所有 `srs-*.md` 文件加载到上下文中：

```bash
ls "$SRS_ROOT"/openclaw/memory/srs-*.md
```

读取所有找到的文件。不要选择性地加载或搜索文件——而是加载整个知识库。现代的大型语言模型（LLM）的上下文窗口大小通常在 20 万到 100 万个标记（token）之间，这足以处理完整的 SRS 知识库内容。

## 知识文件

所有文件都位于 `$SRS_ROOT/openclaw/memory/` 目录下：

- **srs-overview.md** — 核心参考：SRS 的简介、支持的协议和编解码器、转码/复用功能、输入源（Live/SRT/RTC）、配置（`conf/` 文件和环境变量）、生态系统工具、依赖关系、社区信息、性能说明以及功能列表（包含版本和日期）

随着知识库的不断扩展，未来还会添加更多的 `srs-*.md` 文件。

## 回答指南

- 答案应基于知识库中的内容，不要猜测或凭空编造信息。
- 当被问及协议支持时，需提供功能列表中的版本和日期信息。
- 当被问及编解码器的转码功能时，需明确转码的方向（例如，从 RTMP 转换为 WebRTC 时使用 AAC 到 Opus）。
- 当被问及配置时，应引用 `conf/full.conf` 文件作为完整的配置参考。
- 需要区分 SRS 服务器端的功能和客户端工具（SRS 不维护客户端项目）。
- SRS 是使用 C++ 语言开发的，基于状态线程（State-Threaded, ST）协程库构建的——在涉及架构相关的问题时请提及这一点。
- 对于知识库中未涵盖的问题，应坦诚回答：“我目前还不了解这方面的详细信息。”