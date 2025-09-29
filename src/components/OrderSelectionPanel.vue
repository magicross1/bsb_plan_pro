<!-- 订单选择面板 -->
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { 
  ElDialog, 
  ElTable, 
  ElTableColumn, 
  ElButton, 
  ElInput, 
  ElSelect, 
  ElOption,
  ElTag,
  ElPagination,
  ElLoading
} from 'element-plus'
import { Search, Refresh, Plus } from '@element-plus/icons-vue'
import { useOrderSelectionStore } from '@/stores/orderSelection'
import { useGanttStore } from '@/stores/gantt'
import type { Container, TaskType } from '@/types'

const orderSelectionStore = useOrderSelectionStore()
const ganttStore = useGanttStore()

// 选中的容器
const selectedContainers = ref<Container[]>([])
const currentPage = ref(1)
const pageSize = ref(10)

// 计算属性
const filteredContainers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return orderSelectionStore.containers.slice(start, end)
})

const total = computed(() => orderSelectionStore.containers.length)

// 监听搜索关键词变化
watch(() => orderSelectionStore.searchKeyword, (newKeyword) => {
  currentPage.value = 1
})

// 搜索处理
function handleSearch() {
  orderSelectionStore.loadContainers()
}

// 重置筛选
function handleReset() {
  orderSelectionStore.resetFilters()
  currentPage.value = 1
}

// 选择容器
function selectContainer(container: Container) {
  const index = selectedContainers.value.findIndex(c => c.ctnNumber === container.ctnNumber)
  if (index === -1) {
    selectedContainers.value.push(container)
  } else {
    selectedContainers.value.splice(index, 1)
  }
}

// 全选/取消全选
function toggleSelectAll() {
  if (selectedContainers.value.length === filteredContainers.value.length) {
    selectedContainers.value = []
  } else {
    selectedContainers.value = [...filteredContainers.value]
  }
}

// 添加到行程
async function addToTrip(taskType: TaskType) {
  if (selectedContainers.value.length === 0) {
    return
  }

  try {
    for (const container of selectedContainers.value) {
      const response = await fetch('/api/orders/plan-to-task', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          containerNo: container.ctnNumber,
          taskType: taskType
        })
      })
      
      const result = await response.json()
      if (result.code === 0) {
        // 任务创建成功，可以添加到指定行程
        console.log('Task created:', result.data)
      }
    }
    
    // 清空选择
    selectedContainers.value = []
    orderSelectionStore.hide()
  } catch (error) {
    console.error('Error adding to trip:', error)
  }
}

// 创建新行程
async function createNewTrip(taskType: TaskType) {
  if (selectedContainers.value.length === 0) {
    return
  }

  try {
    // 选择第一个可用车辆
    const availableVehicle = ganttStore.vehicles.find(v => v.trips.length < 5) // 假设每辆车最多5个行程
    if (!availableVehicle) {
      console.error('No available vehicle')
      return
    }

    // 创建行程
    const now = new Date()
    const startTime = new Date(now.getTime() + 60 * 60 * 1000) // 1小时后开始
    const endTime = new Date(startTime.getTime() + 2 * 60 * 60 * 1000) // 持续2小时

    const tripResponse = await fetch('/api/gantt/trip', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        vehicleId: availableVehicle.id,
        startTime: startTime.toISOString().slice(0, 19).replace('T', ' '),
        endTime: endTime.toISOString().slice(0, 19).replace('T', ' '),
        fullLoad: 'N'
      })
    })

    const tripResult = await tripResponse.json()
    if (tripResult.code === 0) {
      const tripId = tripResult.data.id

      // 为每个选中的容器创建任务
      for (const container of selectedContainers.value) {
        const taskResponse = await fetch('/api/orders/plan-to-task', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            tripId: tripId,
            containerNo: container.ctnNumber,
            taskType: taskType
          })
        })
        
        const taskResult = await taskResponse.json()
        if (taskResult.code === 0) {
          console.log('Task added to trip:', taskResult.data)
        }
      }
      
      // 刷新车辆数据
      await ganttStore.fetchVehicleList()
      
      // 清空选择并关闭面板
      selectedContainers.value = []
      orderSelectionStore.hide()
    }
  } catch (error) {
    console.error('Error creating new trip:', error)
  }
}

