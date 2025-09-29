// 订单选择面板状态管理

import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Container } from '@/types';

export const useOrderSelectionStore = defineStore('orderSelection', () => {
  // 面板可见性
  const visible = ref(false);
  
  // 容器列表
  const containers = ref<Container[]>([]);
  
  // 加载状态
  const loading = ref(false);
  
  // 搜索关键词
  const searchKeyword = ref('');
  
  // 筛选条件
  const filters = ref({
    logisticsStatus: '',
    deliverType: '',
    terminal: ''
  });

  // 显示订单选择面板
  function show() {
    visible.value = true;
    loadContainers();
  }

  // 隐藏订单选择面板
  function hide() {
    visible.value = false;
  }

  // 加载容器列表
  async function loadContainers() {
    loading.value = true;
    try {
      const params = new URLSearchParams();
      if (searchKeyword.value) {
        params.append('search', searchKeyword.value);
      }
      if (filters.value.logisticsStatus) {
        params.append('logisticsStatus', filters.value.logisticsStatus);
      }
      if (filters.value.deliverType) {
        params.append('deliverType', filters.value.deliverType);
      }
      if (filters.value.terminal) {
        params.append('terminal', filters.value.terminal);
      }

      const response = await fetch(`/api/orders/containers?${params}`);
      const result = await response.json();
      
      if (result.code === 0) {
        containers.value = result.data;
      } else {
        console.error('Failed to load containers:', result.message);
      }
    } catch (error) {
      console.error('Error loading containers:', error);
    } finally {
      loading.value = false;
    }
  }

  // 搜索容器
  function search(keyword: string) {
    searchKeyword.value = keyword;
    loadContainers();
  }

  // 设置筛选条件
  function setFilters(newFilters: Partial<typeof filters.value>) {
    filters.value = { ...filters.value, ...newFilters };
    loadContainers();
  }

  // 重置筛选条件
  function resetFilters() {
    filters.value = {
      logisticsStatus: '',
      deliverType: '',
      terminal: ''
    };
    searchKeyword.value = '';
    loadContainers();
  }

  // 获取容器详情
  async function getContainerDetail(ctnNumber: string): Promise<Container | null> {
    try {
      const response = await fetch(`/api/orders/container/${ctnNumber}`);
      const result = await response.json();
      
      if (result.code === 0) {
        return result.data;
      }
    } catch (error) {
      console.error('Error fetching container detail:', error);
    }
    
    return null;
  }

  return {
    visible,
    containers,
    loading,
    searchKeyword,
    filters,
    show,
    hide,
    loadContainers,
    search,
    setFilters,
    resetFilters,
    getContainerDetail
  };
});
