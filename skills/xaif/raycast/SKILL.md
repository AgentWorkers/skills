---
name: raycast-extensions
description: 使用 Raycast API 构建和维护 Raycast 扩展程序。这些扩展程序可以响应 @raycast/api、List、Grid、Detail、Form、AI.ask、LocalStorage、Cache、.showToast 和 BrowserExtension 等事件。请以该仓库中的 references/api/*.md 文件作为组件规格和 API 使用方式的主要参考资料。
---

# Raycast扩展技能

使用React、TypeScript和Raycast API构建强大的扩展功能。

## 快速入门（代理工作流程）

在实现或修复Raycast功能时，请按照以下步骤操作：

1. **确定核心组件**：判断用户界面需要使用`List`、`Grid`、`Detail`还是`Form`组件。
2. **查阅参考文档**：打开并阅读`references/api/`目录下的相应文件（例如`references/api/list.md`）。
3. **使用默认设置**：
    - **反馈提示**：使用`showToast`来显示加载中、成功或失败的信息；仅在需要快速显示背景状态时使用`showHUD`。
    - **数据存储**：使用`Cache`来存储频繁访问或临时性的数据，使用`LocalStorage`来存储持久化的用户数据。
    - **权限检查**：在使用任何功能之前，务必检查`environment.canAccess(AI)`或`environment.canAccess(BrowserExtension)`。
4. **实现逻辑**：使用`@raycast/api`组件来编写简洁的实现代码。
5. **引用来源**：在代码中明确引用所使用的具体`references/api/*.md`文件。

## 常用模板模式

### 1. 列表与网格（可搜索的用户界面）
- 使用`List`显示文本较多的数据，使用`Grid`显示图片较多的数据。
  - [List参考文档](references/api/list.md) | [Grid参考文档](references/api/grid.md)

```tsx
<List isLoading={isLoading} searchBarPlaceholder="Search items..." throttle>
  <List.Item
    title="Item Title"
    subtitle="Subtitle"
    accessories={[{ text: "Tag" }]}
    actions={
      <ActionPanel>
        <Action.Push title="View Details" target={<Detail markdown="# Details" />} />
        <Action.CopyToClipboard title="Copy" content="value" />
      </ActionPanel>
    }
  />
</List>
```

### 2. 详情页面（富格式Markdown）
- 用于显示长篇内容或项目详情。
  - [详情页面参考文档](references/api/detail.md)

```tsx
<Detail
  isLoading={isLoading}
  markdown="# Heading\nContent here."
  metadata={
    <Detail.Metadata>
      <Detail.Metadata.Label title="Status" text="Active" icon={Icon.Checkmark} />
    </Detail.Metadata>
  }
/>
```

### 3. 表单（用户输入）
- 必须包含`SubmitForm`操作按钮。
  - [表单参考文档](references/api/form.md)

```tsx
<Form
  actions={
    <ActionPanel>
      <Action.SubmitForm onSubmit={(values) => console.log(values)} />
    </ActionPanel>
  }
>
  <Form.TextField id="title" title="Title" placeholder="Enter title" />
  <Form.TextArea id="description" title="Description" />
</Form>
```

### 4. 反馈与交互
- 对于大多数反馈提示，建议使用`showToast`。
  - [Toast参考文档](references/api/toast.md) | [HUD参考文档](references/api/hud.md)

```typescript
// Success/Failure
await showToast({ style: Toast.Style.Success, title: "Success!" });

// HUD (Overlay)
await showHUD("Done!");
```

### 5. 数据持久化
- 使用`Cache`提升性能，使用`LocalStorage`实现数据持久化。
  - [缓存参考文档](references/api/caching.md) | [存储参考文档](references/api/storage.md)

```typescript
// Cache (Sync/Transient)
const cache = new Cache();
cache.set("key", "value");

// LocalStorage (Async/Persistent)
await LocalStorage.setItem("key", "value");
```

### 6. 人工智能与浏览器扩展（受限API）
- 在使用相关API之前，务必进行`environment.canAccess`权限检查。
  - [人工智能相关API](references/api/ai.md) | [浏览器扩展相关API](references/api/browser-extension.md)

## 额外资源

### API参考目录

- **用户界面组件**
  - [操作面板](references/api/action-panel.md)
  - [详情页面](references/api/detail.md)
  - [表单](references/api/form.md)
  - [网格](references/api/grid.md)
  - [列表](references/api/list.md)
  - [用户界面](references/api/user-interface.md)
- **交互功能**
  - [操作](references/api/actions.md)
  - [警告提示](references/api/alert.md)
  - [键盘操作](references/api/keyboard.md)
  - [导航](references/api/navigation.md)
  - [Raycast窗口搜索栏](references/api/raycast-window-search-bar.md)
- **实用工具与服务**
  - [人工智能](references/api/ai.md)
  - [浏览器扩展](references/api/browser-extension.md)
  - [剪贴板](references/api/clipboard.md)
  - [环境管理](references/api/environment.md)
  - **反馈与HUD**：
    - [HUD](references/api/hud.md)
    - [Toast](references/api/toast.md)
  - [OAuth](references/api/oauth.md)
  - [系统工具](references/api/system-utilities.md)
- **数据与配置**
  - [缓存](references/api/caching.md)
  - [颜色设置](references/api/colors.md)
  - [图标与图片](references/api/icons-images.md)
  - [偏好设置](references/apipreferences.md)
  - [存储](references/api/storage.md)
- **高级功能**
  - [命令相关工具](references/api/command-related-utilities.md)
  - [菜单栏命令](references/api/menu-bar-commands.md)
  - [工具](references/api/tool.md)
  - [窗口管理](references/api/window-management.md)

## 示例

有关结合多个组件和API的端到端示例，请参阅[examples.md](examples.md)。