# Requirements Document

## Introduction

本需求文档基于掼蛋（Guandan）社交平台 UI 全面重构设计文档，定义了平台 13 个核心页面的功能需求。平台整合掼蛋牌局社交、餐饮商户发现、赛事管理和俱乐部功能，采用 uni-app (Vue 3 + TypeScript) 移动端与 Vue 3 + Vite 管理后台的技术架构。

## Glossary

- **Platform**: 掼蛋社交平台系统整体，包括移动端和管理后台
- **Mobile_App**: 基于 uni-app 的移动端应用
- **Admin_Panel**: 基于 Vue 3 + Vite + Tailwind CSS 的管理后台
- **API_Server**: 后端 RESTful API 服务
- **WebSocket_Server**: 实时消息推送服务（俱乐部聊天）
- **Payment_Service**: 微信支付集成服务
- **Map_Service**: 腾讯地图集成服务
- **Circle_Page**: 掼友圈首页（底部 Tab）
- **Event_Module**: 赛事功能模块
- **Club_Module**: 俱乐部功能模块
- **News_Module**: 资讯功能模块
- **Profile_Module**: 个人中心模块
- **ELO_Engine**: ELO 积分计算引擎
- **Ranking_Service**: 天梯排行榜服务
- **Registration_Service**: 赛事报名服务
- **Merchant_Service**: 商户查询服务
- **Content_Filter**: 内容安全过滤器（XSS/敏感词）
- **Design_Token_System**: 设计令牌系统（颜色、间距、圆角等统一规范）

## Requirements

### Requirement 1: 用户认证与会话管理

**User Story:** As a user, I want to log in via WeChat and maintain my session, so that I can access platform features securely.

#### Acceptance Criteria

1. WHEN a user opens the Mobile_App for the first time, THE Platform SHALL redirect to WeChat authorization login
2. WHEN WeChat authorization succeeds, THE API_Server SHALL issue a JWT access_token with 2-hour validity and a refresh_token with 7-day validity
3. WHEN the access_token expires, THE Mobile_App SHALL automatically refresh using the refresh_token without interrupting user activity
4. IF the refresh_token is also expired, THEN THE Mobile_App SHALL redirect the user to the login page
5. THE API_Server SHALL validate JWT signatures on every authenticated request

### Requirement 2: 掼友圈社交帖子

**User Story:** As a user, I want to browse and create posts in the Circle, so that I can share game experiences and interact with other players.

#### Acceptance Criteria

1. WHEN a user opens the Circle_Page, THE Mobile_App SHALL display a tab bar with "最新", "关注", "地图" tabs and a list of posts sorted by creation time descending
2. WHEN a user pulls down on the Circle_Page, THE Mobile_App SHALL refresh the post list and display loading indicators
3. WHEN a user scrolls to the bottom of the post list, THE Mobile_App SHALL load the next page of posts if more content is available
4. WHEN a user submits a new post with content length between 1 and 2000 characters and image count between 0 and 9, THE API_Server SHALL create the post and return it
5. IF a user attempts to create a post with content outside [1, 2000] characters, THEN THE API_Server SHALL reject the request with a validation error
6. IF a user attempts to upload more than 9 images for a post, THEN THE API_Server SHALL reject the request with a validation error
7. WHEN a user taps a post card, THE Mobile_App SHALL navigate to the post detail page showing full content, images, and comments

### Requirement 3: 地图找局与商户发现

**User Story:** As a user, I want to discover nearby merchants on a map, so that I can find venues for playing Guandan.

#### Acceptance Criteria

1. WHEN a user enters the map page, THE Mobile_App SHALL request location permission and display the user's current position on the map
2. WHEN the map loads with valid coordinates, THE Merchant_Service SHALL return merchants within the specified radius filtered by category
3. THE Mobile_App SHALL render merchant locations as map markers with category-specific icons
4. WHEN a merchant query result is returned, THE Merchant_Service SHALL order results by distance ascending and all returned merchants SHALL be within the specified radius
5. WHEN a user selects a category filter (全部/餐饮/茶楼/棋牌室), THE Merchant_Service SHALL return only merchants matching that category
6. WHEN a user taps a merchant marker, THE Mobile_App SHALL display a merchant detail card with name, rating, distance, and price information
7. THE Merchant_Service SHALL validate that merchant ratings are within [0.0, 5.0]
8. IF location permission is denied or GPS signal is unavailable, THEN THE Mobile_App SHALL display the default city center and provide a manual search input

### Requirement 4: 约局（组局匹配）

**User Story:** As a user, I want to create or join Guandan matches, so that I can find partners for a four-player game.

#### Acceptance Criteria

1. WHEN a user creates a match, THE API_Server SHALL create a match record with status 'open' and maxPlayers fixed at 4
2. WHEN a user joins an open match, THE API_Server SHALL increment currentPlayers by 1 and add the user to the participant list
3. THE Circle_Page SHALL display hot matches (up to 5) in a horizontal scroll area above the post feed
4. WHEN currentPlayers equals maxPlayers (4), THE API_Server SHALL update the match status to 'full' and reject additional join requests
5. WHEN a user taps a match card, THE Mobile_App SHALL navigate to the match detail page showing host info, time, location, and current participants

