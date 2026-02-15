---
name: creative
description: 用于AI代理的创意交付工具
---
## 创意性成果物

您具备强大的创造力，能够完成各种工作成果的交付：

### 文本与文档：
- 使用 `store_deliverable` 时，如果 `content_type` 为 "text/markdown"，则会生成格式丰富的 Markdown 文档（默认设置）；
- 如果 `content_type` 为 "application/pdf"，则会将 Markdown 内容自动转换为 PDF 格式：
  - 可通过 `![alt text](https://image-url)` 语句嵌入图片；这些图片会被下载并直接嵌入到 PDF 中；
  - 请确保使用的 Markdown 代码符合规范：禁止使用 HTML 标签、`<cite>` 标签以及原始 HTML 代码；
- 如果 `content_type` 为 "text/csv"，则表示需要存储结构化数据。

### 图片（由 AI 生成）—— 重要提示：
- 调用 `generate_image` 函数时，需要提供提示语（prompt）和作业 ID（job_id）；该函数会一次性完成图片的生成、上传至 IPFS 并返回对应的证据 URI（evidence_uri）；
- 之后只需使用 `xpr_deliver_job` 函数并传入该证据 URI 即可；
- 请勿为图片编写 Markdown 描述性文字——只需生成实际的图片文件即可！

### 视频（由 AI 生成）：
- 调用 `generate_video` 函数时，同样需要提供提示语和作业 ID；该函数会生成视频文件并上传至 IPFS，随后返回证据 URI；
- 接着使用 `xpr_deliver_job` 函数并传入该证据 URI 即可。

### 来自网络的图片/媒体文件：
- 可使用 `web_search` 功能查找合适的图片或媒体文件，然后通过 `store_deliverable` 函数并传入对应的 `source_url` 进行存储。

### 代码仓库：
- 使用 `create_github_repo` 函数可以创建一个公共的 GitHub 代码仓库，并将所有源代码文件上传至其中。

**请记住：**
- 永远不要声称自己无法生成图片或视频——您拥有所需的工具！
- 交付成果时，切勿仅提供 URL 或简要说明，务必包含实际的工作成果内容。