# Unbrowse - API流量技能生成工具

该工具通过捕获并分析HTTP API流量，自动生成OpenClaw技能。它能够记录HAR（HTTP存档）文件，提取API模式，并生成可直接使用的OpenClaw技能定义。

## 命令

### 捕获（Capture）

```
unbrowse capture <url> [--output <path>]
```
使用无头浏览器（CDP）从指定URL捕获HTTP流量，并将结果保存为HAR文件以供分析。

### 分析（Analyze）

```
unbrowse analyze <har-file> [--json]
```
分析HAR文件，提取API端点、认证模式、请求/响应格式以及速率限制等信息。

### 生成（Generate）

```
unbrowse generate <har-file> --name <skill-name> [--output-dir <path>]
```
根据HAR文件生成完整的OpenClaw技能包：
- 包含技能定义的SKILL.md文件
- 包含API方法实现的lib/api_client.py文件
- 包含认证逻辑的lib/auth.py文件
- 以及一个名为scripts/<name>.py的CLI入口脚本

### 列出（List）

```
unbrowse list [--dir <skills-dir>]
```
列出所有生成的技能及其状态。

### 发布（Publish）

```
unbrowse publish <skill-dir> [--price <usdc>] [--registry <url>]
```
将生成的技能发布到ClawHub市场平台。
支持使用Base/Solana网络进行x402 USDC支付。

## 环境变量

- `UNBROWSE_OUTPUT_DIR` - 生成技能的默认输出目录（默认值：./generated-skills）
- `UNBROWSE_CHROME_PATH` - 用于CDP捕获的Chrome/Chromium浏览器路径
- `CLAWHUB_API_KEY` - 用于发布技能到ClawHub市场的API密钥
- `CLAWHUB_WALLET` - 用于接收技能销售收益的USDC钱包地址

## 所需依赖项

- Python 3.11及以上版本
- httpx（HTTP客户端库）
- playwright（可选，用于CDP捕获功能）