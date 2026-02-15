---
name: hotjar
description: 通过 API 访问 Hotjar 的录制视频和热图数据，深入了解用户在您网站上的行为。
metadata: {"clawdbot":{"emoji":"🔥","requires":{"env":["HOTJAR_API_KEY","HOTJAR_SITE_ID"]}}}
---
# Hotjar  
行为分析工具  

## 环境设置  
```bash
export HOTJAR_API_KEY="xxxxxxxxxx"
export HOTJAR_SITE_ID="xxxxxxxxxx"
```  

## 查看录制数据  
```bash
curl "https://api.hotjar.com/v1/sites/$HOTJAR_SITE_ID/recordings" \
  -H "Authorization: Bearer $HOTJAR_API_KEY"
```  

## 获取录制文件  
```bash
curl "https://api.hotjar.com/v1/sites/$HOTJAR_SITE_ID/recordings/{recordingId}" \
  -H "Authorization: Bearer $HOTJAR_API_KEY"
```  

## 查看热力图  
```bash
curl "https://api.hotjar.com/v1/sites/$HOTJAR_SITE_ID/heatmaps" \
  -H "Authorization: Bearer $HOTJAR_API_KEY"
```  

## 查看调查问卷结果  
```bash
curl "https://api.hotjar.com/v1/sites/$HOTJAR_SITE_ID/surveys" \
  -H "Authorization: Bearer $HOTJAR_API_KEY"
```  

## 链接  
- 仪表板：https://www.hotjar.com  
- 文档：https://help.hotjar.com/hc/en-us/articles/360033640653-Hotjar-API