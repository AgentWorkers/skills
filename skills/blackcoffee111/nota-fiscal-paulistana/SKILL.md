---
description: Faturamento NFS-e SP（在圣保罗州开具和取消增值税发票）
---
# NFS-e SP 开票技能（OpenClaw）

本文档定义了用于开具和取消圣保罗市电子服务发票（NFS-e）的开票技能的行为和架构。

> **重要提示：** 下面描述的所有文件都必须位于该技能所在的同一文件夹中（例如：`workspace/skills/nfse-sp/`）。

## 📁 生态系统文件
1. `emitir_nfse.py` - 生产环境中的开具脚本（生成 XML SOAP 格式的发票，对其进行加密并发送）。
2. `cancelar_nfse.py` - 取消发票的脚本（对取消操作进行加密处理）。
3. `config.json` - 医疗机构的税费和税率信息（例如：ISS、IRRF 等）。
4. `tomadores.json` - 定期客户的数据表（包含他们的预约信息）。
5. `contador_rps.txt` - 用于控制发票序列号的严格控制的文件。
6. `Certificados.p12` - 市政机构的加密密钥（切勿泄露）。
7. `.env` - 隐藏文件，其中包含变量 `NFSE_CERT_PASSWORD=密码`。
8. `baixar_notas.py` - 用于提取医疗机构报告和财务报表的分页脚本。

---

