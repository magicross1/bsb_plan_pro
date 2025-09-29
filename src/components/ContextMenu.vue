<!-- 右键上下文菜单组件 -->
<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMenu, ElMenuItem, ElDivider, ElIcon } from 'element-plus'
import { 
  Plus, 
  Refresh, 
  DocumentAdd, 
  Van, 
  Edit, 
  Delete, 
  CopyDocument 
} from '@element-plus/icons-vue'
import { useGanttStore } from '@/stores/gantt'
import { useOrderSelectionStore } from '@/stores/orderSelection'

const ganttStore = useGanttStore()
const orderSelectionStore = useOrderSelectionStore()

// 菜单位置
const menuStyle = computed(() => ({
  position: 'fixed',
  left: ganttStore.contextMenu.x + 'px',
  top: ganttStore.contextMenu.y + 'px',
  zIndex: 9999
}))

// 菜单项
const menuItems = computed(() => {
  const items = []
  
  switch (ganttStore.contextMenu.type) {
    case 'blank':
      items.push(
        { label: '新增车辆', action: 'addVehicle', icon: 'Plus' },
        { label: '刷新数据', action: 'refresh', icon: 'Refresh' }
      )
      break
      
    case 'track':
      items.push(
        { label: '新增行程', action: 'addTrip', icon: 'Plus' },
        { label: '添加任务', action: 'addTask', icon: 'DocumentAdd' },
        { label: '打开订单', action: 'openOrders', icon: 'Van' }
      )
      break
      
    case 'trip':
      items.push(
        { label: '编辑行程', action: 'editTrip', icon: 'Edit' },
        { label: '添加任务', action: 'addTask', icon: 'DocumentAdd' },
        { label: '删除行程', action: 'deleteTrip', icon: 'Delete' }
      )
      break
      
    case 'task':
      items.push(
        { label: '编辑任务', action: 'editTask', icon: 'Edit' },
        { label: '复制任务', action: 'copyTask', icon: 'CopyDocument' },
        { label: '删除任务', action: 'deleteTask', icon: 'Delete' }
      )
      break
  }
  
  return items
})

// 处理菜单项点击
function handleMenuClick(action: string) {
  const payload = ganttStore.contextMenu.payload
  
  switch (action) {
    case 'addVehicle':
      addVehicle()
      break
    case 'refresh':
      ganttStore.fetchVehicleList()
      break
    case 'addTrip':
      addTrip(payload)
      break
    case 'addTask':
      addTask(payload)
      break
    case 'openOrders':
      orderSelectionStore.show()
      break
    case 'editTrip':
      editTrip(payload)
      break
    case 'deleteTrip':
      deleteTrip(payload)
      break
    case 'editTask':
      editTask(payload)
      break
    case 'copyTask':
      copyTask(payload)
      break
    case 'deleteTask':
      deleteTask(payload)
      break
  }
  
  // 关闭菜单
  ganttStore.hideContextMenu()
}

// 新增车辆
function addVehicle() {
  // TODO: 打开新增车辆面板
  console.log('Add vehicle')
}

// 新增行程
function addTrip(payload: any) {
  if (payload?.vehicle) {
    // TODO: 打开新增行程面板
    console.log('Add trip to vehicle:', payload.vehicle.id)
  }
}

// 添加任务
function addTask(payload: any) {
  if (payload?.trip) {
    // TODO: 打开添加任务面板
    console.log('Add task to trip:', payload.trip.id)
  } else if (payload?.vehicle) {
    // 先创建行程，再添加任务
    console.log('Create trip and add task for vehicle:', payload.vehicle.id)
  }
}

// 编辑行程
function editTrip(payload: any) {
  if (payload?.trip) {
    // TODO: 打开编辑行程面板
    console.log('Edit trip:', payload.trip.id)
  }
}

// 删除行程
async function deleteTrip(payload: any) {
  if (payload?.trip) {
    try {
      await ganttStore.deleteTrip(payload.trip.id)
    } catch (error) {
      console.error('Failed to delete trip:', error)
    }
  }
}

// 编辑任务
function editTask(payload: any) {
  if (payload?.task) {
    // TODO: 打开编辑任务面板
    console.log('Edit task:', payload.task.id)
  }
}

// 复制任务
function copyTask(payload: any) {
  if (payload?.task) {
    // TODO: 实现任务复制
    console.log('Copy task:', payload.task.id)
  }
}

// 删除任务
async function deleteTask(payload: any) {
  if (payload?.task) {
    try {
      await ganttStore.deleteTask(payload.task.id)
    } catch (error) {
      console.error('Failed to delete task:', error)
    }
  }
}

// 点击外部关闭菜单
function handleClickOutside(event: MouseEvent) {
  if (ganttStore.contextMenu.visible) {
    ganttStore.hideContextMenu()
  }
}

// 键盘事件处理
function handleKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape' && ganttStore.contextMenu.visible) {
    ganttStore.hideContextMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div 
    v-if="ganttStore.contextMenu.visible"
    class="context-menu"
    :style="menuStyle"
    @click.stop
  >
    <ElMenu class="menu">
      <ElMenuItem
        v-for="item in menuItems"
        :key="item.action"
        @click="handleMenuClick(item.action)"
        class="menu-item"
      >
        <template #icon>
          <ElIcon>
            <Plus v-if="item.icon === 'Plus'" />
            <Refresh v-else-if="item.icon === 'Refresh'" />
            <DocumentAdd v-else-if="item.icon === 'DocumentAdd'" />
            <Van v-else-if="item.icon === 'Van'" />
            <Edit v-else-if="item.icon === 'Edit'" />
            <Delete v-else-if="item.icon === 'Delete'" />
            <CopyDocument v-else-if="item.icon === 'CopyDocument'" />
          </ElIcon>
        </template>
        {{ item.label }}
      </ElMenuItem>
    </ElMenu>
  </div>
</template>

<style scoped>
.context-menu {
  background: white;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.menu {
  border: none;
  background: white;
}

.menu-item {
  padding: 8px 16px;
  font-size: 14px;
  color: var(--text-primary);
  cursor: pointer;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: #f5f5f5;
}

.menu-item:focus {
  background-color: #e3f2fd;
  color: #2196f3;
}
</style>
