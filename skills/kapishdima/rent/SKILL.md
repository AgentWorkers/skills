# 租赁敖德萨（Renting Apartments in Odessa）

## 搜索长期租赁的2居室公寓

### 触发条件（Trigger Conditions）：
- 输入关键词 `/rent`
- 输入搜索指令，如 “查找公寓”、“敖德萨的出租公寓” 等

### 过滤条件（Filter Options）：
- 房间数量：2间
- 租金价格：不超过15,000乌克兰格里夫纳/月
- 不包括苏沃罗夫斯基区（Suvorovsky）和佩列西普斯基区（Peresypsky）在内的所有区域
- 允许养宠物
- 新建公寓
- 楼层：不限
- 居住面积：至少40平方米
- 供暖方式：不限
- 带家具

### 数据来源（Data Sources）：
- OLX：https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/?currency=UAH
- DOM.RIA：https://dom.ria.com/uk/search/?category=1&realty_type=2&operation=3&state_id=12&price_cur=1&wo_dupl=1&sort=inspected_sort&firstIteraction=false&limit=20&market=3&excludeSold=1&type=map&without_entity_group=1&city_ids=12&ch=246_244#map_state=30.72139_46.48608_0.0_10.0
- Flatfy：https://flatfy.ua/%D0%B0%D1%80%D0%B5%D0%BD%D0%B4%D0%B0-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80-%D0%BE%D0%B4%D0%B5%D1%81%D1%81%D0%B0
- Rieltor：https://rieltor.ua/ru/odessa/flats-rent/#10.5/0/0
- Lun：https://lun.ua/rent/odesa/flats/ru?srsltid=AfmBOopj60sLsMOT7sdNo_rAx-Cwj4dAttnTGCIg4ms30rFTkdykFNjx
- Atlanta：https://www.atlanta.ua/odessa/filters/arenda/kvartiry
- REM：https://rem.ua/arenda-kvartir-odessa

### 操作步骤（Steps）：
1. 执行 `agent-browser --help` 命令，了解如何使用 `agent-browser` 从这些网站收集数据。
2. 使用 `agent-browser` 访问每个数据来源，根据筛选条件选择合适的公寓。
3. 浏览前两个页面，收集公寓的相关信息。
4. 使用以下模板回复用户，列出找到的公寓信息：

```plaintext
以下是找到的公寓：
1. [公寓名称](链接) - 租金价格（乌克兰格里夫纳/月），所在区域，楼层，面积（平方米）
2. [公寓名称](链接) - 租金价格（乌克兰格里夫纳/月），所在区域，楼层，面积（平方米）
...
```

### 其他说明（Additional Notes）：
- 如果某个数据来源没有找到符合条件的公寓，请在回复中说明。
- 如果所有数据来源都没有找到公寓，请告知用户这一情况。
```