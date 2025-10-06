<template>
  <el-form ref="formRef" :model="form" label-width="80px">
    <el-form-item label="用户名" prop="username">
      <el-input v-model="form.username" placeholder="请输入用户名" />
    </el-form-item>
    <el-form-item label="昵称" prop="nickname">
      <el-input v-model="form.nickname" placeholder="请输入昵称" />
    </el-form-item>
    <el-form-item label="邮箱" prop="email">
      <el-input v-model="form.email" placeholder="请输入邮箱" />
    </el-form-item>
    <el-form-item label="手机号" prop="phone">
      <el-input v-model="form.phone" placeholder="请输入手机号" />
    </el-form-item>
    <el-form-item label="性别" prop="gender">
      <el-select v-model="form.gender" placeholder="请选择性别">
        <el-option label="男" :value="0" />
        <el-option label="女" :value="1" />
      </el-select>
    </el-form-item>
    <el-form-item label="状态" prop="is_active">
      <el-switch v-model="form.is_active" />
    </el-form-item>
    <el-form-item label="描述" prop="description">
      <el-input v-model="form.description" type="textarea" placeholder="请输入描述" />
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive, watch } from "vue";

defineOptions({
  name: "TestUserForm"
});

const props = defineProps({
  formInline: {
    type: Object,
    default: () => ({})
  }
});

const formRef = ref();
const form = reactive({
  id: "",
  username: "",
  nickname: "",
  email: "",
  phone: "",
  gender: 0,
  avatar: "",
  description: "",
  is_active: true
});

watch(
  () => props.formInline,
  newVal => {
    Object.assign(form, newVal);
  },
  { immediate: true, deep: true }
);

function getRef() {
  return formRef.value;
}

defineExpose({ getRef });
</script>