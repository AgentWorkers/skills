<skill>
  <name>kanbanflow</name>
  <description>用于管理 KanbanFlow 工作板任务（包括工作板、列、任务等），支持添加、移动、更改任务颜色以及删除任务。帮助用户更好地组织工作并跟踪进度。</description>
  <usage>
    <command>kanbanflow board</command>  查看工作板信息
    <command>kanbanflow columns</command>  查看/管理列信息
    <command>kanbanflow tasks [columnId]</command>  查看/操作指定列中的任务
    <command>kanbanflow add <columnId> <name> [description> [color]</command>  添加新任务到指定列
    <command>kanbanflow move <taskId> <columnId></command>  将任务移动到指定列
    <command>kanbanflow color <taskId> <color></command>  更改任务的颜色
    <command>kanbanflow delete <taskId></command>  删除任务
  </usage>
</skill>