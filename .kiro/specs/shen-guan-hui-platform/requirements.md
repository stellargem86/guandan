# Requirements Document

## Introduction

深掼会（Shen Guan Hui）是一个集掼蛋牌局社交、商务社交、本地餐饮生活服务为一体的综合平台。平台包含移动端应用（微信小程序优先，跨平台框架）和 Web 管理后台（SaaS 平台），服务于 C 端玩家用户、B 端商户及赛事/俱乐部组织者。

核心技术栈：
- 前端：uni-app 框架，Vue 3 + Vite + Tailwind CSS
- 后端：Python (FastAPI) 或 Node.js (NestJS)，RESTful API
- 数据库：PostgreSQL/MySQL + Redis（高频匹配撮合与 LBS 地理计算）

## Glossary

- **Platform（平台）**: 深掼会系统整体，包含移动端应用和 Web 管理后台
- **Mobile_App（移动端应用）**: 面向 C 端用户和 B 端组织者的微信小程序/跨平台移动应用
- **Admin_Backend（管理后台）**: Web 端 SaaS 管理系统，含平台管理、商户门户、俱乐部/赛事组织者门户
- **User（用户）**: 在移动端注册并使用平台的 C 端掼蛋玩家
- **Merchant（商户）**: 在平台入驻的餐饮/场地服务提供方
- **Organizer（组织者）**: 俱乐部管理员或赛事组织方
- **Matchmaking_Engine（撮合引擎）**: 处理一键组局请求的后端服务模块
- **LBS_Service（地理位置服务）**: 基于实时坐标提供距离计算和排序的服务模块
- **ELO_Engine（天梯积分引擎）**: 基于 ELO 算法计算和更新玩家动态积分的服务模块
- **Payment_Service（支付服务）**: 集成微信支付并处理分账逻辑的服务模块
- **Revenue_Split_Engine（分账引擎）**: 按可配置佣金比例自动分配资金到平台、商户、组织者的服务模块
- **Content_Feed（内容流）**: 掼友圈 UGC 图文帖子流
- **Guandan_Map（掼蛋地图）**: 基于 LBS 的餐厅/场地推荐地图功能
- **Ladder_Ranking（天梯排行榜）**: 基于 ELO 积分的个人/俱乐部/地区排行系统
- **Digital_Wallet（数字钱包）**: 用户在平台内的资金账户，支持充值、消费、提现
- **Club（俱乐部）**: 用户自组织的掼蛋社群组织
- **Dining_Package（餐饮套餐）**: 商户发布的可在线购买的餐饮服务套餐
- **Deposit（保证金）**: 用于防止组局爽约的 AA 制预付款

## Requirements

### Requirement 1: 用户注册与认证

**User Story:** 作为一名掼蛋爱好者，我希望能够快速注册并登录平台，以便使用所有社交和赛事功能。

#### Acceptance Criteria

1. WHEN a User opens the Mobile_App for the first time, THE Platform SHALL provide WeChat one-click authorization login
2. WHEN a User completes WeChat authorization, THE Platform SHALL create a user profile with nickname, avatar, and unique platform ID within 3 seconds
3. WHEN a User logs in successfully, THE Platform SHALL issue a JWT token with a configurable expiration period
4. IF a User's JWT token expires, THEN THE Platform SHALL redirect the User to re-authenticate without losing unsaved state
5. THE Platform SHALL store user credentials using bcrypt hashing with a minimum cost factor of 12

### Requirement 2: 掼友圈内容流（UGC Feed）

**User Story:** 作为一名掼蛋玩家，我希望在掼友圈浏览和发布图文动态，以便与牌友互动交流。

#### Acceptance Criteria

1. THE Content_Feed SHALL display image-text posts in reverse chronological order with infinite scroll pagination
2. WHEN a User submits a new post with text and up to 9 images, THE Content_Feed SHALL publish the post within 2 seconds
3. WHEN a User taps the like button on a post, THE Content_Feed SHALL increment the like count and provide visual feedback within 500ms
4. WHEN a User submits a comment on a post, THE Content_Feed SHALL append the comment in real-time and notify the post author
5. IF a post contains prohibited content, THEN THE Content_Feed SHALL reject the post and display a content policy violation message
6. THE Content_Feed SHALL support pull-to-refresh to load the latest posts

