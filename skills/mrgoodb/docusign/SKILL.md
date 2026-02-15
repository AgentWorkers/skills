---
name: docusign
description: 通过 DocuSign API 发送文档以进行电子签名。创建电子签名信封，跟踪签名进度，并下载已签名的文档。
metadata: {"clawdbot":{"emoji":"✍️","requires":{"env":["DOCUSIGN_ACCESS_TOKEN","DOCUSIGN_ACCOUNT_ID"]}}}
---

# DocuSign

电子签名服务。

## 环境配置

```bash
export DOCUSIGN_ACCESS_TOKEN="xxxxxxxxxx"
export DOCUSIGN_ACCOUNT_ID="xxxxxxxxxx"
export DOCUSIGN_BASE="https://demo.docusign.net/restapi"  # Use na1.docusign.net for prod
```

## 发送文档以获取签名

```bash
curl -X POST "$DOCUSIGN_BASE/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes" \
  -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "emailSubject": "Please sign this document",
    "documents": [{
      "documentBase64": "'$(base64 -w0 document.pdf)'",
      "name": "Contract.pdf",
      "documentId": "1"
    }],
    "recipients": {
      "signers": [{
        "email": "signer@example.com",
        "name": "John Doe",
        "recipientId": "1",
        "tabs": {"signHereTabs": [{"documentId": "1", "pageNumber": "1", "xPosition": "100", "yPosition": "700"}]}
      }]
    },
    "status": "sent"
  }'
```

## 查看待签名的文档列表

```bash
curl "$DOCUSIGN_BASE/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes?from_date=2024-01-01" \
  -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN"
```

## 查看文档的签名状态

```bash
curl "$DOCUSIGN_BASE/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes/{envelope_id}" \
  -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN"
```

## 下载已签名的文档

```bash
curl "$DOCUSIGN_BASE/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes/{envelope_id}/documents/combined" \
  -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN" \
  -o signed_document.pdf
```

## 链接：
- 控制台：https://apps.docusign.com
- 文档中心：https://developers.docusign.com