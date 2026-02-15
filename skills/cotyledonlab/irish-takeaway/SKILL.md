---
name: irish-takeaway
description: 在爱尔兰查找附近的外卖餐厅，并通过 Deliveroo/Just Eat 网站浏览菜单。该系统利用 Google Places API 来发现附近的餐厅位置，同时使用浏览器自动化技术来抓取餐厅的菜单信息。
metadata: {"clawdbot":{"emoji":"🍕","requires":{"bins":["goplaces"],"env":["GOOGLE_PLACES_API_KEY"]}}}
---

# 爱尔兰外卖查找工具 🍕🇮🇪

通过 Deliveroo 或 Just Eat 查找附近的外卖店并获取它们的菜单。

## 先决条件

- 已安装 `goplaces` 命令行工具（使用 `brew install steipete/tap/goplaces` 安装）
- 环境变量 `GOOGLE_PLACES_API_KEY` 已设置
- 拥有可用的浏览器

## 工作流程

### 第一步：查找附近的外卖店

使用 `goplaces` 在指定位置附近搜索餐厅：

```bash
# Search by coordinates (negative longitude needs = syntax)
goplaces search "takeaway" --lat=53.7179 --lng=-6.3561 --radius-m=3000 --limit=10

# Search by cuisine
goplaces search "chinese takeaway" --lat=53.7179 --lng=-6.3561 --radius-m=2000

# Filter by rating
goplaces search "pizza" --lat=53.7179 --lng=-6.3561 --min-rating=4 --open-now
```

爱尔兰的常见地理位置坐标：
- **德罗赫达 (Drogheda)**：53.7179, -6.3561
- **都柏林市 (Dublin City)**：53.3498, -6.2603
- **科克 (Cork)**：51.8985, -8.4756
- **戈尔韦 (Galway)**：53.2707, -9.0568

### 第二步：获取 Deliveroo 的菜单（浏览器自动化）

1. 打开浏览器并访问 Deliveroo 网站：
```
browser action=start target=host
browser action=navigate targetUrl="https://deliveroo.ie/" target=host
```

2. 如果出现提示，接受 cookies（找到“Accept all”按钮）

3. 在地址搜索框中输入位置：
```
browser action=act request={"kind": "type", "ref": "<textbox-ref>", "text": "Drogheda, Co. Louth"}
```

4. 从自动完成的下拉菜单中选择位置

5. 从列表中找到并点击目标餐厅

6. 截取餐厅的页面截图以提取菜单项：
   - 菜单类别标题（h2 标签）
   - 包含名称、描述和价格的菜单项按钮
   - 菜品描述中的过敏原信息

### 第三步：解析菜单数据

菜单项通常以以下结构显示：
- **名称**：位于段落元素中
- **描述**：位于文本内容中
- **价格**：通常采用 “€X.XX” 的格式
- **过敏原**：在描述之后列出（如麸质、牛奶等）

### 示例对话流程

用户：“德罗赫达附近有哪些外卖店？”
→ 使用 `goplaces` 搜索，显示评分最高的 5-10 个结果

用户：“显示 Mizzoni’s 的菜单”
→ 通过浏览器访问 Deliveroo 网站 → 搜索 → 点击餐厅 → 截取页面截图 → 解析菜单

用户：“他们有哪些披萨？”
→ 按类别筛选菜单项，显示披萨选项及其价格

### Just Eat 的替代方案

如果目标餐厅不在 Deliveroo 的服务范围内，可以尝试使用 Just Eat：
```
browser action=navigate targetUrl="https://www.just-eat.ie/" target=host
```

操作流程类似：输入邮政编码/地址 → 浏览餐厅 → 点击查看菜单

### 提示

- 请务必先关闭 cookie 提示框
- 点击之前请等待自动完成建议的显示
- 有些餐厅的订单追踪功能有限，但仍然可以查看菜单
- 价格信息中包含过敏原信息
- 使用 `snapshot` 选项并设置 `compact=true` 以获得更简洁的输出结果

### 需要关注的菜单类别

- 特价套餐与优惠
- 披萨（按大小分类：小号/中号/大号/超大号）
- 开胃菜
- 意大利面
- 汉堡
- 配菜
- 甜点
- 饮料

## 未来改进计划

- [ ] 集成 Twilio 语音服务以实现电话订餐
- [ ] 实现跨平台的价格比较功能
- [ ] 记录用户喜爱的餐厅
- [ ] 提供订单历史记录功能