---
name: githunt
description: 根据地理位置、技术背景和职位对 GitHub 开发者进行筛选和排名。可以搜索合适的候选人，并查看他们的个人资料（包括所使用的技术栈、活跃度以及联系方式）。
version: 1.0.0
author: mordka
---

# GitHunt - 一款用于发现 GitHub 开发者的工具

通过地理位置、技术栈和角色来查找 GitHub 上的顶尖开发者。系统会对候选人进行评分并排名，同时提供详细的个人资料。

**官方网站：** https://githunt.ai

## 使用场景

- 在特定地点寻找开发者/候选人  
- 搜索使用特定技术栈的开发者  
- 招聘/寻找工程师  
- 建立人才招聘流程  

## API 端点  

基础 URL：`https://api.githunt.ai/v1`  

### 搜索开发者（实时流式返回结果） - 主要 API 端点  

该端点会实时返回搜索结果。免费提供前 10 个候选人的示例信息。  

**请求参数：**  
| 参数 | 是否必填 | 描述 |  
|-------|----------|-------------|  
| `location` | 是 | 地点（城市、国家或地区，例如：“berlin”、“germany”、“san francisco”） |  
| `role` | 否 | 角色类型（见下方支持的角色列表） |  
| `skills` | 否 | 需要匹配的技术关键词数组 |  
| `maxUsers` | 否 | 每次搜索的最大用户数量（默认：100） |  

### 支持的角色类型  

| 角色 | 所涉及的技术栈 |  
|------|----------------------|  
| `frontend` | react, vue, angular, svelte, typescript, css, tailwind, nextjs |  
| `backend` | nodejs, python, django, flask, go, rust, java, spring, postgresql |  
| `fullstack` | react, nodejs, nextjs, postgresql, typescript, graphql |  
| `mobile` | react-native, flutter, swift, kotlin, ios, android |  
| `devops` | docker, kubernetes, terraform, aws, azure, jenkins, github-actions |  
| `data` | python, pandas, tensorflow, pytorch, spark, sql, jupyter |  
| `security` | penetration, owasp, cryptography, ethical-hacking, forensics |  
| `blockchain` | ethereum, solidity, web3, smart-contract, defi, nft |  
| `ai` | machine-learning, pytorch, tensorflow, llm, langchain, huggingface |  
| `gaming` | unity, unreal, godot, opengl, vulkan, game-engine |  

### 查看单个用户的评分  

可以获取特定 GitHub 用户的详细评分信息。  

**响应格式：**  
该 API 端点使用 Server-Sent Events (SSE) 格式返回数据。  

## 用户信息字段  

每个用户的结果包含以下字段：  

## 免费与付费服务  

| 功能 | 免费（通过 API） | 完整报告（19 美元） |  
|---------|----------------|-------------------|  
| 结果 | 前 10 个示例结果 | 所有匹配的开发者 |  
| 导出 | 不支持 | 可下载 Excel/CSV 文件 |  
| 联系信息 | 有限 | 全部（电子邮件、网站、社交媒体信息） |  
| 评分详情 | 基本信息 | 详细评分分析 |  

### 获取完整报告  

如需获取所有匹配开发者的完整列表及详细联系信息，请按照以下步骤操作：  
1. 访问 **https://githunt.ai**  
2. 输入地理位置和角色进行搜索  
3. 点击 “购买完整报告”（19 美元，一次性支付）  
4. 下载包含所有候选人的 Excel 报告  

## 使用示例  

- **在柏林查找 React 开发者（实时流式搜索）**  
- **查看特定候选人的评分**  

## 使用技巧：  
1. **明确指定地理位置**：使用 “san francisco” 比使用 “usa” 更精确。  
2. **结合使用角色或技术关键词**：指定角色会自动包含相关技术关键词。  
3. **实时流式结果**：搜索结果会实时显示。  
4. **免费预览仅包含前 10 个结果**：如需完整列表，请购买完整报告。