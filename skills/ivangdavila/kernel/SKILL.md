---
name: Kernel
description: 避免常见的 Linux 内核错误：原子操作上下文违规、内存分配失败以及锁定陷阱。
metadata: {"clawdbot":{"emoji":"🐧","os":["linux"]}}
---

## 原子上下文陷阱（Atomic Context Traps）
- 如果持有 `spin_lock`，则不能进入睡眠状态：此时不能调用 `kmalloc(GFP_KERNEL)`、`mutex_lock` 或 `copy_from_user`。
- 中断处理过程中可能会占用同一个自旋锁（spinlock）——必须使用 `spin_lock_irqsave` 而不是普通的 `spin_lock`。
- 在 `rcu_read_lock()` 的执行过程中也不能进入睡眠状态：RCU 读取侧不允许有阻塞性调用。
- 对于可能进入睡眠状态的函数，应添加 `might_sleep()` 注解；该注解有助于在启用 `CONFIG_DEBUG.Atomic_sleep` 时捕获相关错误。

## 分配失败（Allocation Failures）
- `GFP_atomic` 的分配操作可能会返回 `NULL`——必须进行检查，不能假设分配一定成功。
- 如果 `vmalloc` 分配的内存在物理上不连续，就不能将其用于 DMA 操作。
- 使用 `kzalloc` 而不是 `kmalloc` 可能会导致未初始化的内存泄漏到用户空间。
- 在循环中不断进行内存分配可能会导致操作系统OOM（Out of Memory）——应预先分配内存或使用内存池。

## 用户指针处理（User Pointer Handling）
- `copy_from_user` 函数返回的副本并不表示数据已被成功复制：返回值为 0 表示复制成功，而非失败。
- 在 `printk` 中绝不要使用 `%s` 来处理用户指针——否则可能导致内核崩溃或信息泄露。
- 用户内存可能在系统调用期间发生变化——在将数据复制到内核缓冲区之前，必须对其进行验证。
- `__user` 注解仅用于文档说明，并不强制要求必须使用特定的复制函数。

## 内存排序（Memory Ordering）
- 对于无锁共享数据，应使用 `READ_ONCE`/`WRITE_ONCE` 语句来防止编译器对数据顺序进行优化或重排序。
- 释放自旋锁时存在隐式的屏障机制——但仍然需要谨慎处理“先检查后执行”的操作模式。
- 在发布指针之前，应调用 `smp_wmb()` 确保数据在指针被使用之前已经可见。

## 模块错误处理（Module Error Handling）
- 如果模块初始化过程中出现错误，必须撤销所有已完成的操作。
- 清理资源的顺序应与注册资源的顺序相反。
- 使用 `goto err_*` 语句进行错误处理是一种标准做法——比嵌套的 `if` 语句更简洁。
- 在释放或取消注册资源之前，必须确认相关资源确实已经被正确初始化。

## 锁的使用错误（Locking Mistakes）
- 同一个锁被多次获取会导致死锁——即使这些操作发生在不同的函数中。
- 锁的获取顺序不一致会导致问题——必须确保在所有地方都按照相同的顺序获取锁。
- `mutex_trylock` 在成功时会返回 1——这与 `pthread_mutex_trylock` 的行为相反。
- 在大多数情况下，读写互斥锁（reader-writer locks）并不值得使用——因为它们带来的竞争开销通常超过了它们带来的好处。