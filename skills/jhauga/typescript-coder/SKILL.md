---
name: typescript-coder
description: '拥有十年经验的资深工程师，精通TypeScript的基础知识、迁移策略及最佳实践。当遇到需要“添加TypeScript”、“将代码迁移到TypeScript”、“启用类型检查”、“配置TypeScript环境”、“修复TypeScript错误”或处理.ts/.tsx文件相关任务时，可提供专业支持。具备将JavaScript代码迁移到TypeScript的能力，熟悉JSDoc类型注释、tsconfig.json配置文件以及类型安全的编码规范。'
---
# TypeScript 开发技能

掌握 TypeScript 开发，具备类型系统、迁移策略以及现代 JavaScript/TypeScript 模式的专家级知识。这项技能能将你提升为一名能力出众的工程师，使你能够编写类型安全的代码，并自信地将现有的 JavaScript 项目迁移到 TypeScript。

## 何时使用这项技能

- 当用户请求“添加 TypeScript”、“迁移到 TypeScript”或“转换为 TypeScript”时
- 需要在项目中“添加类型检查”或“修复 TypeScript 错误”时
- 创建或配置项目的 `tsconfig.json` 文件时
- 处理 `.ts`、`.tsx`、`.mts` 或 `.d.ts` 文件时
- 为 JavaScript 文件添加 JSDoc 类型注释时
- 调试类型错误或提升类型安全性时
- 在 Node.js、React 或其他 JavaScript 项目中设置 TypeScript 时
- 创建类型定义或环境声明时
- 实现高级 TypeScript 模式（如泛型、条件类型、映射类型）时

## 先决条件

- 对 JavaScript（ES6+）有基本了解
- 安装了 Node.js 和 npm/yarn（用于 TypeScript 编译）
- 熟悉项目结构和构建工具
- 可以访问 `typescript` 包（如需可安装）

## 缩写命令

以下是触发此技能的缩写命令（就像使用命令行工具一样）：

```javascript
openPrompt = ["typescript-coder", "ts-coder"]
```

使用这些缩写命令可以快速调用 TypeScript 的专业知识，而无需冗长的解释。例如：

- `typescript-coder --check "this code"`
- `typescript-coder check this type guard`
- `ts-coder migrate this file`
- `ts-coder --migrate project-to-typescript`

## 角色与专长

作为 TypeScript 专家，你将运用以下能力：

- **深入的类型系统知识**：理解 TypeScript 的结构类型系统、泛型和高级类型
- **迁移专长**：具备将 JavaScript 逐步迁移到 TypeScript 的成熟策略
- **最佳实践**：了解 TypeScript 的模式、规范和反模式
- **工具精通**：配置 TypeScript 编译器、构建工具和集成到 IDE 中
- **问题解决**：能够解决复杂的类型错误并设计类型安全的架构

## 核心 TypeScript 概念

### TypeScript 类型系统

TypeScript 使用**结构类型**（而非名义类型）：

```typescript
interface Point {
  x: number;
  y: number;
}

// This works because the object has the right structure
const point: Point = { x: 10, y: 20 };

// This also works - structural compatibility
const point3D = { x: 1, y: 2, z: 3 };
const point2D: Point = point3D;  // OK - has x and y
```

### 类型推断

TypeScript 会在可能的情况下进行类型推断，从而减少样板代码：

```typescript
// Type inferred as string
const message = "Hello, TypeScript!";

// Type inferred as number
const count = 42;

// Type inferred as string[]
const names = ["Alice", "Bob", "Charlie"];

// Return type inferred as number
function add(a: number, b: number) {
  return a + b;  // Returns number
}
```

### TypeScript 的关键特性

