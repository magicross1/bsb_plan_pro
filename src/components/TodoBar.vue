<!-- 顶部待办任务区 -->
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElCard, ElTag, ElButton, ElIcon } from 'element-plus'
import { Van, User, Clock } from '@element-plus/icons-vue'
import type { Container } from '@/types'
import { isToday, isTodayOrBefore } from '@/utils/time'

// 待办任务数据
const todoTasks = ref<{
  mustDeliver: Container[]  // 今日必送
  mustReturn: Container[]   // 今日必还
  clientRequest: Container[] // 客户需求
}>({
  mustDeliver: [],
  mustReturn: [],
  clientRequest: []
})

// 加载待办任务
async function loadTodoTasks() {
  try {
    const response = await fetch('/api/orders/containers')
    const result = await response.json()
    
    if (result.code === 0) {
      const containers: Container[] = result.data
      
      // 今日必送：planDeliverDate == 今日 OR lastFree <= 今日 23:59
      todoTasks.value.mustDeliver = containers.filter(container => 
        isToday(container.planDeliverDate) || isTodayOrBefore(container.lastFree)
      )
      
      // 今日必还：planDehireDate == 今日 OR lastFree <= 今日 23:59  
      todoTasks.value.mustReturn = containers.filter(container =>
        isToday(container.planDehireDate) || isTodayOrBefore(container.lastFree)
      )
      
      // 客户需求：logisticsStatus in ['新订单','Client']
      todoTasks.value.clientRequest = containers.filter(container =>
        ['新订单', 'Client'].includes(container.logisticsStatus)
      )
    }
  } catch (error) {
    console.error('Error loading todo tasks:', error)
  }
}

// 添加到行程
function addToTrip(container: Container, taskType: 'deliver' | 'return') {
  // TODO: 打开订单选择面板或直接创建任务
  console.log('Add to trip:', container, taskType)
}

// 新建行程并添加任务
function createTripWithTask(container: Container, taskType: 'deliver' | 'return') {
  // TODO: 打开行程创建面板
  console.log('Create trip with task:', container, taskType)
}

// 打开详情
function openDetail(container: Container) {
  // TODO: 打开容器详情面板
  console.log('Open detail:', container)
}

onMounted(() => {
  loadTodoTasks()
})
</script>

<template>
  <div class="todo-bar">
    <div class="todo-section">
      <div class="todo-header">
        <ElIcon><Van /></ElIcon>
        <span>今日必送</span>
        <ElTag type="danger">{{ todoTasks.mustDeliver.length }}</ElTag>
      </div>
      <div class="todo-cards">
        <ElCard 
          v-for="container in todoTasks.mustDeliver.slice(0, 5)" 
          :key="container.ctnNumber"
          class="todo-card"
          shadow="hover"
        >
          <div class="card-content">
            <div class="card-header">
              <strong>{{ container.ctnNumber }}</strong>
              <ElTag size="small">{{ container.ctnType }}</ElTag>
            </div>
            <div class="card-body">
              <div>{{ container.fullClientName }}</div>
              <div class="address">{{ container.fullDeliverAddress }}</div>
            </div>
            <div class="card-actions">
              <ElButton size="small" @click="addToTrip(container, 'deliver')">
                加入行程
              </ElButton>
              <ElButton size="small" type="primary" @click="createTripWithTask(container, 'deliver')">
                新建行程
              </ElButton>
              <ElButton size="small" text @click="openDetail(container)">
                详情
              </ElButton>
            </div>
          </div>
        </ElCard>
      </div>
    </div>

    <div class="todo-section">
      <div class="todo-header">
        <ElIcon><Clock /></ElIcon>
        <span>今日必还</span>
        <ElTag type="warning">{{ todoTasks.mustReturn.length }}</ElTag>
      </div>
      <div class="todo-cards">
        <ElCard 
          v-for="container in todoTasks.mustReturn.slice(0, 5)" 
          :key="container.ctnNumber"
          class="todo-card"
          shadow="hover"
        >
          <div class="card-content">
            <div class="card-header">
              <strong>{{ container.ctnNumber }}</strong>
              <ElTag size="small" type="warning">{{ container.ctnType }}</ElTag>
            </div>
            <div class="card-body">
              <div>{{ container.fullClientName }}</div>
              <div class="address">{{ container.emptyPark || '待定' }}</div>
            </div>
            <div class="card-actions">
              <ElButton size="small" @click="addToTrip(container, 'return')">
                加入行程
              </ElButton>
              <ElButton size="small" type="primary" @click="createTripWithTask(container, 'return')">
                新建行程
              </ElButton>
              <ElButton size="small" text @click="openDetail(container)">
                详情
              </ElButton>
            </div>
          </div>
        </ElCard>
      </div>
    </div>

    <div class="todo-section">
      <div class="todo-header">
        <ElIcon><User /></ElIcon>
        <span>客户需求</span>
        <ElTag type="success">{{ todoTasks.clientRequest.length }}</ElTag>
      </div>
      <div class="todo-cards">
        <ElCard 
          v-for="container in todoTasks.clientRequest.slice(0, 5)" 
          :key="container.ctnNumber"
          class="todo-card"
          shadow="hover"
        >
          <div class="card-content">
            <div class="card-header">
              <strong>{{ container.ctnNumber }}</strong>
              <ElTag size="small" type="success">{{ container.logisticsStatus }}</ElTag>
            </div>
            <div class="card-body">
              <div>{{ container.fullClientName }}</div>
              <div class="address">{{ container.terminal }}</div>
            </div>
            <div class="card-actions">
              <ElButton size="small" type="primary" @click="createTripWithTask(container, 'deliver')">
                新建行程
              </ElButton>
              <ElButton size="small" text @click="openDetail(container)">
                详情
              </ElButton>
            </div>
          </div>
        </ElCard>
      </div>
    </div>
  </div>
</template>

<style scoped>
.todo-bar {
  display: flex;
  gap: 16px;
  padding: 12px 16px;
  background: white;
  border-bottom: 1px solid var(--border-color);
  overflow-x: auto;
  min-height: 120px;
}

.todo-section {
  min-width: 300px;
  flex-shrink: 0;
}

.todo-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-primary);
}

.todo-cards {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.todo-card {
  min-width: 240px;
  max-width: 240px;
}

.card-content {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.card-body {
  margin-bottom: 12px;
  font-size: 14px;
  color: var(--text-secondary);
}

.address {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-actions {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.card-actions .el-button {
  flex: 1;
  min-width: 0;
}
</style>
