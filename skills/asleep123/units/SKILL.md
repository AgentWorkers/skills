---
name: units
description: 使用 GNU Units 进行单位转换和计算。
metadata: {"clawdbot":{"emoji":"📏","requires":{"bins":["units"]}}}
---

# GNU Units 技能

使用 GNU 的 `units` 命令行工具来进行单位转换和计算。可以通过 `brew` 或 `apt` 在系统中安装 `units` 工具。

## 使用方法

使用 `bash` 命令来运行 `units` 命令。使用 `-t`（简洁）标志可以仅获取数值结果。

```bash
units -t 'from-unit' 'to-unit'
```

### 示例

**基本转换：**
```bash
units -t '10 kg' 'lbs'
# Output: 22.046226
```

**复合单位：**
```bash
units -t '60 miles/hour' 'm/s'
# Output: 26.8224
```

**温度（非线性转换）：**
温度单位需要特定的语法：`tempF(x)`、`tempC(x)`、`tempK(x)`。
```bash
units -t 'tempF(98.6)' 'tempC'
# Output: 37
```

**时间：**
```bash
units -t '2 weeks' 'seconds'
```

**输出格式化：**
要将结果保留到指定的小数位数（例如 3 位），使用 `-o "%.3f"`：
```bash
units -t -o "%.3f" '10 kg' 'lbs'
# Output: 22.046
```

**单位定义查询：**
要查看某个单位的定义（不进行转换），可以省略第二个参数（不使用 `-t` 时，输出会更详细/更有用）：
```bash
units '1 acre'
```

## 注意事项

- **货币：** `units` 支持货币单位（如 USD、EUR 等），但由于单位定义文件中的汇率是静态的，因此汇率可能不够准确。
- **安全性：** 在使用 `units` 时，请务必为输入的单位加上引号，以避免 shell 解释问题（例如：`units -t '1/2 inch' 'mm'`）。