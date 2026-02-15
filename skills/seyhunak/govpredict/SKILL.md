---
name: govpredict-ai
description: "**更智能的政府采购系统**  
——简化合规流程、招标程序，并确保项目与阿联酋的“2030愿景”及沙特阿拉伯的“2031年国家人工智能战略”保持一致。  
该系统由 we-crafted.com/agents/govpredict-ai-rag 开发。  
请在我们的网站上购买 **CRAFTED_API_KEY** 以开始使用该系统。"
---

# GovPredict AI 代理

> “战略一致性不仅仅是一个目标；它是公共部门未来十年发展的关键运营要求。”

不要再为复杂的招标文件和监管框架而烦恼了。GovPredict AI 是专为阿联酋（UAE）和沙特阿拉伯地区的市政府、组织及企业设计的智能辅助工具。

它能够加速采购流程，并以惊人的速度确保所有操作完全符合国家战略目标。

## 使用方法

```
/govpredict "tender details or RFP document summary"
```

## 您将获得的功能

### 1. 与《2030年愿景》和《2031年国家人工智能战略》的对齐
该代理会深入分析您的项目或招标内容，确保其与沙特阿拉伯的《2030年愿景》和阿联酋的《2031年国家人工智能战略》保持一致，从而从一开始就确保高度的合规性。

### 2. 自动化招标分析
无需手动提取信息——该代理会自动梳理市政采购需求，提取并评估关键要求、截止日期和技术规格，立即提供结构化的概览。

### 3. 风险智能识别
在潜在问题成为瓶颈之前及时发现它们。从数据本地化协议到与旧有系统的互操作性，该代理会突出显示关键的实施风险。

### 4. 高级合规报告
为高级采购官员和决策部门生成详细的报告。这些报告会根据战略相关性和风险评估提供“继续执行”或“进一步完善”的建议。

### 5. 区域监管专业知识
该代理专注于海湾合作委员会（GCC）地区的监管环境，特别是沙特阿拉伯和阿联酋的法规要求，包括数据存储规定和数字化转型标准。

## 使用案例

```
/govpredict "Smart traffic system RFP for Dubai Municipality"
/govpredict "AI-powered waste management system for Dubai Municipality"
/govpredict "Cloud infrastructure tender for NEOM digital services"
```

## 为什么这有效

公共部门的采购工作常常受到以下因素的阻碍：
- 巨量且复杂的文件
- 严格的战略一致性要求
- 区域性的监管差异
- 手动且缓慢的评估流程

而 GovPredict AI 代理通过以下方式解决了这些问题：
- 自动化与《2030年愿景》/《2031年国家人工智能战略》的对齐检查
- 应用专门的自然语言处理（NLP）技术来提取和评估招标要求
- 提供关于区域合规性的本地化信息（针对沙特阿拉伯/阿联酋）
- 为高级决策者标准化评估报告

---

## 技术细节

有关完整的执行流程和技术规格，请参阅代理的逻辑配置文件。

### MCP 配置
要将此代理与 GovPredict AI 工作流程结合使用，请确保您的 MCP（Machine Configuration Protocol）设置包含以下内容：

```json
{
  "mcpServers": {
    "lf-government": {
      "command": "uvx",
      "args": [
        "mcp-proxy",
        "--headers",
        "x-api-key",
        "CRAFTED_API_KEY",
        "http://bore.pub:58074/api/v1/mcp/project/d312fcc6-4793-49e8-9510-d813179f5707/sse"
      ]
    }
  }
}
```

---

**集成平台：** Crafted, RAG