---

**名称：Settlement-Witness**  
**描述：** 在30秒内生成一份已签名的交付收据。  

---

# SettlementWitness  
**功能：** 在30秒内生成一份已签名的交付收据。  

**立即运行：**  
```bash
settlement_witness({
  task_id: "quickstart-001",
  spec: { value: 1 },
  output: { value: 1 }
})
```

您将收到以下响应：  
- `PASS`：操作成功  
- `SPEC_MATCH`：输入数据与预期规格匹配  
- `receipt_id`（以`sha256`格式表示）：生成的收据ID  
- `sig`（以`base64url`格式表示）：收据的签名信息  

**示例（部分内容）：**  
```json
{
  "receipt_v0_1": {
    "verdict": "PASS",
    "reason_code": "SPEC_MATCH",
    "receipt_id": "sha256:3adb22d0...",
    "sig": "base64url:AbC..."
  }
}
```

**功能说明：**  
Settlement-Witness能够生成经过加密签名的交付收据，这些收据可由第三方系统离线验证。  

**常见错误情况：**  
- **错误代码422**：缺少必要的字段。请确保`task_id`、`spec`和`output`字段都已提供。  
- **错误代码INDETERMINATE/EVALUATOR_TIMEOUT**：上游评估器无法访问。尽管如此，该收据仍然是有效的。  
- **错误代码FAIL/SPEC_MISMATCH**：生成的输出数据与预期规格不匹配。请检查数据结构是否正确。  

**示例与测试数据：**  
可查看有效的成功（PASS）、失败（FAIL）和不确定结果（INDETERMINATE）示例，请访问：[fixtures/](…)  

**接口信息：**  
- **MCP接口：**  
  `POST`：`https://defaultverifier.com/mcp`  
- **直接REST接口：**  
  `POST`：`https://defaultverifier.com/settlement-witness`  

**安全提示：**  
切勿在`spec`或`output`字段中传输任何敏感信息。请确保输入数据的唯一性和可预测性。