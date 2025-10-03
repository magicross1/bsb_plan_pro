<!-- 顶部待办任务区 -->
<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElTag, ElButton, ElIcon, ElTable, ElTableColumn } from 'element-plus'
import { Van, User, Clock } from '@element-plus/icons-vue'
import type { Container } from '@/types'
import { useGanttStore } from '@/stores/gantt'
import dayjs from 'dayjs'

const ganttStore = useGanttStore()

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

// 获取当前页面日期
const currentPageDate = computed(() => {
  // 从时间轴开始时间提取日期
  return dayjs(ganttStore.timelineStart).format('YYYY-MM-DD')
})

// 加载今日必送数据
async function loadMustDeliver() {
  try {
    const response = await fetch('/api/orders/get_last_pickup_ctns', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query_date: currentPageDate.value
      })
    })
    const result = await response.json()
    
    if (result.code === 0) {
      // 转换数据格式，将字段名转换为驼峰命名
      todoTasks.value.mustDeliver = (result.data.date || []).map((item: any) => ({
        ctnNumber: item['CTN NUMBER'],
        fullDeliverAddress: item['FULL Deliver Address'],
        ctnType: item['CTN Type'],
        terminal: item['Terminal'],
        fullClientName: item['FULL CLIENT Name'],
        logisticsStatus: item['Logitics Status'],
        deliverType: item['Deliver Type'],
        doorPositon: item['Door Positon'],
        fullVesselName: item['FULL Vessel Name'],
        ctnWeight: item['CTN Weight'],
        remark: item['REMARK'],
        freightForwarders: item['Freight Forwarders'],
        eta: item['ETA'],
        etd: item['ETD'],
        firstFree: item['First Free'],
        lastFree: item['Last Free'],
        lastDention: item['Last Dention'],
        dischargeTime: item['Discharge Time'],
        gateoutTime: item['Gateout Time'],
        edoPin: item['EDO PIN'],
        shippingLine: item['Shipping Line'],
        emptyPark: item['Empty Park'],
        pickUpDate: item['Pick Up Date'],
        deliverDate: item['Deliver Date'],
        pickEmptyDate: item['Pick Empty Date'],
        dehireDate: item['Dehire Date'],
        planPickUpDate: item['Plan Pick Up Date'],
        planDeliverDate: item['Plan Deliver Date'],
        planPickEmptyDate: item['Plan Pick Empty Date'],
        planDehireDate: item['Plan Dehire Date'],
        requestDeliverDate : item['Request Deliver Date']
      }))
    }
  } catch (error) {
    console.error('Error loading must deliver:', error)
  }
}

// 加载今日必还数据
async function loadMustReturn() {
  try {
    const response = await fetch('/api/orders/get_last_dehire_ctns', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query_date: currentPageDate.value
      })
    })
    const result = await response.json()
    
    if (result.code === 0) {
      // 转换数据格式，将字段名转换为驼峰命名
      todoTasks.value.mustReturn = (result.data.date || []).map((item: any) => ({
        ctnNumber: item['CTN NUMBER'],
        fullDeliverAddress: item['FULL Deliver Address'],
        ctnType: item['CTN Type'],
        emptyPark: item['Empty Park'],
        fullClientName: item['FULL CLIENT Name'],
        logisticsStatus: item['Logitics Status'],
        deliverType: item['Deliver Type'],
        doorPositon: item['Door Positon'],
        fullVesselName: item['FULL Vessel Name'],
        ctnWeight: item['CTN Weight'],
        remark: item['REMARK'],
        freightForwarders: item['Freight Forwarders'],
        terminal: item['Terminal'],
        eta: item['ETA'],
        etd: item['ETD'],
        firstFree: item['First Free'],
        lastFree: item['Last Free'],
        lastDention: item['Last Dention'],
        dischargeTime: item['Discharge Time'],
        gateoutTime: item['Gateout Time'],
        edoPin: item['EDO PIN'],
        shippingLine: item['Shipping Line'],
        pickUpDate: item['Pick Up Date'],
        deliverDate: item['Deliver Date'],
        pickEmptyDate: item['Pick Empty Date'],
        dehireDate: item['Dehire Date'],
        planPickUpDate: item['Plan Pick Up Date'],
        planDeliverDate: item['Plan Deliver Date'],
        planPickEmptyDate: item['Plan Pick Empty Date'],
        planDehireDate: item['Plan Dehire Date'],
        requestDeliverDate : item['Request Deliver Date']
      }))
    }
  } catch (error) {
    console.error('Error loading must return:', error)
  }
}