| 特性 | 目的 | 使用场景 |
|---------|---------|-------------|
| **接口** | 定义对象结构 | 定义数据结构、API 合同 |
| **类型别名** | 创建自定义类型 | 联合类型、复杂类型、类型工具 |
| **泛型** | 类型安全的可重用组件 | 可处理多种类型的函数/类 |
| **枚举** | 带有名称的常量 | 固定的相关值集合 |
| **类型保护** | 运行时类型检查 | 安全地缩小联合类型范围 |
| **工具类型** | 转换类型 | `Partial<T>`、`Pick<T, K>`、`Omit<T, K>` 等 |

## 分步工作流程

### 任务 1：安装和配置 TypeScript

对于新的或现有的 JavaScript 项目：

1. **将 TypeScript 安装为开发依赖项**：
   ```bash
   npm install --save-dev typescript
   ```

2. **为 Node.js 安装类型定义**（如果使用 Node.js）：
   ```bash
   npm install --save-dev @types/node
   ```

3. **初始化 TypeScript 配置**：
   ```bash
   npx tsc --init
   ```

4. **为项目配置 `tsconfig.json`**：
   ```json
   {
     "compilerOptions": {
       "target": "ES2020",
       "module": "commonjs",
       "lib": ["ES2020"],
       "outDir": "./dist",
       "rootDir": "./src",
       "strict": true,
       "esModuleInterop": true,
       "skipLibCheck": true,
       "forceConsistentCasingInFileNames": true,
       "resolveJsonModule": true,
       "declaration": true,
       "declarationMap": true,
       "sourceMap": true
     },
     "include": ["src/**/*"],
     "exclude": ["node_modules", "dist"]
   }
   ```

5. **在 `package.json` 中添加构建脚本**：
   ```json
   {
     "scripts": {
       "build": "tsc",
       "dev": "tsc --watch",
       "check": "tsc --noEmit"
     }
   }
   ```

### 任务 2：将 JavaScript 迁移到 TypeScript（逐步进行）

安全的逐步迁移策略：

1. **启用 TypeScript 处理 JavaScript 文件**：
   ```json
   {
     "compilerOptions": {
       "allowJs": true,
       "checkJs": false,
       "noEmit": true
     }
   }
   ```

2. **为 JavaScript 文件添加 JSDoc 类型注释**（可选的中间步骤）：
   ```javascript
   // @ts-check

   /**
    * Calculates the sum of two numbers
    * @param {number} a - First number
    * @param {number} b - Second number
    * @returns {number} The sum
    */
   function add(a, b) {
     return a + b;
   }

   /** @type {string[]} */
   const names = ["Alice", "Bob"];

   /** @typedef {{ id: number, name: string, email?: string }} User */

   /** @type {User} */
   const user = {
     id: 1,
     name: "Alice"
   };
   ```

3. **逐步将文件名从 `.js` 更改为 `.ts`**：
   ```bash
   # Start with utility files and leaf modules
   mv src/utils/helpers.js src/utils/helpers.ts
   ```

4. **修复转换后的文件中的 TypeScript 错误**：
   - 在类型推断失败的地方添加显式的类型注释
   - 为复杂对象定义接口
   - 适当处理 `any` 类型
   - 添加类型保护以进行运行时检查

5. **逐步转换剩余的文件**：
   - 从实用工具和共享模块开始
   - 然后转换叶子组件（无依赖项）
   - 最后转换组织/入口文件

6. **逐步启用严格模式**：
   ```json
   {
     "compilerOptions": {
       "strict": false,
       "noImplicitAny": true,
       "strictNullChecks": true
       // Enable other strict flags one at a time
     }
   }
   ```

### 任务 3：定义类型和接口

创建强大的类型定义：

1. **为数据结构定义接口**：
   ```typescript
   // User data model
   interface User {
     id: number;
     name: string;
     email: string;
     age?: number;  // Optional property
     readonly createdAt: Date;  // Read-only property
   }

   // API response structure
   interface ApiResponse<T> {
     success: boolean;
     data?: T;
     error?: {
       code: string;
       message: string;
     };
   }
   ```

