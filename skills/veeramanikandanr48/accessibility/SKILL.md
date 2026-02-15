---
name: accessibility
description: |
  Build WCAG 2.1 AA compliant websites with semantic HTML, proper ARIA, focus management, and screen reader support. Includes color contrast (4.5:1 text), keyboard navigation, form labels, and live regions.

  Use when implementing accessible interfaces, fixing screen reader issues, keyboard navigation, or troubleshooting "focus outline missing", "aria-label required", "insufficient contrast".
---

# 网页无障碍（WCAG 2.1 AA）

**状态**: 已准备好投入生产 ✅  
**最后更新**: 2026-01-14  
**依赖项**: 无（与框架无关）  
**标准**: WCAG 2.1 AA  

---

## 快速入门（5分钟）  

### 1. 语义化HTML基础  

选择正确的元素——不要滥用`<div>`：  
```html
<!-- ❌ WRONG - divs with onClick -->
<div onclick="submit()">Submit</div>
<div onclick="navigate()">Next page</div>

<!-- ✅ CORRECT - semantic elements -->
<button type="submit">Submit</button>
<a href="/next">Next page</a>
```  

**重要性**:  
- 语义化元素具有内置的键盘导航支持；  
- 屏幕阅读器可以自动识别元素的用途；  
- 浏览器会提供默认的无障碍行为。  

### 2. 焦点管理  

确保交互式元素可通过键盘访问：  
```css
/* ❌ WRONG - removes focus outline */
button:focus { outline: none; }

/* ✅ CORRECT - custom accessible outline */
button:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}
```  

**关键点**:  
- 绝不要移除焦点轮廓，除非有替代方案；  
- 使用`:focus-visible`属性仅在键盘聚焦时显示元素；  
- 确保焦点指示器的对比度达到3:1。  

### 3. 文本替代内容  

每个非文本元素都需要有文本替代内容：  
```html
<!-- ❌ WRONG - no alt text -->
<img src="logo.png">
<button><svg>...</svg></button>

<!-- ✅ CORRECT - proper alternatives -->
<img src="logo.png" alt="Company Name">
<button aria-label="Close dialog"><svg>...</svg></button>
```  

---

## 五步无障碍实现流程  

### 第1步：选择语义化HTML  

**元素选择指南**:  
```
Need clickable element?
├─ Navigates to another page? → <a href="...">
├─ Submits form? → <button type="submit">
├─ Opens dialog? → <button aria-haspopup="dialog">
└─ Other action? → <button type="button">

Grouping content?
├─ Self-contained article? → <article>
├─ Thematic section? → <section>
├─ Navigation links? → <nav>
└─ Supplementary info? → <aside>

Form element?
├─ Text input? → <input type="text">
├─ Multiple choice? → <select> or <input type="radio">
├─ Toggle? → <input type="checkbox"> or <button aria-pressed>
└─ Long text? → <textarea>
```  
**详细指南请参阅`references/semantic-html.md`。**  

### 第2步：必要时使用ARIA  

**黄金法则**: 仅在HTML无法表达所需功能时使用ARIA。  
```html
<!-- ❌ WRONG - unnecessary ARIA -->
<button role="button">Click me</button>  <!-- Button already has role -->

<!-- ✅ CORRECT - ARIA fills semantic gap -->
<div role="dialog" aria-labelledby="title" aria-modal="true">
  <h2 id="title">Confirm action</h2>
  <!-- No HTML dialog yet, so role needed -->
</div>

<!-- ✅ BETTER - Use native HTML when available -->
<dialog aria-labelledby="title">
  <h2 id="title">Confirm action</h2>
</dialog>
```  
**常见ARIA属性示例**:  
- `aria-label`：用于没有可见标签的元素；  
- `aria-labelledby`：引用现有文本作为标签；  
- `aria-describedby`：提供额外说明；  
- `aria-live`：用于通知动态内容更新；  
- `aria-expanded`：用于表示可折叠/展开的状态。  
**完整指南请参阅`references/aria-patterns.md`。**  

### 第3步：实现键盘导航  

