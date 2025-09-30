# 对话框组件 (ReDialog)

<cite>
**本文档引用文件**  
- [index.vue](file://web/src/components/ReDialog/index.vue)
- [type.ts](file://web/src/components/ReDialog/type.ts)
- [index.ts](file://web/src/components/ReDialog/index.ts)
- [index.vue](file://web/src/views/components/dialog/index.vue)
</cite>

## 目录
1. [简介](#简介)
2. [核心功能与设计](#核心功能与设计)
3. [Props 属性详解](#props-属性详解)
4. [Events 事件说明](#events-事件说明)
5. [Slots 插槽使用](#slots-插槽使用)
6. [实际使用示例](#实际使用示例)
7. [与 Element Plus 的封装关系](#与-element-plus-的封装关系)
8. [TypeScript 类型定义](#typescript-类型定义)
9. [样式覆盖与主题继承](#样式覆盖与主题继承)
10. [常见问题与解决方案](#常见问题与解决方案)

## 简介

`ReDialog` 是 `vue-pure-admin-all` 项目中对 Element Plus 的 `Dialog` 组件进行二次封装的模态对话框组件。它通过函数式调用方式简化了弹窗的使用流程，支持灵活配置标题、宽度、全屏、遮罩层行为等，并提供了丰富的事件回调和插槽机制，适用于各种业务场景下的弹窗需求。

该组件采用组合式 API 和 TypeScript 实现，具备良好的类型提示和可维护性，广泛应用于系统管理、表单操作、确认提示等交互场景。

**Section sources**
- [index.vue](file://web/src/components/ReDialog/index.vue#L1-L207)
- [index.ts](file://web/src/components/ReDialog/index.ts#L1-L70)

## 核心功能与设计

`ReDialog` 的核心设计思想是**函数式调用 + 状态集中管理**。它通过一个全局的 `dialogStore` 响应式数组来维护所有打开的对话框实例，每个对话框以对象形式存储其配置项（如标题、宽度、可见性等），并通过 `v-for` 渲染多个弹窗。

组件通过 `addDialog` 函数添加新对话框，`closeDialog` 关闭指定对话框，`updateDialog` 动态更新对话框属性，`closeAllDialog` 一键关闭所有弹窗，实现了高度灵活的弹窗控制机制。

其主要优势包括：
- 支持嵌套弹窗
- 可配置延时打开/关闭
- 支持自定义头部、内容、底部渲染
- 提供确定按钮 loading 状态
- 内置 Popconfirm 确认框集成
- 完善的事件生命周期钩子

**Section sources**
- [index.ts](file://web/src/components/ReDialog/index.ts#L1-L70)
- [index.vue](file://web/src/components/ReDialog/index.vue#L1-L207)

## Props 属性详解

`ReDialog` 继承了 Element Plus Dialog 的大部分属性，并扩展了部分实用功能。以下是关键属性说明：

| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| visible | boolean | false | 对话框是否显示 |
| title | string | - | 对话框标题 |
| width | string / number | "50%" | 对话框宽度 |
| fullscreen | boolean | false | 是否全屏显示 |
| fullscreenIcon | boolean | false | 是否显示全屏切换图标 |
| top | string | "15vh" | 距离顶部的距离 |
| modal | boolean | true | 是否显示遮罩层 |
| appendToBody | boolean | false | 是否插入至 body 元素上 |
| lockScroll | boolean | true | 是否锁定 body 滚动 |
| closeOnClickModal | boolean | true | 是否可通过点击遮罩关闭 |
| closeOnPressEscape | boolean | true | 是否可通过 ESC 键关闭 |
| showClose | boolean | true | 是否显示右上角关闭按钮 |
| draggable | boolean | false | 是否可拖拽 |
| destroyOnClose | boolean | false | 关闭时是否销毁内部元素 |

特别说明：
- `fullscreen` 和 `fullscreenIcon` 同时设置时，仅 `fullscreen` 生效。
- `destroyOnClose` 设置为 `true` 可在关闭时销毁内容，避免内存泄漏或状态残留。

**Section sources**
- [type.ts](file://web/src/components/ReDialog/type.ts#L15-L100)
- [index.vue](file://web/src/components/ReDialog/index.vue#L1-L207)

## Events 事件说明

`ReDialog` 提供了完整的生命周期事件回调，便于在不同阶段执行自定义逻辑：

| 事件名 | 回调参数 | 触发时机 |
|--------|----------|----------|
| opened | `{ options, index }` | 对话框打开后的回调 |
| closed | `{ options, index }` | 对话框完全关闭后的回调 |
| openAutoFocus | `{ options, index }` | 输入焦点聚焦时触发 |
| closeAutoFocus | `{ options, index }` | 输入焦点失焦时触发 |
| fullscreenCallBack | `{ options, index }` | 点击全屏按钮时触发 |
| beforeCancel | `(done, { options, index })` | 点击取消按钮前触发，可暂停关闭 |
| beforeSure | `(done, { options, index, closeLoading })` | 点击确定按钮前触发，常用于表单提交前验证或接口调用 |

其中 `beforeCancel` 和 `beforeSure` 接收 `done` 函数作为参数，调用 `done()` 才会真正关闭对话框，适合用于异步操作（如接口请求）完成后才关闭弹窗的场景。

**Section sources**
- [type.ts](file://web/src/components/ReDialog/type.ts#L102-L180)
- [index.vue](file://web/src/components/ReDialog/index.vue#L1-L207)

## Slots 插槽使用

`ReDialog` 支持以下插槽：

### 默认插槽（default）
用于定义对话框主体内容。通常通过 `contentRenderer` 属性动态渲染内容组件。

### Footer 插槽
可通过以下方式自定义底部按钮区域：
- 使用 `footerButtons` 数组配置多个按钮
- 使用 `footerRenderer` 自定义渲染整个底部区域
- 设置 `hideFooter: true` 隐藏默认底部

默认底部包含“取消”和“确定”两个按钮，支持 `popconfirm` 气泡确认框集成。

**Section sources**
- [index.vue](file://web/src/components/ReDialog/index.vue#L1-L207)
- [type.ts](file://web/src/components/ReDialog/type.ts#L102-L180)

## 实际使用示例

### 基本用法
```ts
addDialog({
  title: "基础用法",
  contentRenderer: () => <p>弹框内容-基础用法</p>
});
```

### 表单嵌套（响应式数据）
```ts
const formInline = ref({ user: "菜虚鲲", region: "浙江" });
addDialog({
  title: "结合Form表单",
  contentRenderer: () => h(forms, { formInline: formInline.value }),
  closeCallBack: () => {
    console.log("表单数据:", formInline.value);
  }
});
```

### 异步关闭（带 loading）
```ts
addDialog({
  sureBtnLoading: true,
  beforeSure: (done) => {
    // 模拟异步操作
    setTimeout(() => {
      done(); // 完成后关闭
    }, 800);
  }
});
```

### 自定义底部按钮
```ts
addDialog({
  footerButtons: [
    { label: "保存", type: "primary", btnClick: ({ dialog }) => closeDialog(dialog.options, dialog.index) },
    { label: "取消", btnClick: ({ dialog }) => closeDialog(dialog.options, dialog.index) }
  ]
});
```

**Section sources**
- [index.vue](file://web/src/views/components/dialog/index.vue#L1-L556)

## 与 Element Plus 的封装关系

`ReDialog` 是对 Element Plus `el-dialog` 的**高层封装**，其本质是一个可复用的函数式调用入口。它并未直接替换 `el-dialog`，而是通过维护一个 `dialogStore` 数组，动态渲染多个 `el-dialog` 实例。

主要封装点包括：
- 将组件调用转换为函数调用（`addDialog`）
- 集中管理多个弹窗的状态
- 提供默认的“取消/确定”按钮逻辑
- 集成全屏切换图标与回调
- 支持延时打开/关闭的定时控制
- 统一处理关闭后的资源清理

这种设计使得开发者无需在模板中手动编写 `<el-dialog>` 标签，提升了代码的简洁性和可维护性。

**Section sources**
- [index.vue](file://web/src/components/ReDialog/index.vue#L1-L207)
- [index.ts](file://web/src/components/ReDialog/index.ts#L1-L70)

## TypeScript 类型定义

`ReDialog` 使用 `type.ts` 文件定义了完整的类型接口，提升开发体验和类型安全：

- `DialogProps`：继承 Element Plus Dialog 的所有属性
- `ButtonProps`：定义底部按钮的类型结构，包含 `btnClick` 回调
- `DialogOptions`：综合配置类型，包含 props、事件、渲染器等
- `EventType`：支持的事件类型枚举
- `Popconfirm`：集成 Popconfirm 组件的配置类型

这些类型通过 `export type` 暴露给外部使用，确保在调用 `addDialog` 时能获得完整的类型提示和参数校验。

**Section sources**
- [type.ts](file://web/src/components/ReDialog/type.ts#L1-L276)

## 样式覆盖与主题继承

`ReDialog` 添加了 `pure-dialog` 类名，允许通过 CSS 修改默认样式：

```css
.pure-dialog {
  --el-dialog-border-radius: 12px;
  --el-dialog-padding-primary: 30px;
}
```

组件自动继承项目的主题配置（通过 `useEpThemeStoreHook` 管理），支持深色/浅色模式切换。全屏图标使用 `~icons/ri/fullscreen-fill` 图标库，确保与整体 UI 风格一致。

可通过 `style` 和 `class` 属性动态传入自定义样式，实现弹窗位置、边距等个性化设置。

**Section sources**
- [index.vue](file://web/src/components/ReDialog/index.vue#L1-L207)
- [style](file://web/style/element-plus.scss)

## 常见问题与解决方案

### 遮罩层点击关闭失效

若设置 `closeOnClickModal: false` 仍无法阻止遮罩关闭，可能是由于：
1. 父级组件阻止了事件冒泡
2. 自定义内容区域捕获了点击事件

**解决方案：**
确保 `el-dialog` 的 `close-on-click-modal` 正确绑定，并在自定义内容中避免阻止原生事件冒泡。

### 嵌套弹窗索引错误

嵌套调用时需注意 `index` 参数的传递，建议使用 `updateDialog(value, key, index)` 明确指定目标弹窗。

### 表单数据未重置

使用 `destroyOnClose: true` 可在关闭时销毁组件实例，或在 `closeCallBack` 中手动重置表单数据。

### 函数式调用未注册组件

需确保在 `App.vue` 中引入并注册 `ReDialog` 组件（即使未在模板中使用），否则无法挂载。

**Section sources**
- [index.vue](file://web/src/components/ReDialog/index.vue#L1-L207)
- [index.ts](file://web/src/components/ReDialog/index.ts#L1-L70)
- [index.vue](file://web/src/views/components/dialog/index.vue#L1-L556)