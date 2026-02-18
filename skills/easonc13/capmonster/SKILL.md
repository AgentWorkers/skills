---
name: capmonster
description: 使用 CapMonster Cloud API 解决验证码（reCAPTCHA v2/v3、hCaptcha、Cloudflare Turnstile、图片验证码）问题。当浏览器自动化遇到验证码挑战时，可以使用该 API 进行处理。
---
# CapMonster Cloud CAPTCHA 解决器

通过 CapMonster Cloud API 在浏览器自动化过程中程序化地解决 CAPTCHA 验证问题。

## API 信息

- **基础 URL**: `https://api.capmonster.cloud`
- **API 密钥**: `${CAPMONSTER_API_KEY}`
- **文档**: https://docs.capmonster.cloud/
- **Python 客户端**: `tools/capmonster-cloud/capmonster_api.py`

## 价格（每 1000 次解决）

| 类型 | 价格 | 平均时间 |
|------|-------|----------|
| reCAPTCHA v2 | $0.60 | 10-30 秒 |
| reCAPTCHA v3 | $0.90 | 5-15 秒 |
| hCaptcha | $1.50 | 10-30 秒 |
| Cloudflare Turnstile | $1.20 | 5-15 秒 |
| 图片 CAPTCHA | $0.04 | 2-5 秒 |

## 快速参考

### 查看余额

```bash
curl -s -X POST https://api.capmonster.cloud/getBalance \
  -H "Content-Type: application/json" \
  -d '{"clientKey": "${CAPMONSTER_API_KEY}"}' | jq .balance
```

### 使用 Python 客户端

```python
import sys
sys.path.insert(0, '/Users/eason/clawd/tools/capmonster-cloud')
from capmonster_api import CapMonsterClient

client = CapMonsterClient("${CAPMONSTER_API_KEY}")

# Check balance
print(f"Balance: ${client.get_balance()}")

# Solve reCAPTCHA v2
token = client.solve_recaptcha_v2(
    website_url="https://example.com/page-with-captcha",
    website_key="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"
)
```

---

## 完整工作流程：浏览器自动化 + CAPTCHA 解决

### 第 1 步：检测页面上的 CAPTCHA

获取浏览器截图并检查 CAPTCHA 的存在：

```javascript
// Via browser action=act evaluate
browser action=act profile=chrome request={
  "kind": "evaluate",
  "fn": "(() => {
    const indicators = {
      recaptchaV2: !!document.querySelector('.g-recaptcha, [data-sitekey], iframe[src*=\"recaptcha\"]'),
      recaptchaV3: !!document.querySelector('script[src*=\"recaptcha/api.js?render=\"]'),
      hcaptcha: !!document.querySelector('.h-captcha, [data-hcaptcha-sitekey], iframe[src*=\"hcaptcha\"]'),
      turnstile: !!document.querySelector('.cf-turnstile, [data-sitekey], iframe[src*=\"turnstile\"]')
    };
    return JSON.stringify(indicators);
  })()"
}
```

### 第 2 步：提取站点密钥

**reCAPTCHA v2:**
```javascript
// Option A: From data-sitekey attribute
document.querySelector('[data-sitekey]')?.dataset.sitekey

// Option B: From iframe src
document.querySelector('iframe[src*="recaptcha"]')?.src.match(/k=([^&]+)/)?.[1]

// Option C: From grecaptcha object
window.___grecaptcha_cfg?.clients?.[0]?.Y?.Y?.sitekey
```

**reCAPTCHA v3:**
```javascript
// From script src
document.querySelector('script[src*="recaptcha/api.js?render="]')?.src.match(/render=([^&]+)/)?.[1]

// Or from grecaptcha config
window.___grecaptcha_cfg?.clients?.[0]?.Y?.Y?.sitekey
```