所有交互式元素都必须可通过键盘访问：  
```typescript
// Tab order management
function Dialog({ onClose }) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const previousFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    // Save previous focus
    previousFocus.current = document.activeElement as HTMLElement;

    // Focus first element in dialog
    const firstFocusable = dialogRef.current?.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    (firstFocusable as HTMLElement)?.focus();

    // Trap focus within dialog
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
      if (e.key === 'Tab') {
        // Focus trap logic here
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      // Restore focus on close
      previousFocus.current?.focus();
    };
  }, [onClose]);

  return <div ref={dialogRef} role="dialog">...</div>;
}
```  
**常用键盘操作**:  
- Tab/Shift+Tab：在可聚焦元素间切换；  
- Enter/Space：激活按钮/链接；  
- 方向键：在组件内导航（如标签页、菜单）；  
- Escape：关闭对话框/菜单；  
- Home/End：跳转到页面的首/末项。  
**详细指南请参阅`references/focus-management.md`。**  

### 第4步：确保颜色对比度  

**WCAG AA要求**:  
- 普通文本（小于18号字体）：对比度≥4.5:1；  
- 大字体文本（18号或更粗的字体）：对比度≥3:1；  
- 用户界面元素（如按钮、边框）：对比度≥3:1。  
```css
/* ❌ WRONG - insufficient contrast */
:root {
  --background: #ffffff;
  --text: #999999;  /* 2.8:1 - fails WCAG AA */
}

/* ✅ CORRECT - sufficient contrast */
:root {
  --background: #ffffff;
  --text: #595959;  /* 4.6:1 - passes WCAG AA */
}
```  
**测试工具**:  
- 浏览器开发者工具（Chrome/Firefox内置检查工具）；  
- 对比度检查插件；  
- axe开发者工具。  
**详细指南请参阅`references/color-contrast.md`。**  

### 第5步：使表单可访问  

每个表单输入字段都需要有可见的标签：  
```html
<!-- ❌ WRONG - placeholder is not a label -->
<input type="email" placeholder="Email address">

<!-- ✅ CORRECT - proper label -->
<label for="email">Email address</label>
<input type="email" id="email" name="email" required aria-required="true">
```  
**错误处理**:  
```html
<label for="email">Email address</label>
<input
  type="email"
  id="email"
  name="email"
  aria-invalid="true"
  aria-describedby="email-error"
>
<span id="email-error" role="alert">
  Please enter a valid email address
</span>
```  
**动态错误的提示**:  
```html
<div role="alert" aria-live="assertive" aria-atomic="true">
  Form submission failed. Please fix the errors above.
</div>
```  
**详细指南请参阅`references/forms-validation.md`。**  

---

## 关键规则  

### 必须遵守的规则  

✅ 首先使用语义化HTML元素（如`<button>`、`<a>`、`<nav>`、`<article>`等）；  
✅ 为所有非文本内容提供文本替代内容；  
✅ 确保普通文本的对比度达到4.5:1，大字体文本的对比度达到3:1；  
✅ 使所有功能均可通过键盘访问；  
✅ 仅使用键盘进行测试（禁用鼠标）；  
✅ 使用屏幕阅读器进行测试（Windows使用NVDA，Mac使用VoiceOver）；  
✅ 使用正确的标题层级（h1 → h2 → h3，不得跳过层级）；  
✅ 为所有表单输入字段添加可见的标签；  
✅ 为动态内容使用`aria-live`属性。  

### 绝对不能做的规则  

❌ 不要用`<div>`代替`<button>`并设置`onClick`属性；  
❌ 移除焦点轮廓后不提供替代方案；  
❌ 仅使用颜色来传达信息；  
❌ 用占位符作为标签；  
❌ 跳过标题层级（h1 → h3）；  
❌ 在存在语义化HTML元素的情况下仍使用`aria`属性；  
❌ 关闭对话框后不恢复焦点；  
❌ 为可聚焦元素设置`role="presentation"`。  

---

## 常见问题的预防  

遵循这些规则可以避免12种常见的无障碍问题：  

### 问题1：缺少焦点指示器  

**错误**: 交互式元素没有可见的焦点指示器  
**来源**: WCAG 2.4.7（Focus Visible）  
**原因**: CSS样式重置移除了默认的焦点轮廓  
**预防措施**: 始终为元素添加自定义的`:focus-visible`样式。  

