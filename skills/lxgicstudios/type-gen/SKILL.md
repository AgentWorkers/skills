---
name: JSON to TypeScript - Interface Generator
description: **从 JSON 数据或 API 响应生成 TypeScript 接口**  
这款工具能够自动为你的 API 生成 TypeScript 接口定义。专为 TypeScript 开发者设计的免费命令行工具（CLI）。
---

# 将 JSON 转换为 TypeScript

该工具能够从 JSON 文件自动生成 TypeScript 接口，从而免去手动编写类型定义的麻烦。

## 安装

```bash
npm install -g @lxgicstudios/json-to-ts
```

## 命令

### 从文件读取数据：

```bash
npx @lxgicstudios/json-to-ts data.json
npx @lxgicstudios/json-to-ts response.json -n User
```

### 从 URL 读取数据：

```bash
npx @lxgicstudios/json-to-ts https://api.example.com/users -n User
```

### 通过管道（pipe）传递数据：

```bash
curl https://api.example.com/data | npx @lxgicstudios/json-to-ts -n ApiResponse
```

### 将结果写入文件：

```bash
npx @lxgicstudios/json-to-ts api.json -o src/types/api.ts
```

## 示例

输入 JSON 数据：
```json
{
  "id": 1,
  "name": "John",
  "email": "john@example.com",
  "address": { "city": "NYC" },
  "tags": ["dev", "ts"]
}
```

输出 TypeScript 接口代码：
```typescript
export interface Address {
  city: string;
}

export interface Root {
  id: number;
  name: string;
  email: string;
  address: Address;
  tags: string[];
}
```

## 选项

| 选项          | 描述                                      |
|-----------------|-----------------------------------------|
| `-n, --name`     | 根接口的名称（默认值：Root）                        |
| `-o, --output`    | 将结果写入文件                              |
| `-t, --type`     | 使用 `type` 而不是 `interface`                    |
| `--optional`    | 将所有属性设置为可选                         |
| `--no-export`    | 不添加 `export` 关键字                         |

## 主要功能

- 嵌套对象会被转换为独立的接口             |
- 数组会被正确地赋予类型定义                 |
- 混合类型的数组会被转换为联合类型（union types）       |
- 可以直接从 URL 获取数据                   |
- 空数组会被处理为 `unknown[]`                   |

## 常见使用场景

- 为 API 响应生成类型定义             |
- 为整个项目生成类型定义                   |

---

**由 [LXGIC Studios](https://lxgicstudios.com) 开发**

🔗 [GitHub](https://github.com/lxgicstudios/json-to-ts) · [Twitter](https://x.com/lxgicstudios)