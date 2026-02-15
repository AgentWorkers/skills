# Oura Ring CLI 工具

## 说明
该工具通过命令行接口（CLI）从 Oura Ring API（V2）获取用户的健康和生物特征数据。您可以使用它来了解用户的睡眠情况、活动量、状态以及生理指标。

仓库地址：[https://github.com/ruhrpotter/oura-cli](https://github.com/ruhrpotter/oura-cli)

## 安装

### 1. 构建 CLI
```bash
cd ~
git clone https://github.com/ruhrpotter/oura-cli.git
cd oura-cli
go build -o oura ./cmd/oura
```

### 2. 创建 Oura OAuth 应用
1. 访问 [Oura 开发者门户](https://cloud.ouraring.com/oauth/developer)
2. 创建一个新的应用程序
3. 将重定向 URI 设置为：`http://localhost:8080/callback`
4. 记下您的 **客户端 ID** 和 **客户端密钥**

### 3. 进行身份验证
```bash
export OURA_CLIENT_ID="your_client_id"
export OURA_CLIENT_SECRET="your_client_secret"
./oura auth login
```

系统会打开一个浏览器窗口进行 OAuth 授权。授权生成的令牌将存储在 `~/.config/oura-cli/config.json` 文件中。

## 先决条件
必须先完成 CLI 的身份验证。如果命令执行失败并出现授权错误，请提示用户运行 `./oura auth login` 来完成身份验证。

## 语法
`./oura get <类别> [参数]`

## 可用的类别
- `personal`：用户个人信息（年龄、体重、身高、电子邮件）
- `sleep`：每日睡眠评分和效率
- `activity`：每日活动量、步数及运动情况
- `readiness`：每日状态评分（表示身体的恢复情况）
- `heartrate`：心率数据的时间序列
- `workout`：详细的锻炼记录
- `spo2`：血氧饱和度
- `sleep-details`：详细的睡眠记录（包括睡眠图）
- `sessions`：活动记录（如小憩、休息等）
- `sleep-times`：最佳就寝时间建议
- `stress`：每日压力水平
- `resilience`：每日恢复力评分
- `cv-age`：心血管年龄估算
- `vo2-max`：最大摄氧量（VO2 Max）
- `ring-config`：Ring 硬件配置（颜色、尺寸等）
- `rest-mode`：休息模式的时间段
- `tags`：自定义标签（备注、生活方式等）

## 参数
- `--start <YYYY-MM-DD>`：大多数时间序列数据所需的参数。指定数据范围的开始日期。
- `--end <YYYY-MM-DD>`：可选参数。指定数据范围的结束日期。如果省略，系统可能会默认使用开始日期，或根据具体情况返回单日数据。

## 使用说明
1. **日期解析**：所有相对日期（如 “today”、“yesterday”、“last week”、“this month”）都必须根据当前日期转换为绝对的 `YYYY-MM-DD` 格式。
2. **日期范围**：
    - “today”：将 `--start` 设置为当前日期。
    - “yesterday”：将 `--start` 设置为昨天。
    - “last 7 days”：将 `--start` 设置为 7 天前，`--end` 设置为今天。
3. **路径**：默认情况下，二进制文件位于当前工作目录下的 `./oura`。
4. **输出**：CLI 以 JSON 格式返回数据。您需要解析这些 JSON 数据以生成易于理解的自然语言响应。

## 示例

**用户请求**：“我昨晚的睡眠情况如何？”
**背景**：今天是 2024-03-15。“Last night” 通常指的是截至今天早上的睡眠数据，具体取决于 Oura 的日期计算方式（Oura 按睡眠结束的早晨来记录日期）。
**处理方式**：2024-03-14 夜间的睡眠数据会被记录为 `2024-03-15`。
**命令**：
```bash
./oura get sleep --start 2024-03-15
```

**用户请求**：“我今天的状态评分是多少？”
**背景**：今天是 2024-03-15。
**命令**：
```bash
./oura get readiness --start 2024-03-15
```

**用户请求**：“显示我 2024 年 1 月的第一周的心率数据。”
**命令**：
```bash
./oura get heartrate --start 2024-01-01 --end 2024-01-07
```

**用户请求**：“我是谁？”
**命令**：
```bash
./oura get personal
```