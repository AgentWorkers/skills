# hotel-pricer 技能

这是一个基于 Go 的命令行工具（CLI），用于通过 Amadeus API 检索酒店的可用性和价格信息。

## 描述

该工具允许代理根据城市、入住/退房日期和客人数量来查找酒店优惠信息。它能够安全地管理 Amadeus API 的凭证，并提供格式化的 JSON 输出结果。

## 先决条件

- 安装了 `go` 开发语言环境。
- 拥有 Amadeus for Developers 账户，并获取 API 密钥和密钥串。

## 安装

需要编译 `hotel-pricer` 可执行文件，并将其添加到系统的 `PATH` 环境变量中。

```bash
# From the hotel-pricer source directory
go build
sudo mv hotel-pricer /usr/local/bin/
```

## 配置

在使用前必须设置 API 凭证信息。

```bash
hotel-pricer config set --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET
```

## 使用方法

### 搜索酒店

```bash
hotel-pricer search --city <IATA_CODE> --check-in <YYYY-MM-DD> --check-out <YYYY-MM-DD> [flags]
```

**示例：**
```
hotel-pricer search --city NYC --check-in 2024-12-24 --check-out 2024-12-28 --guests 2
```

### 常用参数：

- `--city, -c`：城市代码（IATA 格式）（必填）
- `--check-in, -i`：入住日期（YYYY-MM-DD 格式）（必填）
- `--check-out, -o`：退房日期（YYYY-MM-DD 格式）（必填）
- `--guests, -g`：客人数量（默认值：1）
- `--radius, -r`：搜索半径（以公里为单位）（默认值：20）
```