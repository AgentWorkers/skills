---
name: srt
description: 韩国SRT（Super Rapid Train）的搜索、预订及票务管理
homepage: https://github.com/khj809/openclaw-srt-skill
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🚅",
        "requires": { "bins": ["python3", "uv"], "env": ["SRT_PHONE", "SRT_PASSWORD"] },
        "install": [
          {"id": "uv", "kind": "uv", "package": "SRTrain", "label": "Install SRTrain from PyPI (uv) — source: https://pypi.org/project/SRTrain / https://github.com/ryanking13/SRT"}
        ]
      },
  }
---
# SRT 韩国火车服务技能

## 先决条件

在运行脚本之前，必须设置环境变量 `SRT_PHONE`（格式：`010-XXXX-XXXX`）和 `SRT_PASSWORD`。

## 参考

**环境变量：**
| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `SRT_PHONE` | ✅ | SRT 账户电话号码（必须使用连字符：`010-XXXX-XXXX`） |
| `SRT_PASSWORD` | ✅ | SRT 账户密码 |
| `SRT_DATA_DIR` | 可选 | 用于存储日志、缓存和状态文件的目录。默认为系统临时目录（`/tmp/srt`）。 |

**车站名称**（仅限韩文）：
수서（水西）、부산（釜山）、동대구（东大邱）、대전（大田）、천안아산（天安牙山）、오송（乌松）、광주송정（光州松亭）、울산（蔚山）、포항（浦项）、경주（庆州）、김천구미（金川九美）、익산（益山）、전주（全州）、목포（木浦）、신경주（新庆州）

**日期：** `YYYYMMDD` · **时间：** `HHMMSS`（例如：`200000` 表示 20:00）

---

## 命令

### 搜索
```bash
cd <project_dir> && uv run --with SRTrain python3 scripts/srt_cli.py search \
  --departure "수서" --arrival "동대구" --date "20260227" --time "200000"
```
搜索参数和结果会被缓存（保存在 `SRT_DATA_DIR` 目录中），并且是 `reserve` 命令所必需的。

### 预订（一次性）
```bash
cd <project_dir> && uv run --with SRTrain python3 scripts/srt_cli.py reserve --train-id "1"
```
`--train-id` 是搜索结果中的索引（从 1 开始）。必须先运行 `search` 命令。

### 查看预订信息
```bash
cd <project_dir> && uv run --with SRTrain python3 scripts/srt_cli.py list --format json
```

### 取消预订
```bash
cd <project_dir> && uv run --with SRTrain python3 scripts/srt_cli.py cancel \
  --reservation-id "RES123456" --confirm
```

---

## 持续监控（取消订单的监控）

对于“不断尝试直到有座位可用”的请求，请**不要在 cron 作业中循环执行**。
正确的做法是：运行 `makereservation.py --retry` 作为持续的后台进程，然后创建另一个 cron 作业来读取日志并生成报告。

### 第一步：搜索（填充缓存）
```bash
cd <project_dir> && uv run --with SRTrain python3 scripts/srt_cli.py search \
  --departure "수서" --arrival "동대구" --date "20260227" --time "200000"
```
从搜索结果中获取目标火车的 `train_id`。

### 第二步：启动后台重试进程
```bash
LOG_FILE=<choose_any_path>.log
PID_FILE=<choose_any_path>.pid
cd <project_dir> && nohup uv run --with SRTrain python3 scripts/make_reservation.py \
  --train-id <id> --retry --timeout-minutes 1440 --wait-seconds 10 \
  --log-file "$LOG_FILE" > /dev/null 2>&1 &
echo $! > "$PID_FILE"
```

脚本在启动时会输出 `LOG_FILE: <path>` —— 请记录这个路径，以便知道日志文件的位置。
您也可以通过设置 `SRT_DATA_DIR` 来指定自动生成的日志和缓存文件的位置。

