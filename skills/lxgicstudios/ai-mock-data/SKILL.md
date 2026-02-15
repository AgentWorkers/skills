---
name: mock-data
description: **从 TypeScript 类型生成逼真的模拟数据**

在开发过程中，有时我们需要根据 TypeScript 类型生成相应的模拟数据，以用于测试或演示目的。以下是一些常用的方法来实现这一目标：

### 方法一：使用 TypeScript 的 `Object.create()` 方法

```typescript
function generateMockData<T>(type: Type) {
  return Object.create({ ...type });
}

// 示例：
const Person = {
  name: string,
  age: number,
  email: string
};

const personMock = generateMockData(Person);
console.log(personMock); // 输出：{ name: '张三', age: 25, email: 'zhangsan@example.com' }
```

### 方法二：利用泛型与自定义构造函数

```typescript
type Person<T> = {
  name: string;
  age: number;
  email: string;
};

function generateMockPerson<T>(type: Person<T>) {
  return new type({ ...type });
}

// 示例：
const Person = {
  name: '李四',
  age: 30,
  email: 'lisi@example.com'
};

const personMock = generateMockPerson(Person);
console.log(personMock); // 输出：{ name: '李四', age: 30, email: 'lisi@example.com' }
```

### 方法三：结合 TypeScript 的 `interface` 和 `class` 定义

```typescript
interface Person {
  name: string;
  age: number;
  email: string;
}

class Person implements Person {
  constructor(name: string, age: number, email: string) {
    this.name = name;
    this.age = age;
    this.email = email;
  }
}

function generateMockPerson(): Person {
  return new Person('王五', 28, 'wangwu@example.com');
}

const personMock = generateMockPerson();
console.log(personMock); // 输出：{ name: '王五', age: 28, email: 'wangwu@example.com' }
```

### 方法四：使用第三方库（如 `mock-data-generator`）

如果你需要更复杂的模拟数据生成逻辑，可以考虑使用第三方库，如 [mock-data-generator](https://github.com/maurycodewarrior/mock-data-generator)。这个库提供了丰富的模板和生成器，可以轻松生成各种类型的模拟数据。

### 注意事项：

- 在生成模拟数据时，确保数据的随机性和多样性，以避免重复或不符合实际数据分布的情况。
- 根据具体需求，可以对模拟数据进行一些简单的处理（如添加错误或异常情况）。

通过以上方法，你可以根据 TypeScript 类型生成逼真的模拟数据，以满足开发中的各种需求。
---

# 模拟数据生成器

您可以指定数据类型，该工具会生成逼真的虚假数据，非常适合用于测试和开发场景。

## 快速入门

```bash
npx ai-mock-data ./src/types/User.ts
```

## 功能介绍

- 读取 TypeScript 接口定义
- 生成逼真的虚假数据
- 识别字段名称（如 email、phone 等）
- 创建包含多样化数据的数组

## 使用示例

```bash
# Generate from type file
npx ai-mock-data ./src/types/Order.ts

# Generate specific count
npx ai-mock-data ./types/User.ts --count 50

# Output as JSON file
npx ai-mock-data ./types/Product.ts --out ./fixtures/products.json

# Generate for specific type
npx ai-mock-data ./types/index.ts --type Customer
```

## 输出示例

```json
[
  {
    "id": "usr_8x7k2m",
    "email": "sarah.chen@gmail.com",
    "name": "Sarah Chen",
    "createdAt": "2024-01-15T09:23:00Z"
  }
]
```

## 智能字段处理

- `email`：生成真实的电子邮件地址
- `phone`：生成格式正确的电话号码
- `address`：生成看起来真实的地址
- `price`：生成符合货币规范的数值

## 系统要求

- 必需安装 Node.js 18 及以上版本，并提供 OPENAI_API_KEY。

## 许可证

采用 MIT 许可协议，永久免费使用。

---

**开发团队：LXGIC Studios**

- GitHub 仓库：[github.com/lxgicstudios/ai-mock-data](https://github.com/lxgicstudios/ai-mock-data)
- Twitter 账号：[@lxgicstudios](https://x.com/lxgicstudios)