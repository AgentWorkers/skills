---
name: evernote
description: 通过 Evernote API 管理笔记、笔记本和标签。可以编程方式创建、搜索和组织笔记。
metadata: {"clawdbot":{"emoji":"🐘","requires":{"env":["EVERNOTE_ACCESS_TOKEN"]}}}
---
# Evernote  
用于笔记记录与信息管理。  
## 环境配置  
```bash
export EVERNOTE_ACCESS_TOKEN="xxxxxxxxxx"
export EVERNOTE_BASE="https://www.evernote.com/shard/s1/notestore"
```  
## 列出笔记本  
```bash
curl "$EVERNOTE_BASE/listNotebooks" -H "Authorization: Bearer $EVERNOTE_ACCESS_TOKEN"
```  
## 创建笔记  
```bash
curl -X POST "$EVERNOTE_BASE/createNote" \
  -H "Authorization: Bearer $EVERNOTE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Note", "content": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\"><en-note>Hello World</en-note>"}'
```  
## 链接  
- 文档：https://dev.evernote.com