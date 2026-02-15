---
name: contrato-locacao-broa
description: 在 Google Forms 中注册合同。
metadata: {
  "name": "contrato-locacao-broa",
  "display_name": "Gerador de Contratos",
  "version": "1.1.0",
  "command": "python3 main.py",
  "dependencies": ["requests"]
}
---

# 技能：租赁合同注册（使用 Google 表单）

## 📝 描述  
该技能可自动化房地产租赁合同的注册流程。它将代理人收集的数据发送到 Google 表单，随后 Google 表单会触发一个 Google Apps Script 脚本，该脚本负责：  
1. 根据 Google 文档中的模板生成 PDF 格式的租赁合同。  
2. 自动计算租赁期限（以天为单位）和每日租金。  
3. 将货币金额格式化为巴西货币单位（雷亚尔，R$）。  
4. 通过电子邮件将签好的 PDF 发送给租户和管理员。  

## 🛠 输入参数  
代理人需要从对话中提取以下数据。所有字段均为必填项，除非另有说明：  

| 字段 | 类型 | 说明 | 示例 |  
| :--- | :--- | :--- | :--- |  
| `email` | string | 租户的电子邮件地址（PDF 的接收者）。 | `example@email.com` |  
| `telefone` | string | 带区号的电话号码（仅输入数字）。 | `16988035666` |  
| `nome` | string | 租户的全名。 | `David Evaristo` |  
| `cpf` | string | 租户的 CPF 号码（仅输入数字）。 | `40544335880` |  
| ` endereco` | string | 房产所在的街道/大道名称。 | `Rua Bichara Damha` |  
| `numero` | string | 房产的门牌号。 | `360` |  
| `bairro` | string | 房产所在的社区名称。 | `Sao Carlos 2` |  
| `cidade` | string | 所在城市。 | `Sao Carlos` |  
| `estado` | string | 所在州的缩写（2 个字母）。 | `SP` |  
| `data_entrada` | string | 租赁开始日期（格式：**YYYY-MM-DD**）。 | `2026-02-10` |  
| `data_saida` | string | 租赁结束日期（格式：**YYYY-MM-DD**）。 | `2026-02-15` |  
| `valor` | string | 租赁总费用。 | `2000` |  
| `caucao` | string | 押金金额（可选）。 | `200` |  
| `complemento` | string | 房产类型（如公寓、楼栋等，可选）。 | `Casa A` |  

## 🤖 人工智能（AI）的指令  
- **日期格式化：** 将所有相对日期（如“下一个星期日”）或巴西格式的日期（如“10/02/26”）统一转换为标准格式 `YYYY-MM-DD`。  
- **验证：** 如果缺少电子邮件地址或 CPF 号码，则不要执行该技能。  
- **确认：** 在发送前显示确认信息：*“确认：合同信息如下：租户 David Evaristo，租赁日期为 2026-02-10 至 2026-02-15，总费用为 2,000.00 雷亚尔。是否生成合同？”*  
- **执行后：** 告知用户合同文件即将通过电子邮件发送给他们。  

## ⚙️ 数据流程  
1. 代理人调用 `fill_rental_form` 函数。  
2. 该函数向 Google 的 `/formResponse` 端点发送 `POST` 请求。  
3. Google 触发 `onFormSubmit` 事件。  
4. 生成租赁合同 PDF 并通过电子邮件发送给相关人员。