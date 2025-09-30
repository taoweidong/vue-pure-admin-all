# 二维码生成组件 (ReQrcode)

<cite>
**本文档引用文件**  
- [index.tsx](file://web/src/components/ReQrcode/src/index.tsx)
- [index.scss](file://web/src/components/ReQrcode/src/index.scss)
- [qrcode.vue](file://web/src/views/able/qrcode.vue)
- [LoginQrCode.vue](file://web/src/views/login/components/LoginQrCode.vue)
</cite>

## 目录
1. [简介](#简介)
2. [核心属性配置](#核心属性配置)
3. [事件监听](#事件监听)
4. [实际应用场景](#实际应用场景)
5. [样式定制](#样式定制)
6. [错误处理机制](#错误处理机制)

## 简介

`ReQrcode` 是一个基于 `qrcode` 第三方库封装的二维码生成组件，支持通过 `canvas` 或 `img` 标签渲染。该组件提供了丰富的配置选项，包括二维码内容、尺寸、边距、颜色、Logo 嵌入等功能，并支持动态内容更新和事件监听。

组件默认使用 `canvas` 渲染，支持嵌入 Logo；若使用 `img` 标签，则不支持 Logo 嵌套。二维码的容错率会根据内容长度自动调整：内容越短，容错率越高（H > Q > M），以提升扫描成功率。

**Section sources**
- [index.tsx](file://web/src/components/ReQrcode/src/index.tsx#L0-L55)

## 核心属性配置

`ReQrcode` 组件提供多个核心属性用于控制二维码的生成与展示：

- **value (`text`)**：二维码的内容，支持字符串或数组类型。当内容为空时，组件不会生成二维码。
- **size (`width`)**：二维码的宽度（同时也是高度，保持正方形），默认值为 `200`。
- **margin**：通过 `options` 属性中的 `margin` 字段设置，控制二维码四周的空白区域，默认由 `qrcode` 库决定。
- **options**：传递给底层 `qrcode` 库的配置项，可自定义颜色、容错率等。例如：
  ```ts
  :options="{
    color: {
      dark: '#55D187',
      light: '#2d8cf0'
    },
    margin: 2
  }"
  ```
- **tag**：指定渲染标签，可选 `canvas`（默认）或 `img`。
- **logo**：嵌入 Logo，支持字符串（图片 URL）或对象形式配置 Logo 样式。

**Section sources**
- [index.tsx](file://web/src/components/ReQrcode/src/index.tsx#L50-L86)
- [qrcode.vue](file://web/src/views/able/qrcode.vue#L48-L81)

## 事件监听

组件支持以下事件监听：

- **`done`**：二维码生成完成后触发，回调参数为生成的 Data URL。可用于预览、下载或上传二维码图片。
- **`click`**：用户点击二维码时触发。
- **`disabled-click`**：当二维码处于失效状态时点击触发。

示例：
```vue
<ReQrcode :text="qrcodeText" @click="codeClick" @done="onQrCodeDone" />
```

**Section sources**
- [index.tsx](file://web/src/components/ReQrcode/src/index.tsx#L50-L86)
- [qrcode.vue](file://web/src/views/able/qrcode.vue#L48-L81)

## 实际应用场景

### 登录场景

在登录页面中，`ReQrcode` 可用于展示扫码登录的二维码。例如，在 `LoginQrCode.vue` 中动态生成包含用户身份信息的二维码：

```vue
<template>
  <ReQrcode :text="t('login.pureTest')" />
</template>
```

此处 `t('login.pureTest')` 为国际化文本，实际使用中可替换为包含用户 token 或临时凭证的 URL。

### 分享功能

在分享功能中，可通过动态绑定 `text` 属性生成个性化分享链接二维码：

```vue
<ReQrcode :text="shareLink" :width="150" :logo="logoUrl" />
```

其中 `shareLink` 可包含用户 ID、时间戳等信息，实现唯一性追踪。

**Section sources**
- [LoginQrCode.vue](file://web/src/views/login/components/LoginQrCode.vue#L0-L27)
- [qrcode.vue](file://web/src/views/able/qrcode.vue#L80-L115)

## 样式定制

通过 `index.scss` 文件可对组件进行样式定制，主要支持以下样式点：

- `.qrcode--disabled`：二维码失效时的遮罩层样式，背景为半透明白色（`rgb(255 255 255 / 95%)`），居中显示刷新图标和提示文字。
- Logo 样式可通过 `logo` 对象配置：
  - `bgColor`：Logo 背景颜色
  - `borderSize`：Logo 边框大小
  - `borderRadius`：Logo 圆角大小
  - `logoRadius`：Logo 图像圆角（需 `canvas` 渲染）

示例：
```ts
:logo="{
  src: 'https://example.com/logo.png',
  logoSize: 0.2,
  bgColor: 'blue',
  borderRadius: 50,
  logoRadius: 10
}"
```

**Section sources**
- [index.scss](file://web/src/components/ReQrcode/src/index.scss#L0-L8)
- [index.tsx](file://web/src/components/ReQrcode/src/index.tsx#L165-L201)

## 错误处理机制

当 `text` 属性为空或无效时，组件不会触发二维码生成，避免错误渲染。此外：

- 若 `text` 为 `null` 或空字符串，`watch` 监听器会直接返回，不执行 `initQrcode()`。
- 组件内部使用 `try/catch` 异常捕获机制（基于 `qrcode` 库），确保生成失败时不会崩溃。
- 失效状态通过 `disabled` 属性控制，点击时触发 `disabled-click` 事件，可用于重新生成二维码。

```vue
<ReQrcode
  :text="qrcodeText"
  disabled
  disabledText="已过期"
  @disabled-click="handleRefresh"
/>
```

**Section sources**
- [index.tsx](file://web/src/components/ReQrcode/src/index.tsx#L83-L134)
- [index.tsx](file://web/src/components/ReQrcode/src/index.tsx#L241-L260)