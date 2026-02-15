---
description: 连接到 Baselight MCP（模型上下文协议）。
  server to discover and query 50+ premium dataset sources including Kaggle,
  OWID, World Bank, Data Commons, Eurostat, FiveThirtyEight, DefiLlama,
  EVM blockchains, Polymarket, NFLverse, Yahoo Finance, FRED, IMF, SEC
  filings, OECD, US Census, CDC, FBI Crime, CIA World Factbook, sports
  (soccer, basketball, fantasy football), weather (Open-Meteo), crypto
  (XrpScan, XRPL, CoinDesk), and education/health statistics. Run live
  SQL queries against structured data from AI tools.
homepage: "https://baselight.ai/docs/connecting-to-the-baselight-mcp-server/"
metadata:
  openclaw:
    emoji: 🔌
    requires:
name: baselight-mcp
---

# Baselight MCP

您可以通过MCP直接从您的AI工具或IDE中浏览、发现和查询Baselight数据集。

MCP服务器地址：https://api.baselight.app/mcp

## 适用场景

- 用户需要某个主题的相关数据集
- 用户需要结构化的数据表
- 用户需要进行SQL分析
- 用户需要可验证的分析结果

## 快速入门

根据您的客户端类型，使用OAuth或API密钥进行连接：

### OAuth客户端

- ChatGPT连接器
- Claude Web/Desktop

### API密钥客户端

- VS Code
- Gemini CLI
- LibreChat

------------------------------------------------------------------------

## 工作流程

1. 明确查询需求
2. 发现相关数据集
3. 查看数据集的结构（模式）
4. 查询数据
5. 返回查询结果及对应的SQL语句

------------------------------------------------------------------------

## 查询格式

数据表的查询格式为：

@username.dataset.table

示例：

SELECT \* FROM @user.soccer.matches LIMIT 10;

------------------------------------------------------------------------

## 最佳实践

- 先查找所需的数据集
- 查看数据集的结构
- 逐步进行数据查询
- 包含查询所使用的SQL语句
- 阐明查询的假设和限制条件

------------------------------------------------------------------------

## 限制事项

- 需要拥有Baselight账户或API密钥
- 查询可能受到数量限制
- 数据集的更新频率不一

------------------------------------------------------------------------

## 故障排除

- 连接失败：请检查MCP服务器地址是否正确，或重新进行身份验证/生成API密钥
- 未经授权：可能是API密钥无效或已过期
- 查询速度较慢：尝试缩小查询范围或添加LIMIT子句

------------------------------------------------------------------------

## 帮助资源

- 文档：https://baselight.ai/docs/connecting-to-the-baselight-mcp-server/
- 官方应用：https://baselight.app