---
name: toingg-create-campaign
description: 通过向 `toingg/make_campaign` API 发送用户提供的 JSON 数据来创建并启动 Toingg 语音通话活动。当 Codex 需要将活动详情（如标题、提示语、语调、通知设置、自动执行选项等）通过 `create_campaign.py` 辅助工具转换为实际的 Toingg 活动时，可以使用此方法。
---
# Toingg活动创建器

该技能使用`create_campaign.py`辅助工具将结构化的活动概要转换为Toingg活动，该工具会调用`https://prepodapi.toingg.com/api/v3/create_campaign`接口。所有活动参数均由用户提供；脚本仅负责处理身份验证和HTTP请求。

## 要求

1. **身份验证令牌**：在运行脚本之前，先导出`TOINGG_API_TOKEN`。
   ```bash
   export TOINGG_API_TOKEN="<bearer token>"
   ```
2. **有效载荷文件**：创建一个符合Toingg数据结构的JSON文件。可以使用`[`references/payload-template.md`](references/payload-template.md)`作为模板，并仅保留活动所需的字段。

## 工作流程

1. **从用户处收集活动信息**：包括活动标题、语音类型、语言、脚本内容/目的、语气、分析方案、通知设置、自动执行选项等。
2. 在工作区中起草有效载荷JSON文件（例如`campaign.json`）。从模板开始，自定义每个字段，并确保填写了必填项（如`title`、`voice`、`language`、`purpose`和`script`）。
3. **安全审查**：确保有效载荷文件中不包含除身份验证令牌之外的任何敏感信息。
4. **创建活动**：
   ```bash
   cd skills/toingg-create-campaign
   ./scripts/create_campaign.py /path/to/campaign.json > create-response.json
   ```
   脚本会打印API的JSON响应（成功对象或错误详情）。
5. **与用户确认结果**：分享`create-response.json`文件，告知新的活动ID或API返回的任何错误信息。

## 故障排除

- **401未经授权**：`TOINGG_API_TOKEN`环境变量缺失或已过期。请在Toingg控制台中刷新令牌并重新导出后，再运行脚本。
- **422/400错误**：有效载荷缺少必填字段或包含无效值。请查看`create-response.json`中的错误信息，并相应地修改JSON内容。
- **网络问题**：在确认网络连接正常后重新运行脚本。该脚本设置了60秒的超时时间；临时性的网络问题可以安全地重试。

## 扩展有效载荷

如果Toingg添加了新的活动字段，只需将这些字段添加到JSON有效载荷中即可——无需修改脚本。请确保更新参考模板，以便未来的操作员了解可用的设置选项。