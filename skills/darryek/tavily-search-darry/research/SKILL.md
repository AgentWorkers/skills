---
name: research  
description: "基于网络数据的综合性研究，包含明确的引用。适用于需要多源信息整合的情况——例如比较分析、时事报道、市场分析或详细报告的撰写。"
---# 研究技能

能够对任何主题进行全面的调研，支持自动收集信息、分析数据并生成带有引用内容的报告。

## 认证

该脚本通过 Tavily MCP 服务器使用 OAuth 进行认证。**无需手动设置**——首次运行时，它会：  
1. 检查 `~/.mcp-auth/` 目录中是否存在有效的 OAuth 令牌；  
2. 如果未找到令牌，会自动打开浏览器进行 OAuth 认证。  

> **注意：** 你必须拥有一个 Tavily 账户。此认证流程仅支持登录，不支持账户创建。如果还没有账户，请先访问 [tavily.com](https://tavily.com) 注册。  

### 替代方案：API 密钥  

如果你更喜欢使用 API 密钥，可以在 [https://tavily.com](https://tavily.com) 获取密钥，并将其添加到 `~/.claude/settings.json` 文件中：  
```json  
{  
  "env": {  
    "TAVILY_API_KEY": "tvly-your-api-key-here"  
  }  
}  
```  

## 快速启动  

> **提示：** 研究过程可能需要 30 至 120 秒。按 **Ctrl+B** 可以在后台运行脚本。  

### 使用脚本  

```bash  
./scripts/research.sh '<json>' [output_file]  
```  

**示例：**  

```bash  
# 基本研究  
./scripts/research.sh '{"input": "量子计算趋势"}'  

# 使用高级模型进行全面分析  
./scripts/research.sh '{"input": "AI 代理的比较", "model": "pro"}'  

# 将结果保存到文件  
./scripts/research.sh '{"input": "电动汽车的市场分析", "model": "pro"}' ./ev-report.md  

# 快速定向研究  
./scripts/research.sh '{"input": "气候变化的影响", "model": "mini"}'  
```  

## 参数  

| 参数 | 类型 | 默认值 | 说明 |  
|-------|------|---------|-------------|  
| `input` | 字符串 | 必填 | 研究主题或问题 |  
| `model` | 字符串 | `"mini"` | 模型：`mini`、`pro`、`auto` |  

## 模型选择  

**使用建议**：  
- 对于简单问题（如“X 是什么？”），选择 `mini` 模型；  
- 对于复杂的多角度分析（如“X 与 Y 与 Z 的比较”或“最佳方法是什么？”），选择 `pro` 模型；  
- 如果系统根据问题复杂性自动选择模型，选择 `auto` 模型。  

| 模型 | 适用场景 | 处理速度 |  
|-------|----------|-------|  
| `mini` | 单一主题的定向研究 | 约 30 秒 |  
| `pro` | 全面的多角度分析 | 约 60–120 秒 |  
| `auto` | 系统根据问题复杂性自动选择模型 | 变动较大 |  

## 示例：**  

### 快速概览  
```bash  
./scripts/research.sh '{"input": "什么是检索增强生成（Retrieval Augmented Generation）？", "model": "mini"}'  
```  

### 技术比较  
```bash  
./scripts/research.sh '{"input": "LangGraph 与 CrewAI 在多智能体系统中的对比", "model": "pro"}'  
```  

### 市场研究  
```bash  
./scripts/research.sh '{"input": "2025 年金融科技初创企业格局", "model": "pro"}' fintech-report.md  
```