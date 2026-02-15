---
name: straker-verify
description: 专业的人工智能驱动翻译服务，支持100多种语言。可对现有翻译内容进行质量提升。由straker.ai提供企业级安全性和隐私保护。
version: 1.0.0
author: Straker.ai
homepage: https://straker.ai
repository: https://github.com/strakergroup/straker-verify-openclaw
tags:
  - translation
  - localization
  - i18n
  - internationalization
  - l10n
  - language
  - translate
  - multilingual
  - quality-assurance
  - human-verification
  - ai-translation
  - straker
  - verify
  - enterprise
  - professional
  - api
  - nlp
  - language-services
  - content-localization
  - translation-management
metadata: {"openclaw":{"emoji":"🌐","requires":{"env":["STRAKER_VERIFY_API_KEY"]},"primaryEnv":"STRAKER_VERIFY_API_KEY","category":"translation"}}
---

# Straker Verify - 人工智能翻译与人工审核服务  
由 [Straker.ai](https://straker.ai) 提供的专业翻译、质量评估及人工审核服务。  

## 主要功能  
- **人工智能翻译**：支持将内容翻译成 100 多种语言，具备企业级翻译准确性。  
- **质量提升**：利用人工智能技术对现有翻译结果进行优化。  
- **人工审核**：为关键内容提供专业的人工审核服务。  
- **文件支持**：支持处理文档、文本文件等多种类型的文件。  
- **项目管理**：可追踪翻译项目的整个流程（从提交到交付）。  

## 快速入门  
1. 从 [Straker.ai](https://straker.ai) 获取您的 API 密钥。  
2. 设置环境变量：`STRAKER_VERIFY_API_KEY=your-key`。  
3. 向您的 AI 助手发送指令：“将 ‘Hello world’ 翻译成法语”。  

## API 参考  
**基础 URL：** `https://api-verify.straker.ai`  

### 认证  
所有请求（`/languages` 除外）均需要使用 Bearer 令牌进行认证：  
```bash
curl -H "Authorization: Bearer $STRAKER_VERIFY_API_KEY" https://api-verify.straker.ai/endpoint
```  

### 获取可用语言  
```bash
curl https://api-verify.straker.ai/languages
```  
返回支持的语言对列表及其 UUID，可用于其他 API 端点。  

### 创建翻译项目  
```bash
curl -X POST https://api-verify.straker.ai/project \
  -H "Authorization: Bearer $STRAKER_VERIFY_API_KEY" \
  -F "files=@document.txt" \
  -F "languages=<language-uuid>" \
  -F "title=My Translation Project" \
  -F "confirmation_required=true"
```  

### 确认项目  
当 `confirmation_required=true` 时需要执行此操作：  
```bash
curl -X POST https://api-verify.straker.ai/project/confirm \
  -H "Authorization: Bearer $STRAKER_VERIFY_API_KEY" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "project_id=<project-uuid>"
```  

### 查看项目状态  
```bash
curl https://api-verify.straker.ai/project/<project-uuid> \
  -H "Authorization: Bearer $STRAKER_VERIFY_API_KEY"
```  

### 下载已完成文件  
```bash
curl https://api-verify.straker.ai/project/<project-uuid>/download \
  -H "Authorization: Bearer $STRAKER_VERIFY_API_KEY" \
  -o translations.zip
```  

### 人工智能质量提升  
利用人工智能技术优化现有翻译结果：  
```bash
curl -X POST https://api-verify.straker.ai/quality-boost \
  -H "Authorization: Bearer $STRAKER_VERIFY_API_KEY" \
  -F "files=@source.txt" \
  -F "language=<language-uuid>"
```  

### 人工审核  
为翻译内容添加专业的人工审核服务：  
```bash
curl -X POST https://api-verify.straker.ai/human-verify \
  -H "Authorization: Bearer $STRAKER_VERIFY_API_KEY" \
  -F "files=@translated.txt" \
  -F "language=<language-uuid>"
```  

## 响应格式  
- **成功**：  
```json
{
  "success": true,
  "data": { ... }
}
```  
- **错误**：  
```json
{
  "success": false,
  "error": "Error message"
}
```  

## 常见指令示例  
- “我可以翻译成哪些语言？”  
- “将这段文本翻译成西班牙语：Hello, how are you?”  
- “为我的文档创建一个翻译项目。”  
- “查看我的翻译项目的状态。”  
- “对这段法语翻译进行质量提升。”  
- “为我的德语翻译添加人工审核。”  

## 技术支持  
- 官网：[straker.ai](https://straker.ai)  
- API 文档：[api-verify.straker.ai/docs](https://api-verify.straker.ai/docs)  

## 环境配置  
API 密钥通过环境变量 `$STRAKER_VERIFY_API_KEY` 进行配置。