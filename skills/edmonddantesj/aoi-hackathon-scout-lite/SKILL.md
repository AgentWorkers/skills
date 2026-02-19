---
name: aoi-hackathon-scout-lite
version: 0.1.6
description: 公开安全的黑客马拉松源代码注册库 + 输出过滤功能（禁止爬取数据、禁止提交代码）。
author: Aoineco & Co.
license: MIT
---
# AOI Hackathon Scout (Lite)

S-DNA: `AOI-2026-0215-SDNA-HACK01`

## 快速入门（复制/粘贴）
```bash
# 1) install
clawhub install aoi-hackathon-scout-lite

# 2) shortlist view / best-effort recommendations
# (reads context/HACKATHON_SHORTLIST.md)
aoi-hackathon recommend --n 5

# 3) browse sources (no API keys)
aoi-hackathon sources
openclaw browser start
openclaw browser open https://devpost.com/c/artificial-intelligence
openclaw browser snapshot --efficient
```

## 功能范围（公开安全）
- ✅ 为黑客马拉松、开发项目或资助申请提供精选的**项目来源列表**  
- ✅ 提供筛选功能：支持仅在线查看、按类型标签筛选  
- ✅ 为用户提供可直接粘贴的摘要模板  
- ❌ 不支持爬取数据、无需登录、无需填写表单，也不提供自动提交功能  
- ❌ 该技能不使用 Notion API（仅提供可粘贴的摘要模板）  

## 数据来源  
- 使用本地注册文件：  
  - `context/HACKATHON_SOURCES_REGISTRY.md`  

## 命令  
### 显示项目来源  
```bash
aoi-hackathon sources
```

### 筛选项目（尽力提供最佳结果）  
```bash
# show only likely-online sources
# (filters Online-only fit = ✅ or ⚠️)
aoi-hackathon sources --online ok

# show only web3 sources
aoi-hackathon sources --type web3
```

### 从候选列表中推荐项目（尽力提供最佳结果）  
```bash
# reads context/HACKATHON_SHORTLIST.md and prints top N online-eligible items
# (excludes rejected; prioritizes 🔥 markers and 'applying/watching')
aoi-hackathon recommend --n 5
```

### 打印 Notion 摘要模板（仅文本格式）  
```bash
aoi-hackathon template
```

## 设置（早期用户）  
该技能默认为**公开安全**模式，无需使用 API 密钥。  

### 推荐的默认设置：使用浏览器（无需密钥）  
- 使用 OpenClaw 浏览器查看项目详情及截止日期。  
- 快速入门步骤：  
  ```bash
  openclaw browser start
  openclaw browser open https://devpost.com/c/artificial-intelligence
  openclaw browser snapshot --efficient
  ```

### 可选：Brave Search API（快速关键词搜索）  
如需超快速度的关键词搜索，可启用 Brave Search 功能：  
- 获取 API 密钥：https://brave.com/search/api/（选择 **Data for Search** 计划）  
- 配置方法：  
  ```bash
  openclaw config set tools.web.search.provider brave
  openclaw config set tools.web.search.apiKey "BRAVE_API_KEY_HERE"
  openclaw config set tools.web.search.enabled true
  ```  
- 取消启用：  
  ```bash
  openclaw config set tools.web.search.enabled false
  ```  
（完整设置指南请参见仓库文件：`context/HACKATHON_SEARCH SETUP_GUIDE_V0_1.md`）  

## 技术支持  
- 如有疑问、遇到问题或需要帮助，请访问：  
  https://github.com/edmonddantesj/aoi-skills/issues  
- 请在问题描述中注明技能名称：`aoi-hackathon-scout-lite`  

## 来源与原创性  
- AOI 功能的实现代码为原创代码；  
- 注册表中的项目链接列表经过精心筛选。