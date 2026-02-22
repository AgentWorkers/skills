# 品牌名称生成器

为任何行业生成20个富有创意的品牌名称建议，并提供这些名称是否适合注册.com域名的提示。

## 输入参数
- `industry`（必填）：行业或细分市场（例如：“fintech”（金融科技），“organic skincare”（有机护肤品），“pet food”（宠物食品）
- `attributes`（可选）：用逗号分隔的品牌属性（例如：“modern”（现代的）、“playful”（有趣的）、“premium”（高端的）
- `style`（可选）：命名风格偏好（可选值：invented（原创词）、compound（复合词）、metaphor（隐喻）、acronym（缩写词）、mixed（混合风格）（默认值：mixed）

## 输出结果
生成20个品牌名称建议，每个建议包含以下信息：
- **名称**：品牌名称
- **风格**：名称的生成方式（原创词、复合词、隐喻等）
- **氛围**：名称所传达的感觉或联想
- **域名可用性提示**：根据词汇的常见程度，判断该名称是否适合注册.com域名（🟢 可能可用，🟡 可能不行，🔴 已被注册）

## 使用方法
```
You are a brand naming expert. Generate 20 creative, memorable brand names.

Industry: {{industry}}
Attributes: {{attributes | default: "modern, memorable, unique"}}
Style preference: {{style | default: "mixed"}}

For each name provide:
1. The brand name
2. Naming style (invented, compound, metaphor, acronym, real-word twist)
3. The vibe/feeling it evokes
4. Domain availability hint using these heuristics:
   - 🟢 Likely available: invented/unusual words, 8+ chars, uncommon combos
   - 🟡 Maybe available: semi-common compounds, moderate length
   - 🔴 Likely taken: real English words, short/common terms, popular prefixes

Format as a numbered list. Be creative — mix unexpected syllables, blend words, use metaphors from nature/science/mythology. Avoid generic names. Each name should be:
- Easy to pronounce
- Easy to spell
- Memorable after one hearing
- Appropriate for the industry

After the list, add 3 "wildcard" bonus names that are extra creative/risky.
```

## 示例
**输入参数：** industry="fintech", attributes="trustworthy", modern, bold
**示例输出名称：** Vaultary, Ledgr, FinPinnacle, Aurumix, Capacita...

**输入参数：** industry="pet food", attributes="playful", natural, premium
**示例输出名称：** Pawtura, Snoutwell, FetchFeast, Grubble, Wildnose...