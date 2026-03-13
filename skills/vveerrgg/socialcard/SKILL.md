# socialcard

通过一个简洁易用的构建器 API，您可以生成精美的社交卡片图片（适用于 Open Graph、Twitter 和 GitHub）。

## 使用场景

当您需要以编程方式生成社交预览图片、Open Graph 卡片、Twitter 卡片或 GitHub 社交图片时，可以使用此功能。

## 安装

```bash
pip install socialcard
```

## 快速示例

```python
from socialcard import SocialCard

SocialCard("og").title("My Project").subtitle("A cool tool").render("card.png")
```

## 预设样式

- `og` (1200×630) — Open Graph 图片
- `twitter` (800×418) — Twitter 图片
- `github` (1280×640) — GitHub 社交图片
- `square` (1080×1080) — Instagram 图片

## 主题样式

- `dark` — 海蓝色背景，蓝色点缀
- `light` — 白色背景，蓝色点缀
- `midnight` — 接近黑色的背景，紫色点缀

## 构建器方法

- `.badge(text)` — 小型标签
- `.title(text)` — 主标题
- `.subtitle(text)` — 副标题
- `.cards(list)` — 图标标签
- `.footer(text)` — 底部文字
- `.accent(hex)` — 更改背景颜色
- `.grid()` — 网格布局
- `.glow()` — 径向发光效果
- `.render(path)` — 保存到文件
- `.render_bytes()` — 获取 PNG 图片的字节数据