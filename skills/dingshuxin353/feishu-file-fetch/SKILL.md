---
name: feishu_file_fetch
description: 实现了一个名为Clawdbot的扩展工具，该工具能够根据`message_id`和`file_key`下载Feishu文件，并将下载后的文件以SHA256哈希值进行加密存储到磁盘上。同时，该工具还设置了文件大小限制以及路径遍历保护机制。适用于用户需要构建或更新`feishu_file_fetch`工具、优化Feishu文件下载流程，或处理Clawdbot扩展程序中接收到的`message_id`/`file_key`输入的情况。
---

# feishu_file_fetch

## 快速入门

在 `scripts/feishu_file_fetch.py` 文件中创建或更新相应的实现代码。该代码需要满足以下要求：

1. 接受 JSON 格式的输入数据，格式如下：`{ message_id, file_key, type="file", outdir="/root/clawd/uploads", max_bytes=104857600 }`
2. 返回 JSON 格式的输出数据，内容如下：`{ ok, path, filename, bytes, sha256, error? }`
3. 使用 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 来获取并缓存 `tenant_access_token`（该令牌的有效期为 2 分钟）。
4. 通过以下 URL 下载文件：`https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources/{file_key}?type={type}`，并在请求头中添加 `Authorization: Bearer <token>` 来进行身份验证。
5. 将下载的文件内容写入 `outdir/yyyyMMdd/` 目录中；从 `Content-Disposition` 头字段中提取文件名；如果无法提取文件名，则使用默认的文件名 `file_key.bin`。
6. 在下载过程中计算文件的 sha256 哈希值；严格限制文件大小不超过 `max_bytes`（如果超过限制，则终止下载并删除临时文件）。
7. 确保最终文件路径位于 `outdir` 目录内，以防止路径遍历攻击。
8. 绝不要记录任何令牌或敏感信息。

## 运行时注意事项：

- 仅使用 Python 标准库（stdlib），以避免引入额外的依赖项。
- 如果文件的 `Content-Length` 超过 `max_bytes` 的限制，应立即终止下载。
- 成功下载后，使用 `os.replace` 函数删除临时文件。

## 示例用法

```
echo '{"message_id":"om_xxx","file_key":"file_xxx"}' | python scripts/feishu_file_fetch.py
```

## 额外资源

- 有关 API 的详细信息及错误处理规则，请参阅 [reference.md](reference.md)。