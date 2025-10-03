import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

type Result = {
  success: boolean;
  data?: {
    /** 列表数据 */
    list: Array<any>;
  };
};

/** 卡片列表 */
export const getCardList = (data?: object) => {
  return http.request<Result>("post", baseUrlApi("/get-card-list"), { data });
};