### Requirement 3: 掼蛋地图（LBS 场地推荐）

**User Story:** 作为一名掼蛋玩家，我希望通过地图发现附近的餐厅和场地，以便找到合适的打牌地点。

#### Acceptance Criteria

1. WHEN a User opens the Guandan_Map, THE LBS_Service SHALL request the User's real-time GPS coordinates
2. WHEN the LBS_Service receives User coordinates, THE Guandan_Map SHALL display nearby Merchant POI markers within a configurable default radius of 5km
3. THE Guandan_Map SHALL sort Merchant listings by distance from the User's current location in ascending order
4. WHEN a User taps a Merchant POI marker, THE Guandan_Map SHALL display the Merchant's detail card including name, distance, rating, available Dining_Packages, and photos
5. IF the LBS_Service fails to obtain User coordinates, THEN THE Guandan_Map SHALL display a prompt requesting location permission and fall back to city-level recommendations
6. THE LBS_Service SHALL calculate distances using the Haversine formula with Earth radius of 6371km

### Requirement 4: 一键组局（Matchmaking）

**User Story:** 作为一名掼蛋玩家，我希望快速发起或加入牌局，以便按时间、地点、段位找到合适的牌友。

#### Acceptance Criteria

1. WHEN a User creates a matchmaking request, THE Matchmaking_Engine SHALL require time, location, skill level (ladder rank), and industry fields
2. WHEN a matchmaking request is published, THE Matchmaking_Engine SHALL notify eligible Users within the specified location radius within 5 seconds
3. WHEN a User joins a matchmaking request, THE Payment_Service SHALL collect an AA Deposit from the joining User
4. IF a User cancels participation less than 2 hours before the scheduled time, THEN THE Payment_Service SHALL forfeit the User's Deposit
5. IF a User cancels participation 2 or more hours before the scheduled time, THEN THE Payment_Service SHALL refund the full Deposit within 24 hours
6. WHEN a matchmaking request reaches the required number of participants, THE Matchmaking_Engine SHALL change the request status to "confirmed" and notify all participants
7. THE Matchmaking_Engine SHALL filter matchmaking listings by ladder rank range, distance, time slot, and industry tag

### Requirement 5: 赛事管理

**User Story:** 作为一名掼蛋玩家，我希望查看和报名官方赛事及商会赛事，以便参加竞技比赛。

#### Acceptance Criteria

1. THE Mobile_App SHALL display a list of upcoming events with title, date, location, entry fee, and registration status
2. WHEN a User taps "Register" on an event, THE Payment_Service SHALL process the registration fee via WeChat Pay
3. WHEN payment is confirmed, THE Platform SHALL record the User's registration and display a confirmation with event details
4. IF an event reaches maximum capacity, THEN THE Platform SHALL disable the registration button and display "Registration Full"
5. WHEN an Organizer publishes a new event via the Admin_Backend, THE Mobile_App SHALL display the event in the event list within 30 seconds
6. IF a User cancels registration before the event's cancellation deadline, THEN THE Payment_Service SHALL process a refund according to the event's refund policy

### Requirement 6: 天梯排行榜系统

**User Story:** 作为一名掼蛋玩家，我希望通过天梯系统查看自己的段位和排名，以便了解自己的竞技水平。

#### Acceptance Criteria

1. THE ELO_Engine SHALL calculate dynamic scores using the ELO algorithm with a base K-factor of 32 for new players and 16 for established players
2. WHEN a match result is submitted, THE ELO_Engine SHALL update both players' ELO scores within 10 seconds
3. THE Ladder_Ranking SHALL provide three leaderboard views: personal ranking, Club ranking, and regional ranking
4. THE Ladder_Ranking SHALL update leaderboard positions in real-time after each score change
5. WHEN a User views the leaderboard, THE Ladder_Ranking SHALL display rank position, player name, ELO score, win rate, and total matches played
6. THE ELO_Engine SHALL define ladder tiers (e.g., Bronze, Silver, Gold, Platinum, Diamond) with configurable score thresholds

