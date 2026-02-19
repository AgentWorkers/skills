---
name: bcra-central-deudores
description: 查询阿根廷中央银行（BCRA）的“Central de Deudores”（债务人数据库）API，以核实阿根廷金融系统中个人或公司的信用状况。当用户需要通过CUIT/CUIL/CDI号码来查询某人的债务情况、信用报告、财务状况、被拒支票信息或信用历史时，可以使用该API。此外，在用户提到“Central de Deudores”、“situación crediticia”（信用状况）、“deudas BCRA”（BCRA债务）、“cheques rechazados”（被拒支票）、“historial crediticio”（信用历史）或希望了解某人/公司在阿根廷金融系统中是否有债务记录时，也应使用该API。
---
# BCRA（阿根廷中央银行）债务人登记系统

通过阿根廷中央银行的债务人登记系统，可以查询并获取基于CUIT/CUIL/CDI编号的信用报告。

## API概述

- **基础URL**: `https://api.bcra.gob.ar`
- **认证**: 无需认证（公共API）
- **响应格式**: JSON
- **输入参数**: CUIT/CUIL/CDI（以整数形式输入，不含连字符），例如 `20123456789`
- **可选的Web界面**: `https://compara.ar/deudores/:cuit`（将 `:cuit` 替换为11位的CUIT/CUIL/CDI编号）

## API端点

### 1. 当前债务信息 — `GET /centraldedeudores/v1.0/Deudas/{Identificacion}`

返回所有金融机构的最新债务状况。

**响应结构：**（具体结构见**CODE_BLOCK_1___）

### 2. 历史债务信息 — `GET /centraldedeudores/v1.0/Deudas/Historicas/{Identificacion}`

返回债务的历史记录，有助于追踪债务人的信用状况随时间的变化。

**响应结构：**与当前债务信息相同，但包含多个时间段的数据。历史记录中的实体信息较为简化（不包含 `fechaSit1`、`diasAtrasoPago` 或其他观察标志）。

### 3. 被拒付的支票信息 — `GET /centraldedeudores/v1.0/Deudas/ChequesRechazados/{Identificacion}`

返回该债务人的被拒付支票信息，按拒付原因和金融机构进行分类。

**响应结构：**（具体结构见**CODE_BLOCK_4___）

## 信用分类代码

| 代码 | 商业贷款组合 | 消费者/住房贷款组合 |
|------|---------------------|--------------------------|
| 1 | 正常 | 正常 |
| 2 | 需特别关注 | 低风险 |
| 3 | 存在问题 | 中等风险 |
| 4 | 高破产风险 | 高风险 |
| 5 | 无法收回 | 无法收回 |
| 6 | 因技术原因无法收回 | 因技术原因无法收回 |

其中，“Situacion 1”表示最佳信用状况。代码值大于或等于2表示存在某种程度的信用风险；代码值大于或等于5表示信用风险较高。

## 关键字段说明

- **monto**: 以千阿根廷比索（ARS）为单位显示的债务金额
- **periodo**: 响应中包含债务的最新报告日期（格式为 `YYYY-MM`）
- **fechaSit1**: 债务人首次被分类为“Situacion 1”的日期
- **diasAtrasoPago**: 逾期天数（0表示当前未逾期）
- **refinanciaciones**: 如果债务已重新融资，则值为 `true`
- **recategorizacionOblig**: 如果债务需要重新分类，则值为 `true`
- **situacionJuridica**: 如果债务人处于法律程序中（如债务重组、破产预防等），则值为 `true`
- **irrecDisposicionTecnica**: 如果债务因技术原因无法收回，则值为 `true`
- **enRevision**: 如果记录正在审核中，则值为 `true`
- **procesoJud**: 如果债务涉及司法程序，则值为 `true`

## 工作流程

1. **验证输入**: 确保输入的CUIT/CUIL/CDI是有效的11位数字（不含连字符）。
2. **首先获取当前债务信息**——这通常是用户的需求。
3. 如果用户需要了解债务变化或过去的信用记录，再获取历史债务信息。
4. 如有必要或用户要求，可获取被拒付的支票信息。
5. 如果用户偏好使用Web界面，可提供 `https://compara.ar/deudores/:cuit` 作为快速查看的选项。
6. 以清晰的方式展示结果，并解释各信用分类代码的含义及债务金额。

## 错误处理

- **400**: 输入的识别号码格式无效。
- **404**: 未找到对应的CUIT/CUIL/CDI记录。
- **500**: BCRA服务器出现错误——请稍后重试。

收到404错误时，应告知用户未找到相关记录。这并不一定意味着该人没有债务，可能是输入的CUIT/CUIL/CDI有误。

## 结果展示

在向用户展示结果时：

- 始终显示个人或公司的名称。
- 按金融机构分类债务，并将信用状况代码大于或等于2的记录标出作为警告。
- 说明金额单位为千阿根廷比索（ARS）。
- 标出`refinanciaciones`、`situacionJuridica`、`procesoJud` 等字段中的`true`值。
- 对于历史数据，展示债务状况的演变趋势（是好转还是恶化）。
- 对于被拒付的支票，标记出未支付的支票（`fechaPago` 为 `null` 的支票）。

## OpenAPI规范

完整的API规范请参见 [references/openapi-spec.json](references/openapi-spec.json)。