### 问题2：颜色对比度不足  

**错误**: 文本的对比度低于4.5:1  
**来源**: WCAG 1.4.3（Contrast Minimum）  
**原因**: 使用浅灰色文本在白色背景上  
**预防措施**: 使用对比度检查工具测试所有文本的颜色。  

### 问题3：缺少alt文本  

**错误**: 图片没有`alt`属性  
**来源**: WCAG 1.1.1（Non-text Content）  
**原因**: 忘记添加`alt`属性，或认为它是可选的  
**预防措施**: 为装饰性图片添加`alt="""`，为有意义的图片添加描述性`alt`文本。  

### 问题4：键盘导航失效  

**错误**: 交互式元素无法通过键盘访问  
**来源**: WCAG 2.1.1（Keyboard）  
**原因**: 使用`<div>`的`onClick`属性代替`<button>`  
**预防措施**: 使用语义化的交互元素（如`<button>`、`<a>`）。  

### 问题5：表单输入字段没有标签  

**错误**: 输入字段没有关联的标签  
**来源**: WCAG 3.3.2（Labels or Instructions）  
**原因**: 使用占位符作为标签  
**预防措施**: 必须使用`<label>`元素，并将其`for`属性与输入字段关联。  

### 问题6：标题层级混乱  

**错误**: 页面的标题层级跳跃（例如从h1直接跳到h3）  
**原因**: 仅为了视觉样式而使用标题，而非根据语义结构  
**预防措施**: 按正确的顺序使用标题，并使用CSS进行样式设置。  

### 问题7：对话框中没有焦点陷阱  

**错误**: 使用Tab键时用户会跳转到背景页面  
**原因**: 未实现焦点陷阱  
**预防措施**: 为模态对话框实现焦点陷阱。  

### 问题8：动态内容没有`aria-live`属性  

**错误**: 屏幕阅读器无法通知动态内容的更新  
**来源**: WCAG 4.1.3（Status Messages）  
**原因**: 动态内容添加时未使用`aria-live`属性  
**预防措施**: 使用`aria-live="polite"`或`aria-live="assertive"`。  

### 问题9：仅使用颜色传达信息  

**错误**: 仅通过颜色显示状态信息  
**原因**: 错误信息仅用颜色显示，没有图标或文字说明  
**预防措施**: 添加图标和文字标签。  

### 问题10：链接文本缺乏描述性  

**错误**: 链接文本过于通用（如“点击这里”或“阅读更多”）  
**来源**: WCAG 2.4.4（Link Purpose）  
**原因**: 链接文本缺乏描述性  
**预防措施**: 使用描述性的链接文本或`aria-label`属性。  

### 问题11：自动播放媒体  

**错误**: 媒体自动播放，用户无法控制  
**来源**: WCAG 1.4.2（Audio Control）  
**原因**: 媒体自动播放时没有用户交互机制  
**预防措施**: 强制用户手动触发媒体播放。  

### 问题12：自定义控件不可访问  

**错误**: 自定义的选择框/复选框无法通过键盘操作  
**原因**: 未使用`aria`属性  
**预防措施**: 使用原生元素或完整的ARIA模式实现自定义控件。  

---

## WCAG 2.1 AA快速检查清单  

### 可感知性（Perceivable）  
- 所有图片都有`alt`文本（装饰性图片使用`alt="""`）；  
- 文本对比度≥4.5:1（普通文本），≥3:1（大字体文本）；  
- 不仅使用颜色来传达信息；  
- 文本可以放大到200%而不丢失内容；  
- 没有自动播放时长超过3秒的音频。  

### 可操作性（Operable）  
- 所有功能均可通过键盘访问；  
- 不存在键盘导航陷阱；  
- 具有可见的焦点指示器；  
- 用户可以暂停/停止/隐藏动态内容；  
- 页面标题能清晰说明页面用途；  
- 焦点切换顺序合理；  
- 链接的用途从文本或上下文中可以明确了解；  
- 有多种方式可以找到页面（菜单、搜索、站点地图）；  
- 标题和标签能清晰说明内容用途。  

