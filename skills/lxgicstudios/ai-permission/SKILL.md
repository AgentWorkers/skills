---
name: permission-gen
description: 生成基于角色的权限系统
---

# 权限生成器

本工具用于描述用户的角色和资源，并实现完整的角色基于角色的访问控制（RBAC）功能。

## 快速入门

```bash
npx ai-permission "Admin, Editor, Viewer roles for posts and comments"
```

## 功能概述

- 生成权限常量  
- 创建角色层级结构  
- 构建权限检查函数  
- 提供中间件支持  

## 使用示例

```bash
# Generate from description
npx ai-permission "Team admin, member, guest for projects and tasks"

# Generate with specific framework
npx ai-permission "roles for e-commerce" --framework express

# Output as module
npx ai-permission "admin system" --out ./src/lib/permissions.ts
```

## 输出内容

- 权限枚举常量  
- 角色定义  
- `hasPermission()` 函数  
- 适用于 Express/Next.js 的中间件  
- TypeScript 类型定义  

## 示例输出

```typescript
export const Permissions = {
  POSTS_CREATE: 'posts:create',
  POSTS_READ: 'posts:read',
  POSTS_UPDATE: 'posts:update',
  POSTS_DELETE: 'posts:delete',
} as const;

export const Roles = {
  ADMIN: [Permissions.POSTS_CREATE, ...],
  EDITOR: [Permissions.POSTS_UPDATE, ...],
};
```

## 系统要求

- 必需安装 Node.js 18 及更高版本。  
- 需要配置 OPENAI_API_KEY。  

## 许可证

采用 MIT 许可协议，永久免费使用。  

---

**开发团队：LXGIC Studios**

- GitHub 仓库：[github.com/lxgicstudios/ai-permission](https://github.com/lxgicstudios/ai-permission)  
- Twitter 账号：[@lxgicstudios](https://x.com/lxgicstudios)