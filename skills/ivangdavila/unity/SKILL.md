---
name: Unity
description: 避免常见的 Unity 错误：生命周期顺序、GetComponent 的缓存机制、物理计算的时机控制，以及 Unity 中的“假 null”（即看似为 null 但实际上并非 null 的对象）。
metadata: {"clawdbot":{"emoji":"🎮","os":["linux","darwin","win32"]}}
---

## 生命周期顺序  
- `Awake` 在 `Start` 之前执行：使用 `Awake` 进行自我初始化，使用 `Start` 进行跨脚本引用。  
- `OnEnable` 在 `Start` 之前执行，但在 `Awake` 之后执行。  
- 脚本之间的执行顺序无法保证；如有需要，请使用 `Script Execution Order`。  
- 即使组件被禁用，`Awake` 仍会被调用；`Start` 仅在组件启用时才会执行。  

## 获取组件的性能优化  
- 每帧都调用 `GetComponent` 会降低性能：可以在 `Awake` 或 `Start` 中缓存组件。  
- `GetComponentInChildren` 会递归搜索组件，对于层次结构较深的场景来说效率较低。  
- `TryGetComponent` 返回布尔值，可以避免空指针检查，从而略微提高性能。  
- 使用 `RequireComponent` 属性可以确保组件依赖关系得到满足，并在文档中明确说明这一要求。  

## 物理引擎的时机选择  
- 物理计算在 `FixedUpdate` 中进行，而非 `Update` 中：这样可以保证在不同帧率下计算结果的一致性。  
- `FixedUpdate` 可能每帧执行0次或多次；不要假设它总是每帧执行一次。  
- 应使用 `Rigidbody.MovePosition` 在 `FixedUpdate` 中进行位置更新，因为 `transform.position` 会绕过物理引擎的计算。  
- 在 `Update` 中使用 `Time.deltaTime`，在 `FixedUpdate` 中使用 `Time.fixedDeltaTime`；或者直接使用 `DeltaTime`。  

## Unity 中的“假空值”问题  
- 被销毁的对象并不会真正变成 `null`——使用 `== null` 时会返回 `true`，但该对象仍然存在。  
- 基于 `null` 的条件运算（如 `?.`）可能无法正确工作；应使用 `== null` 或进行布尔值转换。  
- `Destroy` 操作不会立即生效，对象会在下一帧才被彻底销毁。  
- 仅在编辑器中使用 `DestroyImmediate`，因为它可能在构建过程中引发问题。  

## 协程（Coroutines）  
- 调用 `StartCoroutine` 时，对应的 `MonoBehaviour` 必须处于活动状态；如果 `MonoBehaviour` 被禁用或销毁，协程也会停止执行。  
- `yield return null` 会等待一帧后再继续执行；`yield return new WaitForSeconds(1)` 可用于等待指定时间。  
- 调用 `StopCoroutine` 时，需要提供相同的 `MonoBehaviour` 或协程引用；字符串形式的 `StopCoroutine` 方法不可靠。  
- 协程无法返回值，应使用回调函数或修改相关字段来实现数据传递。  

## 实例化与对象池（Instantiation and Pooling）  
- `Instantiate` 操作较为耗时，应尽量复用频繁创建和销毁的对象。  
- 使用 `Instantiate(prefab, parent)` 可设置组件的父对象，从而避免额外的 `SetParent` 调用。  
- 在将对象放回对象池之前，先将其 `SetActive(false)`，而不是直接调用 `Destroy`。  
- 将不活跃的对象放入对象池中，以保持层次结构的整洁。  

## 序列化（Serialization）  
- 使用 `[SerializeField]` 标记私有字段，以在编辑器中显示这些字段；虽然它们是私有的，但在序列化时仍会被包含。  
- 公共字段（`public`）会自动被序列化，但可能会暴露不必要的API。  
- 使用 `[HideInInspector]` 可隐藏字段，使其在序列化时不被包含；`[NonSerialized]` 可完全忽略该字段的序列化。  
- 序列化后的字段会保留编辑器中的设置；首次序列化后的默认值会被忽略。  

## ScriptableObjects  
- `ScriptableObjects` 是作为资产存在的容器，可以在不同场景或预制件之间共享数据。  
- 使用 `CreateAssetMenu` 属性可以方便地创建此类对象（右键点击 → “Create”）。  
- 在构建过程中不要修改 `ScriptableObjects` 的内容，因为这些更改不会被保存（编辑器除外）。  
- 它们非常适合用于存储配置信息或物品数据库，有助于减少预制件的重复使用。  

## 常见错误  
- 每帧都调用 `Find` 方法会导致不必要的性能开销；应缓存相关引用。  
- 在比较标签时，应使用 `CompareTag("Enemy")` 而不是 `tag == "Enemy"`。  
- 物理查询可能会分配内存；应使用 `NonAlloc` 变体（如 `RaycastNonAlloc`）来避免内存浪费。  
- UI 锚点设置不当可能导致在不同分辨率下显示异常；请确保正确设置锚点。  
- 在没有上下文的情况下使用 `async/await` 会导致错误；请使用 `UniTask` 或仔细处理异常情况。