**hCaptcha:**
```javascript
document.querySelector('[data-hcaptcha-sitekey], .h-captcha[data-sitekey]')?.dataset.sitekey ||
document.querySelector('[data-hcaptcha-sitekey]')?.getAttribute('data-hcaptcha-sitekey')
```

**Cloudflare Turnstile:**
```javascript
document.querySelector('.cf-turnstile[data-sitekey], [data-turnstile-sitekey]')?.dataset.sitekey
```

### 第 3 步：提交到 CapMonster API

**使用 curl（shell）:**

```bash
# Create task
TASK_ID=$(curl -s -X POST https://api.capmonster.cloud/createTask \
  -H "Content-Type: application/json" \
  -d '{
    "clientKey": "${CAPMONSTER_API_KEY}",
    "task": {
      "type": "RecaptchaV2TaskProxyless",
      "websiteURL": "https://scholar.google.com/",
      "websiteKey": "SITEKEY_HERE"
    }
  }' | jq -r .taskId)

echo "Task ID: $TASK_ID"
```

**使用 Python:**

```python
import sys
sys.path.insert(0, '/Users/eason/clawd/tools/capmonster-cloud')
from capmonster_api import CapMonsterClient

client = CapMonsterClient("${CAPMONSTER_API_KEY}")

# For reCAPTCHA v2
token = client.solve_recaptcha_v2(
    website_url="https://scholar.google.com/",
    website_key="EXTRACTED_SITEKEY"
)

# For reCAPTCHA v3
token = client.solve_recaptcha_v3(
    website_url="https://example.com/",
    website_key="EXTRACTED_SITEKEY",
    min_score=0.7,
    page_action="submit"  # Check page source for action name
)

# For hCaptcha
token = client.solve_hcaptcha(
    website_url="https://example.com/",
    website_key="EXTRACTED_SITEKEY"
)

# For Turnstile
token = client.solve_turnstile(
    website_url="https://example.com/",
    website_key="EXTRACTED_SITEKEY"
)
```

### 第 4 步：轮询解决方案

**使用 curl:**

```bash
# Poll until ready (max 120 seconds)
for i in {1..60}; do
  RESULT=$(curl -s -X POST https://api.capmonster.cloud/getTaskResult \
    -H "Content-Type: application/json" \
    -d "{\"clientKey\": \"${CAPMONSTER_API_KEY}\", \"taskId\": $TASK_ID}")
  
  STATUS=$(echo "$RESULT" | jq -r .status)
  
  if [ "$STATUS" = "ready" ]; then
    TOKEN=$(echo "$RESULT" | jq -r '.solution.gRecaptchaResponse // .solution.token')
    echo "Token: $TOKEN"
    break
  fi
  
  echo "Status: $STATUS, waiting..."
  sleep 2
done
```

Python 客户端通过 `solve_and_wait()` 自动处理轮询。

### 第 5 步：将解决方案注入页面

**reCAPTCHA v2/v3:**

```javascript
// Via browser evaluate
browser action=act profile=chrome request={
  "kind": "evaluate",
  "fn": "(() => {
    const token = 'CAPMONSTER_TOKEN_HERE';
    
    // Method 1: Set textarea value (most common)
    const textarea = document.querySelector('#g-recaptcha-response, [name=\"g-recaptcha-response\"]');
    if (textarea) {
      textarea.value = token;
      textarea.style.display = 'block';  // Some sites hide it
    }
    
    // Method 2: Also set any iframe response
    document.querySelectorAll('iframe[src*=\"recaptcha\"]').forEach(iframe => {
      try {
        const doc = iframe.contentDocument || iframe.contentWindow.document;
        const ta = doc.querySelector('#g-recaptcha-response');
        if (ta) ta.value = token;
      } catch(e) {}
    });
    
    // Method 3: Trigger callback if exists
    if (typeof ___grecaptcha_cfg !== 'undefined') {
      const clients = ___grecaptcha_cfg.clients;
      for (let cid in clients) {
        const client = clients[cid];
        // Find callback
        const callback = client?.Y?.Y?.callback || client?.Y?.callback;
        if (typeof callback === 'function') {
          callback(token);
        }
      }
    }
    
    return 'Token injected';
  })()"
}
```

