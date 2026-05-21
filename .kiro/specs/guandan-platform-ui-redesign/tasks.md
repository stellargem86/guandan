# Implementation Plan: 掼蛋平台 UI 全面重构 (Guandan Platform UI Redesign)

## Overview

本实现计划将设计稿拆分为可执行的开发任务，按照 设计系统基础 → 移动端 UI 页面 → 后端 API → 管理后台 → 集成测试 的顺序推进。所有任务基于现有代码结构（uni-app Vue 3 + TypeScript + Sass 移动端，Vue 3 + Vite + Tailwind 管理后台），对已有 stub 页面进行完整重构实现。

## Tasks

- [ ] 1. 设计系统基础 (Design System Foundation)
  - [-] 1.1 创建设计令牌与全局样式变量
    - 创建 `mobile/src/styles/tokens.ts` 定义 DesignTokens 常量（colors, spacing, radius, fontSize, shadow）
    - 创建 `mobile/src/styles/variables.scss` 将 tokens 导出为 Sass 变量（$color-primary: #C41E3A, $color-gold: #D4A843 等）
    - 创建 `mobile/src/styles/mixins.scss` 定义卡片阴影、文本截断、flex 布局等常用 mixin
    - 创建 `mobile/src/styles/global.scss` 定义全局重置样式和页面基础样式
    - 更新 `mobile/src/main.ts` 引入全局样式
    - _Requirements: 14.1, 14.2_

  - [~] 1.2 创建基础 UI 组件库
    - 创建 `mobile/src/components/ui/GdCard.vue` 通用卡片组件（支持 padding, radius, shadow, border 属性）
    - 创建 `mobile/src/components/ui/GdTabs.vue` 标签页组件（支持 scrollable、underline/background lineStyle）
    - 创建 `mobile/src/components/ui/GdButton.vue` 按钮组件（支持 primary/gold/outline 类型、loading、disabled）
    - 创建 `mobile/src/components/ui/GdTag.vue` 标签组件（支持多颜色、圆角样式）
    - 创建 `mobile/src/components/ui/GdAvatar.vue` 头像组件（支持 size、圆角、默认占位）
    - 创建 `mobile/src/components/ui/GdSkeleton.vue` 骨架屏组件（支持行数、头像、卡片模式）
    - 创建 `mobile/src/components/ui/GdEmpty.vue` 空状态组件
    - 创建 `mobile/src/components/ui/GdBadge.vue` 徽章/数字角标组件
    - _Requirements: 14.2, 14.3_

  - [-] 1.3 创建 TypeScript 类型定义
    - 更新 `mobile/src/types/merchant.ts` 添加 MerchantDetail、MerchantCategory、DiningPackage 扩展接口
    - 更新 `mobile/src/types/event.ts` 添加 EventDetail、PrizeSetting、EventSchedule 扩展接口
    - 创建 `mobile/src/types/news.ts` 定义 Article、ArticleComment 接口
    - 创建 `mobile/src/types/ranking.ts` 定义 RankingEntry、ClubRanking 接口
    - 更新 `mobile/src/types/club.ts` 添加 ClubDetail、ClubNotice、ClubAchievement、ClubStats、ClubChatMessage 接口
    - 更新 `mobile/src/types/order.ts` 添加 PaymentOrder 接口
    - 创建 `mobile/src/types/page.ts` 定义所有页面级数据接口（CircleHomeData, MapPageData, EventListData 等）
    - 创建 `mobile/src/types/ui.ts` 定义 UI 组件 Props 接口（CardProps, TabBarProps, MatchCardProps 等）
    - _Requirements: 14.1_

