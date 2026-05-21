# Design Document

## Overview

本设计文档描述深掼会平台的技术架构、数据库设计、核心流程和前端项目结构。基于需求文档中的 15 个需求，提供 Phase 1 的核心实现方案。

深掼会（Shen Guan Hui）是一个集掼蛋牌局社交、商务社交、本地餐饮生活服务为一体的综合平台。平台包含移动端应用（微信小程序优先，跨平台框架）和 Web 管理后台（SaaS 平台），服务于 C 端玩家用户、B 端商户及赛事/俱乐部组织者。

核心技术栈：
- 前端：uni-app 框架，Vue 3 + Vite + Tailwind CSS
- 后端：Python (FastAPI)，RESTful API
- 数据库：PostgreSQL + Redis（高频匹配撮合与 LBS 地理计算）
- 外部服务：微信支付 JSAPI、微信 OAuth 2.0、OSS 对象存储

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
├──────────────────────┬──────────────────────────────────────────┤
│  Mobile App          │  Admin Backend (Web)                      │
│  (uni-app/WeChat     │  (Vue 3 + Vite + Tailwind CSS)           │
│   Mini Program)      │  - Super Admin Portal                     │
│  - 掼友圈            │  - Merchant Portal                        │
│  - 赛事              │  - Organizer Portal                       │
│  - 资讯              │                                           │
│  - 俱乐部            │                                           │
│  - 我的              │                                           │
└──────────┬───────────┴──────────────┬───────────────────────────┘
           │                          │
           ▼                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway (Nginx)                         │