**hCaptcha:**

```javascript
browser action=act profile=chrome request={
  "kind": "evaluate",
  "fn": "(() => {
    const token = 'CAPMONSTER_TOKEN_HERE';
    
    // Set response textarea
    const textarea = document.querySelector('[name=\"h-captcha-response\"], [name=\"g-recaptcha-response\"]');
    if (textarea) textarea.value = token;
    
    // Trigger callback
    if (typeof hcaptcha !== 'undefined') {
      // Find widget ID
      const widget = document.querySelector('.h-captcha');
      const widgetId = widget?.dataset.hcaptchaWidgetId || 0;
      // Some sites have custom callbacks
    }
    
    return 'hCaptcha token injected';
  })()"
}
```

**Cloudflare Turnstile:**

```javascript
browser action=act profile=chrome request={
  "kind": "evaluate",
  "fn": "(() => {
    const token = 'CAPMONSTER_TOKEN_HERE';
    
    // Set the hidden input
    const input = document.querySelector('[name=\"cf-turnstile-response\"]');
    if (input) input.value = token;
    
    // Also set any callback data attribute
    const container = document.querySelector('.cf-turnstile');
    if (container && container.dataset.callback) {
      const callbackName = container.dataset.callback;
      if (typeof window[callbackName] === 'function') {
        window[callbackName](token);
      }
    }
    
    return 'Turnstile token injected';
  })()"
}
```

### 第 6 步：提交表单

注入令牌后，提交表单：

```javascript
// Click submit button
browser action=act profile=chrome request={"kind":"click","ref":"submit button ref"}

// Or trigger form submission
browser action=act profile=chrome request={
  "kind": "evaluate",
  "fn": "document.querySelector('form').submit()"
}
```

---

## Google Scholar 特殊情况

Google Scholar 使用的是 **不可见的 reCAPTCHA v2**，会在检测到可疑活动时触发。

### 检测

```javascript
// Check if blocked
const isBlocked = document.body.textContent.includes('unusual traffic') ||
                  document.body.textContent.includes('我們的系統') ||
                  !!document.querySelector('iframe[src*="recaptcha"]');
```

### 提取站点密钥

```javascript
// Scholar's recaptcha iframe
const iframe = document.querySelector('iframe[src*="recaptcha"]');
const sitekey = iframe?.src.match(/k=([^&]+)/)?.[1];
// Usually: 6LfwuyUTAAAAAOAmoS0fdqijC2PbbdH4kjq62Y1b
```

### 解决并提交

```python
import sys
sys.path.insert(0, '/Users/eason/clawd/tools/capmonster-cloud')
from capmonster_api import CapMonsterClient

client = CapMonsterClient("${CAPMONSTER_API_KEY}")

# Scholar's known sitekey (may change)
token = client.solve_recaptcha_v2(
    website_url="https://scholar.google.com/scholar?q=test",
    website_key="6LfwuyUTAAAAAOAmoS0fdqijC2PbbdH4kjq62Y1b"
)

print(f"Token: {token[:50]}...")
```

然后通过浏览器自动化将解决方案注入页面。

---

## 图片 CAPTCHA

对于传统的图片 CAPTCHA（文本识别）：

```python
import base64
import sys
sys.path.insert(0, '/Users/eason/clawd/tools/capmonster-cloud')
from capmonster_api import CapMonsterClient

client = CapMonsterClient("${CAPMONSTER_API_KEY}")

# From file
text = client.solve_image_captcha(image_path="/tmp/captcha.png")

# From base64
with open("/tmp/captcha.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
text = client.solve_image_captcha(image_base64=b64)

print(f"CAPTCHA text: {text}")
```

---

## 一站式 Shell 脚本