### 可理解性（Understandable）  
- 页面语言已明确指定（`<html lang="en">`）；  
- 语言切换有明确提示（`<span lang="es">`）；  
- 焦点或输入操作不会导致意外的上下文变化；  
- 网站内的导航一致；  
- 提供表单标签和说明；  
- 输入错误有提示和解释；  
- 对法律/财务/数据相关的更改有错误提示。  

### 健壮性（Robust）  
- HTML代码有效（无解析错误）；  
- 所有用户界面元素都有名称、角色和值；  
- 状态信息有明确的`aria-live`属性。  

---

## 测试流程  

### 1. 仅使用键盘的测试（5分钟）  
```
1. Unplug mouse or hide cursor
2. Tab through entire page
   - Can you reach all interactive elements?
   - Can you activate all buttons/links?
   - Is focus order logical?
3. Use Enter/Space to activate
4. Use Escape to close dialogs
5. Use arrow keys in menus/tabs
```  

### 2. 使用屏幕阅读器的测试（10分钟）  

**NVDA（Windows - 免费）**:  
- 下载：https://www.nvaccess.org/download/  
- 启动：Ctrl+Alt+N  
- 导航：使用方向键或Tab键；  
- 阅读内容：NVDA+Down箭头；  
- 停止：NVDA+Q  

**VoiceOver（Mac - 内置）**:  
- 启动：Cmd+F5  
- 导航：使用VO+Right/Left箭头；  
- 阅读内容：VO+A；  
- 停止：Cmd+F5  

**测试内容**:  
- 所有交互式元素是否被正确读取？  
- 图片是否有描述？  
- 表单标签和输入字段是否被正确读取？  
- 动态内容更新是否被通知？  
- 标题结构是否清晰？  

### 3. 自动化测试  

**axe开发者工具**（强烈推荐）:  
- 安装：Chrome/Firefox扩展程序；  
- 运行：F12 → 打开axe开发者工具 → 进行扫描；  
- 修复问题后重新扫描；  
- 修复后再次测试。  

**Lighthouse**（Chrome内置工具）:  
- 打开开发者工具（F12） → 选择“Accessibility”类别；  
- 生成报告；  
- 分数90分以上表示良好，100分为理想状态。  

---

## 常见的无障碍实现模式  

### 模式1：可访问的对话框/模态窗口  

**适用场景**: 任何会阻挡用户与背景内容交互的模态窗口或覆盖层。  

### 模式2：可访问的标签页  

**适用场景**: 具有多个标签页的界面。  

### 模式3：跳过链接的导航  

**适用场景**: 所有多页面网站，且导航栏位于主要内容之前。  

### 模式4：具有验证功能的可访问表单  

**适用场景**: 所有需要验证的表单。  

---

## 使用相关资源  

### 参考资料（references/）  

- **wcag-checklist.md**: 完整的WCAG 2.1 A级和AA级要求及示例；  
- **semantic-html.md**: 元素选择指南；  
- **aria-patterns.md**: ARIA属性的使用方法；  
- **focus-management.md**: 焦点顺序、焦点陷阱和恢复机制；  
- **color-contrast.md**: 对比度要求、测试工具和颜色搭配建议；  
- **forms-validation.md**: 表单的可访问性实现、错误处理和提示信息。  

**何时需要使用这些资源**:  
- 用户需要完整的WCAG检查清单；  
- 需要深入了解特定无障碍实现模式（如标签页、折叠式菜单等）；  
- 需要解决颜色对比度问题或进行颜色搭配设计；  
- 需要处理复杂的表单验证场景。  

### 无障碍审计工具  

- **a11y-auditor.md**: 自动化无障碍审计工具，用于检查页面的合规性。  
**适用场景**: 需要对现有页面或组件进行无障碍审计。  

---

## 高级主题  

### ARIA Live Regions  

**三种提示级别**:  
```html
<!-- Polite: Wait for screen reader to finish current announcement -->
<div aria-live="polite">New messages: 3</div>

<!-- Assertive: Interrupt immediately -->
<div aria-live="assertive" role="alert">
  Error: Form submission failed
</div>

<!-- Off: Don't announce (default) -->
<div aria-live="off">Loading...</div>
```  
**最佳实践**:  
- 对于非关键性的更新（如通知、计数器）使用`aria-live="polite"`；  
- 对于错误或重要提示使用`aria-live="assertive"`；  
- 使用`aria-atomic="true"`在内容更新时显示整个区域；  
- 保持提示信息简洁明了。  