// 获取状态标签类型
function getStatusTagType(status: string) {
  switch (status) {
    case '新订单': return 'success'
    case 'Client': return 'primary'
    case 'Yard(F)': return 'warning'
    case 'Yard(E)': return 'info'
    default: return ''
  }
}
</script>

<template>
  <ElDialog
    v-model="orderSelectionStore.visible"
    title="订单选择"
    width="80%"
    :close-on-click-modal="false"
  >
    <div class="order-selection-panel">
      <!-- 搜索和筛选 -->
      <div class="search-section">
        <div class="search-row">
          <ElInput
            v-model="orderSelectionStore.searchKeyword"
            placeholder="搜索容器号或客户名称"
            @keyup.enter="handleSearch"
            style="width: 300px"
          >
            <template #append>
              <ElButton @click="handleSearch">
                <ElIcon><Search /></ElIcon>
              </ElButton>
            </template>
          </ElInput>
          
          <ElSelect
            v-model="orderSelectionStore.filters.logisticsStatus"
            placeholder="物流状态"
            @change="handleSearch"
            style="width: 150px"
          >
            <ElOption label="全部" value="" />
            <ElOption label="新订单" value="新订单" />
            <ElOption label="Client" value="Client" />
            <ElOption label="Yard(F)" value="Yard(F)" />
            <ElOption label="Yard(E)" value="Yard(E)" />
          </ElSelect>
          
          <ElSelect
            v-model="orderSelectionStore.filters.deliverType"
            placeholder="交付类型"
            @change="handleSearch"
            style="width: 150px"
          >
            <ElOption label="全部" value="" />
            <ElOption label="Full" value="Full" />
            <ElOption label="Empty" value="Empty" />
          </ElSelect>
          
          <ElButton @click="handleReset">
            <ElIcon><Refresh /></ElIcon>
            重置
          </ElButton>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-section" v-if="selectedContainers.length > 0">
        <div class="selected-info">
          已选择 {{ selectedContainers.length }} 个容器
        </div>
        <div class="action-buttons">
          <ElButton type="primary" @click="addToTrip('Client')">
            <ElIcon><Plus /></ElIcon>
            加入现有行程
          </ElButton>
          <ElButton type="success" @click="createNewTrip('Client')">
            <ElIcon><Plus /></ElIcon>
            创建新行程
          </ElButton>
        </div>
      </div>

      <!-- 容器列表 -->
      <div class="table-section">
        <ElTable
          :data="filteredContainers"
          @selection-change="selectedContainers = $event"
          v-loading="orderSelectionStore.loading"
        >
          <ElTableColumn type="selection" width="55" />
          
          <ElTableColumn prop="ctnNumber" label="容器号" width="120" />
          
          <ElTableColumn prop="logisticsStatus" label="物流状态" width="100">
            <template #default="{ row }">
              <ElTag :type="getStatusTagType(row.logisticsStatus)">
                {{ row.logisticsStatus }}
              </ElTag>
            </template>
          </ElTableColumn>
          
          <ElTableColumn prop="fullClientName" label="客户名称" width="150" />
          
          <ElTableColumn prop="ctnType" label="容器类型" width="80" />
          
          <ElTableColumn prop="fullDeliverAddress" label="送货地址" min-width="200" />
          
          <ElTableColumn prop="planDeliverDate" label="计划送货日期" width="120" />
          
          <ElTableColumn prop="planDehireDate" label="计划还柜日期" width="120" />
          
          <ElTableColumn label="操作" width="100">
            <template #default="{ row }">
              <ElButton size="small" @click="selectContainer(row)">
                {{ selectedContainers.find(c => c.ctnNumber === row.ctnNumber) ? '取消' : '选择' }}
              </ElButton>
            </template>
          </ElTableColumn>
        </ElTable>
        
        <!-- 分页 -->
        <div class="pagination-section">
          <ElPagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
          />
        </div>
      </div>
    </div>
  </ElDialog>
</template>

<style scoped>
.order-selection-panel {
  padding: 0;
}

.search-section {
  margin-bottom: 16px;
}

.search-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.action-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-top: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 16px;
}

.selected-info {
  font-size: 14px;
  color: var(--text-secondary);
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.table-section {
  min-height: 400px;
}

.pagination-section {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}
</style>


