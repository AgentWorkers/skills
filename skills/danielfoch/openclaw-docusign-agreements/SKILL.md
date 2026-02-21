---
name: openclaw-docusign-agreements
description: 通过使用 NanoPDF 检测签名区域，并自动插入 DocuSign 标签，将客户协议发送给客户进行签名。当用户需要使用 OpenClaw 工作流程来处理 PDF 协议（包括查找签名位置、识别签名者以及发送 DocuSign 文档）时，该功能非常实用，无需手动插入标签。
---
# OpenClaw 与 DocuSign 协议自动化处理

使用此技能，您可以在 OpenClaw 中自动化发送协议文件，并实现 NanoPDF 签名块的检测以及 DocuSign 信封的创建。

## 工作流程

### 1. 确认输入参数

收集以下信息：

- 协议 PDF 文件的路径
- 客户签名者列表（包括 `name`、`email`，可选的 `key` 和 `routing_order`）
- 电子邮件主题及可选的消息内容

请参考 `references/nano-pdf-signature-schema.md` 了解预期的 NanoPDF 输出格式，以及 `references/docusign-envelope-mapping.md` 以获取签名者与信封标签的映射规则。

### 2. 配置环境变量

设置必要的环境变量：

- `NANOPDF_BASE_URL`  
- `NANOPDF_API_KEY`  
- `DOCUSIGN_BASE_URL`（例如：`https://demo.docusign.net`）  
- `DOCUSIGN_ACCOUNT_ID`  
- `DOCUSIGN_ACCESS_TOKEN`  

可选参数：

- `NANOPDF_DETECT_PATH`（默认值：`/v1/signature-blocks`）  
- `DOCUSIGN_ENVELOPE_subject`  
- `DOCUSIGN_ENVELOPE_BODY`  

### 3. 检测签名块并发送信封

运行以下脚本：

```bash
python3 scripts/send_agreement.py \
  --pdf contracts/nda.pdf \
  --signers-json contracts/signers.json \
  --output-dir output/openclaw-agreements
```  

可选参数：

- `--subject`：覆盖 `DOCUSIGN_ENVELOPE_subject` 的值  
- `--message`：设置电子邮件的正文内容  
- `--status created`：将文件保存为草稿状态（默认为“已发送”）  
- `--scale 1.333333`：将 NanoPDF 中的点坐标转换为 DocuSign 的像素坐标  

脚本将执行以下操作：  
- 调用 NanoPDF 功能来检测签名块  
- 根据 `signer_key` 首先，再按照签名者的顺序，将每个签名块分配给相应的签名者  
- 在 DocuSign 中在检测到的坐标位置创建签名者标签  
- 创建信封（可选）并发送  
- 将生成的文件写入 `--output-dir` 目录中  

### 4. 发送前的验证

检查生成的文件：  
- `nanopdf_blocks.json`  
- `docusign_payload.json`  
- `envelope_result.json`  

如果签名者映射不明确，或者某个签名者没有对应的签名块，请在发送前要求用户明确提供正确的映射信息。

## 安全规则  

- 绝不要猜测收件人的电子邮件地址。  
- 如果检测到缺少签名块，请停止操作，除非用户明确同意采用手动处理方式。  
- 对于新模板或高风险的合同，请先使用 `--status created` 选项将文件保存为草稿状态。  
- 请将 API 密钥仅存储在环境变量中。  

## 参考资料  

- `references/nano-pdf-signature-schema.md`  
- `references/docusign-envelope-mapping.md`