2. **为复杂类型使用类型别名**：
   ```typescript
   // Union type
   type Status = 'pending' | 'active' | 'completed' | 'failed';

   // Intersection type
   type Employee = User & {
     employeeId: string;
     department: string;
     salary: number;
   };

   // Function type
   type TransformFn<T, U> = (input: T) => U;

   // Conditional type
   type NonNullable<T> = T extends null | undefined ? never : T;
   ```

3. **为外部模块创建 `.d.ts` 文件中的类型定义**：
   ```typescript
   // types/custom-module.d.ts
   declare module 'custom-module' {
     export interface Config {
       apiKey: string;
       timeout?: number;
     }

     export function initialize(config: Config): Promise<void>;
     export function fetchData<T>(endpoint: string): Promise<T>;
   }
   ```

### 任务 4：使用泛型

编写类型安全的可重用组件：

1. **泛型函数**：
   ```typescript
   // Basic generic function
   function identity<T>(value: T): T {
     return value;
   }

   const num = identity(42);        // Type: number
   const str = identity("hello");   // Type: string

   // Generic with constraints
   function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
     return obj[key];
   }

   const user = { name: "Alice", age: 30 };
   const name = getProperty(user, "name");  // Type: string
   const age = getProperty(user, "age");    // Type: number
   ```

2. **泛型类**：
   ```typescript
   class DataStore<T> {
     private items: T[] = [];

     add(item: T): void {
       this.items.push(item);
     }

     get(index: number): T | undefined {
       return this.items[index];
     }

     filter(predicate: (item: T) => boolean): T[] {
       return this.items.filter(predicate);
     }
   }

   const numberStore = new DataStore<number>();
   numberStore.add(42);

   const userStore = new DataStore<User>();
   userStore.add({ id: 1, name: "Alice", email: "alice@example.com" });
   ```

3. **泛型接口**：
   ```typescript
   interface Repository<T> {
     findById(id: string): Promise<T | null>;
     findAll(): Promise<T[]>;
     create(item: Omit<T, 'id'>): Promise<T>;
     update(id: string, item: Partial<T>): Promise<T>;
     delete(id: string): Promise<boolean>;
   }

   class UserRepository implements Repository<User> {
     async findById(id: string): Promise<User | null> {
       // Implementation
       return null;
     }
     // ... other methods
   }
   ```

### 任务 5：处理类型错误

常见的类型错误及解决方法：

1. **“属性不存在”错误**：
   ```typescript
   // ❌ Error: Property 'name' does not exist on type '{}'
   const user = {};
   user.name = "Alice";

   // ✅ Solution 1: Define interface
   interface User {
     name: string;
   }
   const user: User = { name: "Alice" };

   // ✅ Solution 2: Type assertion (use cautiously)
   const user = {} as User;
   user.name = "Alice";

   // ✅ Solution 3: Index signature
   interface DynamicObject {
     [key: string]: any;
   }
   const user: DynamicObject = {};
   user.name = "Alice";
   ```

2. **“找不到名称”错误**：
   ```typescript
   // ❌ Error: Cannot find name 'process'
   const env = process.env.NODE_ENV;

   // ✅ Solution: Install type definitions
   // npm install --save-dev @types/node
   const env = process.env.NODE_ENV;  // Now works
   ```

3. **`any` 类型问题**：
   ```typescript
   // ❌ Implicit any (with noImplicitAny: true)
   function process(data) {
     return data.value;
   }

   // ✅ Solution: Add explicit types
   function process(data: { value: number }): number {
     return data.value;
   }

   // ✅ Or use generic
   function process<T>(data: T): T {
     return data;
   }
   ```

4. **联合类型缩小**：
   ```typescript
   function processValue(value: string | number) {
     // ❌ Error: Property 'toUpperCase' does not exist on type 'string | number'
     return value.toUpperCase();

     // ✅ Solution: Type guard
     if (typeof value === "string") {
       return value.toUpperCase();  // TypeScript knows it's string here
     }
     return value.toString();
   }
   ```

### 任务 6：针对特定环境进行配置

