# 财务管理技能

个人财务管理工具：能够解析财务账单、存储交易记录并查询支出情况。

## 数据存储位置
- 交易记录：`~/.openclaw/workspace/finance/transactions.json`
- 原始账单文件：`~/.openclaw/workspace/finance/statements/`

*存储规范：`~/.openclaw/workspace/` 是 OpenClaw 工作区的标准路径，用于存储用户的持久化数据。会话数据和其他相关数据也会存储在该路径下。如果需要，凭证/配置文件可以保存在 `~/.config/finance/` 中。*

## 使用工具

### 1. 解析账单
当用户分享账单文件（图片或 PDF 格式）时：
**⚠️ 重要提示：Telegram 或相关渠道的预览功能会截断 PDF 文件！**  
请务必先使用 `pypdf` 工具提取所有页面内容：

```bash
python3 -c "
import pypdf
reader = pypdf.PdfReader('/path/to/statement.pdf')
for i, page in enumerate(reader.pages):
    print(f'=== PAGE {i+1} ===')
    print(page.extract_text())
"
```

然后解析提取出的文本：
1. 从所有页面中提取交易信息；
2. 将提取到的交易信息转换为 JSON 数组（格式：`[{date, merchant, amount, category}, ...]`）；
3. 运行 `scripts/add-transactions.sh` 脚本将数据添加到存储文件中；
4. **验证支出总额是否与账单一致**（所有支出的总和应与账单上的“总金额”相符）。

**数据提取格式：**
```
Each transaction: {"date": "YYYY-MM-DD", "merchant": "name", "amount": -XX.XX, "category": "food|transport|shopping|bills|entertainment|health|travel|other"}
Negative = expense, positive = income/refund.
```

**支出类别：**
- 食物：餐厅、杂货、咖啡、快餐
- 交通：Waymo、Uber、汽油费、公共交通
- 购物：实体店购物、在线购物
- 账单：水电费、订阅服务
- 娱乐：电影、音乐会、主题公园
- 健康：药店、医疗费用
- 旅行：酒店费用、机票费用

### 2. 查询交易记录
用户询问支出情况时，系统会读取 `transactions.json` 文件，然后根据用户需求进行过滤和汇总后给出答案：
- **示例查询：**
  - “我上个月花了多少钱？” → 计算指定时间范围内的总支出；
  - “我在食物上花了多少钱？” → 按类别筛选支出；
  - “显示我的最大支出项目？” → 按支出金额排序显示。

### 3. 手动添加交易记录
用户输入“我在某处花费了 X 美元”时，系统会将该交易信息添加到 `transactions.json` 文件中。

## 文件格式
```json
{
  "transactions": [
    {
      "id": "uuid",
      "date": "2026-02-01",
      "merchant": "Whole Foods",
      "amount": -87.32,
      "category": "food",
      "source": "statement-2026-01.pdf",
      "added": "2026-02-09T19:48:00Z"
    }
  ],
  "accounts": [
    {
      "id": "uuid",
      "name": "Coinbase Card",
      "type": "credit",
      "lastUpdated": "2026-02-09T19:48:00Z"
    }
  ]
}
```

## 使用流程
1. 用户：分享账单图片；
2. 代理程序通过视觉识别技术提取交易信息并确认交易数量；
3. 代理程序运行 `add-transactions.sh` 脚本将交易信息存储到数据库中；
4. 用户提问：“我在食物上花了多少钱？”
5. 代理程序读取数据库数据并给出查询结果。

## 所需依赖库
- `jq`：用于处理 JSON 数据的存储和查询（可通过 `apt install jq` 或 `brew install jq` 安装）；
- `pypdf`：用于提取 PDF 文件的全部文本内容（可通过 `pip3 install pypdf` 安装）。

## 经验总结：
- **注意：Telegram 的预览功能会截断 PDF 文件内容**，务必使用 `pypdf` 提取所有页面；
- 在导入数据前，请务必核对提取出的支出总额是否与账单上的总金额一致；
- 该系统目前仅支持通过 Coinbase Card 收集交易数据，不支持 Plaid 服务。

## 未来计划：
- 集成 Plaid 服务，实现通过 Plaid 进行 OAuth 认证；
- 自动同步用户关联银行账户的交易记录；
- 保持相同的查询接口，但数据来源将变为 Plaid 提供的银行数据。