---
name: scihub-paper-downloader
description: "如何从 Sci-Hub 获取一个 DOI 对应的 PDF 链接？"
---
# Sci-Hub 论文下载器

给定一个 DOI（Digital Object Identifier），使用随附的 Python 脚本通过当前的 Sci-Hub 和 Sci-Net 流程来获取论文的直接 PDF 链接。

根据脚本的输出结果进行处理：
- 如果脚本返回一个 URL，则将该 URL 作为最终的 PDF 链接使用。
- 如果脚本返回 `NOT_FOUND`，且第二行以 `OA_LINK` 开头，则将该值视为 Sci-Hub 页面上显示的开放获取（OA）链接。该链接可能是出版社页面、仓库页面或其他非 PDF 的页面，而不是最终的 PDF 链接。
- 如果脚本返回 `NOT_FOUND` 且没有第二行，则说明 Sci-Hub 当前没有该论文。
- 如果脚本返回 `MIRROR_ERROR`，则表示无法可靠地访问 Sci-Hub，因此结果不确定。
- 如果脚本返回 `INVALID_INPUT`，则需要提供一个有效的 DOI。