### SPA中的焦点管理  

React Router在导航时不会自动恢复焦点——需要手动处理：  
```typescript
function App() {
  const location = useLocation();
  const mainRef = useRef<HTMLElement>(null);

  useEffect(() => {
    // Focus main content on route change
    mainRef.current?.focus();
    // Announce page title to screen readers
    const title = document.title;
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.textContent = `Navigated to ${title}`;
    document.body.appendChild(announcement);
    setTimeout(() => announcement.remove(), 1000);
  }, [location.pathname]);

  return <main ref={mainRef} tabIndex={-1} id="main-content">...</main>;
}
```  

### 可访问的数据表格  

**关键属性**:  
- `<caption>`：描述表格的用途；  
- `scope="col"`：标识列标题；  
- `scope="row"`：标识行标题；  
- 使用`scope`属性帮助屏幕阅读器理解数据单元格与标题的关系。  

---

## 官方文档  

- **WCAG 2.1**: https://www.w3.org/WAI/WCAG21/quickref/  
- **MDN无障碍指南**: https://developer.mozilla.org/en-US/docs/Web/Accessibility  
- **ARIA编写指南**: https://www.w3.org/WAI/ARIA/apg/  
- **WebAIM**: https://webaim.org/articles/  
- **axe开发者工具**: https://www.deque.com/axe/devtools/  

---

## 故障排除  

### 问题：焦点指示器不可见  

**症状**: 可以使用Tab键导航，但看不到焦点位置  
**原因**: CSS样式移除了焦点轮廓或对比度不足  
**解决方法**: 为相关元素添加`:focus-visible`属性。  

### 问题：屏幕阅读器无法通知更新  

**症状**: 动态内容发生变化但屏幕阅读器没有提示  
**原因**: 未为动态内容添加`aria-live`属性  
**解决方法**: 将动态内容包裹在`<div aria-live="polite">`中，或使用`role="alert"`。  

### 问题：对话框中的焦点会跳转到背景页面  

**症状**: 使用Tab键时用户会跳转到对话框后面的内容  
**原因**: 未实现焦点陷阱  
**解决方法**: 为对话框实现焦点陷阱。  

### 问题：表单错误未得到提示  

**症状**: 动态错误出现但屏幕阅读器未通知  
**原因**: 未为错误信息添加`aria-invalid`属性或`role="alert"`  
**解决方法**: 为错误信息添加`aria-invalid`和`aria-description`属性，并设置`role="alert"`。  

---

## 完整的设置检查清单  

确保每个页面和组件都符合以下要求：  
- 所有交互式元素均可通过键盘访问；  
- 所有可聚焦元素都有可见的焦点指示器；  
- 图片都有`alt`文本（装饰性图片使用`alt="""`）；  
- 文本对比度≥4.5:1（使用axe或Lighthouse工具测试）；  
- 表单输入字段都有关联的标签；  
- 标题层级清晰（无层级跳跃）；  
- 页面使用`<html lang="en">`指定语言；  
- 对话框具有焦点陷阱，并在关闭时恢复焦点；  
- 动态内容使用`aria-live`或`role="alert"`；  
- 不仅使用颜色来传达信息；  
- 仅使用键盘进行测试；  
- 使用屏幕阅读器进行测试；  
- 使用axe开发者工具进行扫描（无违规项）；  
- Lighthouse无障碍评分≥90分。  

---

**有问题或需要帮助吗？**  
1. 查阅`references/wcag-checklist.md`获取完整要求；  
2. 使用`a11y-auditor`工具检查页面；  
3. 使用axe开发者工具进行自动化测试；  
4. 使用键盘和屏幕阅读器进行实际测试。  

**标准**: WCAG 2.1 AA  
**测试工具**: axe开发者工具、Lighthouse、NVDA、VoiceOver  
**成功标准**: Lighthouse评分≥90分，且无严重违规项。