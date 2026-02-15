---
name: visual-regression
description: 视觉回归测试专家。适用于实施视觉测试、检测CSS代码中的回归问题（即代码更改导致的界面显示异常），或管理截图基准数据（用于比较不同版本界面的一致性）。
---

# 视觉回归测试技能

擅长视觉回归测试——利用截图对比、像素差异分析和视觉测试框架，自动化检测Web应用程序中非预期的视觉变化。

## 为什么需要视觉回归测试？

**解决的问题**：
- CSS更改导致布局意外破坏
- 响应式设计出现回退（移动设备/平板电脑/桌面设备）
- 不同浏览器之间的渲染差异
- 组件库的更改影响到用户界面
- 功能测试未能发现的UI问题

**示例场景**：
```
Developer changes global CSS: `.container { padding: 10px }`
  ↓
Accidentally breaks checkout page layout
  ↓
Functional E2E tests pass (buttons still clickable)
  ↓
Visual regression test catches layout shift
```

## 核心工具

### 1. Playwright Visual Snapshots（内置）

**为什么选择Playwright？**
- 无需第三方服务（免费）
- 执行速度快（支持并行执行）
- 内置自动遮罩功能（隐藏动态内容）
- 支持多种浏览器（Chromium、Firefox、WebKit）

#### 基本截图测试

```typescript
import { test, expect } from '@playwright/test';

test('homepage should match visual baseline', async ({ page }) => {
  await page.goto('https://example.com');

  // Take full-page screenshot and compare to baseline
  await expect(page).toHaveScreenshot('homepage.png');
});
```

**首次运行**（创建基准）：
```bash
npx playwright test --update-snapshots
# Creates: tests/__screenshots__/homepage.spec.ts/homepage-chromium-darwin.png
```

**后续运行**（与基准对比）：
```bash
npx playwright test
# Compares current screenshot to baseline
# Fails if difference exceeds threshold
```

#### 元素级截图

```typescript
test('button should match visual baseline', async ({ page }) => {
  await page.goto('/buttons');

  const submitButton = page.locator('[data-testid="submit-button"]');
  await expect(submitButton).toHaveScreenshot('submit-button.png');
});
```

#### 可配置的阈值

```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100, // Allow max 100 pixels to differ
      // OR
      maxDiffPixelRatio: 0.01, // Allow 1% of pixels to differ
    },
  },
});
```

#### 遮罩动态内容

```typescript
test('dashboard with dynamic data', async ({ page }) => {
  await page.goto('/dashboard');

  // Mask elements that change frequently (timestamps, user IDs)
  await expect(page).toHaveScreenshot({
    mask: [
      page.locator('.timestamp'),
      page.locator('.user-avatar'),
      page.locator('[data-testid="ad-banner"]'),
    ],
  });
});
```

#### 响应式测试（多视图窗口）

```typescript
const viewports = [
  { name: 'mobile', width: 375, height: 667 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1920, height: 1080 },
];

for (const viewport of viewports) {
  test(`homepage on ${viewport.name}`, async ({ page }) => {
    await page.setViewportSize({ width: viewport.width, height: viewport.height });
    await page.goto('https://example.com');

    await expect(page).toHaveScreenshot(`homepage-${viewport.name}.png`);
  });
}
```

### 2. Percy（基于云的视觉测试工具）

**为什么选择Percy？**
- 智能差异分析（忽略抗锯齿效果带来的差异）
- 提供UI审查功能（批准/拒绝更改）
- 与GitHub PR集成
- 支持跨浏览器并行测试
- 自动管理基准数据

#### 设置

```bash
npm install --save-dev @percy/playwright
```

```typescript
// tests/visual.spec.ts
import { test } from '@playwright/test';
import percySnapshot from '@percy/playwright';

test('homepage visual test', async ({ page }) => {
  await page.goto('https://example.com');

  // Percy captures screenshot and compares to baseline
  await percySnapshot(page, 'Homepage');
});
```

```bash
# Run tests with Percy
PERCY_TOKEN=your_token npx percy exec -- npx playwright test
```

#### Percy配置

```yaml
# .percy.yml
version: 2
snapshot:
  widths:
    - 375   # Mobile
    - 768   # Tablet
    - 1280  # Desktop
  min-height: 1024
  percy-css: |
    /* Hide dynamic elements */
    .timestamp { visibility: hidden; }
    .ad-banner { display: none; }
```

#### 在CI流程中使用Percy（GitHub Actions）