- [ ] 2. 移动端核心业务组件
  - [~] 2.1 重构约局卡片组件 (MatchCard)
    - 重写 `mobile/src/components/MatchCard.vue` 实现卡片式布局：主人头像+昵称、时间地点、当前人数/总人数进度条、标签列表、状态标识
    - 使用 GdCard 包裹，应用圆角和阴影 token
    - 实现 open/full/started/ended 四种状态的视觉样式
    - _Requirements: 4.3, 4.5, 14.2_

  - [~] 2.2 重构商户卡片组件 (MerchantCard)
    - 重写 `mobile/src/components/MerchantCard.vue` 实现：封面图、名称、评分星级、人均价格、距离、标签、地址
    - 实现横向和纵向两种卡片布局变体
    - _Requirements: 3.6, 14.2_

  - [~] 2.3 重构赛事卡片组件 (EventCard)
    - 重写 `mobile/src/components/EventCard.vue` 实现：封面/标题、时间地点、奖金池、报名费、参赛人数进度条、状态标签
    - 实现报名中/进行中/已结束三种状态样式
    - _Requirements: 5.4, 14.2_

  - [~] 2.4 重构帖子卡片组件 (PostCard)
    - 重写 `mobile/src/components/PostCard.vue` 实现：用户头像+昵称+时间、文字内容、九宫格图片、点赞/评论/分享操作栏
    - 支持图片数量 1-9 的不同网格布局
    - _Requirements: 2.1, 2.7_

  - [~] 2.5 重构排行榜项目组件 (RankingItem)
    - 重写 `mobile/src/components/RankingItem.vue` 实现：排名数字（前三名金银铜特殊样式）、头像、昵称、积分、段位标签
    - 实现前三名高亮 podium 样式
    - _Requirements: 7.3, 7.4_

  - [~] 2.6 重构俱乐部卡片组件 (ClubCard)
    - 重写 `mobile/src/components/ClubCard.vue` 实现：俱乐部 Logo、名称、成员数、地点、标签、简介
    - _Requirements: 9.3, 14.2_

  - [~] 2.7 重构支付按钮组件 (PaymentButton)
    - 重写 `mobile/src/components/PaymentButton.vue` 实现：金额显示、加载状态、禁用状态、倒计时显示
    - 使用金色 (#D4A843) 作为支付按钮主色
    - _Requirements: 6.3, 6.9_

  - [~] 2.8 创建资讯文章卡片组件 (ArticleCard)
    - 创建 `mobile/src/components/ArticleCard.vue` 实现：标题、缩略图（左图右文或大图模式）、来源、发布时间、浏览量、点赞量
    - _Requirements: 11.4_

- [~] 3. Checkpoint - 设计系统与组件库完成
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. 掼友圈页面群 (Circle Pages)
  - [~] 4.1 重构掼友圈首页 (index/index)
    - 重写 `mobile/pages/index/index.vue` 实现完整页面：顶部 Tab 栏（最新/关注/地图）、热门约局横向滚动卡片区、帖子信息流列表
    - 实现下拉刷新和触底加载更多
    - 创建 `mobile/src/composables/useCircleHome.ts` 封装首页数据加载逻辑
    - 实现骨架屏加载状态
    - _Requirements: 2.1, 2.2, 2.3, 4.3, 14.3_

  - [~] 4.2 重构地图找局页面 (index/map)
    - 重写 `mobile/pages/index/map.vue` 实现：顶部分类筛选（全部/餐饮/茶楼/棋牌室）、地图组件（腾讯地图）、商户标记点、底部商户列表
    - 创建 `mobile/src/composables/useMapPage.ts` 封装地图页数据逻辑
    - 实现定位获取、标记点渲染和分类切换
    - 实现定位失败时显示默认位置并提供手动搜索
    - _Requirements: 3.1, 3.2, 3.3, 3.5, 3.8_

  - [~] 4.3 重构商户详情页 (index/merchant-detail)
    - 重写 `mobile/pages/index/merchant-detail.vue` 实现：商户图片轮播、名称评分地址、营业时间电话、套餐列表、预订按钮
    - 实现图片画廊 swiper
    - _Requirements: 3.6_

  - [~] 4.4 重构套餐详情页 (index/package-detail)
    - 重写 `mobile/pages/index/package-detail.vue` 实现：套餐图片、名称价格、详情描述、立即购买按钮
    - _Requirements: 3.6_

  - [~] 4.5 重构发起组局页面 (index/create-match)
    - 重写 `mobile/pages/index/create-match.vue` 实现：标题输入、时间选择、地点选择（关联商户）、标签选择、发布按钮
    - 实现表单验证（maxPlayers 固定为 4）
    - _Requirements: 4.1_

  - [~] 4.6 重构一键组局页面 (index/matchmaking)
    - 重写 `mobile/pages/index/matchmaking.vue` 实现：匹配动画、当前匹配状态、取消匹配按钮
    - _Requirements: 4.2_

  - [~] 4.7 重构帖子详情页 (index/post-detail)
    - 重写 `mobile/pages/index/post-detail.vue` 实现：帖子完整内容、图片查看、评论列表、底部评论输入框、点赞收藏操作
    - _Requirements: 2.7_

  - [~] 4.8 重构发帖页面 (index/create-post)
    - 重写 `mobile/pages/index/create-post.vue` 实现：文本输入区（2000字限制提示）、图片选择（最多9张）、发布按钮
    - 实现图片压缩和上传进度显示
    - _Requirements: 2.4, 2.5, 2.6_

- [ ] 5. 赛事页面群 (Event Pages)
  - [~] 5.1 重构赛事列表页 (events/index)
    - 重写 `mobile/pages/events/index.vue` 实现：顶部 Tab 栏（全部/圈子/进行中/已结束）、赛事卡片列表、天梯榜入口按钮
    - 实现下拉刷新和分页加载
    - _Requirements: 5.1, 5.2_

  - [~] 5.2 重构赛事详情页 (events/detail)
    - 重写 `mobile/pages/events/detail.vue` 实现：赛事封面、基本信息（时间/地点/奖金池）、规则详情、奖金设置表、赛程安排、报名按钮
    - 实现不同状态下按钮文案和可用性控制
    - _Requirements: 5.3, 5.5_

  - [~] 5.3 重构报名支付页 (events/payment)
    - 重写 `mobile/pages/events/payment.vue` 实现：订单信息卡片、金额明细（报名费×数量+保证金）、倒计时显示（30分钟）、支付方式选择、确认支付按钮
    - 创建 `mobile/src/composables/useEventPayment.ts` 封装支付逻辑和倒计时
    - 实现过期后禁用支付
    - _Requirements: 6.2, 6.3, 6.4, 6.9_

  - [~] 5.4 重构天梯排行榜页 (events/rankings)
    - 重写 `mobile/pages/events/rankings.vue` 实现：个人榜/俱乐部榜 Tab 切换、级别筛选（全部/初级/中级/高级）、前三名 podium 展示、榜单列表
    - 创建 `mobile/src/composables/useRankings.ts` 封装排行榜数据逻辑
    - 实现我的排名悬浮显示
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.6_

- [ ] 6. 俱乐部页面群 (Club Pages)
  - [~] 6.1 重构俱乐部列表页 (clubs/index)
    - 重写 `mobile/pages/clubs/index.vue` 实现：搜索栏、推荐俱乐部卡片列表、创建俱乐部入口按钮
    - _Requirements: 9.3_

  - [~] 6.2 重构俱乐部详情页 (clubs/detail)
    - 重写 `mobile/pages/clubs/detail.vue` 实现：俱乐部头部信息（Logo/名称/成员数）、Tab 栏（公告/活动/成就/统计）、对应内容区、加入/管理按钮
    - _Requirements: 9.3, 9.5_

  - [~] 6.3 重构创建俱乐部页 (clubs/create)
    - 重写 `mobile/pages/clubs/create.vue` 实现：名称输入（2-20字）、Logo 上传、标签选择、简介输入、创建按钮
    - 实现名称长度实时验证
    - _Requirements: 9.1, 9.2_

  - [~] 6.4 重构俱乐部管理页 (clubs/manage)
    - 重写 `mobile/pages/clubs/manage.vue` 实现：成员管理列表（角色/移除）、发布公告入口、俱乐部设置
    - _Requirements: 9.5_

  - [~] 6.5 重构俱乐部聊天页 (clubs/chat)
    - 重写 `mobile/pages/clubs/chat.vue` 实现：聊天消息列表（文本/图片/系统消息）、底部输入框（文本+图片发送）、WebSocket 连接管理
    - 创建 `mobile/src/composables/useClubChat.ts` 封装 WebSocket 连接、消息收发、断连重连（指数退避）逻辑
    - 实现消息时间分组和新消息自动滚动
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

  - [~] 6.6 重构成员列表页 (clubs/members)
    - 重写 `mobile/pages/clubs/members.vue` 实现：成员头像/昵称/角色/加入时间列表、搜索功能
    - _Requirements: 9.4_

- [ ] 7. 资讯页面群 (News Pages)
  - [~] 7.1 重构资讯列表页 (news/index)
    - 重写 `mobile/pages/news/index.vue` 实现：分类 Tab 栏（推荐/新闻/教程/文化/体育）、文章卡片列表（大图+列表混排）、下拉刷新和分页
    - _Requirements: 11.1, 11.2, 11.4_

  - [~] 7.2 重构资讯详情页 (news/detail)
    - 重写 `mobile/pages/news/detail.vue` 实现：文章标题、来源+发布时间、富文本正文渲染（rich-text 组件）、底部点赞/收藏/分享操作栏、评论区
    - _Requirements: 11.3, 11.5_

- [ ] 8. 个人中心页面群 (Profile Pages)
  - [~] 8.1 重构个人中心首页 (profile/index)
    - 重写 `mobile/pages/profile/index.vue` 实现：头部用户信息区（头像/昵称/等级）、数据统计卡片（积分/场次/胜率/荣誉）、宫格菜单（我的赛事/我的俱乐部/战绩记录/成就徽章）、列表菜单（钱包/订单/设置/意见反馈）
    - _Requirements: 12.1, 12.2, 12.3, 12.4_

  - [~] 8.2 重构数字钱包页 (profile/wallet)
    - 重写 `mobile/pages/profile/wallet.vue` 实现：余额显示、充值/提现入口、收支记录列表
    - _Requirements: 12.4_

  - [~] 8.3 重构订单记录页 (profile/orders)
    - 重写 `mobile/pages/profile/orders.vue` 实现：Tab 筛选（全部/待支付/已支付/已退款）、订单卡片列表、订单状态标签
    - _Requirements: 12.4_

  - [~] 8.4 重构荣誉徽章页 (profile/badges)
    - 重写 `mobile/pages/profile/badges.vue` 实现：徽章网格展示（已获得高亮/未获得灰色）、点击查看详情
    - _Requirements: 12.2_

  - [~] 8.5 重构设置页 (profile/settings)
    - 重写 `mobile/pages/profile/settings.vue` 实现：个人资料编辑、消息通知开关、隐私设置、关于我们、退出登录
    - 手机号显示脱敏处理（前3后4）
    - _Requirements: 12.4, 15.6_

- [ ] 9. 通用页面 (Common Pages)
  - [~] 9.1 重构登录页 (common/login)
    - 重写 `mobile/pages/common/login.vue` 实现：品牌 Logo + 平台名称、微信一键登录按钮、用户协议/隐私政策勾选
    - 应用深红+金色品牌视觉
    - _Requirements: 1.1_

  - [~] 9.2 重构支付结果页 (common/payment-result)
    - 重写 `mobile/pages/common/payment-result.vue` 实现：成功/失败状态图标、金额信息、操作按钮（查看订单/返回赛事）
    - _Requirements: 6.5_

- [~] 10. Checkpoint - 移动端所有页面完成
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. 后端 API 扩展
  - [~] 11.1 扩展资讯模块 API
    - 创建 `mobile/src/api/news.ts` 实现：getArticleList(category, page)、getArticleDetail(id)、likeArticle(id)、bookmarkArticle(id)
    - 定义 API 响应接口与请求参数类型
    - _Requirements: 11.1, 11.2, 11.3, 11.5_

  - [~] 11.2 扩展排行榜 API
    - 更新 `mobile/src/api/rankings.ts` 实现：getRankings(type, level, page, pageSize)、getMyRanking(type)
    - _Requirements: 7.1, 7.2, 7.4, 7.6_

  - [~] 11.3 扩展赛事报名 API
    - 更新 `mobile/src/api/events.ts` 添加：createRegistration(eventId, quantity)、getEventDetail(id)、getEventSchedule(id)
    - _Requirements: 6.1, 6.2, 5.3_

  - [~] 11.4 扩展俱乐部 API
    - 更新 `mobile/src/api/clubs.ts` 添加：getClubDetail(id)、getClubNotices(id)、getClubActivities(id)、getClubStats(id)、createClub(data)、joinClub(id)
    - _Requirements: 9.1, 9.3, 9.4, 9.5_

  - [~] 11.5 扩展商户地图 API
    - 更新 `mobile/src/api/merchants.ts` 添加：getNearbyMerchants(lat, lng, category, radius, page)、getMerchantDetail(id)、bookMerchant(id)
    - _Requirements: 3.2, 3.4, 3.5_

  - [~] 11.6 创建 WebSocket 聊天服务
    - 创建 `mobile/src/utils/websocket.ts` 实现 WebSocket 封装类：connect、disconnect、send、onMessage、指数退避重连（min(2^(n-1)*1000, 30000)ms）
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

  - [~] 11.7 扩展订单与支付 API
    - 更新 `mobile/src/api/orders.ts` 添加：getOrderList(status, page)、getOrderDetail(id)、confirmPayment(orderNo)、cancelOrder(id)
    - _Requirements: 6.4, 6.9, 6.10_

- [ ] 12. 管理后台更新
  - [~] 12.1 更新管理后台设计系统
    - 更新 `admin/tailwind.config.js` 添加自定义颜色（primary: #C41E3A, gold: #D4A843 及其变体）
    - 更新 `admin/src/styles/index.css` 添加全局样式变量和通用类
    - _Requirements: 14.1_

  - [~] 12.2 重构管理后台仪表盘 (dashboard)
    - 重写 `admin/src/views/dashboard/index.vue` 实现：关键指标卡片（用户数/赛事数/收入/日活）、趋势图表、最近活动列表
    - _Requirements: 13.1_

  - [~] 12.3 重构赛事管理页面
    - 重写 `admin/src/views/events/index.vue` 实现：赛事列表表格（筛选/搜索/分页）、创建赛事表单弹窗、赛事状态管理、奖金设置
    - _Requirements: 13.2_

  - [~] 12.4 重构商户管理页面
    - 重写 `admin/src/views/merchants/index.vue` 实现：商户列表表格、审核功能、商户详情查看
    - _Requirements: 13.2_

  - [~] 12.5 重构用户管理页面
    - 重写 `admin/src/views/users/index.vue` 实现：用户列表表格（搜索/角色筛选）、用户详情抽屉、禁用/启用操作
    - _Requirements: 13.2_

  - [~] 12.6 重构内容管理页面
    - 重写 `admin/src/views/content/index.vue` 实现：资讯文章管理（创建/编辑/删除/发布）、富文本编辑器集成
    - _Requirements: 13.2_

  - [~] 12.7 重构商户门户页面
    - 重写 `admin/src/views/merchant-portal/dashboard.vue` 商户数据看板
    - 重写 `admin/src/views/merchant-portal/packages.vue` 套餐管理 CRUD
    - 重写 `admin/src/views/merchant-portal/verify.vue` 核销页面
    - 重写 `admin/src/views/merchant-portal/settlement.vue` 结算页面
    - _Requirements: 13.3_

  - [~] 12.8 重构赛事组织者门户页面
    - 重写 `admin/src/views/organizer-portal/dashboard.vue` 组织者数据看板
    - 重写 `admin/src/views/organizer-portal/events.vue` 赛事管理
    - 重写 `admin/src/views/organizer-portal/checkin.vue` 签到管理
    - 重写 `admin/src/views/organizer-portal/scoreboard.vue` 计分板
    - 重写 `admin/src/views/organizer-portal/members.vue` 会员管理
    - 重写 `admin/src/views/organizer-portal/reports.vue` 报表统计
    - _Requirements: 13.4_

  - [~] 12.9 实现管理后台 RBAC 权限控制
    - 更新 `admin/src/router/index.ts` 添加路由守卫和角色权限元信息
    - 更新 `admin/src/stores/index.ts` 添加用户角色状态管理
    - 更新各 Layout 组件根据角色动态渲染菜单
    - _Requirements: 13.5, 15.2_

- [~] 13. Checkpoint - 后端 API 与管理后台完成
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. 工具函数与安全模块
  - [~] 14.1 实现内容安全过滤
    - 更新 `mobile/src/utils/format.ts` 添加：sanitizeHtml() XSS 过滤函数（移除 script 标签、事件处理器等）、maskPhoneNumber() 手机号脱敏函数
    - _Requirements: 15.5, 15.6_

  - [~] 14.2 实现表单验证工具
    - 创建 `mobile/src/utils/validators.ts` 实现：validatePostContent(1-2000字)、validateImageCount(0-9张)、validateClubName(2-20字)、validateRating(0-5)、validateCoordinates()
    - _Requirements: 2.4, 2.5, 2.6, 3.7, 9.1, 9.2_

  - [~] 14.3 实现支付金额计算工具
    - 创建 `mobile/src/utils/payment.ts` 实现：calculateRegistrationAmount(fee, quantity, deposit) 金额计算函数、formatCountdown(seconds) 倒计时格式化函数
    - _Requirements: 6.2, 6.3_

- [ ] 15. 集成与功能验证
  - [~] 15.1 页面路由与导航集成
    - 验证 `mobile/pages.json` 中所有页面路由配置正确
    - 确保 TabBar 五个入口正常跳转
    - 确保所有子页面 navigateTo/redirectTo 链路完整
    - _Requirements: 12.4_

  - [~] 15.2 API 联调与数据绑定
    - 确保所有页面组件正确调用 API 接口
    - 验证 composables 中的数据流与错误处理
    - 确保加载状态、空状态、错误状态正确展示
    - _Requirements: 16.2_

  - [ ]* 15.3 Write property test: 支付金额正确性
    - **Property 2: 支付金额正确性**
    - 对任意有效 registrationFee、quantity、deposit，计算结果必须等于 (registrationFee × quantity) + deposit
    - **Validates: Requirements 6.2**

  - [ ]* 15.4 Write property test: 排行榜有序性
    - **Property 3: 排行榜有序性**
    - 对任意排行榜返回结果，所有条目必须按 score 降序排列
    - **Validates: Requirements 7.4, 7.5**

  - [ ]* 15.5 Write property test: ELO 零和性
    - **Property 5: ELO 零和性**
    - 对任意四人局结果，所有玩家积分变化之和的绝对值 ≤ 4
    - **Validates: Requirements 8.2**

  - [ ]* 15.6 Write property test: 帖子内容验证
    - **Property 8: 帖子内容与图片验证**
    - 对任意字符串，长度不在 [1, 2000] 范围内时验证必须拒绝；图片数量 > 9 时必须拒绝
    - **Validates: Requirements 2.4, 2.5, 2.6**

  - [ ]* 15.7 Write property test: 手机号脱敏
    - **Property 15: 手机号脱敏**
    - 对任意有效手机号，脱敏结果只显示前3后4位，中间为 ****
    - **Validates: Requirements 15.6**

  - [ ]* 15.8 Write property test: XSS 内容过滤
    - **Property 16: XSS 内容过滤**
    - 对任意包含 script 标签或事件处理器的 HTML，过滤后不应包含任何危险元素
    - **Validates: Requirements 15.5**

  - [ ]* 15.9 Write property test: WebSocket 重连退避
    - **Property 17: WebSocket 重连退避**
    - 对任意重连次数 n，延迟等于 min(2^(n-1) × 1000, 30000)ms
    - **Validates: Requirements 10.3**

  - [ ]* 15.10 Write property test: 俱乐部名称验证
    - **Property 18: 俱乐部名称验证**
    - 对任意字符串，长度不在 [2, 20] 范围内时验证必须拒绝
    - **Validates: Requirements 9.1, 9.2**

  - [ ]* 15.11 Write property test: 商户评分范围
    - **Property 9: 商户评分范围**
    - 对任意数值，不在 [0.0, 5.0] 范围内时验证必须拒绝
    - **Validates: Requirements 3.7**

  - [ ]* 15.12 Write property test: 分类筛选一致性
    - **Property 10: 分类筛选一致性**
    - 对任意筛选结果列表，所有条目必须匹配所选分类
    - **Validates: Requirements 3.5, 5.2, 7.2, 7.6, 11.2**

- [~] 16. Final checkpoint - 全部功能完成
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- 所有移动端页面为重构现有 stub 文件，无需新建路由
- 设计系统组件以 `Gd` 前缀命名以避免与 uni-app 内置组件冲突
- 管理后台复用现有 Tailwind 体系，通过扩展配置实现品牌色统一

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.3"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8"] },
    { "id": 3, "tasks": ["4.1", "4.2", "4.5", "4.6", "4.7", "4.8", "5.1", "6.1", "6.3", "7.1", "8.1", "9.1"] },
    { "id": 4, "tasks": ["4.3", "4.4", "5.2", "5.4", "6.2", "6.6", "7.2", "8.2", "8.3", "8.4", "8.5", "9.2", "11.1", "11.2", "11.5"] },
    { "id": 5, "tasks": ["5.3", "6.4", "6.5", "11.3", "11.4", "11.6", "11.7", "12.1"] },
    { "id": 6, "tasks": ["12.2", "12.3", "12.4", "12.5", "12.6", "14.1", "14.2", "14.3"] },
    { "id": 7, "tasks": ["12.7", "12.8", "12.9"] },
    { "id": 8, "tasks": ["15.1", "15.2"] },
    { "id": 9, "tasks": ["15.3", "15.4", "15.5", "15.6", "15.7", "15.8", "15.9", "15.10", "15.11", "15.12"] }
  ]
}
```
