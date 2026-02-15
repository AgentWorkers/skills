# 法国服务 — 日常使用的法国服务

这些脚本用于访问法国的各种服务：SNCF火车、La Poste包裹追踪、天气信息以及Île-de-France地区的公共交通信息。

## 可用的脚本

所有脚本均位于 `skills/french-services/scripts/` 目录下。这些脚本仅使用 Python 的标准库（无需额外依赖）。

### 🚄 SNCF — 火车 (`sncf.py`)

通过 Navitia API 查找列车路线和即将发车的列车信息。

```bash
# Rechercher un trajet
python3 scripts/sncf.py search Paris Lyon
python3 scripts/sncf.py search "Gare de Lyon" Marseille --date 2025-01-15 --time 08:00

# Prochains départs depuis une gare
python3 scripts/sncf.py departures Paris

# Perturbations sur une ligne
python3 scripts/sncf.py disruptions
```

**所需 API 密钥：** `SNCF_API_KEY`（Navitia 的 API 密钥 — 可在 https://navitia.io 免费获取）

### 📦 La Poste — 包裹追踪 (`laposte.py`)

```bash
# Suivre un colis
python3 scripts/laposte.py track 6A12345678901

# Suivre plusieurs colis
python3 scripts/laposte.py track 6A12345678901 8R98765432109
```

**所需 API 密钥：** `LAPOSTE_API_KEY`（La Poste 的 API 密钥 — 可在 https://developer.laposte.fr 免费获取）

### 🌤️ 天气 (`meteo.py`

通过 Open-Meteo 提供当前天气和天气预报（使用 Météo France 模型）。**无需 API 密钥。**

```bash
# Météo actuelle + prévisions 3 jours
python3 scripts/meteo.py Paris
python3 scripts/meteo.py Lyon --days 7
python3 scripts/meteo.py --lat 43.6 --lon 1.44    # Toulouse par coordonnées

# Format JSON
python3 scripts/meteo.py Paris --json
```

### 🚇 RATP/IDFM — Île-de-France 公共交通 (`ratp.py`

通过 PRIM API 查看 Île-de-France 地区的交通状况和即将到来的列车/地铁班次。

```bash
# État du trafic global
python3 scripts/ratp.py traffic

# État d'une ligne spécifique
python3 scripts/ratp.py traffic --line "Métro 13"
python3 scripts/ratp.py traffic --line "RER A"

# Prochains passages à un arrêt
python3 scripts/ratp.py next "Châtelet"
```

**所需 API 密钥：** `IDFM_API_KEY`（RATP/IDFM 的 API 密钥 — 可在 https://prim.iledefrance-mobilites.fr 免费获取）

## 常用选项

| 选项          | 描述                                      |
|--------------|---------------------------------------|
| `--json`       | 以 JSON 格式输出结果，而非文本                   |
| `--help`      | 显示脚本的使用说明                         |

## 环境变量

| 变量          | 服务          | 获取方式                                      |
|------------------|------------------|-----------------------------------------|
| `SNCF_API_KEY`    | SNCF          | https://navitia.io （免费，每月 5000 次请求限制）         |
| `LAPOSTE_API_KEY` | La Poste       | https://developer.laposte.fr                 |
| `IDFM_API_KEY`    | RATP/IDFM       | https://prim.iledefrance-mobilites.fr        |

详细配置指南请参阅 `references/api-setup.md`。

## 如何使用相应的脚本

| 用户需求          | 对应脚本                        |
|------------------|-------------------------------------------|
| “前往里昂的下一班火车？”    | `sncf.py`                        |
| “明天早上的巴黎-马赛列车时刻表？” | `sncf.py`                        |
| “我的包裹 6A123... 的状态如何？” | `laposte.py`                      |
| “明天天气如何？”       | `meteo.py`                        |
| “13 号地铁还在运行吗？”     | `ratp.py`                        |
| “夏特莱站下一班地铁是什么时候？” | `ratp.py`                        |

## 注意事项

- 天气信息无需任何配置即可使用（Open-Meteo 是免费且无需 API 密钥）
- 其他服务需要根据 `references/api-setup.md` 中的说明配置 API 密钥
- 脚本会自动处理 API 密钥缺失的情况，并给出相应的提示信息
- 默认输出为中文；如需机器集成，请使用 `--json` 选项