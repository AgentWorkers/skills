---
name: naver-shopping
description: 在Naver Shopping上搜索产品。当用户想要查找产品价格、链接或在韩国市场内比较商品时，可以使用此功能。
---

# Naver Shopping 搜索

使用此技能通过 Naver Search API 在 Naver Shopping 上搜索产品。

## 使用方法

运行搜索脚本并输入查询参数：

```bash
/Users/dryoo/.openclaw/workspace/skills/naver-shopping/scripts/search_shopping.py "상품명"
```

### 选项

- `--display <数字>`：显示的结果数量（默认值：5，最大值：100）
- `--sort <sim|date|asc|dsc>`：排序方式（sim：相似度；date：日期；asc：价格升序；dsc：价格降序）

### 示例

```bash
/Users/dryoo/.openclaw/workspace/skills/naver-shopping/scripts/search_shopping.py "아이폰 16" --display 3 --sort asc
```

## 环境变量

需要在 `.env` 文件中配置以下变量：
- `NAVER_CLIENT_ID`
- `NAVER_CLIENT_Secret`