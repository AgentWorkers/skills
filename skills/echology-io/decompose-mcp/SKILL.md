---
name: decompose-mcp
description: 将任何文本分解为分类的语义单元——包括权威性（authority）、风险（risk）、关注度（attention）以及实体（entities）。该过程不依赖于大型语言模型（LLM），而是基于确定性算法实现的。
homepage: https://echology.io/decompose
metadata: {"clawdbot":{"emoji":"🧩","requires":{"anyBins":["python3","python"]},"install":[{"id":"pip","kind":"uv","pkg":"decompose-mcp","bins":["decompose"],"label":"Install decompose-mcp (pip/uv)"}]}}
---
# **分解功能**  
该工具能够将任何文本或URL分解为分类明确的语义单元。每个单元都会被赋予权限等级、风险类别、关注度评分、实体提取信息以及是否需要保持原样的标志。无需使用大型语言模型（LLM），处理过程完全确定性强，并且可以在本地执行。  

## **设置步骤**  

### 1. 安装  
```bash
pip install decompose-mcp
```  

### 2. 配置MCP服务器  
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

### 3. 验证功能  
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

**示例命令：**  
`decompose_text "This is a sample text."`  

**返回结果：**  
一个JSON对象，其中包含`units`数组。每个单元包含以下信息：  
- `authority`：强制性、指令性、许可性、条件性、信息性  
- `risk`：安全关键、安全相关、合规性、财务相关、合同相关、建议性、信息性  
- `attention`：0.0到10.0的优先级评分  
- `actionable`：是否需要采取行动  
- `irreducible`：内容是否必须保持原样  
- `entities`：引用的标准及规范（如ASTM、ASCE、IBC、OSHA等）  
- `dates`：提取的日期信息  
- `financial`：提取的金额及百分比数据  
- `heading_path`：文档的结构层次  

### `decompose_url`  
该工具可获取URL并解析其内容，支持处理HTML、Markdown和纯文本格式。  

**参数：**  
- `url`（必填）：需要解析的URL  
- `compact`（可选，默认值：`false`）：省略值为零的字段  

**示例命令：**  
`decompose_url "https://spec.example.com/transport"`  

**功能说明：**  
- **权限等级**：根据RFC 2119标准进行分类（例如，“shall”表示强制性要求，“should”表示建议性要求）  
- **风险类别**：分为安全关键、安全相关、合规性、财务相关、合同相关等  
- **关注度评分**：权限等级权重乘以风险系数（0-10分）  
- **标准引用**：如ASTM、ASCE、IBC、OSHA等  
- **财务信息**：金额、百分比等数据  
- **日期信息**：截止日期、里程碑、通知期限等  
- **不可简化内容**：法律强制要求、无法改写的公式等  

**应用场景：**  
- 在将文档发送给大型语言模型之前进行预处理，可节省60-80%的处理时间  
- 按照权限等级对规范、合同、政策、法规进行分类  
- 提取标准引用和合规性要求  
- 将高关注度内容定向到专门的分析流程  
- 从原始文档中构建结构化训练数据  

**性能表现：**  
- 在Apple Silicon平台上，平均处理时间约为14毫秒  
- 每秒可处理超过1000个字符  
- 无需调用任何API，完全无需网络连接，支持离线使用  
- 处理结果始终一致（相同输入产生相同输出）  

**安全与信任机制：**  
- **文本分类**：所有处理都在本地完成，不涉及网络数据传输。  
- **URL解析**：虽然会发起HTTP请求，但仅用于获取目标URL，因此需要`claw.json`文件中设置`network`权限。如无需解析URL，可仅使用`decompose_text`工具（无需网络访问）。  
- **SSRF保护**：在连接前会屏蔽私有/内部IP地址范围（`0.0.0.0/8`等）。  
- **无需API密钥或凭证**：除非使用`decompose_url`获取用户指定的URL，否则不会访问外部服务。  
- **代码透明度**：源代码完全公开（[github.com/echology-io/decompose](https://github.com/echology-io/decompose)），通过GitHub Actions使用PyPI Trusted Publishers（OIDC）发布（[publish.yml](https://github.com/echology-io/decompose/blob/main/.github/workflows/publish.yml)），确保发布版本可追溯到具体提交。  

## **资源链接：**  
- **源代码**：[github.com/echology-io/decompose](https://github.com/echology-io/decompose)  
- **PyPI包**：[https://pypi.org/project/decompose-mcp/](https://pypi.org/project/decompose-mcp/)  
- **文档**：[https://echology.io/decompose]  
- **博客文章**：  
  - [正则表达式为何优于大型语言模型](https://echology.io/blog/regex-beats-llm)  
  - [为什么你的工具需要这种认知功能](https://echology.io/blog/cognitive-primitive)