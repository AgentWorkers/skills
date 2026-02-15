---
name: e2e-gen
description: 根据用户流程生成 Playwright/Cypress 的端到端（E2E）测试
---

# E2E 测试生成器

该工具可描述用户操作流程，并自动生成 Playwright 或 Cypress 测试用例，无需再手动编写登录测试代码。

## 快速入门

```bash
npx ai-e2e-gen "User signs up, verifies email, completes onboarding"
```

## 功能介绍

- 将用户操作流程描述转换为 E2E 测试脚本
- 生成相应的 Playwright 或 Cypress 代码
- 包含必要的等待操作和断言逻辑
- 自动添加数据测试（data-testid）选择器

## 使用示例

```bash
# Generate Playwright test
npx ai-e2e-gen "User adds item to cart and checks out"

# Generate Cypress test
npx ai-e2e-gen "Admin creates new user" --framework cypress

# From existing page
npx ai-e2e-gen --url http://localhost:3000/dashboard
```

## 输出示例

```typescript
test('user completes checkout', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="checkout"]');
  await expect(page.locator('.success')).toBeVisible();
});
```

## 系统要求

- 必须安装 Node.js 18 及更高版本。
- 需要配置 OPENAI_API_KEY。

## 许可证

采用 MIT 许可协议，永久免费使用。

---

**开发团队：LXGIC Studios**

- GitHub 仓库：[github.com/lxgicstudios/ai-e2e-gen](https://github.com/lxgicstudios/ai-e2e-gen)
- Twitter 账号：[@lxgicstudios](https://x.com/lxgicstudios)