│              Rate Limiting / Auth / Load Balancing                │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Application Layer (FastAPI)                    │
├─────────────┬──────────────┬──────────────┬─────────────────────┤
│ Auth        │ Content      │ Matchmaking  │ Payment             │
│ Service     │ Service      │ Service      │ Service             │
├─────────────┼──────────────┼──────────────┼─────────────────────┤
│ Event       │ Club         │ LBS          │ ELO                 │
│ Service     │ Service      │ Service      │ Engine              │
├─────────────┼──────────────┼──────────────┼─────────────────────┤
│ User        │ Merchant     │ Revenue      │ Notification        │
│ Service     │ Service      │ Split Engine │ Service             │
└─────────────┴──────────────┴──────────────┴─────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Data Layer                                  │
├────────────────────────────┬────────────────────────────────────┤
│  PostgreSQL                │  Redis                              │
│  - Users, Merchants       │  - Session / JWT cache              │
│  - Orders, Transactions   │  - GEO (LBS calculations)           │
│  - Events, Clubs          │  - Matchmaking queue                 │
│  - Content (Posts)        │  - Real-time leaderboard             │
│  - ELO scores             │  - Rate limiting counters            │
└────────────────────────────┴────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Services                              │
├───────────────────┬─────────────────┬───────────────────────────┤
│ WeChat Pay API    │ WeChat Login    │ OSS (Image Storage)        │
│ (JSAPI + 分账)    │ (OAuth 2.0)    │ (Alibaba Cloud / Tencent)  │
└───────────────────┴─────────────────┴───────────────────────────┘
```

### Service Responsibilities

| Service | Responsibility |
|---------|---------------|
| Auth Service | 微信 OAuth 登录、JWT 签发/刷新、Session 管理 |
| Content Service | 掼友圈帖子 CRUD、评论、点赞、内容审核 |
| Matchmaking Service | 一键组局创建/匹配/状态管理 |
| Payment Service | 微信支付集成、订单管理、退款处理 |
| Event Service | 赛事发布/报名/签到/成绩录入 |
| Club Service | 俱乐部 CRUD、成员管理、活动发布 |
| LBS Service | 地理位置计算、Redis GEO 查询、距离排序 |
| ELO Engine | ELO 积分计算、段位分配、排行榜维护 |
| Revenue Split Engine | 分账比例计算、微信分账 API 调用 |
| Notification Service | 消息推送、模板消息、实时通知 |

### Redis Usage Strategy

| Use Case | Redis Data Structure | Key Pattern |
|----------|---------------------|-------------|
| LBS 商户位置 | GEO | `geo:merchants` |
| 天梯排行榜 | Sorted Set | `ranking:personal`, `ranking:club:{id}`, `ranking:region:{name}` |
| 组局匹配队列 | Sorted Set + Hash | `match:queue:{region}`, `match:detail:{id}` |
| 用户 Session | String | `session:{user_id}` |
| 限流计数 | String + EXPIRE | `ratelimit:{ip}:{endpoint}` |
| 帖子点赞缓存 | Set | `post:likes:{post_id}` |

## Components and Interfaces

### Authentication APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/wechat-login | 微信授权登录 |
| POST | /api/v1/auth/refresh-token | 刷新 JWT Token |
| GET | /api/v1/auth/me | 获取当前用户信息 |

### Content Feed APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/posts | 获取帖子列表（分页） |
| POST | /api/v1/posts | 发布新帖子 |
| POST | /api/v1/posts/:id/like | 点赞 |
| DELETE | /api/v1/posts/:id/like | 取消点赞 |
| GET | /api/v1/posts/:id/comments | 获取评论 |
| POST | /api/v1/posts/:id/comments | 发表评论 |

### LBS & Map APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/merchants/nearby | 获取附近商户（LBS） |
| GET | /api/v1/merchants/:id | 商户详情 |
| GET | /api/v1/merchants/:id/packages | 商户餐饮套餐列表 |

### Matchmaking APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/matchmaking | 创建组局 |
| GET | /api/v1/matchmaking | 获取组局列表（筛选） |
| POST | /api/v1/matchmaking/:id/join | 加入组局 |
| POST | /api/v1/matchmaking/:id/cancel | 取消参加 |

### Event APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/events | 赛事列表 |
| GET | /api/v1/events/:id | 赛事详情 |
| POST | /api/v1/events/:id/register | 赛事报名 |
| POST | /api/v1/events/:id/cancel | 取消报名 |
| POST | /api/v1/events/:id/checkin | 签到 |
| POST | /api/v1/events/:id/scores | 提交成绩 |

### Ladder & Ranking APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/rankings/personal | 个人排行榜 |
| GET | /api/v1/rankings/club | 俱乐部排行榜 |
| GET | /api/v1/rankings/regional | 地区排行榜 |
| GET | /api/v1/users/:id/elo | 用户 ELO 详情 |

### Club APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/clubs | 俱乐部列表 |
| POST | /api/v1/clubs | 创建俱乐部 |
| POST | /api/v1/clubs/:id/join | 申请加入 |
| GET | /api/v1/clubs/:id/members | 成员列表 |
| GET | /api/v1/clubs/:id/activities | 俱乐部活动 |
| POST | /api/v1/clubs/:id/activities | 创建活动 |

### Payment & Order APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/orders | 创建订单 |
| GET | /api/v1/orders/:id | 订单详情 |
| POST | /api/v1/orders/:id/pay | 发起支付 |
| POST | /api/v1/payments/callback | 微信支付回调 |
| POST | /api/v1/orders/:id/refund | 申请退款 |
| POST | /api/v1/orders/:id/verify | 核销订单 |

### Wallet APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/wallet | 钱包信息 |
| GET | /api/v1/wallet/transactions | 流水记录 |
| POST | /api/v1/wallet/withdraw | 发起提现 |

### Admin APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/admin/dashboard | 管理仪表盘 |
| GET | /api/v1/admin/users | 用户管理 |
| GET | /api/v1/admin/reviews | 内容审核列表 |
| POST | /api/v1/admin/reviews/:id/approve | 审核通过 |
| POST | /api/v1/admin/reviews/:id/reject | 审核拒绝 |
| GET | /api/v1/admin/finance | 财务报表 |
| PUT | /api/v1/admin/config/elo | 配置 ELO 参数 |

### Core Sequence: 餐饮套餐购买→分账→核销流程

```
┌──────┐     ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐
│ User │     │Mobile_App│    │ Payment   │    │ WeChat   │    │ Revenue  │    │Merchant│
│      │     │          │    │ Service   │    │ Pay API  │    │ Split    │    │        │
└──┬───┘     └────┬─────┘    └─────┬─────┘    └────┬─────┘    └────┬─────┘    └───┬────┘
   │               │               │               │               │              │
   │ 1.选择¥199套餐 │               │               │               │              │
   │──────────────>│               │               │               │              │
   │               │               │               │               │              │
   │               │ 2.创建订单     │               │               │              │
   │               │──────────────>│               │               │              │
   │               │               │               │               │              │
   │               │               │ 3.生成预付单   │               │              │
   │               │               │ (idempotency   │               │              │
   │               │               │  key check)    │               │              │
   │               │               │──────────────>│               │              │
   │               │               │               │               │              │
   │               │               │ 4.返回prepay_id│              │              │
   │               │               │<──────────────│               │              │
   │               │               │               │               │              │
   │               │ 5.返回支付参数  │               │               │              │
   │               │<──────────────│               │               │              │
   │               │               │               │               │              │
   │ 6.确认支付     │               │               │               │              │
   │──────────────>│               │               │               │              │
   │               │ 7.调起微信支付  │               │               │              │
   │               │──────────────────────────────>│               │              │
   │               │               │               │               │              │
   │               │               │ 8.支付成功回调  │               │              │
   │               │               │<──────────────│               │              │
   │               │               │               │               │              │
   │               │               │ 9.更新订单状态  │               │              │
   │               │               │  status=paid   │               │              │
   │               │               │               │               │              │
   │               │               │ 10.触发分账    │               │              │
   │               │               │──────────────────────────────>│              │
   │               │               │               │               │              │
   │               │               │               │               │ 11.计算分账:  │
   │               │               │               │               │ 平台: ¥19.9   │
   │               │               │               │               │ 商户: ¥179.1  │
   │               │               │               │               │              │
   │               │               │               │ 12.调用分账API │              │
   │               │               │               │<──────────────│              │
   │               │               │               │               │              │
   │               │               │               │ 13.分账成功    │              │
   │               │               │               │──────────────>│              │
   │               │               │               │               │              │
   │               │               │               │               │ 14.记录分账   │
   │               │               │               │               │  结果         │
   │               │               │               │               │              │
   │               │ 15.生成核销QR码 │               │               │              │
   │               │<──────────────│               │               │              │
   │               │               │               │               │              │
   │ 16.展示QR码   │               │               │               │              │
   │<──────────────│               │               │               │              │
   │               │               │               │               │              │
   │               │               │               │               │              │
   │═══════════════════════ 到店核销 ══════════════════════════════════════════════│
   │               │               │               │               │              │
   │               │               │               │               │  17.商户扫码  │
   │               │               │               │               │<─────────────│
   │               │               │               │               │              │
   │               │               │ 18.验证核销码  │               │              │
   │               │               │<─────────────────────────────────────────────│
   │               │               │               │               │              │
   │               │               │ 19.标记已核销  │               │              │
   │               │               │  记录时间戳    │               │              │
   │               │               │               │               │              │
   │               │               │ 20.核销成功    │               │              │
   │               │               │──────────────────────────────────────────────>│
   │               │               │               │               │              │
   │ 21.推送核销通知│               │               │               │              │
   │<──────────────│               │               │               │              │