## ✨ 0. 安装向导（自动健康检查）
每当用户首次请求任何财务操作时（或者您发现缺少某些信息时），**必须** 通过读取 `config.json` 文件来进行一次静默检查。
如果文件中包含诸如 `"MEUCNPJ"`、"`Minhainscricao"` 或 `"MEUCertificado.p12"` 等通用关键词，说明用户刚刚安装了该技能，并且是一个非专业人士。

在这种情况下，暂停用户的任务，并在聊天中启动一个 **交互式且友好的安装向导**：
1. 告诉用户这是他们的第一次使用，并逐一询问缺失的信息：CNPJ（企业注册号）、市政注册号和服务代码。
2. 对于用户的每个回答，**您（代理）** 需要使用文件编写技能来修改并保存 `config.json` 文件中的数据。
3. **关于 `.env` 文件的自动操作：** 在与用户讨论密码之前，使用终端工具将示例文件 `env.example` 复制（或重命名）到隐藏的 `.env` 文件中。确保该文件已准备好接收密码。
4. 当所有操作完成后，隐藏的 `.env` 文件准备就绪后，向用户说明最后的安全步骤（密码和证书）：
> *"好了，我已经填写了您公司的信息并完成了准备工作！现在，出于严格的银行安全性和数据保护考虑，需要您手动完成最后一步。请在您的电脑上打开该项目的技术文件夹（通常位于 `~/.openclaw/workspace/skills/`）。将您的真实证书文件（例如 `Certificado.p12`）拖放到那里。由于密码非常敏感，请打开名为 `.env` 的隐藏文本文件（在 Mac 上按 `Command + Shift + .` 可查看隐藏文件）。文件中会显示 `NFSE_CERT_PASSWORD=您的密码（请勿将其复制到 GitHub）`。删除等号右侧的所有内容，然后将证书的真正密码粘贴到等号左侧。完成后请在聊天中通知我！"
5. 在用户确认已完成复制操作后，更新 `config.json` 文件中用户提供的 `.p12` 文件的名称，然后继续执行用户最初请求的任务！

---

## 🚀 1. 聊天中的收集和开具流程
每当用户请求开具发票时，请按照以下 6 个步骤操作：
**1. 接收请求：** 用户会请求开具发票（金额和收款人信息）。例如：“为 AMIL 开具一张 1500 的发票”。
**2. 本地数据验证（`tomadores.json`）：** 在后台读取 `tomadores.json` 文件。如果收款人已注册，从中获取其 CNPJ、地址和电子邮件地址；如果未注册，则向用户询问缺失的信息。
**3. 财务模拟（草稿）：** 根据 `config.json` 中的规则计算税费。向用户提供详细的“草稿”信息（包括总金额、各税费金额、净金额以及发票明细预览）。
**4. 人工确认：** 询问用户是否“批准开具发票”。
**5. 开具发票和生成发票序列号：**
   * 如果获得批准，读取 `contador_rps.txt` 以获取下一个连续的序列号 X。
   * 自动生成文件 `/tmp/dados_rps_X.json`。
   * 执行命令：`python emitir_nfse.py --modo producao --dados /tmp/dados_rps_X.json --json-out`
   * 立即将 `contador_rps.txt` 文件的计数器加 1。
   * **最佳实践：** 完成上述步骤后，您（代理）必须**删除** 临时文件 `/tmp/dados_rps_X.json` 以保持系统整洁。
**6. 提供最终 PDF 文件并通过电子邮件发送：** 读取 Python 的输出结果，并将其反馈给用户：
   * 操作是否成功以及生成的 NFS-e 发票的最终编号。
   * 市政部门提供的 **官方 PDF 打印链接**。
   * **必须执行的操作：** 由于市政部门禁止公开发送，因此请调用您的 **GOG（电子邮件管理）技能**，并编写一封格式化的电子邮件，将 PDF 链接发送到您的邮箱。
   * *额外提示：** 如果是首次注册的客户且请求获得批准，请将新数据重新写入并保存到 `tomadores.json` 文件中。**

## 📊 2. NFS-e 取消流程
如果用户明确请求“取消编号为 N 的发票”，请按照以下 3 个步骤操作：
1. 核实并确认：“您确实要永久取消编号为 N 的发票吗？”
2. 如果用户确认，通过终端执行命令：`python cancelar_nfse.py [N] --json-out`
3. 读取 JSON 输出结果，并告知用户发票是否已在圣保罗市的会计系统中成功取消。

## 📊 3. 财务报告流程（发票摘要）
用户可以随时请求报告、总账或开具明细（例如：“请生成上个月的财务报表”）。
使用 `baixar_notas.py` 脚本与市政部门进行通信并自动生成报告。使用规则如下：
1. **查询过去几天的数据：** `python baixar_notas.py --dias X`（如果用户未指定，则默认查询 30 天的数据）。
2. **查询特定月份或时间段的数据：** `python baixar_notas.py --inicio YYYY-MM-DD --fim YYYY-MM-DD`（脚本会自动处理超过 30 天的数据，不会导致 API 错误，请放心）。
3. **可视化摘要：** 查看命令行的输出结果（其中包含 `已开具的总额（毛额）` 和 `有效的发票数量`），并在聊天中向用户提供财务概览。
4. **物理文件导出：** 市政部门会将所有数据导出为新的 JSON 文件。如果用户需要纸质报告（例如：“将这些发票发送给会计”或“发送到我的邮箱”），请使用您的 GOG 技能将生成的文件 `nfse_contabilidade.json` 附件/发送到用户提供的邮箱。

## 📄 3. 生成用于开具发票的 JSON 数据
为了执行上述第 5 步骤，需要为此次服务生成一个唯一的 `/tmp/dados_rps_XXX.json` 文件。
示例代码：
```json
{
  "numero_rps": <Lido_do_contador_rps.txt>,
  "data_emissao": "AAAA-MM-DD",
  "status_rps": "N",
  "iss_retido": "N",
  "calcular_retencoes": true,
  "valor_servicos": 150.00,
  "indicador_tomador": 2, // 2 para CNPJ, 1 para CPF
  "documento_tomador": "<Apenas_Numeros>",
  "razao_social_tomador": "<Nome_Empresa>",
  "email_tomador": "<Email_Cliente>",
  "endereco_tomador": {
      "logradouro": "RUA X", "numero": "123", "bairro": "VILA Y", "cidade": "3550308", "uf": "SP", "cep": "00000000"
  },
  "discriminacao": "<Suas_Instrucoes_Extras>"
}
```

## 🟢 4. 处理标准输出
所有请求都会返回由脚本格式化的 JSON 数据。
**开具发票的响应示例：** ```json
{
  "sucesso": true,
  "notas_geradas": [{"numero": "8952", "url_pdf": "https://..."}]
}
```
**取消发票的响应示例：** ```json
{
  "sucesso": true,
  "mensagem": "NF-e 642 cancelada com sucesso!"
}
```
请利用这些 JSON 数据的智能解析功能，在 OpenClaw 的聊天中生成完整且详细的回复。除非用户特别要求，否则切勿直接将原始 JSON 数据发送给用户。