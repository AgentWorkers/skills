---
name: paramus-chemistry
description: 来自Paramus Chemistry OS的319种化学、材料科学、热力学和数据科学工具
metadata: {"openclaw": {"emoji": "⚗", "requires": {"anyBins": ["curl", "wget"]}, "primaryEnv": "PARAMUS_API_TOKEN", "homepage": "https://cloud1.paramus.ai"}}
---
## Paramus 化学与材料科学

您可以使用 Paramus，这是一个科学计算平台，提供了 319 种工具，用于化学、聚合物科学、热力学、电化学、材料科学和数据科学领域的研究。

### 自动检测连接方式

在首次使用 Paramus 之前，请运行以下脚本，以自动检测本地模式或云模式是否可用：

```bash
# Auto-detect: try local first, fall back to cloud
if curl -sf -o /dev/null --connect-timeout 2 http://localhost:8765/health 2>/dev/null; then
  PARAMUS_URL="http://localhost:8765/"
  PARAMUS_AUTH=""
  echo "Paramus: local mode (localhost:8765)"
elif [ -n "$PARAMUS_API_TOKEN" ]; then
  PARAMUS_URL="https://cloud1.paramus.ai/mcp"
  PARAMUS_AUTH="-H \"Authorization: Bearer $PARAMUS_API_TOKEN\""
  echo "Paramus: cloud mode (cloud1.paramus.ai)"
else
  echo "Paramus: not available. Start the tray app or set PARAMUS_API_TOKEN."
fi
```

如果两种方式均无法使用，请告知用户：
- **本地模式**：从 https://cloud1.paramus.ai 下载 Paramus 并启动托盘应用程序。该应用程序运行在 `localhost:8765` 上。
- **云模式**：访问 https://cloud1.paramus.ai/api/token，输入您的 XXX-XXX-XXX 许可证密钥，复制Bearer 令牌，然后设置 `export PARAMUS_API_TOKEN="<token>"`。

### 如何调用工具

所有工具的调用均通过 curl 和 JSON-RPC 协议完成。在自动检测完成后，系统会设置 `PARAMUS_URL` 和 `PARAMUS_AUTH` 的值：

**搜索**（根据描述查找工具）：
```bash
curl -s -X POST "$PARAMUS_URL" \
  -H "Content-Type: application/json" \
  $PARAMUS_AUTH \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search","arguments":{"query":"molecular weight from SMILES"}}}'
```

**直接调用**（通过工具的准确名称运行工具）：
```bash
curl -s -X POST "$PARAMUS_URL" \
  -H "Content-Type: application/json" \
  $PARAMUS_AUTH \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"directCall","arguments":{"tool_name":"calculate_molecular_weight","parameters":{"smiles":"CCO"}}}}'
```

**获取工具参数结构**（在调用前检查所需参数）：
```bash
curl -s -X POST "$PARAMUS_URL" \
  -H "Content-Type: application/json" \
  $PARAMUS_AUTH \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"getSchema","arguments":{"tool_name":"calculate_logp"}}}'
```

**列出工具类别**：
```bash
curl -s -X POST "$PARAMUS_URL" \
  -H "Content-Type: application/json" \
  $PARAMUS_AUTH \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"listCategories","arguments":{}}}'
```

**列出某个类别中的工具**：
```bash
curl -s -X POST "$PARAMUS_URL" \
  -H "Content-Type: application/json" \
  $PARAMUS_AUTH \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"listByCategory","arguments":{"category":"Chemistry"}}}'
```

### 可用的工具类别

| 类别 | 示例工具 |
|----------|---------|
| 化学 | 分子量、LogP、TPSA、氢键供体/受体、Lipinski 指数、QED 分析、分子指纹、相似性检测 |
| 分子转化 | 将 SMILES 转换为 InChI、将 InChI 转换为 SMILES、分子结构规范化、验证 |
| 结构分析 | 芳香性分析、子结构搜索、环结构信息、立体异构体识别、3D 构象分析 |
| 聚合物 | BigSMILES 验证、聚合物指纹分析、pSMILES 解析、聚合物相似性比较 |
| 热力学 | CoolProp 流体性质分析（支持 120 多种流体）、饱和度计算、临界点/ triple 点分析、传输特性研究 |
| 动力学 | Cantera 平衡计算、反应速率分析、火焰传播速度、着火延迟预测 |
| 电化学 | Nernst 方程计算、Butler-Volmer 方程、电导率测量、Faraday 电解实验 |
| 数据科学 | DOE 设计（因子实验、拉丁超立方实验设计）、PCA 分析、k-means 算法、回归分析、统计处理 |
| 材料科学 | pymatgen 晶体结构数据库、XRD 图谱分析 |
| BRAIN 平台 | 机器学习辅助的性能预测、玻璃化转变温度（Tg）估算、高性能计算（Psi4、NWChem、ORCA） |

### 工作流程

1. 首次使用前，请运行上述的 **自动检测** 脚本。
2. 使用 **搜索** 功能查找所需的工具。
3. 使用 **获取工具参数结构** 功能查看具体需要的输入参数。
4. 使用 **直接调用** 功能并传入参数。
5. 解析 JSON 响应并展示结果。

### 注意事项

- 服务器重启后的首次调用可能需要约 1 秒的时间（用于加载相关库）。后续调用时间通常小于 10 毫秒。
- SMILES 是主要的分子输入格式；如果用户提供了化合物名称，系统会要求用户提供对应的 SMILES 字符串或帮助用户查询该化合物的 SMILES 表达式。
- 所有数值结果都会包含相应的单位信息（如克/升 [g/L]、摩尔/升 [mol/L] 等）。