#### Node.js 项目

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "types": ["node"],
    "moduleResolution": "node",
    "esModuleInterop": true
  }
}
```

#### React 项目

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "esnext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true
  }
}
```

#### 库/包

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "esnext",
    "declaration": true,
    "declarationMap": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

## TypeScript 最佳实践

### 应该做的

- ✅ **启用严格模式**（`"strict": true`）以获得最大的类型安全性
- ✅ **使用类型推断**——在类型明显时让 TypeScript 自动推断
- ✅ **优先使用接口而非类型别名**（提供更好的错误信息）
- ✅ **使用 `unknown` 而不是 `any`——在使用前强制进行类型检查
- ✅ **创建工具类型**以进行常见的类型转换
- ✅ **使用常量断言**（`as const`）处理字面量类型
- ✅ **利用类型保护**进行运行时类型检查
- ✅ **用 JSDoc 注释记录复杂类型**
- ✅ **使用区分联合类型**进行类型安全的状态管理
- ✅ **保持类型代码的简洁性**——提取并重用类型定义

### 不应该做的

- ❌ **不要到处使用 `any`——这违背了 TypeScript 的目的**
- ❌ **不要无理由地使用 `@ts-ignore` 忽略 TypeScript 错误**
- ❌ **不要过度复杂化类型**——在安全性和可读性之间找到平衡
- ❌ **不要过度使用类型断言**——这可能表明设计问题
- ❌ **不要重复类型定义**——使用共享类型
- ❌ **不要忘记进行 `null/undefined` 检查**——启用 `strictNullChecks`
- ❌ **不要对所有内容都使用枚举**——考虑使用联合类型
- ❌ **不要省略外部库的类型定义**——安装 `@types/*`
- ❌ **不要无故禁用严格模式**
- ❌ **不要在生产环境中混合使用 JavaScript 和 TypeScript**——完成迁移

## 常见模式

### 模式 1：区分联合类型

类型安全的状态管理：

```typescript
type LoadingState = { status: 'loading' };
type SuccessState<T> = { status: 'success'; data: T };
type ErrorState = { status: 'error'; error: Error };

type AsyncState<T> = LoadingState | SuccessState<T> | ErrorState;

function handleState<T>(state: AsyncState<T>) {
  switch (state.status) {
    case 'loading':
      console.log('Loading...');
      break;
    case 'success':
      console.log('Data:', state.data);  // TypeScript knows state.data exists
      break;
    case 'error':
      console.log('Error:', state.error.message);  // TypeScript knows state.error exists
      break;
  }
}
```

### 模式 2：构建器模式

类型安全的流畅 API：

```typescript
class QueryBuilder<T> {
  private filters: Array<(item: T) => boolean> = [];
  private sortFn?: (a: T, b: T) => number;
  private limitCount?: number;

  where(predicate: (item: T) => boolean): this {
    this.filters.push(predicate);
    return this;
  }

  sortBy(compareFn: (a: T, b: T) => number): this {
    this.sortFn = compareFn;
    return this;
  }

  limit(count: number): this {
    this.limitCount = count;
    return this;
  }

  execute(data: T[]): T[] {
    let result = data.filter(item =>
      this.filters.every(filter => filter(item))
    );

    if (this.sortFn) {
      result = result.sort(this.sortFn);
    }

    if (this.limitCount) {
      result = result.slice(0, this.limitCount);
    }

    return result;
  }
}

// Usage
const users = [/* ... */];
const result = new QueryBuilder<User>()
  .where(u => u.age > 18)
  .where(u => u.email.includes('@example.com'))
  .sortBy((a, b) => a.name.localeCompare(b.name))
  .limit(10)
  .execute(users);
```

### 模式 3：类型安全的事件发射器

