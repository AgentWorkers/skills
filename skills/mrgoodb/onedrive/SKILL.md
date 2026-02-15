---
name: onedrive
description: 通过 Microsoft Graph 管理 OneDrive 文件和文件夹。可以上传、下载和共享文件。
metadata: {"clawdbot":{"emoji":"☁️","requires":{"env":["MICROSOFT_ACCESS_TOKEN"]}}}
---
# OneDrive  
微软的云存储服务。  

## 环境设置  
```bash
export MICROSOFT_ACCESS_TOKEN="xxxxxxxxxx"
```  

## 列出根目录下的文件  
```bash
curl "https://graph.microsoft.com/v1.0/me/drive/root/children" -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN"
```  

## 上传文件  
```bash
curl -X PUT "https://graph.microsoft.com/v1.0/me/drive/root:/filename.txt:/content" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary @localfile.txt
```  

## 下载文件  
```bash
curl "https://graph.microsoft.com/v1.0/me/drive/items/{itemId}/content" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN" -o downloaded.txt
```  

## 链接  
- 文档：https://docs.microsoft.com/en-us/graph/api/resources/onedrive