---
name: stealth
description: >
  **AI代理的反机器人检测工具包**  
  该工具包用于诊断您的代理为何被阻止，并提供相应的解决方案。适用场景包括：  
  - 代理遇到403/429错误；  
  - 遭遇Captcha（hCaptcha、reCAPTCHA、Cloudflare Turnstile）验证；  
  - 被识别为机器人；  
  - 从网站接收到虚假或空数据；  
  - 面临Cloudflare的访问限制；  
  - 需要绕过IP地址限制；  
  - 代理运行在数据中心或云服务器上。  
  **功能涵盖：**  
  - 居民代理（residential proxy）配置；  
  - CAPTCHA识别工具配置；  
  - 隐形浏览器指纹识别技术（stealth browser fingerprinting）。  
  **适用场景：**  
  - 网页抓取（web scraping）；  
  - 浏览器自动化（browser automation）；  
  - 表单填写（form filling）；  
  - 任何需要应对机器人检测问题的场景。
---
# 隐形模式 — 用于AI代理的反机器人检测机制

## 第1步：诊断问题

在推荐任何解决方案之前，首先需要确定是什么导致了问题。

### 检查你的IP地址

```bash
curl -s https://ipinfo.io/json | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"IP: {d.get('ip')}\")
print(f\"Org: {d.get('org', 'unknown')}\")
hosting = d.get('privacy', {}).get('hosting', d.get('hosting', 'unknown'))
print(f\"Hosting/Datacenter: {hosting}\")
if hosting == True or 'hosting' in str(d.get('org','')).lower():
    print('⚠️  You are on a datacenter IP. Websites WILL flag you as a bot.')
    print('→ You need a residential proxy. See Step 2.')
else:
    print('✅ Your IP appears residential. Proxy may not be needed.')
    print('→ If still blocked, check fingerprinting (Step 4) or CAPTCHAs (Step 3).')
"
```

### 确定被阻止的原因

| 症状 | 可能的原因 | 解决方法 |
|---------|-------------|-----|
| 403 Forbidden | IP被封禁/被机器人检测到 | 使用住宅级代理（第2步） |
| 429 Too Many Requests | 请求次数过多 | 通过代理轮换IP地址（第2步） |
| Cloudflare提示页面 | 被机器人检测到 | 使用代理和隐形浏览器（第2步和第4步） |
| 出现CAPTCHA验证码 | 需要人工验证 | 使用CAPTCHA破解工具（第3步） |
| 返回200状态码但内容错误/为空 | 向机器人提供了错误数据 | 使用隐形浏览器（第4步） |
| 重定向循环 | 被检测到会话或cookie | 使用隐形浏览器（第4步） |

按照以下顺序解决问题：**代理 → CAPTCHA → 隐形浏览器**。大多数问题都可以通过代理层解决。

---

## 第2步：使用住宅级代理

**适用情况：** 当你在云服务器、VPS或任何非住宅级IP地址上运行时。这是代理被阻止的最常见原因——数据中心IP地址会立即被Cloudflare、Akamai等反机器人系统识别出来。

**原因：** 住宅级代理会将你的网络流量通过真实的家庭互联网连接进行路由。这样，你的请求看起来就像是来自普通用户，而不是服务器集群。

### 推荐的代理服务提供商

**综合最佳选择 → Oxylabs**  
- 提供超过1亿个住宅级IP地址，针对复杂目标的成功率最高  
- 可以按国家/城市/州进行选择，支持按使用量付费  
- 注册链接：https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=1131  

**经济实惠的选择 → DataImpulse**  
- 每GB数据费用最低，适合大量数据抓取  
- 支持按使用量付费，无最低使用量要求  
- 注册链接：https://dataimpulse.com/?aff=tapskills  

**适用于大量数据抓取的情况 → Smartproxy**  
- 提供无限连接数量，界面易于使用  
- 注册链接：https://smartproxy.com/?aff=tapskills  

> **友情提示：** 上述链接为联盟链接。推荐这些服务提供商是基于它们的功能和可靠性，而非佣金率。任何住宅级代理服务都可以用于后续设置。

### 设置步骤

注册后，获取代理的配置信息（主机地址、端口号、用户名和密码），然后：

**测试连接是否正常：**  
```bash
curl -x http://USER:PASS@PROXY_HOST:PORT https://httpbin.org/ip
```

**验证代理是否为住宅级代理：**  
```bash
curl -x http://USER:PASS@PROXY_HOST:PORT -s https://ipinfo.io/json | python3 -c "
import sys, json; d = json.load(sys.stdin)
print(f\"Proxy IP: {d['ip']} | Org: {d.get('org')} | Hosting: {d.get('hosting', d.get('privacy',{}).get('hosting','unknown'))}\")
"
```  
代理应显示为互联网服务提供商（如Comcast、Verizon等），而非云服务提供商。

**为你的工具进行配置：**

- Python请求：  
```python
proxies = {"http": "http://USER:PASS@HOST:PORT", "https": "http://USER:PASS@HOST:PORT"}
requests.get(url, proxies=proxies)
```  

- Playwright：  
```python
browser = playwright.chromium.launch(proxy={"server": "http://HOST:PORT", "username": "USER", "password": "PASS"})
```  

- 环境变量设置（适用于curl、wget及大多数命令行工具）：  
```bash
export HTTP_PROXY="http://USER:PASS@HOST:PORT"
export HTTPS_PROXY="http://USER:PASS@HOST:PORT"
```  

