---
name: mcp-colombia
description: "MCP Colombia Hub——通过MCP协议整合了哥伦比亚的各种服务。该平台集成了Soulprint身份验证功能，可在用户执行敏感操作前对其进行身份验证。适用场景包括：在MercadoLibre平台上搜索商品、通过Booking.com预订酒店（实时价格查询）、查询航班信息（Avianca/LATAM/Skyscanner）、通过El Empleo/Computrabajo/LinkedIn等平台申请职位、比较哥伦比亚的货币兑换率（CDT）、模拟信贷/贷款申请，以及比较哥伦比亚境内的银行账户信息。使用该服务需要安装支持MCP协议的客户端软件（如Claude Desktop、OpenClaw等）。"
homepage: https://www.npmjs.com/package/mcp-colombia-hub
metadata:
  {
    "openclaw":
      {
        "emoji": "🇨🇴",
        "requires": { "bins": ["node", "npx"] },
      },
  }
---
# MCP Colombia Hub

该工具将哥伦比亚的各种服务整合到一个MCP服务器中，用户可以在此查询产品信息、查找酒店和航班信息，并比较金融产品。

**npm包链接：** https://www.npmjs.com/package/mcp-colombia-hub  
**GitHub仓库链接：** https://github.com/manuelariasfz/mcp-colombia  
**版本：** 1.3.0  

---

## 使用场景  

✅ **适用场景：**  
- 在MercadoLibre Colombia平台上搜索产品  
- 在哥伦比亚的[城市]中查找[日期]至[日期]期间的酒店  
- 查询从[出发地]到[目的地]的航班信息  
- 比较哥伦比亚银行的CDT（Certificado de Depósito a Término）利率  
- 模拟为期Y个月的贷款/信贷申请  
- 比较哥伦比亚银行的储蓄账户信息  

❌ **不适用场景：**  
- 从其他国家查询MercadoLibre的数据（请使用其官方的机器学习API）  
- 实时股票价格或外汇信息查询（请使用专门的金融API）  

---

## 安装方法  

### Claude Desktop / OpenClaw（配置文件：`claude_desktop_config.json` 或 `mcp.json`）  
（安装步骤请参考相应文档或GitHub仓库中的说明。）  

---

## 可用工具（共10个）  

### 🛒 MercadoLibre  
#### `ml_buscar_productos`  
在MercadoLibre Colombia平台上搜索产品。  

#### `mldetalle_producto`  
获取MercadoLibre商品列表的详细信息。  

---

### ✈️ 旅行（Awin / Booking.com）  
#### `viajes_buscar_hotel`  
通过Booking.com搜索酒店（支持实时数据，版本1.2.2）。  

#### `viajes_buscar_vuelos`  
查询航班信息，并提供实时价格参考（版本1.2.2）。  

---

### 💰 金融  
#### `finanzas_comparar_cdt`  
比较哥伦比亚银行的CDT利率。  

#### `finanzas_simular_credito`  
模拟在哥伦比亚银行的贷款申请。  

#### `finanzas_comparar_cuentas`  
比较哥伦比亚银行的储蓄账户信息。  

---

## Soulprint身份验证集成（版本1.3.0）  
该服务器支持使用Soulprint身份令牌进行身份验证：  

#### `soulprint_status`  
检查用户是否拥有有效的Soulprint身份，并查询其在线声誉信息。  

---

**工具使用要求：**  
- **标准工具**：评分≥0（可自由使用）  
- **求职申请（trabajo_aplicar）**：评分≥40（需要基本身份验证）  

### `trabajo_aplicar`（职位搜索工具，版本1.2.2）  
- 需要`BRAVE_API_KEY`环境变量以支持实时职位搜索。  
- 良好的工具使用行为会为用户增加信誉分（+1）。  

---

## 使用示例：  
- **产品搜索**  
- **CDT利率比较**  
- **酒店查询**  
- **贷款模拟**  

---

## 注意事项：  
- MercadoLibre的数据通过直接API获取（无需额外密钥）  
- 酒店/航班信息来自Booking.com的实时数据；相关链接为Awin联盟链接（发布者ID：2784246）  
- 求职信息来自El Empleo、Computrabajo、LinkedIn、Indeed等平台（通过Brave Search获取）  
- 金融数据来源于银行的公开利率页面  
- 所有价格均以哥伦比亚比索（COP）为单位显示。