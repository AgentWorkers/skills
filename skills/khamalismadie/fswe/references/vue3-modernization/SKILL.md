# Vue 3 现代化改造

## 组合式 API（Composition API）

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// Reactive state
const count = ref(0)
const users = ref<User[]>([])

// Computed
const doubleCount = computed(() => count.value * 2)

// Methods
function increment() {
  count.value++
}

// Lifecycle
onMounted(async () => {
  users.value = await fetchUsers()
})
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Double: {{ doubleCount }}</p>
    <button @click="increment">Add</button>
  </div>
</template>
```

## 状态管理（Pinia）

```typescript
// stores/user.ts
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false,
  }),
  
  getters: {
    userName: (state) => state.user?.name ?? 'Guest',
  },
  
  actions: {
    async login(credentials: Credentials) {
      const user = await api.login(credentials)
      this.user = user
      this.isAuthenticated = true
    },
    
    logout() {
      this.user = null
      this.isAuthenticated = false
    },
  },
})
```

## 组件架构

```
components/
├── Base/          # Button, Input, Card
├── Layout/        # Header, Sidebar, Footer
├── Features/      # Feature-specific components
└── Shared/        # Reusable across features
```

## 检查清单

- [ ] 迁移至组合式 API
- [ ] 配置 Pinia 进行状态管理
- [ ] 实现组合式函数（composables）
- [ ] 添加 TypeScript 支持
- [ ] 配置 Vue Router
- [ ] 实现代码拆分（code splitting）