```

### Flow Description

1. **用户下单**: 用户在掼蛋地图选择商户的 ¥199 餐饮套餐，点击购买
2. **创建订单**: Payment_Service 生成唯一订单号和幂等键，创建 pending 状态订单
3. **预付单**: Payment_Service 调用微信 JSAPI 统一下单接口，获取 prepay_id
4. **前端支付**: Mobile_App 使用 prepay_id 调起微信支付弹窗
5. **支付回调**: 微信支付异步通知 Payment_Service 支付结果
6. **状态更新**: 验证签名后更新订单状态为 paid
7. **触发分账**: Revenue_Split_Engine 按配置比例计算分账（平台10%=¥19.9，商户90%=¥179.1）
8. **执行分账**: 调用微信支付分账 API 完成资金划转
9. **生成核销码**: 生成唯一核销码和对应 QR 图片，设置过期时间
10. **到店核销**: 商户使用 Merchant Portal 扫描用户 QR 码
11. **验证核销**: 系统验证核销码有效性（未过期、未使用），标记已核销

### ELO Algorithm Implementation

```python
def calculate_elo(winner_score: int, loser_score: int, k_winner: int, k_loser: int) -> tuple[int, int]:
    """
    计算 ELO 分数变化
    - 新玩家 K=32, 成熟玩家(>30场) K=16
    - 期望胜率: E = 1 / (1 + 10^((Rb - Ra) / 400))
    """
    expected_winner = 1.0 / (1.0 + 10 ** ((loser_score - winner_score) / 400.0))
    expected_loser = 1.0 - expected_winner
    
    new_winner = winner_score + round(k_winner * (1 - expected_winner))
    new_loser = loser_score + round(k_loser * (0 - expected_loser))
    
    return new_winner, max(new_loser, 0)  # ELO 分不低于0
```

### Frontend Project Structure

```
shen-guan-hui/
├── mobile/                           # 移动端 uni-app 项目
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── manifest.json                 # uni-app 配置
│   ├── pages.json                    # 页面路由配置
│   ├── App.vue
│   ├── main.ts
│   ├── uni.scss                      # 全局样式变量
│   ├── src/
│   │   ├── api/                      # API 请求层
│   │   │   ├── index.ts              # Axios/请求封装
│   │   │   ├── auth.ts
│   │   │   ├── posts.ts
│   │   │   ├── merchants.ts
│   │   │   ├── matchmaking.ts
│   │   │   ├── events.ts
│   │   │   ├── clubs.ts
│   │   │   ├── rankings.ts
│   │   │   ├── orders.ts
│   │   │   └── wallet.ts
│   │   ├── composables/              # Vue 3 组合函数
│   │   │   ├── useAuth.ts
│   │   │   ├── useLocation.ts
│   │   │   ├── usePagination.ts
│   │   │   └── usePayment.ts
│   │   ├── stores/                   # Pinia 状态管理
│   │   │   ├── index.ts
│   │   │   ├── user.ts
│   │   │   ├── location.ts
│   │   │   └── app.ts
│   │   ├── utils/                    # 工具函数
│   │   │   ├── request.ts            # 请求拦截器
│   │   │   ├── storage.ts            # 本地存储
│   │   │   ├── format.ts             # 格式化
│   │   │   └── geo.ts                # 地理计算
│   │   └── types/                    # TypeScript 类型定义
│   │       ├── user.ts
│   │       ├── post.ts
│   │       ├── merchant.ts
│   │       ├── event.ts
│   │       ├── club.ts
│   │       └── order.ts
│   ├── pages/                        # 页面目录
│   │   ├── index/                    # Tab 1: 掼友圈
│   │   │   ├── index.vue             # 主页（Feed + 地图入口）
│   │   │   ├── post-detail.vue       # 帖子详情
│   │   │   ├── create-post.vue       # 发帖
│   │   │   ├── map.vue               # 掼蛋地图
│   │   │   ├── merchant-detail.vue   # 商户详情
│   │   │   ├── package-detail.vue    # 套餐详情/购买
│   │   │   ├── matchmaking.vue       # 组局列表
│   │   │   └── create-match.vue      # 发起组局
│   │   ├── events/                   # Tab 2: 赛事
│   │   │   ├── index.vue             # 赛事列表
│   │   │   ├── detail.vue            # 赛事详情/报名
│   │   │   └── rankings.vue          # 天梯排行榜
│   │   ├── news/                     # Tab 3: 资讯
│   │   │   ├── index.vue             # 资讯列表
│   │   │   └── detail.vue            # 文章详情
│   │   ├── clubs/                    # Tab 4: 俱乐部
│   │   │   ├── index.vue             # 俱乐部大厅
│   │   │   ├── detail.vue            # 俱乐部详情
│   │   │   ├── members.vue           # 成员列表
│   │   │   ├── chat.vue              # 内部聊天
│   │   │   └── create.vue            # 创建俱乐部
│   │   ├── profile/                  # Tab 5: 我的
│   │   │   ├── index.vue             # 个人中心
│   │   │   ├── wallet.vue            # 数字钱包
│   │   │   ├── orders.vue            # 订单记录
│   │   │   ├── badges.vue            # 荣誉徽章
│   │   │   └── settings.vue          # 设置
│   │   └── common/                   # 公共页面
│   │       ├── login.vue             # 登录页
│   │       ├── payment-result.vue    # 支付结果
│   │       └── webview.vue           # 内嵌 H5
│   ├── components/                   # 全局组件
│   │   ├── PostCard.vue              # 帖子卡片
│   │   ├── MerchantCard.vue          # 商户卡片
│   │   ├── EventCard.vue             # 赛事卡片
│   │   ├── ClubCard.vue              # 俱乐部卡片
│   │   ├── MatchCard.vue             # 组局卡片
│   │   ├── RankingItem.vue           # 排行榜条目
│   │   ├── PaymentButton.vue         # 支付按钮
│   │   ├── EmptyState.vue            # 空状态
│   │   ├── LoadMore.vue              # 加载更多
│   │   └── TabBar.vue                # 底部导航栏
│   └── static/                       # 静态资源
│       ├── images/
│       └── icons/
│
├── admin/                            # Web 管理后台项目
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── index.html
│   ├── src/
│   │   ├── main.ts
│   │   ├── App.vue
│   │   ├── router/                   # Vue Router
│   │   │   └── index.ts
│   │   ├── api/                      # API 层
│   │   │   └── ...
│   │   ├── stores/                   # Pinia
│   │   │   └── ...
│   │   ├── views/                    # 页面视图
│   │   │   ├── dashboard/            # 仪表盘
│   │   │   ├── users/                # 用户管理
│   │   │   ├── content/              # 内容审核
│   │   │   ├── finance/              # 财务管理
│   │   │   ├── events/               # 赛事管理
│   │   │   ├── merchants/            # 商户管理
│   │   │   ├── clubs/                # 俱乐部管理
│   │   │   ├── ads/                  # 广告管理
│   │   │   ├── config/               # 系统配置（ELO参数等）
│   │   │   └── merchant-portal/      # 商户专用视图
│   │   │       ├── dashboard.vue
│   │   │       ├── verify.vue        # 核销页面
│   │   │       ├── packages.vue      # 套餐管理
│   │   │       └── settlement.vue    # 结算/提现
│   │   ├── components/               # 通用组件
│   │   │   └── ...
│   │   └── layouts/                  # 布局组件
│   │       ├── AdminLayout.vue
│   │       └── MerchantLayout.vue
│   └── public/
│
└── server/                           # 后端 FastAPI 项目
    ├── requirements.txt
    ├── pyproject.toml
    ├── alembic.ini                   # 数据库迁移配置
    ├── app/
    │   ├── __init__.py
    │   ├── main.py                   # FastAPI 入口
    │   ├── config.py                 # 配置管理
    │   ├── dependencies.py           # 依赖注入
    │   ├── api/                      # 路由层
    │   │   ├── __init__.py
    │   │   ├── v1/
    │   │   │   ├── __init__.py
    │   │   │   ├── auth.py
    │   │   │   ├── posts.py
    │   │   │   ├── merchants.py
    │   │   │   ├── matchmaking.py
    │   │   │   ├── events.py
    │   │   │   ├── clubs.py
    │   │   │   ├── rankings.py
    │   │   │   ├── orders.py
    │   │   │   ├── wallet.py
    │   │   │   └── admin.py
    │   │   └── deps.py               # 路由依赖
    │   ├── models/                   # SQLAlchemy 模型
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   │   ├── post.py
    │   │   ├── merchant.py
    │   │   ├── order.py
    │   │   ├── event.py
    │   │   ├── club.py
    │   │   ├── elo.py
    │   │   └── wallet.py
    │   ├── schemas/                  # Pydantic 模型
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   │   ├── post.py
    │   │   ├── merchant.py
    │   │   ├── order.py
    │   │   ├── event.py
    │   │   ├── club.py
    │   │   └── wallet.py
    │   ├── services/                 # 业务逻辑层
    │   │   ├── __init__.py
    │   │   ├── auth_service.py
    │   │   ├── content_service.py
    │   │   ├── lbs_service.py
    │   │   ├── matchmaking_service.py
    │   │   ├── event_service.py
    │   │   ├── club_service.py
    │   │   ├── elo_service.py
    │   │   ├── payment_service.py
    │   │   ├── revenue_split_service.py
    │   │   └── notification_service.py
    │   ├── core/                     # 核心模块
    │   │   ├── __init__.py
    │   │   ├── security.py           # JWT / 加密
    │   │   ├── redis.py              # Redis 连接
    │   │   └── wechat.py             # 微信 SDK 封装
    │   └── migrations/               # Alembic 迁移
    │       └── versions/
    └── tests/
        ├── __init__.py
        ├── conftest.py
        ├── test_auth.py
        ├── test_payment.py
        ├── test_elo.py
        └── test_lbs.py
