---
name: PyTorch
description: 避免常见的 PyTorch 错误：训练/评估模式设置不当、梯度泄漏、设备类型不匹配以及检查点（checkpoint）相关的问题。
metadata: {"clawdbot":{"emoji":"🔥","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

## 训练模式（Train Mode）与评估模式（Eval Mode）
- `model.train()`：启用dropout机制和BatchNorm层的更新；这是模型初始化后的默认模式。
- `model.eval()`：禁用dropout机制，使用模型在训练过程中的统计信息（running stats）；在进行推理时必须使用此模式。
- 模式的设置是持久的，除非明确更改。
- 注意：`model.eval()`并不会禁用梯度计算（gradient calculation）；仍需要使用`torch.no_grad()`来禁用梯度计算。

## 梯度控制（Gradient Control）
- 使用`torch.no_grad()`进行推理：可以减少内存占用并加快计算速度。
- `loss.backward()`用于累积梯度；在调用`loss.backward()`之前，需要先调用`optimizer.zero_grad()`来清除之前的梯度。
- `zero_grad()`的调用时机很重要：应在前向传播（forward pass）之前调用，而不是在反向传播（backward pass）之后。
- 使用`.detach()`可以阻止梯度在计算过程中的传播，从而避免内存泄漏。

## 设备管理（Device Management）
- 模型和数据必须位于同一设备上：使用`model.to(device)`和`tensor.to(device)`进行转换。
- `.cuda()`和`.to('cuda')`都可以将张量转移到GPU上，但`.to(device)`更加灵活。
- CUDA张量不能直接转换为numpy数组，需要使用`.cpu().numpy()`进行转换。
- 代码示例：`torch.device('cuda' if torch.cuda.is_available() else 'cpu')`可以实现跨平台的代码运行。

## 数据加载器（Data Loader）
- 当`num_workers > 0`时，会使用多线程进行数据加载；在Windows系统中，需要添加`if __name__ == '__main__':`语句。
- 使用`pin_memory=True`可以提高数据传输到GPU的速度（尤其是使用CUDA时）。
- 各个工作线程之间不会共享状态；随机种子会在每个线程中单独设置（在`worker_init_fn`函数中定义）。
- 过高的`num_workers`可能会导致内存问题；建议从2-4开始尝试，如果计算资源受限，可以适当增加线程数。

## 保存与加载模型（Saving and Loading Models）
- 推荐使用`torch.save(model.state_dict(), path)`来保存模型状态（仅保存模型权重）。
- 加载模型时，先创建模型对象，然后使用`model.load_state_dict(torch.load(path))`。
- 使用`map_location`参数可以实现跨设备的数据加载；如果模型保存在GPU上，可以使用`torch.load(path, map_location='cpu')`。
- 如果直接保存整个模型对象（使用pickle格式），代码修改后可能会导致问题。

## 在位操作（In-place Operations）
- 在位操作通常以`_`结尾（例如`tensor.add_(1)`而不是`tensor.add(1)`）。
- 对叶子节点（leaf nodes）进行在位操作会破坏自动求导（autograd）功能；修改叶子节点会导致错误。
- 对中间节点进行在位操作可能会破坏梯度计算；应避免在计算图中使用此类操作。
- `tensor.data`可以直接访问张量的原始数据，但这种方式不够安全；建议使用`.detach()`来确保数据的正确处理。

## 内存管理（Memory Management）
- 累积的张量可能会导致内存泄漏；使用`.detach()`可以释放不再需要的张量所占用的内存。
- `torch.cuda.empty_cache()`可以清除GPU缓存中的数据，但无法解决所有内存泄漏问题。
- 如果需要，可以删除对张量的引用并调用`gc.collect()`来释放内存。
- 在进行验证（validation）循环时，务必使用`with torch.no_grad()`来避免不必要的梯度计算。

## 常见错误（Common Mistakes）
- 在训练模式下使用`batch_size=1`进行BatchNorm操作会导致错误；此时应使用评估模式或设置`track_running_stats=False`。
- 损失函数（loss function）的默认累积方式是“mean”；如果需要累积梯度，应使用“sum”。
- `cross_entropy`函数期望输入的是logits，而不是softmax输出。
- 使用`.item()`获取Python标量值是正确的做法；使用`.numpy()`或`[0]`可能会导致错误或结果不正确。