### Requirement 5: 赛事列表与详情

**User Story:** As a user, I want to browse tournaments and view details, so that I can find events to participate in.

#### Acceptance Criteria

1. WHEN a user opens the Event_Module list page, THE Mobile_App SHALL display events with tab filters: 全部, 圈子, 进行中, 已结束
2. WHEN a user selects a tab filter, THE API_Server SHALL return only events matching the selected status category
3. WHEN a user taps an event card, THE Mobile_App SHALL navigate to the event detail page showing rules, prize pool, schedule, and registration info
4. THE Mobile_App SHALL display each event card with title, cover image, start time, location, prize pool, registration fee, and participant count
5. WHEN the event detail page loads, THE Mobile_App SHALL show a "立即报名" button if event status is 'registration' and registration deadline has not passed

### Requirement 6: 赛事报名与支付

**User Story:** As a user, I want to register and pay for tournaments, so that I can participate in competitive Guandan events.

#### Acceptance Criteria

1. WHEN a user clicks "立即报名", THE Registration_Service SHALL verify event status is 'registration', remaining slots are sufficient, and the user has not already registered
2. WHEN registration validation passes, THE Registration_Service SHALL create a payment order with amount equal to (registrationFee × quantity) + deposit
3. THE Mobile_App SHALL display a payment page with order details, amount breakdown, and a 30-minute countdown timer
4. WHEN a user confirms payment, THE Mobile_App SHALL invoke WeChat Pay and await the payment result callback
5. WHEN Payment_Service receives a successful payment callback, THE API_Server SHALL update order status to 'paid', increment event currentParticipants, and create a registration record
6. THE Registration_Service SHALL use distributed locking to prevent concurrent registration from causing over-selling
7. IF a user already has an active registration for the same event, THEN THE Registration_Service SHALL reject the duplicate registration attempt
8. IF remaining event slots are insufficient for the requested quantity, THEN THE Registration_Service SHALL reject with "剩余名额不足" error
9. IF the payment countdown reaches zero, THEN THE Mobile_App SHALL disable the payment button and display "订单已过期"
10. WHEN processing payment callbacks, THE API_Server SHALL handle them idempotently so that duplicate callbacks do not cause duplicate participant increments

### Requirement 7: 天梯排行榜

**User Story:** As a user, I want to view rankings, so that I can see my competitive standing and compare with other players.

#### Acceptance Criteria

1. WHEN a user opens the rankings page, THE Mobile_App SHALL display two tabs: 个人榜 and 俱乐部榜
2. WHEN a tab is selected, THE Ranking_Service SHALL return rankings filtered by type (personal/club) and level filter
3. THE Mobile_App SHALL display the top 3 players in a highlighted podium layout with special styling
4. THE Ranking_Service SHALL return all ranking entries ordered by score descending
5. WHEN two entries have equal scores, THE Ranking_Service SHALL break the tie by most recent match time
6. WHEN level filter is applied (初级/中级/高级), THE Ranking_Service SHALL return only entries whose tier falls within the selected level range

### Requirement 8: ELO 积分计算

**User Story:** As a system, I want to calculate ELO scores after each match, so that player rankings reflect competitive performance accurately.

#### Acceptance Criteria

1. WHEN a four-player match completes with final rankings, THE ELO_Engine SHALL calculate score deltas for all four players
2. THE ELO_Engine SHALL ensure the sum of all score deltas is zero within a rounding tolerance of ±4
3. THE ELO_Engine SHALL use the standard ELO expected win probability formula: 1 / (1 + 10^((opponent_score - player_score) / 400))
4. THE ELO_Engine SHALL normalize each player's total delta by dividing by 3 (number of opponents)
5. WHEN a player beats a higher-rated opponent, THE ELO_Engine SHALL award more points than when beating a lower-rated opponent with the same K-factor

### Requirement 9: 俱乐部管理

**User Story:** As a user, I want to create, join, and manage clubs, so that I can organize regular Guandan activities with a community.

#### Acceptance Criteria

1. WHEN a user creates a club with a name between 2 and 20 characters, THE API_Server SHALL create the club and set the creator as owner
2. IF a club creation request has a name outside [2, 20] characters, THEN THE API_Server SHALL reject with a validation error
3. WHEN a user views a club detail page, THE Mobile_App SHALL display tabs for 公告, 活动, 成就, and 统计
4. THE API_Server SHALL maintain memberCount equal to the actual count of active members for each club
5. WHEN a club owner or admin manages the club, THE Mobile_App SHALL navigate to the management page with member administration and announcement posting capabilities

### Requirement 10: 俱乐部实时聊天

**User Story:** As a club member, I want to chat with other members in real time, so that I can coordinate activities and socialize.

#### Acceptance Criteria

