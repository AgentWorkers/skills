# 引语生成器

**版本：** 1.0.0  
**作者：** OpenClaw Evolution（周期号 #2597）

## 说明  
这是一个简单的工具，用于在代理的响应、报告或日志中插入鼓舞人心或技术性的引语。  
它有助于提升系统的“个性化”表现，同时打破机器人输出的单一性（即避免过于机械、缺乏情感的表达）。

## 使用方法  

### 获取随机引语（文本格式）  
```bash
node skills/quote-generator/index.js
```  

### 获取随机引语（JSON格式）  
```bash
node skills/quote-generator/index.js --format json
```  

### 将引语写入文件  
```bash
node skills/quote-generator/index.js --output /tmp/quote.txt
```