保存为 `solve-recaptcha.sh`：

```bash
#!/bin/bash
# Usage: ./solve-recaptcha.sh <website_url> <sitekey>

API_KEY="${CAPMONSTER_API_KEY}"
WEBSITE_URL="$1"
SITEKEY="$2"

# Create task
echo "Creating task..."
RESPONSE=$(curl -s -X POST https://api.capmonster.cloud/createTask \
  -H "Content-Type: application/json" \
  -d "{
    \"clientKey\": \"$API_KEY\",
    \"task\": {
      \"type\": \"RecaptchaV2TaskProxyless\",
      \"websiteURL\": \"$WEBSITE_URL\",
      \"websiteKey\": \"$SITEKEY\"
    }
  }")

TASK_ID=$(echo "$RESPONSE" | jq -r .taskId)
ERROR_ID=$(echo "$RESPONSE" | jq -r .errorId)

if [ "$ERROR_ID" != "0" ]; then
  echo "Error: $(echo "$RESPONSE" | jq -r .errorDescription)"
  exit 1
fi

echo "Task ID: $TASK_ID"

# Poll for result
echo "Waiting for solution..."
for i in {1..60}; do
  RESULT=$(curl -s -X POST https://api.capmonster.cloud/getTaskResult \
    -H "Content-Type: application/json" \
    -d "{\"clientKey\": \"$API_KEY\", \"taskId\": $TASK_ID}")
  
  STATUS=$(echo "$RESULT" | jq -r .status)
  
  if [ "$STATUS" = "ready" ]; then
    TOKEN=$(echo "$RESULT" | jq -r '.solution.gRecaptchaResponse')
    COST=$(echo "$RESULT" | jq -r '.cost')
    echo "✅ Solved! Cost: \$$COST"
    echo ""
    echo "TOKEN:"
    echo "$TOKEN"
    exit 0
  fi
  
  printf "."
  sleep 2
done

echo ""
echo "❌ Timeout after 120 seconds"
exit 1
```

---

## 故障排除

### 令牌无效/过期

- 令牌大约在 2 分钟后过期
- 收到令牌后立即注入并提交
- 确保 `websiteURL` 与实际页面 URL 匹配

### ERROR_CAPTCHA_UNSOLVABLE

- 重试 2-3 次
- 检查站点密钥是否正确
- 页面可能有额外的保护机制

### ERROR_RECAPTCHA_TIMEOUT

- CapMonster 与目标网站之间的网络问题
- 重新尝试，或使用代理版本（RecaptchaV2Task）

### 令牌已注入但表单提交失败

- 网站可能在服务器端通过 IP 地址验证令牌
- 尝试使用带有您 IP 地址的代理版本
- 有些网站需要触发回调

### 查找回调 URL

```javascript
// Check grecaptcha config for callback
JSON.stringify(___grecaptcha_cfg, (k, v) => typeof v === 'function' ? '[Function]' : v, 2)

// Or check data-callback attribute
document.querySelector('[data-callback]')?.dataset.callback
```

---

## 最佳实践

1. **及时提取站点密钥** - 不要硬编码，站点密钥可能会更新
2. **使用正确的 URL** - 必须与显示 CAPTCHA 的页面匹配
3. **快速注入令牌** - 令牌大约在 120 秒后过期
4. **检查是否使用 v3 版本** - 有些网站使用不可见的 reCAPTCHA，需要设置 `pageAction`
5. **监控余额** - 设置低余额提醒
6. **失败时重试** - CapMonster 有时会失败

## 成本估算

| 使用场景 | 每天 CAPTCHAs 数量 | 每月成本 |
|----------|--------------|--------------|
| 轻量级（研究） | 10 | ~$0.18 |
| 中等程度（数据抓取） | 100 | ~$1.80 |
| 重度（自动化） | 1000 | ~$18.00 |

当前余额约为 $10，足够解决约 16,000 个 reCAPTCHA v2 验证问题。