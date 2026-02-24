---
name: brand-manager
description: 在社交媒体运营系统中管理品牌。可以添加新的品牌、编辑现有品牌的资料，或者将品牌归档。每个品牌都有自己的资料页面、内容发布指南、资源文件目录以及对应的频道主题。该功能适用于品牌所有者需要添加新品牌、修改品牌设置或停用某个品牌的情况。
---
# 品牌管理器

## 概述

负责管理品牌的整个生命周期，包括创建、配置和归档。每个品牌都是一个独立的单元，拥有自己的资料、内容指南、行业知识文件以及沟通渠道。

## 命令

### `add` — 添加新品牌

为新的品牌创建所有必要的文件和目录。

**需要从所有者处收集的信息：**
1. **品牌ID** — 一个简短的小写标识符（例如：“skincare”、“cafe”、“fitness”）
2. **显示名称** — 便于人类阅读的名称（例如：“Glow Skincare”）
3. **本地名称** — 本地语言中的名称（可选）
4. **业务领域** — 品牌的主要业务范围（例如：“高端护肤品”）
5. **目标市场** — 地理或人群定位（例如：“泰国市场”、“美国千禧一代”）
6. **内容语言** — 该品牌内容使用的语言（默认为实例的默认语言）
7. **频道主题ID** — 如果使用主题模式，该品牌的Telegram频道主题ID

**创建的文件：**
- `shared/brands/{id}/profile.md` — 根据收集的信息自动生成的模板文件
- `shared/brands/{id}/content-guidelines.md` — 内容指南模板文件
- `shared/domain/{id}-industry.md` — 行业相关信息模板文件
- `assets/{id}/generated/` — 用于存放AI生成内容的目录
- `assets/{id}/received/` — 用于存放所有者提供的文件的目录
- 在 `shared/brand-registry.md` 中添加品牌条目
- 在 `shared/operations/posting-schedule.md` 中添加相关内容
- 在 `shared/operations/channel-map.md` 中添加品牌对应的沟通渠道信息

**示例：**
```
Owner: Add a new brand
Bot: Let's set up a new brand.

1. Brand ID (short, lowercase)?
> bakery

2. Display name?
> Sweet Sunrise Bakery

3. Local name (optional)?
> 甜蜜日出

4. What does this brand do?
> Artisan bakery and pastry shop

5. Target market?
> Taiwan, young professionals

6. Content language?
> 繁體中文

7. Telegram topic thread ID?
> 8

Brand "bakery" created! Next: fill in shared/brands/bakery/profile.md with brand details.
```

### `edit` — 修改品牌设置

修改现有品牌的注册信息（显示名称、内容语言、沟通渠道等）。

**使用方法：`edit {brand_id}`

### `archive` — 归档品牌

将品牌移至 `brand-registry.md` 的归档部分。文件不会被删除，仅会标记为已归档状态以供参考。

**使用方法：`archive {brand_id}`

### `list` — 列出所有品牌

显示 `brand-registry.md` 中的所有活跃品牌和已归档品牌。

## 文件之间的关系**
```
brand-manager add "mybrand"
  │
  ├── shared/brands/mybrand/profile.md        (from _template)
  ├── shared/brands/mybrand/content-guidelines.md  (from _template)
  ├── shared/domain/mybrand-industry.md        (from _template)
  ├── assets/mybrand/generated/               (empty dir)
  ├── assets/mybrand/received/                (empty dir)
  ├── shared/brand-registry.md                (new row added)
  ├── shared/operations/posting-schedule.md   (new section added)
  └── shared/operations/channel-map.md        (new row added)
```