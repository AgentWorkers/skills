---
name: CSVKit Next - Advanced CSV Toolkit
description: 转换、过滤、合并、验证和分析 CSV 文件。完全无需依赖任何第三方库或工具。这是一个功能强大的 CSV 处理工具，支持通过命令行进行操作，且完全免费。
---

# CSVKit Next

一个功能强大的CSV文件处理工具，支持过滤、转换、合并、验证和分析操作。

## 安装

```bash
npm install -g @lxgicstudios/csvkit-next
```

## 命令

### 过滤行

```bash
csvkit filter data.csv age gt 30
csvkit filter users.csv email contains @gmail
csvkit filter sales.csv status eq completed
```

支持的操作符：eq（等于）、ne（不等于）、gt（大于）、lt（小于）、gte（大于或等于）、lte（小于或等于）、contains（包含）、startswith（以...开头）、endswith（以...结尾）、regex（正则表达式）、empty（为空）、notempty（非空）

### 转换列数据

```bash
csvkit transform data.csv "full_name=first+' '+last"
csvkit transform prices.csv "total=price*quantity"
csvkit transform users.csv "domain=email.split('@')[1]"
```

### 合并文件

```bash
csvkit merge users.csv orders.csv -o combined.csv
```

### 验证数据格式

```bash
csvkit validate data.csv
csvkit validate data.csv schema.json
```

示例数据结构：
```json
{
  "required": ["id", "email"],
  "types": { "age": "number", "email": "email" }
}
```

### 统计分析

```bash
csvkit stats sales.csv
```

可以显示：行数、列数、最小值/最大值/平均值、唯一值等信息。

### 其他命令

```bash
csvkit head data.csv 20          # First 20 rows
csvkit tail data.csv 20          # Last 20 rows
csvkit columns data.csv          # List columns
csvkit sort data.csv price desc  # Sort
csvkit unique data.csv category  # Unique values
csvkit sample data.csv 50        # Random rows
csvkit convert data.csv -t json  # To JSON
```

## 常见使用场景

- **过滤高价值订单：**
```bash
csvkit filter orders.csv total gt 1000 -o high_value.csv
```

- **添加计算列：**
```bash
csvkit transform sales.csv "profit=revenue-cost" -o with_profit.csv
```

- **快速查看数据概览：**
```bash
csvkit stats large_dataset.csv
```

## 主要特性

- 无依赖项
- 能够快速处理大型文件
- 支持基于表达式的数据转换
- 提供数据格式验证功能
- 支持多种输出格式

---

**由 [LXGIC Studios](https://lxgicstudios.com) 开发**

🔗 [GitHub](https://github.com/lxgicstudios/csvkit-next) · [Twitter](https://x.com/lxgicstudios)