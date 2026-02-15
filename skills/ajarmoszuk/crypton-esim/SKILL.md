---
name: crypton-esim
description: 使用 BTC/XMR 或银行卡购买匿名 eSIM 卡——无需注册账户
---

# Crypton eSIM

您可以直接通过聊天窗口购买匿名eSIM卡。支持使用比特币（Bitcoin）、门罗币（Monero）或信用卡支付，无需注册账户。

## 相关术语/命令

- **esim**：浏览并购买170多个国家的eSIM卡。
- **buy**：使用您选择的支付方式购买eSIM套餐。
- **status**：查询现有订单的状态。
- **help**：显示可用的命令及其使用说明。

## 功能特性

- 支持170多个国家的eSIM卡购买。
- 无需注册账户即可匿名购买。
- 支付方式包括比特币（BTC）、门罗币（XMR）或信用卡。
- 提供实时订单状态跟踪功能。
- 可获取激活码和二维码。
- 无需使用API密钥。

## 示例对话

LPA:1$smdp.example.com$ACTIVATION-CODE

## API说明

本技能使用了Crypton的Guest eSIM API：

- **基础URL**：`https://crypton.sh/api/v1/guest/esim`
- **认证方式**：无需认证。
- **文档链接**：https://crypton.sh/esim/guest

### API端点

| 方法        | 端点            | 描述                                      |
|------------|------------------|----------------------------------------|
| GET        | `/plans`         | 列出可购买的eSIM套餐                         |
| GET        | `/countries`       | 列出提供eSIM服务的国家                         |
| POST        | `/checkout`       | 创建购买请求                             |
| GET        | `/order/{uuid}`      | 查询订单状态                             |
| POST        | `/refresh/{uuid}`      | 更新订单的使用数据                         |

## 速率限制

- **GET请求**：每分钟30次请求。
- **/checkout**：每分钟10次请求。
- **/refresh**：每分钟5次请求。

## 配置参数

| 参数        | 默认值          | 描述                                      |
|------------|------------------|----------------------------------------|
| `api_base_url` | `https://crypton.sh/api/v1/guest/esim` | API基础URL                             |
| `default_payment_method` | `btc`         | 默认支付方式（比特币/门罗币/Stripe）                   |

## 所需依赖库

- Python 3.7及以上版本
- `requests`库

## 文件结构

- `SKILL.md`：本技能的配置文件。
- `crypton_esim.py`：技能的具体实现代码。
- `README.md`：附加的使用说明文档。
- `requirements.txt`：Python项目的依赖库列表。

## 测试说明

（测试相关内容请参见`CODE_BLOCK_2_`）

## 技术支持

- 官方网站：https://crypton.sh
- API文档：https://crypton.sh/esim/guest

## 许可证

本技能遵循MIT许可证（MIT License）。