<template>
  <div class="main">
    <el-form
      ref="formRef"
      :inline="true"
      :model="form"
      class="search-form bg-bg_color w-full pl-8 pt-[12px] overflow-auto"
    >
      <el-form-item label="用户名称：" prop="username">
        <el-input
          v-model="form.username"
          placeholder="请输入用户名称"
          clearable
          class="w-[180px]"
        />
      </el-form-item>
      <el-form-item label="手机号码：" prop="phone">
        <el-input
          v-model="form.phone"
          placeholder="请输入手机号码"
          clearable
          class="w-[180px]"
        />
      </el-form-item>
      <el-form-item label="状态：" prop="status">
        <el-select
          v-model="form.status"
          placeholder="请选择"
          clearable
          class="w-[180px]"
        >
          <el-option label="已开启" value="1" />
          <el-option label="已关闭" value="0" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          :loading="loading"
          @click="onSearch"
        >
          搜索
        </el-button>
        <el-button @click="resetForm(formRef)">
          重置
        </el-button>
      </el-form-item>
    </el-form>

    <div class="table-container">
      <div class="table-header">
        <el-button
          type="primary"
          @click="openDialog()"
        >
          新增用户
        </el-button>
      </div>
      
      <div
        v-if="selectedNum > 0"
        class="selection-info"
      >
        <span>
          已选 {{ selectedNum }} 项
        </span>
        <el-button type="primary" text @click="onSelectionCancel">
          取消选择
        </el-button>
        <el-popconfirm title="是否确认删除?" @confirm="onbatchDel">
          <template #reference>
            <el-button type="danger" text>
              批量删除
            </el-button>
          </template>
        </el-popconfirm>
      </div>
      
      <el-table
        ref="tableRef"
        :data="dataList"
        row-key="id"
        v-loading="loading"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="用户编号" width="90" />
        <el-table-column prop="username" label="用户名称" min-width="130" />
        <el-table-column prop="nickname" label="用户昵称" min-width="130" />
        <el-table-column prop="gender" label="性别" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.gender === 1 ? 'danger' : ''">
              {{ scope.row.gender === 1 ? '女' : '男' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="手机号码" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="150" />
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="scope">
            <el-switch
              v-model="scope.row.is_active"
              active-value="1"
              inactive-value="0"
              active-text="启用"
              inactive-text="停用"
            />
          </template>
        </el-table-column>
        <el-table-column prop="created_time" label="创建时间" min-width="160">
          <template #default="scope">
            {{ scope.row.created_time ? scope.row.created_time.replace('T', ' ').substring(0, 19) : '' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="180">
          <template #default="scope">
            <el-button
              link
              type="primary"
              @click="openDialog('修改', scope.row)"
            >
              修改
            </el-button>
            <el-popconfirm
              :title="`是否确认删除用户编号为${scope.row.id}的这条数据`"
              @confirm="handleDelete(scope.row)"
            >
              <template #reference>
                <el-button link type="primary">
                  删除
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      
      <el-pagination
        v-model:current-page="pagination.currentPage"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        :page-sizes="[10, 20, 50, 100]"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useTestUser } from "./utils/hook";

defineOptions({
  name: "TestUser"
});

const formRef = ref();
const tableRef = ref();

const {
  form,
  loading,
  dataList,
  selectedNum,
  pagination,
  onSearch,
  resetForm,
  onbatchDel,
  openDialog,
  handleDelete,
  handleSizeChange,
  onSelectionCancel,
  handleCurrentChange,
  handleSelectionChange
} = useTestUser(tableRef);
</script>

<style scoped>
.main {
  padding: 20px;
}

.search-form {
  margin-bottom: 20px;
  padding: 12px;
  background-color: var(--el-bg-color);
  border-radius: 4px;
}

.search-form .el-form-item {
  margin-right: 20px;
  margin-bottom: 12px;
}

.table-container {
  background-color: var(--el-bg-color);
  padding: 20px;
  border-radius: 4px;
}

.table-header {
  margin-bottom: 20px;
}

.selection-info {
  display: flex;
  align-items: center;
  padding: 10px;
  margin-bottom: 10px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.selection-info span {
  margin-right: 20px;
  color: var(--el-text-color-secondary);
}

.el-pagination {
  margin-top: 20px;
  justify-content: flex-end;
}
</style>