---
name: church-account
description: 自动化处理 churchofjesuschrist.org 和 LCR（Leader & Clerk Resources）网站上的任务。适用于登录 LDS 教会账户、查询教区/分会成员名单、管理教会职务分配、查看圣殿推荐状态、访问会员目录等操作。涵盖了 OAuth 登录流程、会话管理以及相关的教会服务 URL。
---
# 教堂账户（LDS/LCR）

自动化登录及在 churchofjesuschrist.org 上执行相关任务。

## 登录

### OAuth 流程
该教堂通过 `id.churchofjesuschrist.org` 使用 OAuth 进行身份验证。所有受保护的页面在用户尝试访问时都会引导用户进行登录：
1. 输入用户名 → 点击“下一步”
2. 输入密码 → 点击“验证”
3. 系统会使用会话 cookie 将用户重定向回目标页面

通常不需要多因素认证（MFA）或验证码（CAPTCHA）。Playwright 和 playwright-stealth 工具可以很好地处理这些登录流程。

### 认证信息
将认证信息存储在密码管理工具或环境变量中：
- 用户名（教堂账户邮箱或会员 ID）
- 密码

### 使用 Playwright 进行登录
```python
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def login(target_url="https://lcr.churchofjesuschrist.org", cookies_path="/tmp/church_cookies.json"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ..."
        )
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        await page.goto(target_url)

        # Enter username
        await page.fill('input[name="identifier"]', USERNAME)
        await page.click('button[type="submit"]')

        # Enter password
        await page.wait_for_selector('input[type="password"]')
        await page.fill('input[type="password"]', PASSWORD)
        await page.click('button[type="submit"]')

        # Wait for redirect
        await page.wait_for_url(f"{target_url}/**", timeout=30000)

        # Save session
        await context.storage_state(path=cookies_path.replace('.json', '_state.json'))
        await browser.close()
```

### 重用会话
登录后，可以利用已保存的会话状态信息避免再次进行身份验证：
```python
context = await browser.new_context(
    storage_state="/tmp/church_cookies_state.json",
    viewport={"width": 1920, "height": 1080},
    user_agent="Mozilla/5.0 ..."
)
page = await context.new_page()
await Stealth().apply_stealth_async(page)
```

## 主要网址
| 服务 | 网址 |
|---------|-----|
| LCR（领导与职员资源） | https://lcr.churchofjesuschrist.org |
| 会众目录 | https://directory.churchofjesuschrist.org |
| 日历 | https://www.churchofjesuschrist.org/calender |
| 捐赠 | https://donations.churchofjesuschrist.org |
| 圣殿预约 | https://tos.churchofjesuschrist.org |
| 我的主页 | https://www.churchofjesuschrist.org/my-home |
| 账户设置 | https://id.churchofjesuschrist.org/account |

## LCR 功能模块
登录后，用户可以访问以下内容：
- **会员信息**：会员记录、新成员信息、成员的加入/退出状态
- **圣职安排**：当前的圣职分配、支持信息
- **事工与福利**：工作任务及需求
- **财务**：什一税缴纳情况、预算信息、捐赠记录
- **传教工作**：全职及会众传教士的相关信息
- **圣殿事务**：圣殿使用状态、圣殿活动信息
- **报告**：出勤记录、季度报告

## 提示：
- 登录会话通过 cookie 保持有效——无需每次请求都重新登录
- 使用 playwright-stealth 与无头浏览器（headless Chrome）可避免被检测到
- 会话状态文件中包含认证令牌——请将其视为敏感信息妥善处理