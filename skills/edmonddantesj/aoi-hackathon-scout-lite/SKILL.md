---
name: aoi-hackathon-scout-lite
version: 0.1.0
description: 公开安全的黑客马拉松源代码注册库 + 输出过滤功能（不支持爬取数据，也不接受用户提交代码）。
author: Aoineco & Co.
license: MIT
---
# AOI Hackathon Scout (Lite)

S-DNA: `AOI-2026-0215-SDNA-HACK01`

## 功能范围（公开安全）
- ✅ 为黑客马拉松、开发项目及资助申请提供精选的**资源列表**  
- ✅ 提供过滤功能：支持仅在线查看、按类型筛选资源  
- ✅ 为用户提供可直接复用的摘要模板  
- ❌ 不支持数据爬取、无需登录、无需填写表单，也不提供自动提交功能  
- ❌ 该工具仅使用 Notion 的文本模板功能（不涉及 API 接口）

## 数据来源  
- 该工具使用本地注册文件：`context/HACKATHON_SOURCES_REGISTRY.md`

## 命令  
### 显示所有资源  
```bash
aoi-hackathon sources
```

### 过滤资源（尽力提供最佳结果）  
```bash
# show only likely-online sources
# (filters Online-only fit = ✅ or ⚠️)
aoi-hackathon sources --online ok

# show only web3 sources
aoi-hackathon sources --type web3
```

### 从候选资源中推荐合适的资源  
```bash
# reads context/HACKATHON_SHORTLIST.md and prints top N online-eligible items
# (excludes rejected; prioritizes 🔥 markers and 'applying/watching')
aoi-hackathon recommend --n 5
```

### 打印 Notion 摘要模板（仅文本格式）  
```bash
aoi-hackathon template
```

## 技术支持  
- 如有疑问、错误或功能请求，请访问：https://github.com/edmonddantesj/aoi-skills/issues  
- 请在问题描述中注明工具的名称：`aoi-hackathon-scout-lite`

## 来源与原创性  
- AOI 的实现代码为原创代码；  
- 注册表中的链接列表经过精心筛选。