```yaml
name: Visual Tests

on: [pull_request]

jobs:
  percy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install --with-deps

      - name: Run Percy tests
        run: npx percy exec -- npx playwright test
        env:
          PERCY_TOKEN: ${{ secrets.PERCY_TOKEN }}
```

### 3. Chromatic（Storybook视觉测试工具）

**为什么选择Chromatic？**
- 专为组件库设计（与Storybook集成）
- 自动捕获所有组件状态
- 提供UI审查流程（批准/拒绝更改）
- 能检测可访问性问题
- 支持设计系统的版本控制

#### 设置（Storybook + Chromatic）

```bash
npm install --save-dev chromatic
npx chromatic --project-token=your_token
```

```javascript
// .storybook/main.js
module.exports = {
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: ['@storybook/addon-essentials'],
};
```

```typescript
// Button.stories.tsx
import { Button } from './Button';

export default {
  title: 'Components/Button',
  component: Button,
};

export const Primary = () => <Button variant="primary">Click me</Button>;
export const Disabled = () => <Button disabled>Disabled</Button>;
export const Loading = () => <Button loading>Loading...</Button>;
```

```bash
# Chromatic captures all stories automatically
npx chromatic --project-token=your_token
```

#### 在CI流程中使用Chromatic

```yaml
name: Chromatic

on: push

jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0 # Required for Chromatic
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx chromatic --project-token=${{ secrets.CHROMATIC_TOKEN }}
```

### 4. BackstopJS（基于配置的视觉测试工具）

**为什么选择BackstopJS？**
- 无需编写代码（仅通过JSON配置）
- 本地执行（无需依赖云服务）
- 提供交互式报告
- 支持基于CSS选择器的测试场景

#### 配置

```json
{
  "id": "myapp_visual_tests",
  "viewports": [
    { "label": "phone", "width": 375, "height": 667 },
    { "label": "tablet", "width": 768, "height": 1024 },
    { "label": "desktop", "width": 1920, "height": 1080 }
  ],
  "scenarios": [
    {
      "label": "Homepage",
      "url": "https://example.com",
      "selectors": ["document"],
      "delay": 500
    },
    {
      "label": "Login Form",
      "url": "https://example.com/login",
      "selectors": [".login-form"],
      "hideSelectors": [".banner-ad"],
      "delay": 1000
    }
  ],
  "paths": {
    "bitmaps_reference": "backstop_data/bitmaps_reference",
    "bitmaps_test": "backstop_data/bitmaps_test",
    "html_report": "backstop_data/html_report"
  }
}
```

```bash
# Create baseline
backstop reference

# Run test (compare to baseline)
backstop test

# Update baseline (approve changes)
backstop approve
```

## 测试策略

### 1. 组件级视觉测试

**应用场景**：设计系统组件（按钮、输入框、模态框）

```typescript
// Component snapshots
test.describe('Button component', () => {
  test('primary variant', async ({ page }) => {
    await page.goto('/storybook?path=/story/button--primary');
    await expect(page.locator('.button')).toHaveScreenshot('button-primary.png');
  });

  test('disabled state', async ({ page }) => {
    await page.goto('/storybook?path=/story/button--disabled');
    await expect(page.locator('.button')).toHaveScreenshot('button-disabled.png');
  });

  test('hover state', async ({ page }) => {
    await page.goto('/storybook?path=/story/button--primary');
    const button = page.locator('.button');
    await button.hover();
    await expect(button).toHaveScreenshot('button-hover.png');
  });
});
```

### 2. 页面级视觉测试

**应用场景**：整个页面（首页、结账页面、个人资料页面）

```typescript
test('checkout page visual baseline', async ({ page }) => {
  await page.goto('/checkout');

  // Wait for page to fully load
  await page.waitForLoadState('networkidle');

  // Mask dynamic content
  await expect(page).toHaveScreenshot('checkout.png', {
    mask: [page.locator('.cart-timestamp'), page.locator('.promo-banner')],
    fullPage: true, // Capture entire page (scrolling)
  });
});
```

### 3. 基于交互的视觉测试

**应用场景**：模态框、下拉菜单、工具提示（需要用户交互）

```typescript
test('modal visual test', async ({ page }) => {
  await page.goto('/');

  // Open modal
  await page.click('[data-testid="open-modal"]');
  await page.waitForSelector('.modal');

  // Capture modal screenshot
  await expect(page.locator('.modal')).toHaveScreenshot('modal-open.png');

  // Test error state
  await page.fill('input[name="email"]', 'invalid');
  await page.click('button[type="submit"]');
  await expect(page.locator('.modal')).toHaveScreenshot('modal-error.png');
});
```

