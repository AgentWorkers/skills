---
name: trmnl
description: 使用 TRMNL CSS 框架为 TRMNL 电子墨水显示设备生成内容，并通过 trmnl CLI 进行发送。当用户希望在他们的 TRMNL 设备上显示信息、向电子墨水显示屏发送消息、创建仪表板内容、显示通知或更新终端显示时，可以使用此功能。该框架支持丰富的布局方式（如 flexbox、grid、表格、进度条以及排版工具）。
---

# TRMNL内容生成器

用于为TRMNL电子墨水显示设备生成HTML内容。

## 先决条件

**将`trmnl` CLI安装到最新版本：**
```bash
npm install -g trmnl-cli@latest
```

**配置Webhook插件（一次性设置）：**
```bash
# Add a plugin
trmnl plugin add home "https://trmnl.com/api/custom_plugins/{uuid}"

# Verify it's configured
trmnl plugin
```

## 快速启动工作流程

1. **安装/更新CLI：** 运行 `npm install -g trmnl-cli@latest`
2. **检查插件：** 运行 `trmnl plugin` — 如果没有插件，提示用户添加一个
3. 确认设备类型（默认：TRMNL OG，2位屏幕，800x480像素）
4. 根据内容需求阅读相关参考文档
5. 使用TRMNL框架类生成HTML
6. 将生成的HTML写入临时文件并发送：
   ```bash
   trmnl send --file /tmp/trmnl-content.html
   # Or to a specific plugin:
   trmnl send --file /tmp/trmnl-content.html --plugin office
   ```
7. **仅进行最基本的确认** — 不要将内容回显到聊天界面

## 发送内容

**建议从文件发送：**
```bash
# Write HTML content to file first
cat > /tmp/trmnl-content.html << 'EOF'
<div class="layout layout--col gap--space-between">
  <div class="item">
    <span class="value value--xlarge value--tnums">Hello TRMNL!</span>
  </div>
</div>
<div class="title_bar">
  <span class="title">My Plugin</span>
</div>
EOF

# Send to display
trmnl send --file /tmp/trmnl-content.html
```

**发送前进行验证：**
```bash
trmnl validate --file /tmp/trmnl-content.html
```

**查看发送历史记录：**
```bash
trmnl history
trmnl history --today
trmnl history --failed
```

## Webhook限制

| 等级 | 承载量大小 | 调用限制 |
|------|--------------|------------|
| 免费 | **2 KB**（2,048字节） | 每小时12次请求 |
| TRMNL+ | **5 KB**（5,120字节） | 每小时30次请求 |

全局设置等级以进行准确验证：
```bash
trmnl tier plus  # or "free"
```

## 参考文档

根据需要阅读以下文件：

| 文件 | 阅读时机 |
|------|--------------|
| `references/patterns.md` | **从这里开始** — 常见插件模式 |
| `references/framework-overview.md` | 设备规格、电子墨水显示器的限制 |
| `references/css-utilities.md` | 颜色、排版、尺寸、间距设置 |
| `references/layout-systems.md` | Flexbox布局、网格系统、溢出处理机制 |
| `references/components.md` | 标题栏、分隔符、列表项、表格 |
| `references/webhook-api.md` | 承载格式、故障排除 |
| `assets/anti-patterns.md` | 需避免的常见错误 |

## 标准插件结构

**所有插件都遵循以下结构：**

```html
<div class="layout layout--col gap--space-between">
  <!-- Content sections separated by dividers -->
</div>
<div class="title_bar">
  <img class="image" src="icon.svg">
  <span class="title">Plugin Name</span>
  <span class="instance">Context</span>
</div>
```

- `layout` + `layout--col` = 垂直Flex容器
- `gap--space-between` = 将各个部分均匀分布到页面边缘
- `title_bar` = 始终位于页面底部，位于`layout`之外
- `divider` = 用于分隔主要部分
- **重要提示：** 每个页面只能使用一个`.layout`元素

## 快速参考

### 网格系统（10列）

```html
<div class="grid">
  <div class="col--span-3">30%</div>
  <div class="col--span-7">70%</div>
</div>
```

### 列表项组件

```html
<div class="item">
  <div class="content">
    <span class="value value--xlarge value--tnums">$159,022</span>
    <span class="label">Total Sales</span>
  </div>
</div>
```

### 数字显示格式

**数字显示时必须使用`value--tnums`类：**

| 类别 | 用途 |
|-------|-------|
| `value--xxxlarge` | 重要KPI指标 |
| `value--xxlarge` | 较大的价格数值 |
| `value--xlarge` | 较小的数值 |
| `value--tnums` | **数字显示时必须使用** |

### 灰度类

建议使用渐变类而非内联颜色：
- `bg--black`, `bg--gray-60`, `bg--gray-30`, `bg--gray-10`, `bg--white`
- `text--black`, `text--gray-50`

### 数据属性

| 属性 | 用途 |
|-----------|---------|
| `data-fit-value="true"` | 自动调整文本大小以适应显示区域 |
| `data-clamp="N"` | 限制文本显示为最多N行 |
| `data-overflow="true"` | 启用文本溢出处理功能 |

## 最佳实践

1. 使用`layout` + `title_bar`结构
2. 数字显示时始终使用`value--tnums`类
3. 对于关键指标，使用`data-fit-value`属性
4. 使用`bg--gray-*`类来实现渐变背景效果
5. 确保发送的负载量不超过等级限制
6. **仅进行最基本的确认** — 仅显示“内容已发送至TRMNL”

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| `trmnl: command not found` | 运行 `npm install -g trmnl-cli@latest` |
| 未配置插件 | 运行 `trmnl plugin add <插件名称> <插件URL>` |
| Webhook调用失败 | 使用 `trmnl config` 命令验证插件URL |
| 承载量过大 | 使用 `trmnl validate --file` 检查文件大小 |
| 数字显示错位 | 为数字添加`value--tnums`类 |
| 查看发送历史记录 | 使用 `trmnl history --failed` 命令查看失败日志 |