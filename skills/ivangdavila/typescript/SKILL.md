---
name: TypeScript
description: 避免常见的 TypeScript 错误——比如类型泄漏、类型推断失败以及类型范围变窄的问题。
metadata: {"clawdbot":{"emoji":"🔷","requires":{"bins":["tsc"]},"os":["linux","darwin","win32"]}}
---

## 停止使用 `any`  
- `unknown` 强制你在使用前明确指定类型；而 `any` 会默默地破坏类型安全性。  
- 对于 API 返回值，要么指定具体类型，要么使用 `unknown`，绝不要使用 `any`。  
- 当你不知道类型时，应该使用 `unknown`，而不是 `any`。  

## 类型限定失败的情况  
- `filter(Boolean)` 并不能真正限定类型；应使用 `.filter((x): x is T => Boolean(x))` 来明确类型。  
- `Object.keys(obj)` 返回的是 `string[]`，而不是 `keyof typeof obj`——这是有意为之，因为对象可能包含额外的键。  
- `Array.isArray()` 会将类型限定为 `any[]`；可能需要额外的断言来确认元素的类型。  
- `in` 运算符虽然可以限定类型，但仅当属性存在于联合类型（union type）的某个特定分支中时才有效。  

## 字面量类型的陷阱  
- `let x = "hello";` 的类型是 `string`；对于字面量类型，应使用 `const` 或 `as const`。  
- 对象的属性类型是可变的：`{ status: "ok" }` 中的 `status` 类型是 `string`；应使用 `as const` 或类型注解来明确类型。  
- 函数的返回类型也是可变的；对于字面量返回值，需要明确进行类型注解。  

## 类型推断的限制  
- 在某些数组方法中，回调函数的类型无法被自动推断；当 TypeScript 推断错误时，需要手动为参数添加类型注解。  
- 泛型函数需要通过实际使用来推断类型；`fn<T>()` 无法自动推断类型，需要传递一个值或手动添加类型注解。  
- 嵌套泛型通常会导致类型推断失败；应通过显式类型来解决问题。  

## 区分性联合类型（Discriminated Unions）  
- 为每个联合类型变体添加 `type` 或 `kind` 字段，以便进行全面的类型检查。  
- 使用 `default: const _never: never = x` 来确保所有情况都被覆盖；如果遗漏了某个情况，编译器会报错。  
- 不要将区分性联合类型与可选属性混合使用，否则会导致类型限定失败。  

## `satisfies` 与类型注解的区别  
- `const x: Type = val` 会将类型泛化，从而丢失字面量信息；  
- `const x = val satisfies Type` 可以保留字面量类型，并检查兼容性——适用于配置对象。  

## 关于严格空值的注意事项  
- 可选链操作 `?.` 返回的是 `undefined`，而不是 `null`；这对于期望接收 `null` 的 API 来说很重要。  
- `??` 只能捕获 `null` 或 `undefined`；`||` 则会捕获所有假值（包括 `0` 和 `""`）。  
- 非空值判断（`!`）应该是最后的手段；优先使用类型限定或提前返回错误。  

## 模块边界相关的问题  
- 对于仅用于导入类型的变量，应使用 `import type`；这样在运行时类型信息会被剥离，避免打包工具（bundleer）出现问题。  
- 重新导出类型时，应使用 `export type { X }` 来防止运行时产生不必要的依赖。  
- 使用 `.d.ts` 文件进行类型增强时，需要使用 `declare module` 并指定模块路径。