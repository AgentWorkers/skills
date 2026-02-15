---
name: 2captcha
description: 使用 2Captcha 服务通过 CLI（命令行界面）来解决验证码问题。该服务可用于在网页自动化、账户创建或表单提交过程中绕过验证码。
homepage: https://github.com/adinvadim/2captcha-cli
---

# 2Captcha 技能

使用 2Captcha 人工验证服务以编程方式解决验证码问题。

## 安装

```bash
# One-line install
curl -fsSL https://raw.githubusercontent.com/adinvadim/2captcha-cli/main/solve-captcha \
  -o /usr/local/bin/solve-captcha && chmod +x /usr/local/bin/solve-captcha

# Verify
solve-captcha --version
```

## 配置

```bash
# Save your 2Captcha API key
mkdir -p ~/.config/2captcha
echo "YOUR_API_KEY" > ~/.config/2captcha/api-key

# Or use environment variable
export TWOCAPTCHA_API_KEY="your-key"
```

请在 https://2captcha.com/enterpage 获取您的 API 密钥。

## 快速参考

### 先检查余额
```bash
./solve-captcha balance
```

### 图片验证码
```bash
# From file
./solve-captcha image /path/to/captcha.png

# From URL  
./solve-captcha image "https://site.com/captcha.jpg"

# With options
./solve-captcha image captcha.png --numeric 1 --math
./solve-captcha image captcha.png --comment "Enter red letters only"
```

### reCAPTCHA v2
```bash
./solve-captcha recaptcha2 --sitekey "6Le-wvk..." --url "https://example.com"
```

### reCAPTCHA v3
```bash
./solve-captcha recaptcha3 --sitekey "KEY" --url "URL" --action "submit" --min-score 0.7
```

### hCaptcha
```bash
./solve-captcha hcaptcha --sitekey "KEY" --url "URL"
```

### Cloudflare Turnstile
```bash
./solve-captcha turnstile --sitekey "0x4AAA..." --url "URL"
```

### FunCaptcha (Arkose)
```bash
./solve-captcha funcaptcha --public-key "KEY" --url "URL"
```

### GeeTest
```bash
# v3
./solve-captcha geetest --gt "GT" --challenge "CHALLENGE" --url "URL"

# v4
./solve-captcha geetest4 --captcha-id "ID" --url "URL"
```

### 文本验证码
```bash
./solve-captcha text "What color is the sky?" --lang en
```

## 获取验证码参数

### reCAPTCHA 的站点密钥（sitekey）
- 在 HTML 中查找 `data-sitekey` 属性
- 在 reCAPTCHA iframe 的 URL 中查找 `k=` 参数
- 向 `google.com/recaptcha/api2/anchor` 发送网络请求

### hCaptcha 的站点密钥（sitekey）
- 在 hCaptcha 的 div 元素中查找 `data-sitekey`
- 向 `hcaptcha.com` 发送网络请求

### Turnstile 的站点密钥（sitekey）
- 在 Turnstile 小部件中查找 `data-sitekey`
- 查找带有 `cf-turnstile` 类的元素

## 浏览器自动化的工作流程

1. **检测验证码** - 检查页面是否存在验证码元素
2. **提取参数** - 从页面源代码中获取站点密钥（sitekey）和验证码挑战内容（challenge）
3. **通过 CLI 解决验证码** - 使用 `solve-captcha` 命令并传入参数
4. **注入令牌** - 设置 `g-recaptcha-response` 或回调函数

### 示例：注入 reCAPTCHA 令牌
```javascript
// After getting token from solve-captcha
document.getElementById('g-recaptcha-response').value = token;
// Or call callback if defined
___grecaptcha_cfg.clients[0].callback(token);
```

## 成本说明

- 在进行大量自动化操作前，请先检查账户余额：
  - 图片验证码：每次解决大约 0.001 美元
  - reCAPTCHA/hCaptcha/Turnstile：每次解决大约 0.003 美元

## 错误处理

常见错误：
- `ERROR_ZERO_BALANCE` - 账户余额不足，请充值
- `ERROR_NO_slot_AVAILABLE` - 几秒后重试
- `ERROR_CAPTCHA_UNSOLVABLE` - 图片质量差或验证码无法识别
- `ERROR_wrong_CAPTCHA_ID` - 任务 ID 无效

## 注意事项

- 解决验证码所需时间因类型而异，通常在 10 到 60 秒之间
- reCAPTCHA v3 可能需要多次尝试才能成功解决
- 一些网站会检测到自动化行为，请谨慎使用
- 令牌有有效期，请在 2 到 5 分钟内使用完毕