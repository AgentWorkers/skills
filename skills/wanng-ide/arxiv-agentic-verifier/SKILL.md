# ArXiv Agentic Verifier

**源论文：** [用于竞赛编程的智能验证器扩展](https://arxiv.org/abs/2602.09012) (ID: 4a4c4dae6a5145ebc4d62eb2d64b0f0f)  
**类型：** 代码验证 / 测试生成  

## 描述  
该工具实现了一个“智能验证器”，它通过生成有针对性的、具有区分能力的测试用例来主动判断代码的正确性。与随机采样不同，该验证器会分析问题的约束条件和代码逻辑，以发现边缘情况或逻辑错误。  

## 特点：  
- **分析代码：** 能够理解 Python/JS 代码的逻辑。  
- **生成测试用例：** 创建特定的输入来触发代码错误。  
- **执行与验证：** 使用生成的测试用例运行代码（建议在生产环境中使用沙箱环境）。  

## 使用方法  

```javascript
const AgenticVerifier = require('./index');
const verifier = new AgenticVerifier(process.env.OPENAI_API_KEY);

const problem = "Given two integers A and B, output their sum.";
const code = "print(int(input().split()[0]) + int(input().split()[1]))";

verifier.verify(problem, code, 'python')
  .then(result => console.log(result))
  .catch(err => console.error(err));
```  

## 配置参数：  
- **OPENAI_API_KEY：** 需要用于 LLM（Large Language Model）的推理功能。  

## 安全提示：  
该工具会执行接收到的代码。请在受限环境或沙箱环境中使用。