---
name: lean
description: 运行 QuantConnect LEAN 回测工具，并管理美国股票的算法开发工作。当需要回测交易策略、运行 LEAN 算法、分析回测结果、下载市场数据或将其部署到 Interactive Brokers TWS 平台时，请使用该工具。该工具涵盖了算法创建、数据管理、配置编辑以及结果分析等核心功能。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["dotnet"], "anyBins": ["python3", "python"], "env": ["LEAN_ROOT", "DOTNET_ROOT", "PYTHONNET_PYDLL"] },
        "install":
          [
            {
              "id": "dotnet",
              "kind": "download",
              "url": "https://dotnet.microsoft.com/download/dotnet/8.0",
              "label": "Install .NET 8 SDK"
            }
          ]
      }
  }
---
# LEAN引擎 — QuantConnect算法交易

## 先决条件与设置

### 必需的环境变量

| 变量 | 用途 | 示例 |
|----------|---------|---------|
| `LEAN_ROOT` | 克隆的LEAN仓库路径 | `/home/user/lean` |
| `DOTNET_ROOT` | .NET SDK的安装路径 | `/home/user/.dotnet` |
| `PYTHONNET_PYDLL` | Python共享库的路径（LEAN的pythonnet模块所需） | `$LEAN_ROOT/.libs/libpython3.11.so.1.0` |

在使用此功能之前，必须设置这三个环境变量。请将它们添加到您的shell配置文件中：
```bash
export LEAN_ROOT="$HOME/lean"
export DOTNET_ROOT="$HOME/.dotnet"
export PATH="$PATH:$DOTNET_ROOT"
export PYTHONNET_PYDLL="$LEAN_ROOT/.libs/libpython3.11.so.1.0"
```

> **注意：** LEAN在其`$LEAN_ROOT/.libs/`目录中包含了自身的Python共享库。如果您是从源代码编译了LEAN，那么编译完成后该库应该已经存在。如果不存在，请安装`libpython3.11-dev`，并将`PYTHONNET_PYDLL`指向系统中的`libpython3.11.so`文件。

### 首次设置

1. **安装.NET 8 SDK：**
   ```bash
   # Linux/macOS
   wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh
   chmod +x dotnet-install.sh
   ./dotnet-install.sh --channel 8.0
   export DOTNET_ROOT="$HOME/.dotnet"
   export PATH="$PATH:$DOTNET_ROOT"
   ```

2. **克隆并编译LEAN：**
   ```bash
   git clone https://github.com/QuantConnect/Lean.git "$LEAN_ROOT"
   cd "$LEAN_ROOT"
   dotnet build QuantConnect.Lean.sln -c Debug
   ```

3. **下载初始市场数据：**
   ```bash
   pip install yfinance pandas
   python3 {baseDir}/scripts/download_us_universe.py --symbols sp500 --start 2020-01-01 --data-dir "$LEAN_ROOT/Data"
   ```

4. **验证设置：**
   ```bash
   ls "$LEAN_ROOT/Data/equity/usa/daily/"  # Should list .zip files
   ls "$LEAN_ROOT/Launcher/bin/Debug/"      # Should contain QuantConnect.Lean.Launcher.dll
   ```

## 环境配置

- **LEAN源代码：** `$LEAN_ROOT/`
- **启动器（预编译版本）：** `$LEAN_ROOT/Launcher/bin/Debug/`
- **配置文件：** `$LEAN_ROOT/Launcher/config.json`
- **Python算法代码：** `$LEAN_ROOT/Algorithm.Python/`
- **市场数据：** `$LEAN_ROOT/Data/`
- **.NET SDK：** `$DOTNET_ROOT/dotnet`（将路径添加到PATH环境变量中：`export PATH="$PATH:$DOTNET_ROOT"`）

## 快速参考

### 运行回测

1. 将算法代码保存到`$LEAN_ROOT/Algorithm.Python/YourAlgo.py`文件中。
2. 修改配置文件以指定该算法的路径。
3. 运行回测脚本：
   ```bash
   export PATH="$PATH:$DOTNET_ROOT"
   cd "$LEAN_ROOT/Launcher/bin/Debug"
   dotnet QuantConnect.Lean.Launcher.dll
   ```
4. 结果将显示在标准输出（stdout）和`$LEAN_ROOT/Results/`目录中。

**或者使用辅助脚本：**
```bash
bash {baseDir}/scripts/run_backtest.sh YourClassName YourAlgo.py
```

### 配置文件编辑

使用以下字段编辑`$LEAN_ROOT/Launcher/config.json`：

| 字段 | 用途 | 示例 |
|-------|---------|---------|
| `algorithm-type-name` | Python类名 | `"MyStrategy"` |
| `algorithm-language` | 语言 | `"Python"` |
| `algorithm-location` | .py文件的路径 | `"../../../Algorithm.Python/MyStrategy.py"` |
| `data-folder` | 市场数据路径 | `"../Data/"` |
| `environment` | 模式 | `"backtesting"` 或 `"live-interactive"` |