```

### WeChat Pay Integration Key Points

1. **统一下单**: 使用 JSAPI 下单接口，必须在微信环境内调用
2. **签名验证**: 回调需验证微信签名防止伪造
3. **幂等处理**: 使用 `idempotency_key` 确保同一订单不会重复扣款
4. **分账配置**: 需在微信商户后台开通分账权限，配置分账接收方
5. **退款流程**: 支持原路退回，退款金额不超过原订单金额

### Security Considerations

1. **JWT 认证**: Access Token (15min) + Refresh Token (7d)，Redis 维护 Token 黑名单
2. **API 限流**: 基于 IP + 用户 ID 的双重限流
3. **支付安全**: 所有支付回调验签，敏感数据 AES 加密
4. **RBAC 权限**: 基于角色的访问控制，Admin/Merchant/Organizer/User 四级
5. **内容审核**: UGC 内容先发后审 + 敏感词过滤 + 人工复审机制


## Data Models

### Entity Relationship Overview

```
Users ─┬─< Posts (1:N)
       ├─< MatchmakingParticipants (1:N)
       ├─< EventRegistrations (1:N)
       ├─< ClubMembers (1:N)
       ├─< Orders (1:N)
       ├─< WalletTransactions (1:N)
       └─< EloScores (1:1)

Merchants ─┬─< DiningPackages (1:N)
            └─< MerchantSettlements (1:N)

Clubs ─┬─< ClubMembers (1:N)
       └─< ClubActivities (1:N)

Events ─┬─< EventRegistrations (1:N)
        └─< MatchResults (1:N)

Orders ─┬─< RevenueSplits (1:N)
        └── PackageVerifications (1:1)
```

### Core Tables DDL

```sql
-- =============================================
-- 1. 用户表 (Users)
-- =============================================
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    platform_id VARCHAR(32) UNIQUE NOT NULL,      -- 平台唯一 ID
    wechat_openid VARCHAR(128) UNIQUE,            -- 微信 OpenID
    wechat_unionid VARCHAR(128),                  -- 微信 UnionID
    nickname VARCHAR(64) NOT NULL,
    avatar_url VARCHAR(512),
    phone VARCHAR(20),
    industry VARCHAR(64),                         -- 所属行业（用于组局匹配）
    role VARCHAR(20) DEFAULT 'user',              -- user / merchant / organizer / admin
    status VARCHAR(20) DEFAULT 'active',          -- active / banned / inactive
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_wechat_openid ON users(wechat_openid);
CREATE INDEX idx_users_platform_id ON users(platform_id);