```typescript
type EventMap = {
  'user:created': { id: string; name: string };
  'user:updated': { id: string; changes: Partial<User> };
  'user:deleted': { id: string };
};

class TypedEventEmitter<T extends Record<string, any>> {
  private listeners: { [K in keyof T]?: Array<(data: T[K]) => void> } = {};

  on<K extends keyof T>(event: K, listener: (data: T[K]) => void): void {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event]!.push(listener);
  }

  emit<K extends keyof T>(event: K, data: T[K]): void {
    const eventListeners = this.listeners[event];
    if (eventListeners) {
      eventListeners.forEach(listener => listener(data));
    }
  }
}

// Usage with type safety
const emitter = new TypedEventEmitter<EventMap>();

emitter.on('user:created', (data) => {
  console.log(data.id, data.name);  // TypeScript knows the shape
});

emitter.emit('user:created', { id: '123', name: 'Alice' });  // Type-checked
```

## 故障排除

| 问题 | 原因 | 解决方案 |
|-------|-------|----------|
| **模块未找到** | 缺少类型定义 | 安装 `@types/[package-name]` 或添加 `declare module` |
| **隐式 `any` 错误** | 启用了 `noImplicitAny` | 添加显式的类型注释 |
| **找不到全局类型** | `compilerOptions` 中缺少库 | 在 `lib` 中添加：`["ES2020", "DOM"]` |
| **`node_modules` 中的类型错误** | 第三方库的类型 | 在 `tsconfig.json` 中添加 `skipLibCheck: true` |
| **带有 `.ts` 扩展名的导入错误** | 导入解析问题 | 使用不带扩展名的导入 |
| **构建耗时过长** | 编译的文件太多 | 使用 `incremental: true` 和 `tsBuildInfoFile` |
| **类型推断不起作用** | 类型推断复杂 | 添加显式的类型注释 |
| **循环依赖错误** | 导入循环 | 重构以打破循环，使用接口 |

## 高级 TypeScript 特性

### 映射类型

转换现有的类型：

```typescript
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

type Partial<T> = {
  [P in keyof T]?: T[P];
};

type Pick<T, K extends keyof T> = {
  [P in K]: T[P];
};

// Usage
interface User {
  id: number;
  name: string;
  email: string;
}

type ReadonlyUser = Readonly<User>;  // All properties readonly
type PartialUser = Partial<User>;    // All properties optional
type UserNameEmail = Pick<User, 'name' | 'email'>;  // Only name and email
```

### 条件类型

根据条件变化的类型：

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<string>;   // true
type B = IsString<number>;   // false

// Practical example: Extract function return type
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

function getUser() {
  return { id: 1, name: "Alice" };
}

type User = ReturnType<typeof getUser>;  // { id: number; name: string }
```

### 模板字面量类型

在类型级别进行字符串操作：

```typescript
type Greeting<T extends string> = `Hello, ${T}!`;

type WelcomeMessage = Greeting<"World">;  // "Hello, World!"

// Practical: Create event names
type EventName<T extends string> = `on${Capitalize<T>}`;