### Requirement 7: 资讯模块

**User Story:** 作为一名掼蛋爱好者，我希望阅读官方资讯、教程和文化文章，以便提升掼蛋知识和技巧。

#### Acceptance Criteria

1. THE Mobile_App SHALL display an information feed with articles categorized as official news, beginner tutorials, and cultural articles
2. WHEN a User opens an article, THE Mobile_App SHALL render rich-text content with images and embedded video support
3. THE Mobile_App SHALL reserve designated native advertisement slots within the information feed at configurable intervals
4. WHEN new articles are published by Platform administrators, THE Mobile_App SHALL display articles in reverse chronological order within the respective category

### Requirement 8: 俱乐部管理

**User Story:** 作为一名掼蛋玩家，我希望加入或创建俱乐部，以便与固定牌友组织活动和交流。

#### Acceptance Criteria

1. THE Mobile_App SHALL display a Club listing with search and filter capabilities by region, size, and activity level
2. WHEN a User applies to join a Club with paid membership, THE Payment_Service SHALL process the membership fee via WeChat Pay
3. WHEN a User is approved as a Club member, THE Platform SHALL grant access to the Club's internal circle including members-only chat, activities, and statistics
4. THE Club internal circle SHALL provide real-time messaging among Club members
5. WHEN a Club Organizer creates an activity within the Club, THE Platform SHALL notify all Club members within 60 seconds
6. THE Platform SHALL display Club statistics including total members, active members, average ELO score, and match count

### Requirement 9: 个人中心与数字钱包

**User Story:** 作为一名平台用户，我希望管理我的个人信息和资金，以便查看记录和进行提现操作。

#### Acceptance Criteria

1. THE Mobile_App SHALL display a personal profile page with avatar, nickname, ELO rank, honor badges, and certifications
2. THE Digital_Wallet SHALL display current balance, transaction history, and provide top-up and withdrawal functions
3. WHEN a User initiates a withdrawal, THE Payment_Service SHALL process the withdrawal to the User's bound WeChat account within 72 hours
4. THE Mobile_App SHALL display a complete history of event registrations with status (upcoming, completed, cancelled)
5. IF a withdrawal request exceeds the User's available balance, THEN THE Digital_Wallet SHALL reject the request and display an insufficient balance message

### Requirement 10: 餐饮套餐购买与核销流程

**User Story:** 作为一名掼蛋玩家，我希望在线购买餐饮套餐并到店核销，以便享受打牌配套的餐饮服务。

#### Acceptance Criteria

1. WHEN a User selects a Dining_Package and confirms purchase, THE Payment_Service SHALL process payment via WeChat Pay
2. WHEN payment is confirmed, THE Revenue_Split_Engine SHALL automatically split the payment amount according to configurable commission rates (e.g., Platform 10%, Merchant 90%)
3. WHEN the revenue split is completed, THE Platform SHALL generate a unique verification QR code for the User
4. WHEN the Merchant scans the verification QR code, THE Platform SHALL mark the Dining_Package as redeemed and record redemption timestamp
5. IF a Dining_Package verification code expires (configurable expiration period), THEN THE Platform SHALL invalidate the code and initiate a refund process
6. THE Revenue_Split_Engine SHALL support configurable commission rate distribution among Platform, Merchant, and Organizer (when applicable)
7. THE Platform SHALL provide the Merchant with a real-time dashboard displaying package sales count, revenue amount, and pending verifications

### Requirement 11: SaaS 管理后台 - 平台超级管理

**User Story:** 作为平台管理员，我希望通过 Web 后台管理全平台用户、内容和财务，以便确保平台运营安全高效。

#### Acceptance Criteria

