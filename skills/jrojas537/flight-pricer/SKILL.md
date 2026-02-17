# flight-pricer 技能

这是一个命令行接口（CLI），用于使用 Duffel API 搜索航班价格。

该技能被设计为一个专业级别的 CLI 工具，其设计理念借鉴了 `gog` 技能的高质量标准。

## 先决条件

- Python 3.7 及以上版本和 `pip`。
- 一个 Duffel API 密钥。

## 安装

该技能被设计为可以在自己的虚拟环境中安装为一个独立的命令行工具。这样可以隔离其依赖项，并使其在整个系统中可供代理使用。

在 workspace 的根目录下执行以下命令：

```bash
# 1. Activate the virtual environment
source flight-pricer/.venv/bin/activate

# 2. Perform an editable install
pip install -e flight-pricer/

# 3. Deactivate (optional, the command is now linked)
deactivate
```

此操作只需执行一次。

## 设置

在搜索航班之前，您必须使用您的 Duffel API 密钥来配置该技能。

### `config set`

将您的 API 密钥安全地保存到 `~/.config/flight-pricer/config.yaml` 文件中。

**使用方法：**
```bash
flight-pricer config set --api-key <YOUR_DUFFEL_API_KEY>
```

## 命令

### `search`

根据指定的条件搜索航班信息。该命令会自动使用您配置中的 API 密钥。

**使用方法：**
```bash
flight-pricer search [OPTIONS]
```

**必选参数：**

- `--from <IATA>`：出发机场的 IATA 代码（例如：`DTW`）。
- `--to <IATA>`：到达机场的 IATA 代码（例如：`MIA`）。
- `--depart <YYYY-MM-DD>`：出发日期。

**可选参数：**

- `--return <YYYY-MM-DD>`：往返航班的返回日期。
- `--passengers <number>`：乘客人数（默认值：1）。
- `--max-stops <number>`：最大中转次数。
- `--non-stop`：`--max-stops 0` 的简写形式。
- `--cabin <class>`：舱位等级。可选值：`economy`、`business`、`first`、`premium_economy`。

**示例：**

搜索从底特律到迈阿密的直达头等舱航班，出发日期为 2026 年 4 月 6 日，返回日期为 2026 年 4 月 10 日，适用于 1 位乘客。

```bash
flight-pricer search --from DTW --to MIA --depart 2026-04-06 --return 2026-04-10 --non-stop --cabin first
```