type ClickEvent = EventName<"click">;  // "onClick"
type HoverEvent = EventName<"hover">;  // "onHover"
```

## TypeScript 配置参考

### `tsconfig.json` 的关键选项

| 选项 | 目的 | 推荐值 |
|--------|---------|-------------|
| `strict` | 启用所有严格的类型检查 | `true` |
| `target` | ECMAScript 目标版本 | `ES2020` 或更高 |
| `module` | 模块系统 | `commonjs`（Node）或 `esnext`（打包工具） |
| `lib` | 包含类型定义 | `["ES2020"]` + `DOM`（如果用于浏览器） |
| `outDir` | 输出目录 | `./dist` |
| `rootDir` | 源代码目录 | `./src` |
| `sourceMap` | 生成源映射 | `true`（用于调试） |
| `declaration` | 为库生成 `.d.ts` 文件 | `true` |
| `esModuleInterop` | 启用 CommonJS 和 ES 模块之间的互操作 | `true` |
| `skipLibCheck` | 跳过 `.d.ts` 文件的类型检查 | `true`（为了性能） |
| `forceConsistentCasingInFileNames` | 强制文件名大小写一致 | `true` |
| `resolveJsonModule` | 允许导入 JSON 文件 | 如有需要则启用 |
| `allowJs` | 允许 JavaScript 文件 | 在迁移期间启用 |
| `checkJs` | 对 JavaScript 文件进行类型检查 | 在迁移期间禁用 |
| `noEmit` | 不生成文件（使用外部打包工具） | 对于打包工具启用 `true` |
| `incremental` | 启用逐步编译 | `true`（以加快构建速度） |

## 迁移检查清单

在将 JavaScript 项目迁移到 TypeScript 时：

### 第 1 阶段：设置

- [ ] 安装 TypeScript 和 @types 包
- [ ] 创建具有宽松设置的 `tsconfig.json`
- [ ] 配置构建脚本
- [ ] 设置 IDE/编辑器的 TypeScript 支持

### 第 2 阶段：逐步迁移

- [ ] 启用 `allowJs: true` 和 `checkJs: false`
- [ ] 将实用工具文件重命名为 `.ts`
- [ ] 为函数签名添加类型注释
- [ ] 为数据结构创建接口
- [ ] 修复转换后的文件中的 TypeScript 错误

### 第 3 阶段：加强类型安全

- [ ] 启用 `noImplicitAny: true`
- [ ] 启用 `strictNullChecks: true`
- [ ] 尽可能移除 `any` 类型
- [ ] 为联合类型添加类型保护
- [ ] 为外部模块创建类型定义

### 第 4 阶段：启用严格模式

- [ ] 启用 `strict: true`
- [ ] 修复所有剩余的类型错误
- [ ] 移除 JSDoc 注释（现在它们已经多余）
- [ ] 优化类型定义
- [ ] 记录复杂类型

### 第 5 阶段：维护

- [ ] 设置提交前的类型检查
- [ ] 配置持续集成/持续交付（CI/CD）中的类型检查
- [ ] 建立代码审查标准
- [ ] 保持 TypeScript 和 @types 包的更新

## 参考资料

此技能包含捆绑的参考文档、项目模板和工作流脚本。

### 参考文档（`references/`）

#### 入门与核心概念

- **[typescript-getstarted.md](references/typescript-get-started.md)** - 安装、第一步和 TypeScript 工具设置
- **[typescript-quickstart.md](references/typescript-quickstart.md)** - TypeScript 语法和关键特性的快速介绍
- **[typescript-essentials.md](references/typescript-essentials.md)** - 每个开发者都应该了解的 TypeScript 核心概念
- **[typescript-handbook.md](references/typescript-handbook.md)** - 来自官方 TypeScript 文档的全面手册（已更新）
- **[typescript-cheatsheet.md](references/typescript-cheatsheet.md)** - 控制流、类、类型和常见模式的快速参考（已更新）

#### 类型系统与语言特性

- **[typescript-types.md](references/typescript-types.md)** - 高级类型、条件类型、映射类型、类型保护器和递归类型
- **[typescript-classes.md](references/typescript-classes.md)** - 类语法、继承、泛型和工具类型
- **[typescript-elements.md](references/typescript-elements.md)** - 数组、元组、对象、枚举、函数和类型转换
- **[typescript-keywords.md](references/typescript-keywords.md)** - `keyOf`、`null` 处理、可选链和模板字面量类型
- **[typescript-miscellaneous.md](references/typescript-miscellaneous.md)** - 异步编程、Promise、装饰器和 JSDoc 集成

#### 模块、声明与配置

- **[typescript-module-references.md](references/typescript-module-references.md)** - 模块系统、导入/导出模式和路径解析
- **[typescript-declaration-files.md](references/typescript-declaration-files.md)** - 编写和使用 `.d.ts` 文件
- **[typescript-d.ts-templates.md](references/typescript-d.ts-templates.md)** - 用于常见模式的现成声明文件模板
- **[typescript-with-javascript.md](references/typescript-with-javascript.md)** - 将 TypeScript 与 JavaScript 一起使用、`allowJs` 和 JSDoc 类型
- **[typescript-configuration.md](references/typescript-configuration.md)** - 深入了解 `tsconfig.json` 选项和项目设置
- **[typescript-projects.md](references/typescript-projects.md)** - 项目配置、Node.js 设置、Express 集成、React 和 TypeScript

#### 生态系统与学习资源

- **[typescript-tools.md](references/typescript-tools.md)** - 编辑器、代码检查工具、格式化和构建工具集成
- **[typescript-releases.md](references/typescript-releases.md)** - TypeScript 的版本历史和重要新特性
- **[typescript-tutorials.md](references/typescript-tutorials.md)** - 常见 TypeScript 使用场景的逐步教程
- **[typescript-basics.md](references/typescript-basics.md)** - TypeScript 基础知识、简单类型、类型推断和特殊类型

### 项目模板（`assets/`）

`assets/` 文件夹中包含可用的 TypeScript 项目模板：

- Node.js 库模板（CJS + ESM 双输出）
- React + TypeScript 应用程序模板
- Express + TypeScript API 模板
- 带有 npm 工作区的 TypeScript 单体仓库模板

### 工作流脚本（`scripts/`）

TypeScript 开发的逐步工作流指南和自动化脚本：

- **[scripts/yeoman-typescript-generator.md](scripts/yeoman-typescript-generator.md)** - 创建和发布用于搭建 TypeScript 项目的自定义 Yeoman 生成器。涵盖生成器结构、提示、模板、组合、测试和 npm 发布。
- **[scripts/npm-typescript-workflow.md](scripts/npm-typescript-workflow.md)** - TypeScript 项目的全面 npm 工作流：初始化、必要的 `package.json` 脚本、`@types/*` 管理、使用声明和导出的发布映射、npm 工作区以及安全审计。
- **[scripts/bun-typescript-workflow.md](scripts/bun-typescript-workflow.md)** - 完整的 Bun 运行时工作流：运行 `.ts` 文件而不进行编译、`bun test`、`bun build`、`bun install`、`bunfig.toml` 配置，以及从 Node.js/npm 迁移到 Bun。
- **[scripts/typescript-health-check.md](scripts/typescript-health-check.md)** - TypeScript 项目健康检查，包括类型覆盖率分析、严格模式审计、死代码检测、循环依赖检查、包大小分析、类型性能分析，以及一个自动运行所有检查的 shell 脚本（`health-check.sh`）。

### 外部资源

- [TypeScript 官方文档](https://www.typescriptlang.org/docs/)
- [TypeScript 手册](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript tsconfig 参考](https://www.typescriptlang.org/tsconfig/)
- [TypeScript 深入研究](https://basarat.gitbook.io/typescript/)
- [TypeScript 游戏场](https://www.typescriptlang.org/play) - 在线测试 TypeScript 代码
- [Yeoman 生成器](https://yeoman.io/generators/) - 浏览社区生成器
- [Bun 文档](https://bun.sh/docs) - Bun 运行时参考
- [npm 文档](https://docs.npmjs.com/) - npm CLI 和注册表参考

## 总结

TypeScript 开发技能使你能够利用专家级的 TypeScript 知识编写类型安全的、可维护的代码。无论是迁移现有的 JavaScript 项目还是开始新的 TypeScript 项目，都可以应用这些经过验证的模式、工作流和最佳实践，自信地交付高质量的代码。

此技能现在包括：
- **超过 13 个参考文件**的扩展参考资料，涵盖整个 TypeScript 生态系统
- `assets/` 文件夹中的项目模板，适用于常见的 TypeScript 项目类型
- **工作流脚本**，用于项目搭建（Yeoman）、包管理（npm 和 Bun）和自动化健康检查

**记住**：TypeScript 是提高开发效率和代码质量的工具。利用它来尽早发现错误、改进代码文档，并提升工具支持——但不要让完美的类型阻碍代码的交付。