**`make_reservation.py` 的选项：**
| 选项 | 默认值 | 说明 |
|--------|---------|-------------|
| `--train-id` | （所有） | 搜索结果中的索引（用逗号分隔多个火车） |
| `--retry` | false | 启用持续重试模式 |
| `--timeout-minutes` | 60 | 总时长。设置为 1440 表示 24 小时 |
| `--wait-seconds` | 10 | 每次尝试之间的延迟时间 |
| `--log-file` | auto | 显式的日志文件路径（覆盖 `SRT_DATA_DIR` 的默认值） |

需要关注的日志标记：
- `=== 시도 #N` —— 尝试次数 |
- `SUCCESS` —— 预订成功（包含预订编号和座位信息） |
- `TIMEOUT` —— 未成功且超时

### 第三步：创建定期报告的 cron 作业
创建一个每隔 15 分钟执行的 cron 作业，该作业会：
1. 检查进程状态：
   ```bash
   PID=$(cat <pid_file> 2>/dev/null)
   kill -0 "$PID" 2>/dev/null && echo "RUNNING" || echo "NOT_RUNNING"
   ```
2. 读取日志尾部内容：`tail -50 <log_file>`
3. 从日志中解析尝试次数和最后一次尝试的时间
4. 向指定频道报告结果
5. 当日志中显示 `SUCCESS` 时，提取预订编号和座位信息，然后停止该 cron 作业
6. 当发生 `TIMEOUT` 或进程停止运行时，报告结果并停止该 cron 作业

### 第四步：创建终止作业
在任务结束时间创建一个 `at`-schedule 类型的 cron 作业，该作业会：
1. 杀死相关进程：`kill $(cat <pid_file>)`
2. 根据 ID 删除之前的报告 cron 作业
3. 读取最终日志并报告结果

---

## JSON 输出

**搜索结果项：**
```json
{
  "train_number": "369",
  "departure_time": "200000",
  "arrival_time": "213600",
  "departure_station": "수서",
  "arrival_station": "동대구",
  "seat_available": false,
  "general_seat": "매진",
  "special_seat": "매진",
  "train_id": "1"
}
```

**预订结果：**
```json
{
  "success": true,
  "data": {
    "reservation_id": "RES123456",
    "train_number": "369",
    "seat_number": "3A",
    "payment_required": true
  }
}
```

退出代码：`0` = 成功 · `1` = 可重试（没有座位） · `2` = 错误

---

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|-----------|
| `AuthenticationFailed` | 凭据错误 | 检查 `SRT_PHONE` 和 `SRT_PASSWORD` 是否正确 |
| `NoSeatsAvailable` | 座位已售罄 | 使用 `--retry` 选项或尝试其他火车 |
| `StationNotFound` | 车站名称无效 | 请使用上述韩文车站名称 |
| `NoTrainsFound` | 未找到火车 | 尝试其他日期/时间 |
| `RateLimitExceeded` | 尝试次数过多 | 等待几分钟后再试 |

---

## 自然语言处理

从韩文输入中提取的信息：
- 车站名称 → 使用韩文表示（如 수서、동대구 等）
- 日期 → 使用相对表达式（例如 “내일” 或 “다음주 금요일”）转换为 `YYYYMMDD` 格式
- 时间 → 使用 “20시 이후” 或 “오후 2시” 等表达式转换为 `HHMMSS` 格式
- 乘客人数 → 如果未指定，则默认为 1

**常见指令模式：**
- “검색해줘” → 执行 `search` 命令
- “예약해줘”（一次性预订） → 先执行 `search`，然后执行 `reserve` 命令
- “취소표 나오면 잡아줘 / 될 때까지 돌려줘” → 使用上述的持续监控流程
- “내 예약 확인해줘” → 执行 `list` 命令
- “취소해줘” → 先执行 `list`，然后执行 `cancel` 命令

## 支付说明
预订必须在预订后的 20 分钟内通过 SRT 应用程序或 <https://etk.srail.kr> 完成支付。