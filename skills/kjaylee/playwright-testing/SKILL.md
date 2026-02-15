---
name: playwright-testing
description: 使用 Playwright 在 MiniPC 上测试 Web 应用程序和游戏。适用于验证前端功能、调试用户界面行为、捕获截图或进行游戏的质量保证（QA）测试。该工具支持通过 `nodes.run` 或 `browser.proxy` 实现无头浏览器自动化。
metadata:
  author: misskim
  version: "1.0"
  origin: Concept from Anthropic webapp-testing, adapted for Clawdbot + MiniPC environment
---

# Playwright 测试（MiniPC）

利用安装在 MiniPC 上的 Playwright 进行 Web 应用程序/游戏的测试。

## 环境

- **执行位置：** MiniPC（通过 `nodes.run` 或 `browser.proxy`）
- **浏览器：** 无头版 Chromium
- **用途：** 游戏质量保证（QA）、Web 应用功能测试、截图、控制台日志捕获

## 判断流程

```
테스트 대상 → 정적 HTML인가?
├─ Yes → 파일 내용 직접 읽어 셀렉터 파악
│        → Playwright 스크립트로 자동화
└─ No (동적 웹앱) → 서버 실행 중인가?
    ├─ No → 서버 먼저 실행 (MiniPC에서)
    └─ Yes → 정찰-행동 패턴:
        1. 페이지 이동 + networkidle 대기
        2. 스크린샷 또는 DOM 검사
        3. 셀렉터 파악
        4. 동작 실행
```

## 核心测试模式

### 侦察-行动（Reconnaissance-Then-Action）模式

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:PORT')
    page.wait_for_load_state('networkidle')  # 필수!

    # 1. 정찰: DOM 상태 파악
    page.screenshot(path='/tmp/inspect.png', full_page=True)

    # 2. 셀렉터 탐색
    buttons = page.locator('button').all()

    # 3. 행동: 파악된 셀렉터로 조작
    page.click('text=Start Game')

    browser.close()
```

### 游戏质量保证（QA）测试

```python
# 게임 로드 확인
page.goto('http://localhost:9877/game.html')
page.wait_for_load_state('networkidle')

# 캔버스 렌더링 확인
canvas = page.locator('canvas')
assert canvas.is_visible()

# 게임 상호작용 테스트
page.click('canvas', position={'x': 400, 'y': 300})
page.wait_for_timeout(1000)

# 스코어/상태 변화 확인
score = page.locator('#score').inner_text()
page.screenshot(path='/tmp/game-test.png')

# 콘솔 에러 캡처
errors = []
page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
```

## ⚠️ 重要注意事项

- **务必先使用 `networkidle`！** 对于动态应用程序，必须等待 JavaScript 执行完毕后再进行 DOM 检查。
- **必须设置 `headless=True`（MiniPC 没有显示器）。
- **必须在 MiniPC 上执行测试** — 禁止在 Mac Studio 中直接使用浏览器进行测试。
- **仅通过代码审查无法完成质量保证** — 必须进行实际的游戏测试。
- **建议使用 `browser.proxy` 或 `nodes.run` 来执行测试。

## 在 Clawdbot 上的执行方法

```
# 방법 1: browser tool (proxy)
browser action=navigate target=node node=MiniPC targetUrl="http://localhost:9877/game.html"
browser action=screenshot target=node node=MiniPC

# 방법 2: nodes.run으로 Python 스크립트 실행
nodes.run node=MiniPC command=["python3", "test_script.py"]
```