-- =============================================
-- 2. ELO 积分表 (ELO Scores)
-- =============================================
CREATE TABLE elo_scores (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    score INTEGER DEFAULT 1200,                   -- 初始 ELO 分
    tier VARCHAR(20) DEFAULT 'bronze',            -- bronze/silver/gold/platinum/diamond
    total_matches INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    win_rate DECIMAL(5,4) DEFAULT 0.0000,
    k_factor INTEGER DEFAULT 32,                  -- 新手32, 成熟玩家16
    region VARCHAR(64),                           -- 地区（用于地区排行）
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

CREATE INDEX idx_elo_scores_score ON elo_scores(score DESC);
CREATE INDEX idx_elo_scores_region ON elo_scores(region, score DESC);

-- =============================================
-- 3. 商户表 (Merchants)
-- =============================================
CREATE TABLE merchants (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id), -- 关联管理员用户
    name VARCHAR(128) NOT NULL,
    description TEXT,
    address VARCHAR(256),
    latitude DECIMAL(10, 7),                      -- 纬度
    longitude DECIMAL(10, 7),                     -- 经度
    geohash VARCHAR(12),                          -- GeoHash 索引
    phone VARCHAR(20),
    rating DECIMAL(3, 2) DEFAULT 0.00,
    cover_image VARCHAR(512),
    photos JSONB DEFAULT '[]',                    -- 商户图片数组
    business_hours VARCHAR(128),
    bank_account VARCHAR(64),                     -- 结算银行账户
    commission_rate DECIMAL(4, 3) DEFAULT 0.100,  -- 平台佣金比例，默认10%
    status VARCHAR(20) DEFAULT 'pending',         -- pending / active / suspended
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_merchants_geohash ON merchants(geohash);
CREATE INDEX idx_merchants_status ON merchants(status);

-- =============================================
-- 4. 餐饮套餐表 (Dining Packages)
-- =============================================
CREATE TABLE dining_packages (
    id BIGSERIAL PRIMARY KEY,
    merchant_id BIGINT NOT NULL REFERENCES merchants(id),
    name VARCHAR(128) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,                -- 售价（元）
    original_price DECIMAL(10, 2),                -- 原价
    cover_image VARCHAR(512),
    validity_days INTEGER DEFAULT 30,             -- 有效天数
    inventory INTEGER DEFAULT 999,                -- 库存
    sold_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',          -- active / offline / soldout
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_dining_packages_merchant ON dining_packages(merchant_id, status);

-- =============================================
-- 5. 订单表 (Orders)
-- =============================================
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    order_no VARCHAR(64) UNIQUE NOT NULL,         -- 订单号（业务唯一）
    user_id BIGINT NOT NULL REFERENCES users(id),
    order_type VARCHAR(30) NOT NULL,              -- dining_package / event_reg / club_membership / matchmaking_deposit / withdrawal
    target_id BIGINT,                             -- 关联业务 ID（套餐ID/赛事ID等）
    amount DECIMAL(10, 2) NOT NULL,               -- 支付金额
    wechat_transaction_id VARCHAR(64),            -- 微信支付交易号
    status VARCHAR(20) DEFAULT 'pending',         -- pending / paid / refunded / cancelled / failed
    paid_at TIMESTAMP WITH TIME ZONE,
    refunded_at TIMESTAMP WITH TIME ZONE,
    verification_code VARCHAR(64),                -- 核销码（餐饮套餐用）
    verification_qr_url VARCHAR(512),             -- 核销二维码 URL
    verified_at TIMESTAMP WITH TIME ZONE,         -- 核销时间
    expires_at TIMESTAMP WITH TIME ZONE,          -- 核销码过期时间
    idempotency_key VARCHAR(64) UNIQUE,           -- 幂等键，防止重复支付
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_orders_user ON orders(user_id, created_at DESC);
CREATE INDEX idx_orders_order_no ON orders(order_no);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_verification ON orders(verification_code) WHERE verification_code IS NOT NULL;

-- =============================================
-- 6. 分账记录表 (Revenue Splits)
-- =============================================
CREATE TABLE revenue_splits (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(id),
    receiver_type VARCHAR(20) NOT NULL,           -- platform / merchant / organizer
    receiver_id BIGINT NOT NULL,                  -- 收款方 ID
    amount DECIMAL(10, 2) NOT NULL,               -- 分账金额
    ratio DECIMAL(4, 3) NOT NULL,                 -- 分账比例
    wechat_split_id VARCHAR(64),                  -- 微信分账单号
    status VARCHAR(20) DEFAULT 'pending',         -- pending / completed / failed
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_revenue_splits_order ON revenue_splits(order_id);
CREATE INDEX idx_revenue_splits_receiver ON revenue_splits(receiver_type, receiver_id);

-- =============================================
-- 7. 数字钱包表 (Wallets)
-- =============================================
CREATE TABLE wallets (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL,                     -- 用户/商户 ID
    owner_type VARCHAR(20) NOT NULL,              -- user / merchant
    balance DECIMAL(12, 2) DEFAULT 0.00,          -- 可用余额
    frozen_balance DECIMAL(12, 2) DEFAULT 0.00,   -- 冻结金额
    total_income DECIMAL(12, 2) DEFAULT 0.00,     -- 累计收入
    total_withdrawal DECIMAL(12, 2) DEFAULT 0.00, -- 累计提现
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(owner_id, owner_type)
);

-- =============================================
-- 8. 钱包流水表 (Wallet Transactions)
-- =============================================
CREATE TABLE wallet_transactions (
    id BIGSERIAL PRIMARY KEY,
    wallet_id BIGINT NOT NULL REFERENCES wallets(id),
    order_id BIGINT REFERENCES orders(id),
    type VARCHAR(30) NOT NULL,                    -- income / expense / withdrawal / refund / deposit_freeze / deposit_release
    amount DECIMAL(10, 2) NOT NULL,
    balance_after DECIMAL(12, 2) NOT NULL,        -- 交易后余额
    description VARCHAR(256),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_wallet_transactions_wallet ON wallet_transactions(wallet_id, created_at DESC);

-- =============================================
-- 9. 组局表 (Matchmaking Requests)
-- =============================================
CREATE TABLE matchmaking_requests (
    id BIGSERIAL PRIMARY KEY,
    creator_id BIGINT NOT NULL REFERENCES users(id),
    title VARCHAR(128),
    scheduled_time TIMESTAMP WITH TIME ZONE NOT NULL,
    location_name VARCHAR(128),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    radius_km INTEGER DEFAULT 5,                  -- 匹配范围（公里）
    min_elo INTEGER,                              -- 最低段位要求
    max_elo INTEGER,                              -- 最高段位要求
    industry_tag VARCHAR(64),                     -- 行业标签
    required_players INTEGER DEFAULT 4,           -- 所需人数（掼蛋通常4人）
    current_players INTEGER DEFAULT 1,            -- 当前已加入人数
    deposit_amount DECIMAL(10, 2) DEFAULT 0.00,   -- AA 保证金金额
    status VARCHAR(20) DEFAULT 'open',            -- open / confirmed / cancelled / completed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_matchmaking_scheduled ON matchmaking_requests(scheduled_time, status);
CREATE INDEX idx_matchmaking_location ON matchmaking_requests(latitude, longitude);

-- =============================================
-- 10. 组局参与者表 (Matchmaking Participants)
-- =============================================
CREATE TABLE matchmaking_participants (
    id BIGSERIAL PRIMARY KEY,
    request_id BIGINT NOT NULL REFERENCES matchmaking_requests(id),
    user_id BIGINT NOT NULL REFERENCES users(id),
    deposit_order_id BIGINT REFERENCES orders(id),
    status VARCHAR(20) DEFAULT 'joined',          -- joined / cancelled / forfeited
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    cancelled_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(request_id, user_id)
);

-- =============================================
-- 11. 赛事表 (Events)
-- =============================================
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    organizer_id BIGINT NOT NULL REFERENCES users(id),
    club_id BIGINT,                               -- 可选：所属俱乐部
    title VARCHAR(128) NOT NULL,
    description TEXT,
    event_type VARCHAR(30) DEFAULT 'official',    -- official / chamber / club
    scheduled_time TIMESTAMP WITH TIME ZONE NOT NULL,
    location VARCHAR(256),
    entry_fee DECIMAL(10, 2) DEFAULT 0.00,
    max_capacity INTEGER,
    current_registrations INTEGER DEFAULT 0,
    cancellation_deadline TIMESTAMP WITH TIME ZONE,
    refund_policy TEXT,
    commission_rate DECIMAL(4, 3) DEFAULT 0.100,  -- 平台抽成比例
    status VARCHAR(20) DEFAULT 'upcoming',        -- upcoming / ongoing / completed / cancelled
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_events_time ON events(scheduled_time, status);
CREATE INDEX idx_events_organizer ON events(organizer_id);

-- =============================================
-- 12. 赛事报名表 (Event Registrations)
-- =============================================
CREATE TABLE event_registrations (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id),
    user_id BIGINT NOT NULL REFERENCES users(id),
    order_id BIGINT REFERENCES orders(id),
    status VARCHAR(20) DEFAULT 'registered',      -- registered / checked_in / cancelled / refunded
    checked_in_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(event_id, user_id)
);

-- =============================================
-- 13. 比赛成绩表 (Match Results)
-- =============================================
CREATE TABLE match_results (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT REFERENCES events(id),
    matchmaking_id BIGINT REFERENCES matchmaking_requests(id),
    player1_id BIGINT NOT NULL REFERENCES users(id),
    player2_id BIGINT NOT NULL REFERENCES users(id),
    player1_score INTEGER,
    player2_score INTEGER,
    winner_id BIGINT REFERENCES users(id),
    elo_change_p1 INTEGER,                        -- 玩家1 ELO 变化
    elo_change_p2 INTEGER,                        -- 玩家2 ELO 变化
    recorded_by BIGINT REFERENCES users(id),      -- 记录人（组织者）
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_match_results_event ON match_results(event_id);
CREATE INDEX idx_match_results_players ON match_results(player1_id, player2_id);

-- =============================================
-- 14. 俱乐部表 (Clubs)
-- =============================================
CREATE TABLE clubs (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    cover_image VARCHAR(512),
    owner_id BIGINT NOT NULL REFERENCES users(id),
    region VARCHAR(64),
    membership_fee DECIMAL(10, 2) DEFAULT 0.00,   -- 会费（0 为免费）
    max_members INTEGER DEFAULT 200,
    current_members INTEGER DEFAULT 1,
    avg_elo DECIMAL(8, 2) DEFAULT 1200.00,
    total_matches INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',          -- active / suspended / disbanded
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_clubs_region ON clubs(region, status);

-- =============================================
-- 15. 俱乐部成员表 (Club Members)
-- =============================================
CREATE TABLE club_members (
    id BIGSERIAL PRIMARY KEY,
    club_id BIGINT NOT NULL REFERENCES clubs(id),
    user_id BIGINT NOT NULL REFERENCES users(id),
    role VARCHAR(20) DEFAULT 'member',            -- owner / admin / member
    status VARCHAR(20) DEFAULT 'pending',         -- pending / active / removed
    order_id BIGINT REFERENCES orders(id),        -- 付费入会关联订单
    joined_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(club_id, user_id)
);

-- =============================================
-- 16. 帖子表 (Posts - 掼友圈)
-- =============================================
CREATE TABLE posts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    images JSONB DEFAULT '[]',                    -- 图片URL数组，最多9张
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'published',       -- published / reviewing / rejected / deleted
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_posts_user ON posts(user_id, created_at DESC);
CREATE INDEX idx_posts_timeline ON posts(status, created_at DESC);

-- =============================================
-- 17. 评论表 (Comments)
-- =============================================
CREATE TABLE comments (
    id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL REFERENCES posts(id),
    user_id BIGINT NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    parent_id BIGINT REFERENCES comments(id),     -- 回复评论
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_comments_post ON comments(post_id, created_at);

-- =============================================
-- 18. 点赞表 (Likes)
-- =============================================
CREATE TABLE likes (
    id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL REFERENCES posts(id),
    user_id BIGINT NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(post_id, user_id)
);

-- =============================================
-- 19. 文章表 (Articles - 资讯)
-- =============================================
CREATE TABLE articles (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(256) NOT NULL,
    content TEXT NOT NULL,                         -- 富文本内容
    cover_image VARCHAR(512),
    category VARCHAR(30) NOT NULL,                 -- news / tutorial / culture
    author_id BIGINT REFERENCES users(id),
    view_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'published',
    published_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_articles_category ON articles(category, published_at DESC);

-- =============================================
-- 20. 广告表 (Advertisements)
-- =============================================
CREATE TABLE advertisements (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    image_url VARCHAR(512) NOT NULL,
    redirect_url VARCHAR(512),
    slot_position VARCHAR(30) NOT NULL,           -- feed_inline / banner_top / detail_bottom
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    impression_count INTEGER DEFAULT 0,
    click_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_ads_slot ON advertisements(slot_position, status, start_time, end_time);
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: ELO Score Conservation

*For any* two players with valid ELO scores and a match result, the ELO calculation SHALL produce new scores where: (a) the winner's score increases, (b) the loser's score decreases or stays at 0, (c) the K-factor is 32 for players with fewer than 30 matches and 16 otherwise, and (d) the score change magnitude is bounded by the K-factor.

**Validates: Requirements 6.1, 13.4**

### Property 2: ELO Tier Assignment Consistency

*For any* ELO score, the assigned tier (Bronze/Silver/Gold/Platinum/Diamond) SHALL be deterministic and correspond to exactly one tier based on configured score thresholds. For any two scores where score_a > score_b, the tier of score_a SHALL be greater than or equal to the tier of score_b.

**Validates: Requirements 6.6**

### Property 3: Leaderboard Ordering Invariant

*For any* leaderboard query result (personal, club, or regional), the returned entries SHALL be sorted in strictly descending order by ELO score, such that for consecutive entries at positions i and i+1, score[i] >= score[i+1].

**Validates: Requirements 6.4**

### Property 4: Haversine Distance Properties

*For any* two valid GPS coordinate pairs (lat1, lon1) and (lat2, lon2) where latitude ∈ [-90, 90] and longitude ∈ [-180, 180], the Haversine distance SHALL satisfy: (a) non-negativity: d(a,b) >= 0, (b) identity: d(a,a) = 0, (c) symmetry: d(a,b) = d(b,a), and (d) upper bound: d(a,b) <= π * 6371 km (half Earth circumference).

**Validates: Requirements 3.6, 15.1**

### Property 5: LBS Radius Query Correctness

*For any* user coordinate, radius R (1-50km), and set of merchant locations, all merchants returned by the radius query SHALL have Haversine distance <= R from the user, AND the results SHALL be sorted in ascending order by distance.

**Validates: Requirements 3.2, 3.3, 15.4**

### Property 6: Revenue Split Sum Invariant

*For any* payment amount and set of commission rate configurations (where all rates sum to 1.0), the Revenue_Split_Engine SHALL produce split amounts that: (a) sum exactly to the total payment amount (accounting for rounding to 2 decimal places), and (b) each individual split equals floor/round(amount * rate) with rounding residual assigned to the primary receiver.

**Validates: Requirements 10.2, 10.6**

### Property 7: Deposit Refund Policy Completeness

*For any* matchmaking participation cancellation with a scheduled_time and cancel_time, the deposit disposition SHALL be: (a) forfeited if (scheduled_time - cancel_time) < 2 hours, or (b) fully refunded if (scheduled_time - cancel_time) >= 2 hours. These two conditions form a complete partition—every cancellation falls into exactly one category.

**Validates: Requirements 4.4, 4.5**

### Property 8: Payment Idempotency

*For any* order with a given idempotency_key, submitting the same payment request N times (N >= 1) SHALL result in exactly one successful payment record and one charge to the user. Subsequent requests with the same idempotency_key SHALL return the existing payment result without creating new transactions.

**Validates: Requirements 14.6**

### Property 9: Matchmaking Status Transition

*For any* matchmaking request with required_players = N, when the current_players count reaches N, the status SHALL transition to "confirmed". While current_players < N, the status SHALL remain "open". The transition is monotonic—once confirmed, the status SHALL not revert to "open".

**Validates: Requirements 4.6**

### Property 10: Filter Query Correctness

*For any* set of filter criteria (ELO range, distance, time slot, industry tag, region, activity level) applied to a list query (matchmaking, clubs, or transactions), every item in the returned results SHALL satisfy ALL specified filter criteria simultaneously.

**Validates: Requirements 4.7, 8.1, 11.5**

### Property 11: Event Capacity Enforcement

*For any* event where current_registrations >= max_capacity, new registration attempts SHALL be rejected. The system SHALL never allow current_registrations to exceed max_capacity.

**Validates: Requirements 5.4**

### Property 12: Withdrawal Balance Constraint

*For any* withdrawal request with amount W and wallet with available balance B, the request SHALL be rejected if W > B. After a successful withdrawal of amount W, the new balance SHALL equal B - W.

**Validates: Requirements 9.5**

### Property 13: Verification Code Uniqueness

*For any* set of N generated verification codes across all orders, all N codes SHALL be distinct (no two orders share the same verification code).

**Validates: Requirements 10.3**

### Property 14: Expired Code Rejection

*For any* verification code where current_time > expires_at, a redemption attempt SHALL be rejected. Only codes where current_time <= expires_at AND status != "redeemed" SHALL be accepted for redemption.

**Validates: Requirements 10.5**

### Property 15: Content Feed Ordering

*For any* paginated feed query result, posts SHALL be returned in strictly descending order by created_at timestamp. For any two consecutive posts in the result, post[i].created_at >= post[i+1].created_at.

**Validates: Requirements 2.1, 7.4**

### Property 16: RBAC Access Control

*For any* API request from a user with role R, access to endpoints requiring a higher privilege role SHALL be denied with HTTP 403. The role hierarchy is: user < organizer < merchant < admin (super admin has access to all).

**Validates: Requirements 11.1**

## Error Handling

### Error Response Format

All API errors follow a consistent JSON structure:

```json
{
  "code": "ERROR_CODE",
  "message": "Human-readable error description",
  "details": {}
}
```

### Error Categories and Strategies

| Category | HTTP Status | Strategy | Example |
|----------|-------------|----------|---------|
| Validation Error | 400 | Return field-level error details | Missing required matchmaking fields |
| Authentication Error | 401 | Clear JWT, redirect to login | Expired/invalid token |
| Authorization Error | 403 | Log attempt, return forbidden | User accessing admin endpoint |
| Resource Not Found | 404 | Return resource type and ID | Event/club/order not found |
| Conflict | 409 | Return current state | Duplicate like, duplicate order |
| Rate Limited | 429 | Return retry-after header | Too many API calls |
| Payment Error | 502 | Retry with backoff, notify user | WeChat Pay timeout |
| Internal Error | 500 | Log full stack trace, return generic message | Unexpected exceptions |

### Payment Error Handling

1. **WeChat Pay Timeout**: Retry up to 3 times with exponential backoff (1s, 2s, 4s). If all retries fail, mark order as "pending" and schedule background reconciliation.
2. **Callback Signature Verification Failure**: Reject the callback, log the event for security review. Do NOT update order status.
3. **Duplicate Payment Callback**: Check idempotency_key. If order already paid, return success without re-processing.
4. **Refund Failure**: Mark refund as "pending_retry", schedule retry within 30 minutes. Alert operations team after 3 failed attempts.
5. **Revenue Split Failure**: Revenue split operates asynchronously. If WeChat split API fails, queue for retry. Merchant funds remain in platform escrow until split succeeds.

### LBS Error Handling

1. **Location Permission Denied**: Fall back to city-level recommendations using user's registered city or IP geolocation.
2. **Redis GEO Query Failure**: Fall back to PostgreSQL geohash-based query (slower but reliable).
3. **Invalid Coordinates**: Validate latitude ∈ [-90, 90] and longitude ∈ [-180, 180] at API layer. Reject with 400 if invalid.

### ELO Engine Error Handling

1. **Invalid Match Result**: Reject if winner_id not in [player1_id, player2_id], or if match already processed.
2. **Score Update Race Condition**: Use PostgreSQL row-level locking (SELECT FOR UPDATE) on elo_scores during calculation to prevent concurrent modification.
3. **Redis Leaderboard Sync Failure**: ELO scores are authoritative in PostgreSQL. Redis leaderboard is eventually consistent—schedule background sync every 60 seconds.

### Content Moderation Error Handling

1. **Sensitive Word Filter Timeout**: If the content filter service is unavailable, queue the post for manual review (status = "reviewing") rather than rejecting outright.
2. **Image Upload Failure**: Return specific error indicating which image(s) failed. Allow retry without re-uploading successful images.

## Testing Strategy

### Testing Approach

The platform uses a dual testing approach combining property-based tests for universal invariants and example-based tests for specific scenarios and integration points.

### Property-Based Testing

**Library**: [Hypothesis](https://hypothesis.readthedocs.io/) (Python)

Property-based tests target the pure logic layers of the system:
- **ELO Engine**: Score calculation, tier assignment, K-factor selection
- **LBS Service**: Haversine distance calculation, radius filtering, distance sorting
- **Revenue Split Engine**: Commission calculation, sum invariants, rounding behavior
- **Matchmaking Logic**: Deposit policy, status transitions, filter correctness
- **Payment Service**: Idempotency guarantees, balance constraints

Each property test:
- Runs a minimum of **100 iterations** with randomly generated inputs
- References its design document property with a tag comment
- Tag format: **Feature: shen-guan-hui-platform, Property {number}: {property_text}**

### Unit Tests (Example-Based)

Unit tests cover specific scenarios, edge cases, and error conditions:
- JWT token issuance and validation (specific token formats, expiry scenarios)
- Content feed pagination (boundary pages, empty results)
- Event registration flow (capacity reached, deadline passed)
- Verification code generation and redemption (specific valid/expired/used scenarios)
- RBAC permission checks (specific role-endpoint combinations)
- Error response formatting

### Integration Tests

Integration tests verify external service interactions and data flow:
- WeChat OAuth login flow (mocked WeChat API)
- WeChat Pay order creation and callback handling (mocked payment gateway)
- Redis GEO query integration (real Redis instance)
- PostgreSQL transaction isolation (real database)
- Full payment → split → verification flow (end-to-end with mocks)

### Test Infrastructure

```
tests/
├── conftest.py                  # Shared fixtures, test database setup
├── properties/                  # Property-based tests
│   ├── test_elo_properties.py   # Properties 1, 2, 3
│   ├── test_lbs_properties.py   # Properties 4, 5
│   ├── test_revenue_properties.py  # Property 6
│   ├── test_matchmaking_properties.py  # Properties 7, 9, 10
│   ├── test_payment_properties.py  # Properties 8, 12, 13, 14
│   └── test_feed_properties.py  # Property 15
├── unit/                        # Example-based unit tests
│   ├── test_auth.py
│   ├── test_content.py
│   ├── test_events.py
│   ├── test_clubs.py
│   ├── test_wallet.py
│   └── test_rbac.py             # Property 16
└── integration/                 # Integration tests
    ├── test_wechat_pay.py
    ├── test_wechat_auth.py
    ├── test_redis_geo.py
    └── test_full_payment_flow.py
```

### Test Execution

```bash
# Run all tests
pytest

# Run property tests only (minimum 100 iterations each)
pytest tests/properties/ --hypothesis-seed=random

# Run unit tests
pytest tests/unit/

# Run integration tests (requires Docker services)
pytest tests/integration/ --docker
```

