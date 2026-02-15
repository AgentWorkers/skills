---
name: decompose-mcp
description: 将任何文本分解为分类的语义单元——包括权威性（authority）、风险（risk）、关注度（attention）以及实体（entities）。该过程不依赖于大型语言模型（LLM），且是确定性的（deterministic）。
homepage: https://echology.io/decompose
metadata: {"clawdbot":{"emoji":"🧩","requires":{"anyBins":["python3","python"]},"install":[{"id":"pip","kind":"uv","pkg":"decompose-mcp","bins":["decompose"],"label":"Install decompose-mcp (pip/uv)"}]}}
---
# **Decompose**  
该工具可将任何文本或URL分解为分类明确的语义单元。每个单元都会被赋予权限级别、风险类别、关注度评分、实体提取结果以及是否应被原样保留的标志。无需使用大型语言模型（LLM），处理过程完全确定性强，且可在本地执行。  

## **设置**  

### 1. **安装**  
```bash
pip install decompose-mcp
```  

### 2. **配置MCP服务器**  
将相关配置添加到您的OpenClaw MCP系统中：  
```json
{
  "mcpServers": {
    "decompose": {
      "command": "python3",
      "args": ["-m", "decompose", "--serve"]
    }
  }
}
```  

### 3. **验证**  
```bash
python3 -m decompose --text "The contractor shall provide all materials per ASTM C150-20."
```  

## **可用工具**  

### `decompose_text`  
该工具可将任意文本分解为分类明确的语义单元。  

**参数：**  
- `text`（必填）：需要分解的文本  
- `compact`（可选，默认值：`false`）：省略值为零的字段以简化输出  
- `chunk_size`（可选，默认值：2000）：每个单元的最大字符数  

**示例提示：** “分解此规范文件，并告诉我哪些部分是强制性的。”  

**返回值：** JSON格式的数据，其中包含`units`数组。每个单元包含以下信息：  
- `authority`：强制性、禁止性、指令性、允许性、条件性或信息性  
- `risk`：安全性风险、合规性风险、财务风险、合同风险或建议性风险  
- `attention`：0.0到10.0的优先级评分  
- `actionable`：是否需要采取行动  
- `irreducible`：内容是否必须保持原样  
- `entities`：引用的标准及规范（如ASTM、ASCE、IBC、OSHA等）  
- `dates`：提取的日期信息  
- `financial`：提取的金额及百分比数据  
- `heading_path`：文档的层级结构  

### `decompose_url`  
该工具可获取URL并解析其内容，支持处理HTML、Markdown和纯文本格式。  

**参数：**  
- `url`（必填）：需要解析的URL  
- `compact`（可选，默认值：`false`）：省略值为零的字段  

**示例提示：** “解析URL `https://spec.example.com/transport`，并显示其中的安全要求。”  

## **功能说明**  
- **权限级别**：根据RFC 2119标准进行分类（例如：“shall”表示强制性要求，“should”表示指令性建议）  
- **风险类别**：安全性风险、合规性风险、财务风险、合同风险  
- **关注度评分**：权限权重乘以风险系数（0-10分）  
- **标准引用**：ASTM、ASCE、IBC、OSHA等国际标准  
- **财务信息**：金额、百分比等数值数据  
- **日期信息**：截止日期、里程碑、通知期限等  
- **不可简化内容**：法律规定的强制性条款、不可替换的公式等  

**应用场景**：  
- 在将文档发送给大型语言模型之前进行预处理，可节省60-80%的处理时间  
- 按照权限级别对规范文件、合同、政策及法规进行分类  
- 提取标准引用和合规性要求  
- 将高关注度内容转发至专门的分析流程  
- 从原始文档中构建结构化的训练数据  

## **性能表现**：  
- 在Apple Silicon平台上，平均处理时间约为14毫秒  
- 每秒可处理超过1000个字符  
- 无需调用任何API，完全免费，支持离线运行  
- 处理结果具有确定性：相同的输入总是产生相同的输出  

**安全性特性**：  
- 所有处理过程均在本地完成，数据不会离开用户的设备  
- URL解析会过滤掉内部/私有IP地址（防止SSRF攻击）  
- 无需使用API密钥，也不依赖任何外部服务  

**资源链接**：  
- [PyPI仓库](https://pypi.org/project/decompose-mcp/)  
- [GitHub仓库](https://github.com/echology-io/decompose)  
- [官方文档](https://echology.io/decompose)  
- [博客文章：正则表达式为何优于大型语言模型](https://echology.io/blog/regex-beats-llm)