---
name: snapshot-test
description: 为组件生成Jest快照测试
---

# 快照测试生成器（Snapshot Test Generator）

将此工具应用于您的组件，即可生成相应的快照测试。该工具能够覆盖组件的常见状态和属性。

## 快速入门

```bash
npx ai-snapshot-test ./src/components/Button.tsx
```

## 功能介绍

- 生成 Jest 快照测试
- 测试组件的默认状态及边界情况
- 检查各种属性组合
- 支持异步组件的测试

## 使用示例

```bash
# Generate for a component
npx ai-snapshot-test ./src/components/Card.tsx

# Generate for directory
npx ai-snapshot-test ./src/components/

# With specific test runner
npx ai-snapshot-test ./components --runner vitest
```

## 输出示例

```typescript
describe('Button', () => {
  it('renders default state', () => {
    const { container } = render(<Button>Click me</Button>);
    expect(container).toMatchSnapshot();
  });

  it('renders disabled state', () => {
    const { container } = render(<Button disabled>Click me</Button>);
    expect(container).toMatchSnapshot();
  });
});
```

## 生成的测试用例包括：

- 默认属性
- 必需属性的各种取值
- 边界情况（空值、null）
- 组件的加载/错误状态
- 不同的组件尺寸/变体

## 系统要求

- Node.js 18.0 或更高版本
- 需要配置 OPENAI_API_KEY

## 许可证

- MIT 许可证。永久免费使用。

---

**开发团队：LXGIC Studios**

- GitHub 仓库：[github.com/lxgicstudios/ai-snapshot-test](https://github.com/lxgicstudios/ai-snapshot-test)
- Twitter 账号：[@lxgicstudios](https://x.com/lxgicstudios)