### 4. 跨浏览器视觉测试

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
```

```bash
# Run tests across all browsers
npx playwright test

# Generates separate baselines per browser:
# - homepage-chromium-darwin.png
# - homepage-firefox-darwin.png
# - homepage-webkit-darwin.png
```

## 最佳实践

### 1. 在捕获测试结果前确保页面稳定

**问题**：动画效果、懒加载内容、字体加载等问题可能导致测试结果不稳定。

```typescript
// ❌ BAD: Capture immediately
await page.goto('/');
await expect(page).toHaveScreenshot();

// ✅ GOOD: Wait for stability
await page.goto('/');
await page.waitForLoadState('networkidle'); // Wait for network idle
await page.waitForSelector('.main-content'); // Wait for key element
await page.evaluate(() => document.fonts.ready); // Wait for fonts

// Disable animations for consistent screenshots
await page.addStyleTag({
  content: `
    *, *::before, *::after {
      animation-duration: 0s !important;
      transition-duration: 0s !important;
    }
  `,
});

await expect(page).toHaveScreenshot();
```

### 2. 遮罩动态内容

```typescript
await expect(page).toHaveScreenshot({
  mask: [
    page.locator('.timestamp'), // Changes every second
    page.locator('.user-id'), // Different per user
    page.locator('[data-dynamic="true"]'), // Marked as dynamic
    page.locator('video'), // Video frames vary
  ],
});
```

### 3. 为测试用例起有意义的名称

```typescript
// ❌ BAD: Generic names
await expect(page).toHaveScreenshot('test1.png');

// ✅ GOOD: Descriptive names
await expect(page).toHaveScreenshot('homepage-logged-in-user.png');
await expect(page).toHaveScreenshot('checkout-empty-cart-error.png');
```

### 4. 仅测试关键路径

**视觉回归测试耗时较长（速度慢，占用存储空间较大）**。因此，应优先测试关键路径：

```typescript
// ✅ High Priority (critical user flows)
- Homepage (first impression)
- Checkout flow (revenue-critical)
- Login/signup (user acquisition)
- Product details (conversion)

// ⚠️ Medium Priority (important but not critical)
- Profile settings
- Search results
- Category pages

// ❌ Low Priority (skip or sample)
- Admin dashboards (internal users)
- Footer (rarely changes)
- Legal pages
```

### 5. 基准数据管理策略

**何时更新基准数据**：
- ✅ 经设计团队批准的设计更改
- ✅ 组件库升级（经过审查）
- ✅ 浏览器更新（已知会有差异）
- ❌ 非预期的更改（需先进行调查！）

```bash
# Review diff report BEFORE approving
npx playwright test --update-snapshots # Use carefully!

# Better: Update selectively
npx playwright test homepage.spec.ts --update-snapshots
```

## 调试视觉差异

### 1. 查看差异报告

Playwright会生成包含对比结果的HTML报告：

```bash
npx playwright test
# On failure, opens: playwright-report/index.html
# Shows: Expected | Actual | Diff (highlighted pixels)
```

### 2. 调整阈值

```typescript
// Tolerate minor differences (anti-aliasing, font rendering)
await expect(page).toHaveScreenshot({
  maxDiffPixelRatio: 0.02, // 2% tolerance
});
```

### 3. 忽略特定区域

```typescript
// Ignore regions that legitimately differ
await expect(page).toHaveScreenshot({
  mask: [page.locator('.animated-banner')],
  clip: { x: 0, y: 0, width: 800, height: 600 }, // Capture specific area
});
```

## CI/CD集成

### 1. 使用GitHub Actions进行Playwright截图测试

```yaml
name: Visual Regression Tests

on:
  pull_request:
    branches: [main]

jobs:
  visual:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install --with-deps

      - name: Run visual tests
        run: npx playwright test

      - name: Upload diff report
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: visual-diff-report
          path: playwright-report/
```

### 2. 基准数据存储策略

**选项1：Git LFS（大文件存储）**
- 将基准数据存储在Git仓库中（与代码一起版本控制）
- 使用Git LFS避免仓库文件过大
- 自动在开发人员之间同步基准数据

```bash
# .gitattributes
*.png filter=lfs diff=lfs merge=lfs -text