1. THE Admin_Backend SHALL provide role-based access control with three portal levels: Super Admin, Merchant, and Organizer
2. WHEN a Super Admin logs into the Admin_Backend, THE Platform SHALL display a dashboard with key metrics including DAU, revenue, active events, and pending reviews
3. THE Admin_Backend SHALL provide content review tools to approve or reject User-generated posts and Merchant listings
4. THE Admin_Backend SHALL provide configuration interfaces for ELO_Engine parameters including K-factors, tier thresholds, and decay rules
5. THE Admin_Backend SHALL display all financial transactions with filtering by date range, transaction type, and participant
6. THE Admin_Backend SHALL provide advertisement placement management including slot configuration, scheduling, and performance metrics

### Requirement 12: SaaS 管理后台 - 商户门户

**User Story:** 作为入驻商户，我希望通过管理门户查看订单数据和进行提现，以便管理我的线上业务。

#### Acceptance Criteria

1. WHEN a Merchant logs into the Merchant Portal, THE Admin_Backend SHALL display a simplified dashboard with today's verifications, total sales, and available balance
2. THE Admin_Backend SHALL provide the Merchant with a verification page to scan User QR codes for Dining_Package redemption
3. THE Admin_Backend SHALL display Dining_Package sales data with daily, weekly, and monthly aggregation views
4. WHEN a Merchant initiates a withdrawal, THE Payment_Service SHALL process the withdrawal to the Merchant's bound bank account according to the configured settlement cycle
5. THE Admin_Backend SHALL allow Merchants to create and manage Dining_Package listings including name, price, description, validity period, and inventory count

### Requirement 13: SaaS 管理后台 - 俱乐部/赛事组织者门户

**User Story:** 作为俱乐部/赛事组织者，我希望通过管理门户管理会员、发布赛事和记录成绩，以便高效组织掼蛋活动。

#### Acceptance Criteria

1. THE Admin_Backend SHALL provide the Organizer with a member management interface displaying member list, join date, ELO score, and activity status
2. WHEN an Organizer publishes an event, THE Admin_Backend SHALL provide a one-click event creation form with fields for title, time, location, entry fee, capacity, and rules
3. THE Admin_Backend SHALL provide a check-in management interface for Organizers to verify participant attendance
4. WHEN an Organizer enters match scores, THE ELO_Engine SHALL process the results and update all participants' rankings
5. THE Admin_Backend SHALL provide a live scoreboard display page suitable for projection during events
6. THE Admin_Backend SHALL provide event revenue reports showing registration fees collected, commission deductions, and net Organizer earnings

### Requirement 14: 微信支付深度集成

**User Story:** 作为平台运营方，我希望系统深度集成微信支付，以便支持所有付费场景并实现自动分账。

#### Acceptance Criteria

1. THE Payment_Service SHALL integrate with WeChat Pay JSAPI for all in-app payment scenarios
2. WHEN a payment is initiated, THE Payment_Service SHALL create a WeChat Pay order with merchant ID, amount, description, and callback URL
3. WHEN THE Payment_Service receives a successful payment callback from WeChat Pay, THE Platform SHALL update the order status to "paid" within 5 seconds
4. THE Revenue_Split_Engine SHALL invoke WeChat Pay profit-sharing API to distribute funds according to configured ratios
5. IF a WeChat Pay callback indicates payment failure, THEN THE Payment_Service SHALL mark the order as "failed" and notify the User with retry options
6. THE Payment_Service SHALL maintain an idempotent transaction log to prevent duplicate payments for the same order
7. THE Payment_Service SHALL support refund processing via WeChat Pay refund API with configurable refund policies

### Requirement 15: LBS 地理位置计算服务

**User Story:** 作为平台技术团队，我希望实现高效的地理位置计算服务，以便支撑地图展示和组局匹配的核心功能。

#### Acceptance Criteria

1. THE LBS_Service SHALL store Merchant POI data with latitude, longitude, and geohash index in the database
2. THE LBS_Service SHALL use Redis GEO commands for high-frequency proximity queries with sub-100ms response time
3. WHEN a User's location is updated, THE LBS_Service SHALL recalculate nearby Merchant distances and return sorted results within 200ms
4. THE LBS_Service SHALL support radius-based queries with configurable range from 1km to 50km
5. THE LBS_Service SHALL batch-update Merchant POI coordinates when Merchants modify their address information
