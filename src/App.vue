<script setup lang="ts">
import { onMounted } from 'vue'
import { useGanttStore } from './stores/gantt'
import TodoBar from './components/TodoBar.vue'
import GanttControlPanel from './components/GanttControlPanel.vue'
import GanttMain from './components/GanttMain.vue'
import ContextMenu from './components/ContextMenu.vue'
import OrderSelectionPanel from './components/OrderSelectionPanel.vue'

const ganttStore = useGanttStore()

onMounted(() => {
  // 加载设置
  ganttStore.loadSettings()
  
  // 获取车辆数据
  ganttStore.fetchVehicleList()
})
</script>

<template>
  <div class="gantt-app">
    <!-- 顶部待办区 -->
    <TodoBar />
    
    <!-- 控制面板 -->
    <GanttControlPanel />
    
    <!-- 主体甘特图 -->
    <GanttMain />
    
    <!-- 上下文菜单 -->
    <ContextMenu />
    
    <!-- 订单选择面板 -->
    <OrderSelectionPanel />
  </div>
</template>

<style>
.gantt-app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* CSS变量定义 */
:root {
  --row-height: 60px;
  --task-margin: 4px;
  --trip-background: #e3f2fd;
  --timeline-bg: #f5f5f5;
  --border-color: #e0e0e0;
  --text-primary: #333;
  --text-secondary: #666;
}

/* 全局样式重置 */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #fafafa;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
