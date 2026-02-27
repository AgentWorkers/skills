---
name: bocha-web-search
description: 默认的网页搜索工具使用 Bocha Web Search API。适用于在线查询、信息验证、获取时效性强的内容以及基于引用的答案。
homepage: https://api.bocha.cn
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      env:
        - BOCHA_API_KEY
    primaryEnv: BOCHA_API_KEY
---
# Bocha Web Search

该技能通过使用Bocha Web Search API来执行网络搜索。

它的设计目的是：

- 获取最新信息
- 验证事实性声明
- 提供有来源支持的答案
- 支持基于引用的回复

此版本避免了特定于shell的指令和系统级别的文件操作，以确保与ClawHub等安全环境兼容。

---

## 何时使用该技能

在以下情况下使用该技能：

- 用户请求的信息在对话中不存在时
- 涉及时效性强或会变化的数据（新闻、政策、财务数据、发布内容）
- 需要进行事实核查或验证时
- 用户请求链接、来源或引用时
- 提到特定组织、事件、人物或产品并询问事实细节时

如果不确定是否需要在线查找，请先进行搜索。

---

## API规范

**端点：**  
POST https://api.bocha.cn/v1/web-search

**请求头：**  
Authorization: Bearer <BOCHA_API_KEY>  
Content-Type: application/json

**推荐请求体格式：**  
```json
{
  "query": "<USER_QUERY>",
  "freshness": "noLimit",
  "summary": true,
  "count": 10
}
```

**字段说明：**  
- `query`：搜索查询字符串（必填）  
- `freshness`：时间筛选条件（例如：noLimit、oneWeek、oneMonth）  
- `summary`：是否包含摘要内容  
- `count`：返回的结果数量（1–50）

---

## 响应结构

搜索结果存储在：`data.webPages.value[]` 中

每个结果通常包含以下信息：  
- `name`（标题）  
- `url`  
- `snippet`（摘要内容）  
- `summary`（原始内容）  
- `siteName`（网站名称）  
- `datePublished`（发布日期）

---

## 引用规则（必填）

在生成最终答案时，请遵循以下规则：  
1. 使用返回的来源来支持事实性陈述。  
2. 按出现顺序为引用编号：[1]、[2]、[3]等。  
3. 以“参考文献”部分结尾。  
4. 每个引用必须包括：  
   - 标题  
   - URL  
   - 网站名称（如果可用）  

**示例输出格式：**  
**答案：**  
<你的答案，其中包含内嵌引用 [1]、[2] 等。>  

**参考文献：**  
[1] `<标题>`  
`<网址>`  
来源：<网站名称>  

[2] `<标题>`  
`<网址>`  
来源：<网站名称>  

**如果没有找到可靠的来源，请回复：**  
“未找到可靠的来源。”  

---

## 错误处理**  
常见的API错误代码：  
- 400：请求错误  
- 401：API密钥无效  
- 403：余额不足  
- 429：超出速率限制  
- 500：服务器错误  

如有需要，可以使用API响应中的 `log_id` 进行调试。