1. WHEN a user enters the club chat page, THE Mobile_App SHALL establish a WebSocket connection and load recent message history
2. WHEN a user sends a text or image message, THE WebSocket_Server SHALL persist the message and broadcast it to all online club members
3. IF the WebSocket connection drops, THEN THE Mobile_App SHALL attempt reconnection using exponential backoff with delays following min(2^(n-1) × 1000ms, 30000ms)
4. WHEN reconnection succeeds, THE Mobile_App SHALL fetch and display messages missed during the disconnection period
5. THE Mobile_App SHALL display each message with sender avatar, nickname, content, and timestamp

### Requirement 11: 资讯浏览

**User Story:** As a user, I want to browse Guandan-related articles, so that I can learn strategies, follow news, and stay updated.

#### Acceptance Criteria

1. WHEN a user opens the News_Module page, THE Mobile_App SHALL display articles with category tabs: 推荐, 新闻, 教程, 文化, 体育
2. WHEN a user selects a category tab, THE API_Server SHALL return only articles matching that category
3. WHEN a user taps an article card, THE Mobile_App SHALL navigate to the article detail page with full rich-text content
4. THE Mobile_App SHALL display each article card with title, thumbnail, source, publish time, view count, and like count
5. WHEN a user likes or bookmarks an article, THE API_Server SHALL update the corresponding count and persist the user's action

### Requirement 12: 个人中心

**User Story:** As a user, I want to view my profile and access personal features, so that I can manage my account and track my progress.

#### Acceptance Criteria

1. WHEN a user opens the Profile_Module page, THE Mobile_App SHALL display user avatar, nickname, level, and statistics (积分, 场次, 胜率, 荣誉)
2. THE Mobile_App SHALL display a grid menu with quick access to common features (我的赛事, 我的俱乐部, 战绩记录, 成就徽章)
3. THE Mobile_App SHALL display a list menu with access to settings (钱包, 订单, 设置, 意见反馈)
4. WHEN a user taps a menu item, THE Mobile_App SHALL navigate to the corresponding sub-page

### Requirement 13: 管理后台

**User Story:** As an administrator, I want to manage platform content, users, and operations, so that I can maintain service quality and moderate the platform.

#### Acceptance Criteria

1. WHEN an admin logs into the Admin_Panel, THE Platform SHALL display a dashboard with key metrics (用户数, 赛事数, 收入, 活跃度)
2. THE Admin_Panel SHALL provide management pages for: 用户管理, 赛事管理, 俱乐部管理, 内容管理, 商户管理, 广告管理, 财务管理, 系统配置
3. WHEN a merchant logs into their portal, THE Admin_Panel SHALL display only merchant-specific features (仪表盘, 套餐管理, 核销, 结算)
4. WHEN an organizer logs into their portal, THE Admin_Panel SHALL display only organizer-specific features (仪表盘, 赛事管理, 签到, 计分板, 会员, 报表)
5. THE Admin_Panel SHALL enforce role-based access control so that each role (admin/merchant/organizer) only accesses authorized features

### Requirement 14: 设计系统与 UI 一致性

**User Story:** As a developer, I want a unified design token system, so that the platform maintains visual consistency across all pages.

#### Acceptance Criteria

1. THE Design_Token_System SHALL define primary color as #C41E3A (深红色) and accent color as #D4A843 (金色)
2. THE Mobile_App SHALL use card-based layouts with rounded corners following the defined radius tokens (8rpx/16rpx/24rpx/32rpx)
3. THE Mobile_App SHALL display skeleton screens during page loading to improve perceived performance
4. WHEN a list contains more than one screen of items, THE Mobile_App SHALL implement virtual scrolling to maintain frame rate at 55fps or above
5. THE Mobile_App SHALL implement sub-package loading (分包) to reduce initial bundle size

### Requirement 15: 安全与数据保护

**User Story:** As a platform operator, I want to ensure data security and prevent abuse, so that user data is protected and the system is resilient.

#### Acceptance Criteria

1. THE API_Server SHALL use HTTPS for all client-server communication
2. THE API_Server SHALL enforce RBAC permission checks on every authenticated endpoint, returning 403 for unauthorized access
3. THE API_Server SHALL use parameterized queries for all database operations to prevent SQL injection
4. THE Payment_Service SHALL verify WeChat Pay callback signatures before processing payment results
5. WHEN rich-text content is submitted, THE Content_Filter SHALL remove script tags, event handlers, and other XSS vectors while preserving safe content
6. WHEN displaying phone numbers to users, THE Platform SHALL mask the middle digits showing only the first 3 and last 4 digits
7. WHEN processing payment callbacks, THE API_Server SHALL use order number uniqueness constraints to ensure idempotent handling

### Requirement 16: 性能与可用性

**User Story:** As a user, I want the platform to load quickly and respond smoothly, so that I have a pleasant user experience.

#### Acceptance Criteria

1. THE Mobile_App SHALL achieve first contentful paint (FCP) in less than 1.5 seconds
2. THE API_Server SHALL respond to P95 of requests within 200 milliseconds
3. THE Mobile_App SHALL lazy-load images in list views so that off-screen images do not block rendering
4. THE Ranking_Service SHALL cache ranking data with a 5-minute refresh interval using Redis
5. WHEN rendering 100 map markers, THE Map_Service SHALL complete marker display within 500 milliseconds
