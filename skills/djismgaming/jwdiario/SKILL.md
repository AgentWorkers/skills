---
name: jwdiario
description: 从耶和华见证人官方网站（wol.jw.org/es/）上搜索并获取当天的每日文本。使用 `web_fetch` 工具来访问内容并提取当天的文本。当需要获取耶和华见证人的每日文本或每日圣经内容时，请使用此方法。
---

# Habilidad JWDiario

此功能可用于获取耶和华见证人官方网站（[wol.jw.org/es/](https://wol.jw.org/es/wol/h/r4/lp-s)）上的每日文本。

## 主要功能

该功能执行以下操作：
1. 访问耶和华见证人的在线圣经图书馆页面。
2. 提取当前日期的每日文本。
3. 以圣经背景和相关解释的形式展示该文本。

## 常见使用场景

当用户请求以下内容时，该功能可发挥作用：
- “耶和华见证人的每日文本”
- “今天的耶和华见证人文本”
- “查找今天的阅读内容”
- “显示耶和华见证人的每日读物”

## 工作流程

1. 使用 `web_fetch` 函数访问页面 `https://wol.jw.org/es/wol/h/r4/lp-s/AAAA/MM/DD`（例如：2026年2月8日的页面为 `https://wol.jw.org/es/wol/h/r4/lp-s/2026/2/8`）。
2. 提取当天的内容。
3. 在输出中包含当天的标题、相应的圣经引文以及解释内容，同时保持原文的格式不变。
4. 在消息末尾添加链接 `https://wol.jw.org/es/`。

## 重要提示

- **请始终使用西班牙语版本的网站**（wol.jw.org/es/）。
- **不要对文本进行翻译**，内容应直接从西班牙语的官方网站中提取。

## 使用示例

```
Usuario: "Texto diario de JW por favor"
Habilidad: Obtiene el texto del día desde `https://wol.jw.org/es/wol/h/r4/lp-s` y lo presenta con el versículo bíblico y explicación correspondiente. No cambia el texto original. Añade el enlace al final.
```

## 所需资源

- 用于访问网站的 `web_fetch` 函数。
- 处理文本的能力，以便正确格式化输出结果。