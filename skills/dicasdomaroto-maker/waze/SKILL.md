---
name: waze
version: 1.0.0
author: eliolonghi
tags: [navigation, waze, maps, briefing, location, rota, endereco]
description: 生成 Waze 导航链接，适用于任何目的地：地址、商家名称、日程中的约会地点。每当用户提到某个目的地、请求路线、想要了解如何到达某个地方，或者日程中的活动有明确地点时，都应使用这些链接。在这种情况下，无需用户额外请求，即可自动将链接添加到信息简报中。如果目的地信息不明确（例如企业名称、商家类型或“最近的加油站”），请先搜索用户所在城市最近的相应地点，再生成链接——切勿使用其他城市的地址。
---
# Waze 导航技能

## 功能介绍

该技能可生成 Waze 导航链接。用户只需在手机上点击这些链接，即可直接打开 Waze 应用并查看已规划的路线。该功能通过 Waze 的公开深度链接实现，无需使用 API 密钥。

## 链接格式

```
https://waze.com/ul?q=ENDEREÇO_CODIFICADO&navigate=yes
```

链接地址需要经过 URL 编码。如果条件允许，请使用 Python 进行编码：

```python
from urllib.parse import quote
address = "Av. Jerônimo Monteiro, 1000, Vitória, ES, Brasil"
link = f"https://waze.com/ul?q={quote(address)}&navigate=yes"
print(link)
```

---

## 使用流程

### 第一步：获取用户位置

首先，确定用户所在的城市。可以在以下文件中查找相关信息：
- 当前工作区的 `USER.md` 文件
- `SOUL.md` 文件或任何工作区的个人资料文件

如果找不到相关信息，请询问用户。城市信息对于查找附近的商家或地点至关重要，切勿使用默认位置或搜索结果中的第一个城市名称。

### 第二步：确定目的地类型

- **具体目的地**（完整地址、邮政编码、坐标）：
  → 直接进入第 4 步。

- **模糊目的地**（商家名称、类别、"最近的位置"）：
  → 先进入第 3 步。

### 第三步：查找最近的位置

使用 Tavily 工具搜索：“**地点名称** + **城市名称** + **州名”。
从搜索结果中提取**完整地址**（街道名、门牌号、社区名称、城市名称、州名）。
如果有多个结果，请选择距离用户最近的地址，或让用户自行选择。

> 例如：用户位于巴西埃斯帕尼奥拉州的维多利亚市，请求搜索“Leroy Merlin”。
  → 搜索：“Leroy Merlin Vitória ES”。
  → 找到地址：“Av. Fernando Ferrari, 2600, Goiabeiras, Vitória, ES”。
  → 进入第 4 步。

### 第四步：生成链接

对地址进行 URL 编码并构建链接。务必在地址中包含州名和国家名称，以避免混淆（同名城市可能存在于不同国家）。

### 第五步：展示链接

链接应使用 markdown 格式 `[链接文本](链接地址)` 来显示，切勿直接显示原始 URL。这样在 Telegram 中链接会以可点击的文本形式呈现，更加美观易用。

**在日常对话中：**
```
📍 Leroy Merlin — Av. Fernando Ferrari, 2600, Goiabeiras, Vitória, ES
🗺️ [Abrir no Waze](https://waze.com/ul?q=Av.+Fernando+Ferrari%2C+2600%2C+Vit%C3%B3ria%2C+ES%2C+Brasil&navigate=yes)
```

**在晨会中**（当活动有具体地点时）：
```
📅 *AGENDA DE HOJE*
09:00 — Reunião com Fornecedor
📍 Leroy Merlin — Av. Fernando Ferrari, 2600, Vitória, ES
🗺️ [Abrir no Waze](https://waze.com/ul?q=Av.+Fernando+Ferrari%2C+2600%2C+Vit%C3%B3ria%2C+ES%2C+Brasil&navigate=yes)
```

在 Telegram 中，链接会显示为蓝色的可点击文本“在 Waze 中打开”，且不会显示完整的 URL。

---

## 与晨会系统的集成

在生成晨会内容时，如果活动信息中填写了地点信息，系统会自动在活动下方生成 Waze 链接，无需用户另行请求。这对于在出门前查看晨会内容的人来说非常方便。

如果活动地点是商家名称（而非完整地址），请先使用第 3 步获取实际地址后再生成链接。

---

## 注意事项

- 该链接适用于所有安装了 Waze 的设备。如果设备上没有 Waze 应用，系统会通过浏览器打开 Waze。
- 请务必在地址中包含州名和国家名称，以避免混淆。
- 注意区分巴西埃斯帕尼奥拉州的维多利亚市（Vitória, ES）与澳大利亚或加拿大的维多利亚市（Victoria）。
- 如果用户仅请求“最近的加油站”等模糊信息而未提供具体路线信息，请使用其个人资料中的城市名称作为搜索起点。