对于IB实时交易，请将`environment`设置为`"live-interactive"`，并配置相应的字段（账户、用户名、密码、主机、端口和交易模式）。

### 数据管理

**检查可用数据：**
```bash
ls "$LEAN_ROOT/Data/equity/usa/daily/"
```

**数据格式：** 数据文件为ZIP格式，包含CSV格式的数据。每行数据格式为：
`YYYYMMDD HH:MM,Open*10000,High*10000,Low*10000,Close*10000,Volume`

价格以整数形式存储（实际值为价格的10000倍）。LEAN会自动处理数据格式的转换。

**下载更多数据：**
```bash
python3 {baseDir}/scripts/download_us_universe.py --symbols sp500 --data-dir "$LEAN_ROOT/Data"
```

有关扩展数据来源的更多方法，请参阅`{baseDir}/references/data-download.md`。

### 编写算法

LEAN的Python算法继承自`QCAlgorithm`类：

```python
from AlgorithmImports import *

class MyAlgo(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2024, 1, 1)
        self.SetEndDate(2025, 1, 1)
        self.SetCash(100_000)
        self.AddEquity("SPY", Resolution.Daily)
        self.SetBenchmark("SPY")
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage,
                               AccountType.Margin)

    def OnData(self, data):
        if not self.Portfolio.Invested:
            self.SetHoldings("SPY", 1.0)
```

**关键API方法：**
- `self.History(symbol, periods, resolution)` — 获取历史数据
- `self.SetHoldings(symbol, weight)` — 设置投资组合权重
- `self.Liquidate(symbol)` — 平仓
- `self.AddUniverse(coarse_fn, fine_fn)` — 动态选择数据源
- `self.Schedule.On(date_rule, time_rule, action)` — 安排事件
- `self.Debug(msg)` — 日志输出

### 分析结果

回测完成后，请检查回测结果：
```bash
ls "$LEAN_ROOT/Results/"
# Key files: *-log.txt, *-order-log.txt, *.json (statistics)
```

### 重新编译LEAN（如果源代码有更改）

```bash
export PATH="$PATH:$DOTNET_ROOT"
cd "$LEAN_ROOT"
dotnet build QuantConnect.Lean.sln -c Debug
```

## 安全注意事项

### `config.json`的安全性

`run_backtest.sh`脚本**不会**修改您的原始`config.json`文件。它会：
1. 以只读方式读取原始配置文件作为模板。
2. 创建一个新的`config.backtest.json`文件，仅修改与算法相关的字段（类名、文件路径、语言和模式）。
3. 在运行回测时使用新的配置文件，测试完成后会恢复原始配置文件。

`configure_algo.py`辅助脚本会在一个独立的输出文件中执行字段替换操作。您的原始配置文件（包括用于实时交易的IB账户信息）不会被修改。

**仅在临时副本中修改的字段：**
- `algorithm-type-name` — 设置为所需的类名
- `algorithm-language` — 设置为`Python`
- `algorithm-location` — 设置为所需的.py文件路径
- `environment` — 设置为`backtesting`

### 网络访问

设置过程中涉及网络下载操作：
- 从GitHub（QuantConnect/Lean仓库）使用`git clone`命令克隆代码。
- 使用`dotnet build`命令编译代码。
- 使用`pip install yfinance pandas`命令安装Python包。
- 使用`download_us_universe.py`脚本从Yahoo Finance下载市场数据。

所有数据来源均为公开可用的资源。为确保安全性，建议在容器或虚拟机中运行设置脚本。

### 环境变量

运行此功能需要以下环境变量：
- `LEAN_ROOT` — 克隆的LEAN仓库路径
- `DOTNET_ROOT` — .NET SDK的安装路径
- `PYTHONNET_PYDLL` — Python共享库的路径（如果未设置，系统会自动从`$LEAN_ROOT/.libs/`目录中查找）

这些环境变量已在技能元数据中声明，使用前必须进行设置。

## 故障排除

- **“未找到数据文件”** → 检查`config.json`中的`data-folder`字段是否指向正确的路径。
- **Python导入错误** → LEAN自带了Python环境；如果使用了自定义包，请检查`python-venv`配置。
- **回测速度慢** → 减少数据源的数量或时间范围；调整`resolution`参数（例如，从“Minute”改为“Daily”）。
- **IB连接问题** → 确保TWS/Gateway正在运行，并且端口号与配置文件中的设置一致（默认为4002）。
- **未设置`LEAN_ROOT`** → 将`export LEAN_ROOT="$HOME/lean"`添加到shell配置文件中。
- **未找到`.NET SDK`** — 将`export PATH="$PATH:$DOTNET_ROOT"`添加到shell配置文件中。
- **`Runtime.PythonDLL`未设置** — 将`PYTHONNET_PYDLL`设置为正确的Python共享库路径（参见上述环境变量表）。