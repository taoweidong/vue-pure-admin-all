import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

type Result = {
  success: boolean;
  data?: Array<any>;
};

type ResultTable = {
  success: boolean;
  data?: {
    /** 列表数据 */
    list: Array<any>;
    /** 总条目数 */
    total?: number;
    /** 每页显示条目个数 */
    pageSize?: number;
    /** 当前页数 */
    currentPage?: number;
  };
};

/** 获取测试用户管理列表 */
export const getTestUserList = (data?: object) => {
  return http.request<ResultTable>("get", baseUrlApi("/test-users"), { data });
};

/** 获取测试用户详情 */
export const getTestUserDetail = (id: string) => {
  return http.request<Result>("get", baseUrlApi(`/test-users/${id}`));
};

/** 创建测试用户 */
export const createTestUser = (data?: object) => {
  return http.request<Result>("post", baseUrlApi("/test-users"), { data });
};

/** 更新测试用户 */
export const updateTestUser = (id: string, data?: object) => {
  return http.request<Result>("put", baseUrlApi(`/test-users/${id}`), { data });
};

/** 删除测试用户 */
export const deleteTestUser = (id: string) => {
  return http.request("delete", baseUrlApi(`/test-users/${id}`));
};