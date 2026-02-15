---
name: gerador-contrato-locacao-preview
description: 通过 Google 表单注册租赁合同。
metadata: {
  "name": "gerador-contrato-locacao-preview",
  "display_name": "Gerador de Contratos de Locação",
  "version": "1.0.0",
  "command": "python3 scripts/main.py",
  "input": {
    "type": "json",
    "root": "dados",
    "description": "Dados estruturados do contrato de locação"
  },
  "dependencies": ["requests"],
  "env_vars": ["FORM_ID", "DRY_RUN"]
}
---

# 📄 技能：租赁合同注册

该技能通过 **Google Forms** 注册租赁合同，对所有数据进行完整验证，生成 **确认摘要**，并在获得批准后才会发送数据。

---

## ⚠️ 执行规则（必须遵守）
1. 在执行之前，必须验证所有必填字段。
2. 环境变量 `FORM_ID` 是 **必需的**。
3. 代理 **必须向用户展示数据摘要并请求明确确认**。
4. 如果验证失败，执行过程将中止。
5. 支持使用 `DRY_RUN` 模式进行模拟运行。

---

## ⚙️ 环境变量

### `FORM_ID`（必需）
用于接收数据的 Google Forms 的 ID。

```bash
export FORM_ID="SEU_FORM_ID"
```

### `DRY_RUN`（可选）
当设置为 `DRY_RUN` 时，该技能 **不会发送实际数据**，仅显示生成的负载（payload）。

```bash
export DRY_RUN=1
```

---

## 📥 数据输入方式

### ✅ 推荐方式：STDIN
```bash
echo '{"dados": {...}}' | python3 scripts/main.py
```

### 替代方式：CLI 参数
```bash
python3 scripts/main.py '{"dados": {...}}'
```

---

## 📦 负载（Payload）的预期结构

```json
{
  "dados": {
    "email": "string (obrigatório)",
    "telefone": "string (obrigatório, apenas dígitos)",
    "nome": "string (obrigatório)",
    "cpf": "string (obrigatório, apenas dígitos)",
    "endereco": "string (obrigatório)",
    "numero": "string (obrigatório)",
    "bairro": "string (obrigatório)",
    "cidade": "string (obrigatório)",
    "estado": "UF (obrigatório)",
    "data_entrada": "YYYY-MM-DD (obrigatório)",
    "data_saida": "YYYY-MM-DD (obrigatório)",
    "valor": "string (obrigatório)",
    "caucao": "string (opcional)",
    "complemento": "string (opcional)"
  }
}
```

---

## 📓� 负载（Payload）示例

```json
{
  "dados": {
    "email": "exemplo@email.com",
    "telefone": "11988887777",
    "nome": "Fulano de Tal",
    "cpf": "12345678910",
    "endereco": "Rua das Flores",
    "numero": "123",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "estado": "SP",
    "data_entrada": "2025-05-01",
    "data_saida": "2025-05-05",
    "valor": "2500",
    "caucao": "1000",
    "complemento": "Apto 42"
  }
}
```

---

## 📥 输入参数

### 必填字段
| 字段 | 类型 | 说明 |
|------|------|-----------|
| `email` | string | 租户的电子邮件 |
| `telefone` | string | 带区号的电话号码 |
| `nome` | string | 全名 |
| `cpf` | string | 社会安全号码（11位） |
| `endereco` | string | 街道/大道 |
| `numero` | string | 房屋编号 |
| `bairro` | string | 街区 |
| `cidade` | string | 城市 |
| `estado` | string | 州（2个字母） |
| `data_entrada` | string | 格式为 `YYYY-MM-DD` 的入住日期 |
| `data_saida` | string | 格式为 `YYYY-MM-DD` 的退房日期 |
| `valor` | string | 总租金 |

### 可选字段
| 字段 | 类型 | 说明 |
|------|------|-----------|
| `caucao` | string | 押金 |
| `complemento` | string | 地址的补充信息 |

---

## 🔄 执行流程
1. 通过聊天收集数据。
2. 进行结构性和格式验证。
3. 显示确认摘要。
4. 确认后执行技能。
5. 通过 POST 请求将数据发送到 Google Forms。
6. 返回成功或错误信息。

---

## ✅ 预期返回结果

### 成功
```
Sucesso: contrato registrado e PDF será enviado.
```

### 验证错误
```
Erro: Campos obrigatórios ausentes: email, cpf
```

### DRY_RUN 模式
```
[DRY-RUN] Payload gerado: {...}
```

---

版本 1.0.0