// 加载客户需求数据
async function loadClientRequest() {
  try {
    const response = await fetch('/api/orders/get_today_deliver_ctns', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query_date: currentPageDate.value
      })
    })
    const result = await response.json()
    
    if (result.code === 0) {
      // 转换数据格式，将字段名转换为驼峰命名
      todoTasks.value.clientRequest = (result.data.date || []).map((item: any) => ({
        ctnNumber: item['CTN NUMBER'],
        fullDeliverAddress: item['FULL Deliver Address'],
        ctnType: item['CTN Type'],
        terminal: item['Terminal'],
        fullClientName: item['FULL CLIENT Name'],
        logisticsStatus: item['Logitics Status'],
        deliverType: item['Deliver Type'],
        doorPositon: item['Door Positon'],
        fullVesselName: item['FULL Vessel Name'],
        ctnWeight: item['CTN Weight'],
        remark: item['REMARK'],
        freightForwarders: item['Freight Forwarders'],
        eta: item['ETA'],
        etd: item['ETD'],
        firstFree: item['First Free'],
        lastFree: item['Last Free'],
        lastDention: item['Last Dention'],
        dischargeTime: item['Discharge Time'],
        gateoutTime: item['Gateout Time'],
        edoPin: item['EDO PIN'],
        shippingLine: item['Shipping Line'],
        emptyPark: item['Empty Park'],
        pickUpDate: item['Pick Up Date'],
        deliverDate: item['Deliver Date'],
        pickEmptyDate: item['Pick Empty Date'],
        dehireDate: item['Dehire Date'],
        planPickUpDate: item['Plan Pick Up Date'],
        planDeliverDate: item['Plan Deliver Date'],
        planPickEmptyDate: item['Plan Pick Empty Date'],
        planDehireDate: item['Plan Dehire Date'],
        requestDeliverDate: item['Request Deliver Date']
      }))
    }
  } catch (error) {
    console.error('Error loading client request:', error)
  }
}

// 加载所有待办任务
async function loadTodoTasks() {
  await Promise.all([
    loadMustDeliver(),
    loadMustReturn(),
    loadClientRequest()
  ])
}

// 新建行程并添加任务
function createTripWithTask(container: Container, taskType: 'deliver' | 'return') {
  // TODO: 打开行程创建面板
  console.log('Create trip with task:', container, taskType)
}

// 监听当前页面日期变化，重新加载数据
watch(currentPageDate, () => {
  loadTodoTasks()
}, { immediate: true })

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
      <div class="table-container">
        <ElTable 
          :data="todoTasks.mustDeliver" 
          size="small"
          stripe
          :show-header="true"
          :max-height="200"
        >
          <ElTableColumn prop="ctnNumber" label="柜号" width="120" show-overflow-tooltip />
          <ElTableColumn prop="fullDeliverAddress" label="送货地址" min-width="200" show-overflow-tooltip />
          <ElTableColumn prop="ctnType" label="柜型" width="80" />
          <ElTableColumn prop="terminal" label="码头" width="120" show-overflow-tooltip />
          <ElTableColumn label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <ElButton size="small" type="primary" @click="createTripWithTask(row, 'deliver')">
                新建行程
              </ElButton>
            </template>
          </ElTableColumn>
        </ElTable>
      </div>
    </div>

    <div class="todo-section">
      <div class="todo-header">
        <ElIcon><Clock /></ElIcon>
        <span>今日必还</span>
        <ElTag type="warning">{{ todoTasks.mustReturn.length }}</ElTag>
      </div>
      <div class="table-container">
        <ElTable 
          :data="todoTasks.mustReturn" 
          size="small"
          stripe
          :show-header="true"
          :max-height="200"
        >
          <ElTableColumn prop="ctnNumber" label="柜号" width="120" show-overflow-tooltip />
          <ElTableColumn prop="fullDeliverAddress" label="送货地址" min-width="200" show-overflow-tooltip />
          <ElTableColumn prop="ctnType" label="柜型" width="80" />
          <ElTableColumn prop="emptyPark" label="空柜场" width="120" show-overflow-tooltip />
          <ElTableColumn label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <ElButton size="small" type="primary" @click="createTripWithTask(row, 'return')">
                新建行程
              </ElButton>
            </template>
          </ElTableColumn>
        </ElTable>
      </div>
    </div>

    <div class="todo-section">
      <div class="todo-header">
        <ElIcon><User /></ElIcon>
        <span>客户需求</span>
        <ElTag type="success">{{ todoTasks.clientRequest.length }}</ElTag>
      </div>
      <div class="table-container">
        <ElTable 
          :data="todoTasks.clientRequest.slice(0, 10)" 
          size="small"
          stripe
          :show-header="true"
          :max-height="200"
        >
          <ElTableColumn prop="ctnNumber" label="柜号" width="120" show-overflow-tooltip />
          <ElTableColumn prop="fullClientName" label="客户名称" min-width="150" show-overflow-tooltip />
          <ElTableColumn prop="logisticsStatus" label="状态" width="100" />
          <ElTableColumn prop="terminal" label="码头" width="120" show-overflow-tooltip />
          <ElTableColumn label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <ElButton size="small" type="primary" @click="createTripWithTask(row, 'deliver')">
                新建行程
              </ElButton>
            </template>
          </ElTableColumn>
        </ElTable>
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
  min-width: 400px;
  flex-shrink: 0;
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.todo-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-weight: 500;
  color: var(--text-primary);
  font-size: 16px;
}

.table-container {
  border-radius: 4px;
  overflow: hidden;
}

.table-container :deep(.el-table) {
  border-radius: 4px;
}

.table-container :deep(.el-table th) {
  background-color: #f8f9fa;
  color: #495057;
  font-weight: 600;
}

.table-container :deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background-color: #f8f9fa;
}

.table-container :deep(.el-table td) {
  padding: 8px 0;
}

.table-container :deep(.el-button--small) {
  padding: 4px 8px;
  font-size: 12px;
}
</style>
