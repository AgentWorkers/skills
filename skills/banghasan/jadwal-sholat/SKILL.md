---
name: jadwal-sholat
description: 从 MuslimApi.myquran.com（该数据来源于印度尼西亚宗教事务部（Kemenag Bimas Islam））的 API 中获取印度尼西亚各城市/县的礼拜时间（晨礼、晌礼、正午礼、晡礼、昏礼、宵礼）。当用户需要查询特定日期或地点的当天的礼拜时间，或者需要查找某个城市/县的 ID 时，可以使用该功能。
---

# 礼拜时间表 (api.myquran.com)

API 基址：`https://api.myquran.com/v3`

推荐使用的脚本辅助工具：`scripts/myquran_sholat.py`

## 快速入门

1. **查找地点（县/市）：**
   ```bash
python3 scripts/myquran_sholat.py cari "tangerang"
```

2. **根据关键词查询当天的礼拜时间表（亚洲/雅加达地区）：**
   ```bash
python3 scripts/myquran_sholat.py hari-ini "kota tangerang"
```

3. **查询特定日期的礼拜时间表（格式：YYYY-MM-DD）：**
   ```bash
python3 scripts/myquran_sholat.py tanggal "kota tangerang" 2026-02-03
```

4. **查询某个月的礼拜时间表（格式：YYYY-MM）：**
   ```bash
python3 scripts/myquran_sholat.py bulan "kota tangerang" 2026-02
```

## 关于地点选择的说明：

- 查找端点会返回多个候选地点。脚本会：
  - 尽量与 `lokasi` 列进行精确匹配（不区分大小写）；
  - 如果无法匹配，则使用第一个搜索结果。

- 如果搜索结果不够准确，请使用更具体的关键词（例如：`KOTA TANGERANG` 而不是 `TANGERANG`），或者获取地点的 `id`，然后使用该 `id` 来调用相关功能。

## 直接通过 curl 调用 API（无需脚本）

1. **查找县/市：**
   ```bash
curl -s "https://api.myquran.com/v3/sholat/kabkota/cari/tangerang"
```

2. **获取当天的礼拜时间表：**
   ```bash
curl -s "https://api.myquran.com/v3/sholat/jadwal/<ID>/today?tz=Asia/Jakarta"
```

3. **获取指定时间段的礼拜时间表（按月/按日）：**
   ```bash
# bulanan
curl -s "https://api.myquran.com/v3/sholat/jadwal/<ID>/2026-02?tz=Asia/Jakarta"

# harian
curl -s "https://api.myquran.com/v3/sholat/jadwal/<ID>/2026-02-03?tz=Asia/Jakarta"
```