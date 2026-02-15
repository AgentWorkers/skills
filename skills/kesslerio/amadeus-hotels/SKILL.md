---
name: amadeus-hotels
description: 通过 Amadeus API 搜索酒店价格和可用性。可以根据城市、坐标或酒店设施来查找度假酒店。比较价格、查看评分、获取优惠详情，并设置价格监控提醒。适用于用户请求“查找酒店”、“在[城市]搜索酒店”、“查询酒店价格”、“度假住宿”、“酒店优惠”或“跟踪酒店价格”的场景。
homepage: https://github.com/kesslerio/amadeus-hotels-clawhub-skill
metadata:
  {
    "openclaw":
      {
        "emoji": "🏨",
        "requires":
          {
            "bins": ["python3"],
            "env": ["AMADEUS_API_KEY", "AMADEUS_API_SECRET"],
          },
        "primaryEnv": "AMADEUS_API_KEY",
        "install":
          [
            {
              "id": "pip-requests",
              "kind": "pip",
              "packages": ["requests"],
              "label": "Install requests (pip)",
            },
          ],
      },
  }
---

# Amadeus Hotels Skill 🏨

通过 Amadeus 自助服务 API 搜索酒店价格、可用性和评分。非常适合度假规划和寻找优惠。

## 设置

1. **获取 API 凭据**：访问 https://developers.amadeus.com/self-service
   - 创建账户 → 我的应用程序 → 创建新应用程序
   - 复制 API 密钥（API Key）和 API 秘密（API Secret）

2. **设置环境变量：**
```bash
export AMADEUS_API_KEY="your-api-key"
export AMADEUS_API_SECRET="your-api-secret"
export AMADEUS_ENV="test"  # or "production" for real bookings
```

3. **安装依赖项：**
```bash
pip install requests
```

**免费 tier：** 测试环境每月约 2,000 次请求；生产环境按使用量计费。

## 快速参考

| 任务 | 脚本 | 示例 |
|------|--------|---------|
| 按城市搜索 | `scripts/search.py` | `--city PAR --checkin 2026-03-15 --checkout 2026-03-20` |
| 获取优惠信息 | `scripts/offers.py` | `--hotels HTPAR123,HTPAR456 --adults 2` |
| 查看优惠详情 | `scripts/details.py` | `--offer-id ABC123` |
| 跟踪价格变化 | `scripts/track.py` | `--add --hotel HTPAR123 --target 150` |
| 检查跟踪结果 | `scripts/track.py` | `--check` |

## 功能

### 1. 酒店搜索

可以通过城市代码（IATA）或坐标查找酒店：

```bash
# By city
python3 <skill>/scripts/search.py --city PAR --checkin 2026-03-15 --checkout 2026-03-20

# By coordinates (near a landmark)
python3 <skill>/scripts/search.py --lat 48.8584 --lon 2.2945 --radius 5 --checkin 2026-03-15 --checkout 2026-03-20

# With filters
python3 <skill>/scripts/search.py --city NYC --amenities WIFI,POOL,SPA --ratings 4,5
```

**常见城市代码：** PAR（巴黎），NYC（纽约），TYO（东京），BCN（巴塞罗那），LON（伦敦），LAX（洛杉矶），SFO（旧金山）

### 2. 获取价格和可用性信息

搜索到酒店 ID 后，可以获取以下信息：

```bash
python3 <skill>/scripts/offers.py \
  --hotels HTPAR001,HTPAR002 \
  --checkin 2026-03-15 \
  --checkout 2026-03-20 \
  --adults 2 \
  --rooms 1
```

返回内容：房间类型、价格、取消政策、餐饮类型。

### 3. 优惠详情

在预订前查看特定优惠的详细信息：

```bash
python3 <skill>/scripts/details.py --offer-id <offer-id-from-search>
```

返回内容：详细的房间信息、完整的取消政策、付款条款、酒店联系方式。

### 4. 酒店评分和用户反馈

获取汇总的用户评价：

```bash
python3 <skill>/scripts/details.py --hotel-id HTPAR001 --ratings
```

