import { message } from "@/utils/message";
import { usePublicHooks } from "../../system/hooks";
import { addDialog } from "@/components/ReDialog";
import editForm from "../form/index.vue";
import {
  getTestUserList,
  createTestUser,
  updateTestUser,
  deleteTestUser
} from "@/api/testUser";
import { deviceDetection } from "@pureadmin/utils";
import { ElMessageBox } from "element-plus";
import { h, ref, reactive, onMounted } from "vue";

export function useTestUser(tableRef: any) {
  const form = reactive({
    username: "",
    phone: "",
    status: ""
  });
  const formRef = ref();
  const dataList = ref([]);
  const loading = ref(true);
  const { switchStyle } = usePublicHooks();
  const selectedNum = ref(0);
  const pagination = reactive({
    total: 0,
    pageSize: 10,
    currentPage: 1,
    background: true
  });
  const columns: any = [
    {
      label: "勾选列",
      type: "selection",
      fixed: "left",
      reserveSelection: true
    },
    {
      label: "用户编号",
      prop: "id",
      width: 90
    },
    {
      label: "用户名称",
      prop: "username",
      minWidth: 130
    },
    {
      label: "用户昵称",
      prop: "nickname",
      minWidth: 130
    },
    {
      label: "性别",
      prop: "gender",
      minWidth: 90,
      cellRenderer: ({ row, props }: any) => {
        return h(
          "el-tag", 
          {
            size: props.size,
            type: row.gender === 1 ? "danger" : null,
            effect: "plain"
          }, 
          row.gender === 1 ? "女" : "男"
        );
      }
    },
    {
      label: "手机号码",
      prop: "phone",
      minWidth: 120
    },
    {
      label: "邮箱",
      prop: "email",
      minWidth: 150
    },
    {
      label: "状态",
      prop: "is_active",
      minWidth: 90,
      cellRenderer: (scope: any) => {
        return h(
          "el-switch", 
          {
            size: scope.props.size === "small" ? "small" : "default",
            modelValue: scope.row.is_active,
            "onUpdate:modelValue": (val: any) => {
              scope.row.is_active = val;
            },
            activeValue: true,
            inactiveValue: false,
            activeText: "启用",
            inactiveText: "停用",
            inlinePrompt: true,
            style: switchStyle.value
          }
        );
      }
    },
    {
      label: "创建时间",
      minWidth: 160,
      prop: "created_time",
      formatter: ({ created_time }: any) =>
        created_time ? created_time.replace("T", " ").substring(0, 19) : ""
    },
    {
      label: "操作",
      fixed: "right",
      width: 180,
      slot: "operation"
    }
  ];

  function handleDelete(row: any) {
    ElMessageBox.confirm(
      `是否确认删除用户名称为${row.username}的这条数据?`,
      "系统提示",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        draggable: true
      }
    )
      .then(async () => {
        await deleteTestUser(row.id);
        message(`已删除用户名称为${row.username}的这条数据`, {
          type: "success"
        });
        onSearch();
      })
      .catch(() => {
        message("已取消删除", { type: "info" });
      });
  }

  function handleSizeChange(val: any) {
    pagination.pageSize = val;
    onSearch();
  }

  function handleCurrentChange(val: any) {
    pagination.currentPage = val;
    onSearch();
  }

  function handleSelectionChange(val: any) {
    selectedNum.value = val.length;
    tableRef.value.setAdaptive();
  }

  function onSelectionCancel() {
    selectedNum.value = 0;
    tableRef.value.getTableRef().clearSelection();
  }

  function onbatchDel() {
    const curSelected = tableRef.value.getTableRef().getSelectionRows();
    if (curSelected.length === 0) {
      message("请至少选择一条数据", { type: "warning" });
      return;
    }
    
    ElMessageBox.confirm(
      `是否确认删除选中的${curSelected.length}条数据?`,
      "系统提示",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        draggable: true
      }
    )
      .then(async () => {
        let successCount = 0;
        let failCount = 0;
        
        for (const row of curSelected) {
          try {
            await deleteTestUser(row.id);
            successCount++;
          } catch (error) {
            failCount++;
          }
        }
        
        message(`删除成功${successCount}条，失败${failCount}条`, { 
          type: successCount > 0 ? "success" : "error" 
        });
        
        tableRef.value.getTableRef().clearSelection();
        onSearch();
      })
      .catch(() => {
        message("已取消删除", { type: "info" });
      });
  }

  async function onSearch() {
    loading.value = true;
    try {
      const params: any = {
        page: pagination.currentPage,
        page_size: pagination.pageSize,
        username: form.username || undefined,
        phone: form.phone || undefined,
        status: form.status !== "" ? parseInt(form.status) : undefined
      };
      
      const res: any = await getTestUserList(params);
      if (res.success) {
        dataList.value = res.data.list;
        pagination.total = res.data.total;
      } else {
        message(`获取数据失败`, { type: "error" });
      }
    } catch (error: any) {
      message(`获取数据失败: ${error.message}`, { type: "error" });
    } finally {
      setTimeout(() => {
        loading.value = false;
      }, 500);
    }
  }

  function resetForm(formEl: any) {
    if (!formEl) return;
    formEl.resetFields();
    onSearch();
  }

  function openDialog(title = "新增", row?: any) {
    addDialog({
      title: `${title}测试用户`,
      props: {
        formInline: {
          id: row?.id ?? "",
          username: row?.username ?? "",
          nickname: row?.nickname ?? "",
          email: row?.email ?? "",
          phone: row?.phone ?? "",
          gender: row?.gender ?? 0,
          avatar: row?.avatar ?? "",
          description: row?.description ?? "",
          is_active: row?.is_active ?? true
        }
      },
      width: "46%",
      draggable: true,
      fullscreen: deviceDetection(),
      fullscreenIcon: true,
      closeOnClickModal: false,
      contentRenderer: () => h(editForm, { ref: formRef }),
      beforeSure: async (done: any, { options }: any) => {
        const FormRef = formRef.value.getRef();
        const curData = options.props.formInline;
        
        FormRef.validate(async (valid: any) => {
          if (valid) {
            try {
              if (title === "新增") {
                await createTestUser(curData);
              } else {
                await updateTestUser(curData.id, curData);
              }
              
              message(`${title}测试用户成功`, { type: "success" });
              done();
              onSearch();
            } catch (error: any) {
              message(`${title}测试用户失败: ${error.message}`, { type: "error" });
            }
          }
        });
      }
    });
  }

  onMounted(() => {
    onSearch();
  });

  return {
    form,
    loading,
    columns,
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
  };
}