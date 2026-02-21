---
name: omie
description: "通过 API 实现与 Omie ERP 的集成。可以管理客户、产品、订单、发票（NF-e 格式）、财务数据（应收/应付账款）以及库存信息。当用户需要查询与 Omie ERP 相关的数据（如客户信息、订单详情、发票状态、库存情况或财务数据）时，可以使用该功能。同时，该系统还支持 Webhook，以实现实时事件的通知和处理。"
---
# Omie ERP 技能

通过 REST API 与 Omie ERP 进行集成。

## 设置

需要以下环境变量：
```bash
export OMIE_APP_KEY="your_app_key_here"
export OMIE_APP_SECRET="your_app_secret_here"
```

## API 客户端

使用 Python 脚本执行所有操作：
```bash
python3 skills/omie/scripts/omie_client.py <command> [args]
```

### 可用的命令

#### 客户信息
```bash
python3 scripts/omie_client.py clientes_listar [pagina] [por_pagina]
python3 scripts/omie_client.py clientes_buscar cnpj_cpf=00.000.000/0001-00
python3 scripts/omie_client.py clientes_buscar codigo=1234567
python3 scripts/omie_client.py clientes_detalhar codigo=1234567
```

#### 产品信息
```bash
python3 scripts/omie_client.py produtos_listar [pagina] [por_pagina]
python3 scripts/omie_client.py produtos_detalhar codigo=1234567
```

#### 销售订单
```bash
python3 scripts/omie_client.py pedidos_listar [pagina] [por_pagina]
python3 scripts/omie_client.py pedidos_detalhar numero=1234
python3 scripts/omie_client.py pedidos_status numero=1234
```

#### 财务信息
```bash
python3 scripts/omie_client.py contas_receber [pagina] [por_pagina]
python3 scripts/omie_client.py contas_pagar [pagina] [por_pagina]
python3 scripts/omie_client.py resumo_financeiro
```

#### 发票信息
```bash
python3 scripts/omie_client.py nfe_listar [pagina] [por_pagina]
python3 scripts/omie_client.py nfe_detalhar numero=1234
```

#### 库存信息
```bash
python3 scripts/omie_client.py estoque_posicao [pagina] [por_pagina]
python3 scripts/omie_client.py estoque_produto codigo=1234567
```

## Webhook

Omie 可以向指定的 HTTP 端点发送事件。配置方法如下：
Omie → 设置 → 集成 → Webhook

支持的事件类型：
- `pedido.incluido` / `pedido.alterado`（订单已添加 / 订单已修改）
- `nfe.emitida` / `nfe.cancelada`（发票已生成 / 发票已取消）
- `financas.recebido` / `financas.pago`（收款 / 支付）
- `cliente.incluido` / `cliente.alterado`（客户已添加 / 客户已修改）

要启动 Webhook 接收器，请执行以下操作：
```bash
python3 scripts/omie_webhook.py --port 8089
```

## API 限制

- **速率限制：** 每个应用每秒最多 3 个请求
- **分页：** 每页最多显示 500 条记录
- **超时：** 30 秒