git lfs install
git add tests/__screenshots__/*.png
git commit -m "Add visual baselines"
```

**选项2：云存储（S3、GCS）**
- 将基准数据存储在云服务器上
- 在CI过程中下载基准数据
- 提高CI效率（无需等待Git LFS同步）

```yaml
- name: Download baselines
  run: aws s3 sync s3://my-bucket/baselines tests/__screenshots__/
```

**选项3：使用Percy/Chromatic进行管理**
- 基准数据由服务端管理（无需使用Git）
- 自动更新基准数据
- 提供UI界面用于审查更改

### 3. 处理基准数据漂移问题

**问题**：开发者A更新了基准数据，导致开发者B的测试失败。

**解决方案1：要求进行基准数据审查**
```yaml
# PR merge rules
- Require approval for changes in tests/__screenshots__/
```

**解决方案2：在CI过程中自动更新基准数据**
```yaml
- name: Update baselines if approved
  if: contains(github.event.pull_request.labels.*.name, 'update-baselines')
  run: |
    npx playwright test --update-snapshots
    git config user.name "GitHub Actions"
    git add tests/__screenshots__/
    git commit -m "Update visual baselines"
    git push
```

## 常见问题及解决方法

### 1. 由于动画效果导致的测试结果不稳定

❌ **错误做法**：
```typescript
await page.goto('/'); // Page has CSS animations
await expect(page).toHaveScreenshot(); // Fails randomly (mid-animation)
```

✅ **正确做法**：
```typescript
await page.goto('/');
await page.addStyleTag({ content: '* { animation: none !important; }' });
await expect(page).toHaveScreenshot();
```

### 2. 字体加载问题

❌ **错误做法**：
```typescript
await page.goto('/'); // Fonts loading async
await expect(page).toHaveScreenshot(); // Sometimes uses fallback font
```

✅ **正确做法**：
```typescript
await page.goto('/');
await page.evaluate(() => document.fonts.ready); // Wait for fonts
await expect(page).toHaveScreenshot();
```

### 3. 测试所有内容（导致CI流程缓慢）

❌ **错误做法**：进行大量视觉测试（CI耗时30分钟）
✅ **正确做法**：仅测试关键视觉元素（CI耗时5分钟）

**优化方法**：
```typescript
// Run visual tests only on visual changes
if (changedFiles.some(file => file.endsWith('.css'))) {
  runVisualTests();
}
```

### 4. 不同平台（macOS与Linux）之间的显示差异

**问题**：macOS（本地开发环境）和Linux（CI环境）下的截图可能不一致。

**解决方案**：使用Docker进行本地开发

```bash
# Local development with Docker
docker run -it --rm -v $(pwd):/work -w /work mcr.microsoft.com/playwright:v1.40.0-focal npx playwright test
```

## 高级技术

### 1. 针对电子邮件的视觉回归测试

```typescript
test('email template visual test', async ({ page }) => {
  const emailHtml = await generateEmailTemplate({ userName: 'John', orderTotal: '$99.99' });

  await page.setContent(emailHtml);
  await expect(page).toHaveScreenshot('order-confirmation-email.png');
});
```

### 2. PDF格式的视觉测试

```typescript
test('invoice PDF visual test', async ({ page }) => {
  await page.goto('/invoice/123');
  const pdfBuffer = await page.pdf({ format: 'A4' });

  // Convert PDF to image and compare
  const pdfImage = await pdfToImage(pdfBuffer);
  expect(pdfImage).toMatchSnapshot('invoice.png');
});
```

### 3. A/B测试（比较不同版本的UI）

```typescript
test('A/B test variant visual comparison', async ({ page }) => {
  // Test control variant
  await page.goto('/?variant=control');
  await expect(page).toHaveScreenshot('homepage-control.png');

  // Test experiment variant
  await page.goto('/?variant=experiment');
  await expect(page).toHaveScreenshot('homepage-experiment.png');

  // Manual review to ensure both look good
});
```

## 参考资源

- [Playwright视觉对比工具文档](https://playwright.dev/docs/test-snapshots)
- [Percy文档](https://docs.percy.io/)
- [Chromatic文档](https://www.chromatic.com/docs/)
- [BackstopJS文档](https://github.com/garris/BackstopJS)

## 常见问题解答

- **如何设置视觉回归测试？**
- **Playwright如何进行截图测试？**
- **Percy与Chromatic哪个更好？**
- **如何针对组件进行视觉测试？**
- **如何解决测试结果不稳定的问题？**
- **如何在CI过程中管理视觉测试的基准数据？**
- **如何进行跨浏览器视觉测试？**
- **截图对比的最佳实践是什么？**
- **如何将视觉回归测试集成到CI流程中？**