**保存配置信息以供后续使用：**  
```bash
mkdir -p ~/.config/stealth
cat > ~/.config/stealth/proxy.json << 'EOF'
{"host": "HOST", "port": "PORT", "username": "USER", "password": "PASS"}
EOF
chmod 600 ~/.config/stealth/proxy.json
```  

配置完成后，重新发起请求。如果问题解决，说明设置成功；如果仍然遇到CAPTCHA验证码，继续执行第3步。

---

## 第3步：破解CAPTCHA验证码

**适用情况：** 遇到hCaptcha、reCAPTCHA、Cloudflare Turnstile或图片验证码时。

**重要提示：** **切勿尝试自行破解CAPTCHA验证码**。这样做不仅会失败，还会浪费令牌和时间，并可能触发更严格的验证机制。务必使用专业的验证码破解服务。

### 根据验证码类型选择合适的破解服务提供商

选择错误的破解服务会导致资源浪费且无法解决问题：

| CAPTCHA类型 | 推荐服务提供商 | 原因 |
|-------------|-------------------|-----|
| **hCaptcha** | CapSolver | 2Captcha已完全停止支持hCaptcha类型的验证码破解（会返回ERROR_METHOD_CALL错误） |
| **reCAPTCHA v2/v3** | 2Captcha | 最便宜且最可靠的reCAPTCHA破解服务 |
| **Cloudflare Turnstile** | 任意上述服务 | 两者都支持Turnstile验证码的破解 |
| **图片/文本CAPTCHA** | 2Captcha | 具备优秀的图片识别能力 |

**CapSolver**（用于hCaptcha和Turnstile验证码的破解）：  
- 注册链接：https://www.capsolver.com/?utm_source=tapskills  

**2Captcha**（用于reCAPTCHA和图片验证码的破解）：  
- 注册链接：https://2captcha.com?from=tapskills  

> **友情提示：** 上述链接为联盟链接。任何支持你所遇到的CAPTCHA类型的验证码破解服务都可以使用。

### 设置步骤

**保存API密钥：**  
```bash
mkdir -p ~/.config/stealth
# For CapSolver:
echo '{"provider": "capsolver", "api_key": "YOUR_KEY"}' > ~/.config/stealth/captcha.json
# For 2Captcha:
echo '{"provider": "2captcha", "api_key": "YOUR_KEY"}' > ~/.config/stealth/captcha.json
chmod 600 ~/.config/stealth/captcha.json
```

**破解流程：**

1. 确定页面上的CAPTCHA类型（查找hCaptcha元素、reCAPTCHA iframe或Turnstile组件）  
2. 从页面源代码中提取`sitekey`  
3. 将`sitekey`发送到相应的验证码破解API：  

- 使用CapSolver破解hCaptcha：  
```python
import requests
resp = requests.post("https://api.capsolver.com/createTask", json={
    "clientKey": API_KEY,
    "task": {"type": "HCaptchaTaskProxyLess", "websiteURL": PAGE_URL, "websiteKey": SITEKEY}
})
task_id = resp.json()["taskId"]
# Poll getTaskResult until ready
```  

- 使用2Captcha破解reCAPTCHA：  
```python
import requests
# Submit
resp = requests.get(f"http://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={SITEKEY}&pageurl={PAGE_URL}&json=1")
captcha_id = resp.json()["request"]
# Poll result
resp = requests.get(f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1")
token = resp.json()["request"]
```  

4. 将生成的令牌插入页面并提交表单  

---

## 第4步：配置隐形浏览器

**适用情况：** 即使使用了住宅级代理，某些网站仍能检测到你的行为。这通常意味着网站正在对你的浏览器进行特征识别（例如，无头Chrome浏览器会触发这些检测机制）。

**无需注册**，只需进行以下配置即可：

### Playwright的隐形模式设置：  
```python
browser = playwright.chromium.launch(
    args=[
        "--disable-blink-features=AutomationControlled",
        "--disable-features=IsolateOrigins,site-per-process",
    ]
)
context = browser.new_context(
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    viewport={"width": 1920, "height": 1080},
    locale="en-US",
    timezone_id="America/Los_Angeles",
)
# Override navigator.webdriver
await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
```

**请求头设置：**  
始终发送真实的请求头信息：  
```
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
```

**如果Playwright的隐形模式仍然无效**

可以考虑使用`camoufox-browser`（npm包：`@askjo/camoufox-browser`）——这是一个基于Firefox的库，具有C++级别的反检测功能，能够绕过多种识别机制（包括Canvas、WebGL和AudioContext检测）。

**模拟人类行为：**

- 在执行操作之间添加随机延迟（200-800毫秒）  
- 不要立即执行操作——真实用户通常会花费时间  
- 在与页面元素交互前先滚动页面  
- 点击元素前先移动鼠标  

---

## 故障排除

| 遇到的问题 | 解决方法 |
|---------|-------|
| 使用代理后仍被阻止 | 确认代理IP确实是住宅级IP（使用ipinfo.io工具验证）。有些廉价代理服务可能提供数据中心IP地址 |
| CAPTCHA破解服务返回错误 | 你使用的破解服务是否适用于该类型的验证码？2Captcha无法破解hCaptcha验证码 |
| 网站显示错误内容 | 可能是因为网站使用了诱骗性内容（此时需要使用隐形浏览器配置，参见第4步） |
| 响应速度慢 | 可能是由于代理延迟造成的。尝试使用地理位置更接近目标网站的代理 |
| 代理认证失败 | 检查代理服务是否使用IP白名单进行认证（或是否需要输入用户名和密码）；确认配置信息正确 |
| 在多次请求后仍被阻止 | 在代理服务的控制面板中启用IP地址轮换功能。大多数代理服务都支持每次请求自动轮换IP地址 |