返回内容：整体评分（0-100 分），各类别评分（员工服务、地理位置、WiFi、清洁度等）。

### 5. 价格跟踪

跟踪酒店价格变化，并在价格下降时收到警报：

```bash
# Add hotel to tracking
python3 <skill>/scripts/track.py --add \
  --hotel HTPAR001 \
  --checkin 2026-03-15 \
  --checkout 2026-03-20 \
  --adults 2 \
  --target 150  # Alert if price drops below $150/night

# Check all tracked hotels (run via cron)
python3 <skill>/scripts/track.py --check

# List tracked hotels
python3 <skill>/scripts/track.py --list

# Remove from tracking
python3 <skill>/scripts/track.py --remove --hotel HTPAR001
```

### 用于价格警报的 Cron 任务设置

将脚本添加到 OpenClaw 的 Cron 任务中以实现自动价格监控：

```yaml
# Check hotel prices twice daily
- schedule: "0 9,18 * * *"
  task: "Run hotel price tracker and alert on drops"
  command: "python3 <skill>/scripts/track.py --check"
```

当价格低于设定目标时，脚本会输出警报信息。请在 Cron 任务中配置通知渠道。

## 输出格式

脚本默认输出 JSON 格式。使用 `--format human` 选项可获取更易读的格式：

```bash
python3 <skill>/scripts/search.py --city PAR --format human
```

**人类可读格式示例：**
```
🏨 Hotel & Spa Paris Marais ★★★★
   📍 15 Rue du Temple, Paris
   💰 €189/night (was €220)
   ✨ WIFI, SPA, RESTAURANT
   📊 Rating: 87/100 (Staff: 92, Location: 95)
```

## 酒店设施代码

`--amenities` 参数的常用筛选条件：

| 代码 | 含义 |
|------|---------|
| WIFI | 免费 WiFi |
| POOL | 游泳池 |
| SPA | 水疗中心 |
| GYM | 健身中心 |
| RESTAURANT | 酒店内餐厅 |
| PARKING | 提供停车位 |
| PETS_ALLOWED | 允许携带宠物 |
| AIR_CONDITIONING | 空调 |
| KITCHEN | 厨房/小厨房 |

完整列表请参见 `references/amenities.md`。

## ⚠️ 重要提示：价格说明

**Amadeus API 返回的价格并非零售价格。** 这些价格是经过协商后的净价或批发价，并非您在 Booking.com、Expedia 或酒店网站上看到的公开价格。

**关键区别：**
- **净价与零售价：** API 返回的是“净价”（未加利润的原始价格）。
- **B2B 定价：** 专为旅行社和开发者设计，允许他们自行加价。
- **协商价格：** 可能包含企业或联盟专享的价格，消费者无法直接获取。
- **税费分项：** 价格通常会分别显示基础价格和税费。

**请将这些价格用于比较和趋势分析，** 而非作为最终的零售报价。实际预订价格可能与这些价格有所不同。

## 限制与注意事项

- **测试环境：** 数据有限且可能被缓存，不支持实时更新。适合开发用途。
- **生产环境：** 显示实际价格，但需要在 Amadeus 控制面板中切换到“生产模式”。
- **无法直接预订：** API 只返回优惠详情，实际预订需要处理支付流程（符合 PCI 标准）。
- **请求速率限制：** 测试环境为 10 TPS（每秒请求数），生产环境为 40 TPS。脚本中包含了防超负荷机制。
- **数据更新频率：** 价格会频繁变动，预订前请务必重新查询。
- **非零售价格：** 请注意上述的价格说明。

## 错误处理

| 错误代码 | 含义 | 处理方式 |
|-------|---------|--------|
| 401 | 认证失败 | 检查 API 密钥/秘密 |
| 429 | 请求次数过多 | 等待片刻后重试（系统自动处理） |
| 400 | 请求错误 | 检查参数（日期、代码等） |
| 无结果 | 酒店不可用 | 尝试其他日期或扩大搜索范围 |

## 参考资料

- `references/amenities.md` — 完整的酒店设施代码列表
- https://developers.amadeus.com/self-service/apis-docs — 官方 API 文档