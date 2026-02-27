---
name: amazon
slug: amazon-ordering
version: 1.0.0
description: 使用浏览器自动化技术在亚马逊上购买商品并退货。该技术可用于完成购买、重新下单、查看订单历史以及处理退货等操作。
compatibility: Requires agent-browser CLI with Chrome DevTools Protocol (CDP). Chrome must be running with --remote-debugging-port. Optional VNC for headless setups.
---
# 亚马逊购物流程

## 先决条件

- 已安装 `agent-browser` 命令行工具。
- Chrome 浏览器已开启，并设置 `--remote-debugging-port=9222`（详见 [如果浏览器未运行，请启动浏览器](#starting-the-browser-if-not-running)）。
- 已登录亚马逊账户；如果未登录，请从密码管理器中找回密码。
- 如果在无头模式下运行（Linux/VNC），请转发 VNC 端口以便进行可视化验证：`ssh -L 6080:localhost:6080 <host>` → 访问 `http://localhost:6080/vnc.html`。

## 设置

请设置以下环境变量或使用默认值：

```bash
# Your default shipping address (verify on checkout)
export AMAZON_SHIPPING_ADDRESS="Your shipping address"
# Your preferred payment method description (verify on checkout)
export AMAZON_PAYMENT_METHOD="Your preferred card"
# Your preferred return drop-off location
export AMAZON_RETURN_DROPOFF="Whole Foods"
```

下单前，请务必核对收货地址和支付方式是否正确。

## 退货流程

### 默认回复内容（除非用户另有说明）

- **退货原因**：**“改变主意”** → “我的需求发生了变化”
- **包装是否被打开**：是
- **商品是否仍在原包装中**：是
- **是否使用过商品**：是
- **商品是否有使用痕迹**：无
- **电池是否有泄漏或过热现象**：无
- **所有配件是否齐全**：是
- **退款方式**：退款至原支付方式（不提供替换品或礼品卡）
- **退货地点**：可以选择 `AMAZON_RETURN_DROPOFF` 或 Whole Foods。

### 退货步骤
1. 进入订单页面 → 找到所需商品 → 选择“退货或更换商品”
2. 选择“改变主意” → “我的需求发生了变化” → 点击“继续”
3. 使用上述默认答案回答相关问题
4. 继续操作，跳过“获取产品支持”的提示
5. 选择“退款至原支付方式”
6. 选择退货地点
7. 确认退货操作
8. 退货流程完成 → 退货二维码将通过电子邮件发送给您。

### 通信方式
- **无需逐一说明每个步骤**，只需默默地完成整个退货流程。
- 退货确认完成后，仅向用户发送一条简短的消息，内容包括：
  - 商品名称
  - 退款金额
  - 退货地点及截止日期
- 如果遇到问题或需要进一步说明，请随时联系客服。

## 订购规则

### 重新订购之前已购买的商品
- 直接进入订单历史记录，找到所需商品
- 点击“再次购买”
- 核对收货地址和支付方式
- **无需截图**即可直接下单。

### 新商品（从未购买过）
- 搜索或导航至商品页面
- **发送商品页面的截图**（滚动屏幕以确保价格和商品图片均可见，忽略导航栏）
- 在添加商品到购物车前等待用户确认
- 核对收货地址和支付方式
- 确认后下单。

## 工作流程

### 连接浏览器
```bash
agent-browser connect 9222
```

**请始终打开新标签页**——不同的会话会共享同一个 Chrome 浏览器实例。每次使用 `open` 命令时，请加上 `--new-tab` 选项。

### 查看订单历史记录
```bash
agent-browser open "https://www.amazon.com/gp/your-account/order-history"
agent-browser snapshot -i
# Find search box, fill with item name, click search
```

### 重新订购流程
```bash
# From order history search results
agent-browser click @[buy-it-again-ref]
# Wait for checkout page
agent-browser snapshot
# Verify correct address and payment method are selected
agent-browser click @[place-order-ref]
```

### 截图技巧
- 在截图前请先滚动屏幕，确保价格和商品图片均显示在屏幕上。
- 将截图保存到临时文件夹中。
- 通过消息工具发送截图，并附上说明文字。

## 启动浏览器（如果浏览器未运行）

**macOS**（打开可见的 Chrome 窗口）：
```bash
open -na "Google Chrome" --args --user-data-dir=$HOME/.config/chrome-agent --no-first-run --remote-debugging-port=9222 https://www.amazon.com
```

**Linux**（无头模式，使用 Xvfb/VNC）：
```bash
DISPLAY=:99 google-chrome --user-data-dir=$HOME/.config/chrome-agent --no-first-run --remote-debugging-port=9222 https://www.amazon.com &
```

**Linux**（桌面模式/GUI 会话）：
```bash
google-chrome --user-data-dir=$HOME/.config/chrome-agent --no-first-run --remote-debugging-port=9222 https://www.amazon.com &
```

## 注意事项

- 浏览器配置文件保存在 `$HOME/.config/chrome-agent` 中。
- 在无头 Linux 环境中，VNC 显示通常使用端口 `5999`（noVNC 使用端口 `6080`）。
- 订单确认信息会发送到您的亚马逊账户邮箱。
- 如果遇到验证码或需要二次验证（2FA），请告知用户在 Chrome 窗口中完成相关操作（适用于 macOS 或 Linux 桌面环境）。