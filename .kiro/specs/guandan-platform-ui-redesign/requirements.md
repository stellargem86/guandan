# Requirements Document

## Introduction

本文档定义掼蛋社交平台 UI 全面重构项目的功能需求。平台整合掼蛋牌局社交、餐饮商户发现、赛事管理和俱乐部功能，采用深红色+金色主视觉风格，移动端基于 uni-app (Vue 3 + TypeScript)，管理后台基于 Vue 3 + Vite + Tailwind CSS。

## Glossary

- **Platform**: 掼蛋社交平台整体系统
- **Mobile_App**: 基于 uni-app 的移动端应用（微信小程序 + H5）
- **Admin_Panel**: 基于 Vue 3 + Tailwind 的管理后台
- **Circle_Module**: 掼友圈模块，包含论坛帖子、地图找局、商户发现功能
- **Event_Module**: 赛事模块，包含赛事管理、报名支付、天梯排行功能
- **Club_Module**: 俱乐部模块，包含俱乐部管理、聊天、活动功能
- **News_Module**: 资讯模块，包含文章、教程、文化内容展示
- **Profile_Module**: 个人中心模块，包含用户信息、订单、钱包、设置
- **Payment_System**: 微信支付集成系统，处理报名费和商户订单
- **Map_Service**: 腾讯地图服务，提供商户定位和距离计算
- **Design_System**: 设计令牌系统，定义颜色、间距、圆角等视觉规范
- **ELO_Engine**: 基于 ELO 算法的掼蛋积分计算引擎
- **User**: 使用移动端的注册用户
- **Merchant**: 入驻平台的餐饮/茶室/棋牌室商户
- **Organizer**: 赛事组织者，拥有赛事发布和管理权限
- **Administrator**: 平台管理员，拥有后台全部权限

## Requirements

### Requirement 1: 设计系统与公共组件

**User Story:** As a developer, I want a unified design system with reusable components, so that the UI remains consistent across all pages and development is efficient.

#### Acceptance Criteria

1. THE Design_System SHALL define color tokens including primary (#C41E3A), gold (#D4A843), background, surface, and semantic colors (success, warning, error)
2. THE Design_System SHALL define spacing tokens (xs through xl), border radius tokens (sm through full), and font size tokens (xs through 2xl) using rpx units
3. WHEN a UI component is rendered, THE Mobile_App SHALL apply the card-based layout with rounded corners and shadow tokens from the Design_System
4. THE Mobile_App SHALL provide reusable components including Card, TabBar, MatchCard, MerchantCard, EventCard, RankingItem, ClubCard, ArticleCard, and PaymentButton
5. WHEN the app launches, THE Mobile_App SHALL display a bottom tab bar with five tabs: 掼友圈, 赛事, 资讯, 俱乐部, 我的

### Requirement 2: 掼友圈论坛与帖子

**User Story:** As a user, I want to browse and publish posts in the Guandan community circle, so that I can share experiences and connect with other players.

#### Acceptance Criteria

1. WHEN a user opens the Circle_Module, THE Mobile_App SHALL display a tab bar with filters (最新, 好友, 地图) and a scrollable feed of posts
2. WHEN a user pulls down on the post feed, THE Circle_Module SHALL refresh the data and reset pagination
3. WHEN a user scrolls to the bottom of the feed, THE Circle_Module SHALL load the next page of posts
4. WHEN a user creates a post, THE Circle_Module SHALL validate that content length is between 1 and 2000 characters
5. WHEN a user creates a post with images, THE Circle_Module SHALL validate that the image count does not exceed 9
6. WHEN a user creates a post with valid content, THE Circle_Module SHALL persist the post and display it in the feed
7. WHEN a user taps a post in the feed, THE Mobile_App SHALL navigate to the post detail page showing full content, images, and comments

### Requirement 3: 地图找局与商户发现

**User Story:** As a user, I want to discover nearby merchants on a map, so that I can find suitable venues for playing Guandan.

#### Acceptance Criteria

1. WHEN a user opens the map page, THE Map_Service SHALL obtain the current location and display nearby merchants as markers on the map
2. WHEN a user selects a merchant category filter (全部, 餐饮, 茶室, 棋牌), THE Circle_Module SHALL display only merchants matching that category
3. WHEN a user taps a merchant marker, THE Mobile_App SHALL display the merchant detail card with name, rating, distance, and tags
4. THE Map_Service SHALL return only merchants within the specified radius, ordered by distance ascending
5. WHEN the user's location cannot be obtained, THE Map_Service SHALL display a default city center position and show a location failure message
6. WHEN a user opens a merchant detail page, THE Mobile_App SHALL display merchant photos, business hours, phone, packages, and reviews
7. THE Platform SHALL validate that merchant ratings are within the range 0.0 to 5.0

### Requirement 4: 组局与约局功能

**User Story:** As a user, I want to create or join Guandan match sessions, so that I can easily find players and arrange games.

#### Acceptance Criteria

1. WHEN a user creates a match, THE Circle_Module SHALL validate that the maximum players is 4 (fixed four-player game)
2. WHEN a user creates a match, THE Circle_Module SHALL collect title, time, location, and optional tags
3. WHEN a user views the match list, THE Circle_Module SHALL display match cards showing host info, time, location, current/max players, and status
4. WHEN a match reaches maximum capacity, THE Circle_Module SHALL update the match status to 'full' and prevent further joins
5. WHEN a user uses matchmaking, THE Circle_Module SHALL find available matches based on location and preferences

### Requirement 5: 赛事列表与详情

**User Story:** As a user, I want to browse tournaments and view event details, so that I can decide which events to participate in.

#### Acceptance Criteria

1. WHEN a user opens the Event_Module, THE Mobile_App SHALL display event cards with title, time, location, prize pool, registration fee, and participant count
2. WHEN a user selects an event tab filter (全部, 圈内, 进行中, 已结束), THE Event_Module SHALL display only events matching the filter
3. WHEN a user taps an event card, THE Mobile_App SHALL navigate to the event detail page showing rules, prize settings, schedule, and registration deadline
4. WHEN a user pulls down on the event list, THE Event_Module SHALL refresh the data and reset pagination
5. WHEN a user scrolls to the bottom of the event list, THE Event_Module SHALL load the next page of events

### Requirement 6: 赛事报名与支付

**User Story:** As a user, I want to register and pay for tournaments, so that I can secure my participation in events.

#### Acceptance Criteria

1. WHEN a user clicks "立即报名" on an event, THE Event_Module SHALL verify that the event status is 'registration' and remaining slots are sufficient
2. WHEN a user submits a registration, THE Payment_System SHALL create a pending order with amount equal to (registrationFee × quantity) + deposit
3. WHEN an order is created, THE Payment_System SHALL set the payment deadline to 30 minutes from creation time
4. WHEN the payment countdown reaches zero, THE Payment_System SHALL disable the payment button and display an expiration message
5. WHEN a user confirms payment, THE Payment_System SHALL invoke WeChat Pay and process the payment callback
6. WHEN payment is successful, THE Payment_System SHALL update the order status to 'paid' and increment the event participant count
7. IF a user has already registered for the same event, THEN THE Event_Module SHALL reject the duplicate registration
8. IF concurrent registrations exceed available slots, THEN THE Payment_System SHALL use a distributed lock to prevent overselling
9. WHEN a payment order expires, THE Payment_System SHALL mark the order status as 'expired' and the order SHALL NOT be payable

### Requirement 7: 天梯排行榜

**User Story:** As a user, I want to view player and club rankings, so that I can track my progress and compare with others.

#### Acceptance Criteria

1. WHEN a user opens the rankings page, THE Event_Module SHALL display a tab switch between personal rankings and club rankings
2. WHEN a user selects a level filter (全部, 初级, 中级, 高级), THE Event_Module SHALL display only rankings matching that level
3. THE Event_Module SHALL display the top three players with highlighted styling (podium display)
4. THE Event_Module SHALL order all ranking entries by score in descending order
5. WHEN two players have equal scores, THE ELO_Engine SHALL rank them by most recent match time
6. THE Event_Module SHALL display each ranking entry with rank number, avatar, nickname, score, and tier

### Requirement 8: ELO 积分计算

**User Story:** As a platform operator, I want accurate ELO score calculations after each match, so that player rankings reflect true skill levels.

#### Acceptance Criteria

1. WHEN a four-player match completes, THE ELO_Engine SHALL calculate score changes for all four players based on their finishing positions
2. THE ELO_Engine SHALL ensure the sum of all score deltas in a single match is zero (zero-sum property, allowing rounding tolerance)
3. THE ELO_Engine SHALL calculate expected win probability using the formula: 1 / (1 + 10^((opponent_score - player_score) / 400))
4. THE ELO_Engine SHALL normalize score changes by dividing by the number of opponents (3) for four-player games
5. WHEN a higher-ranked player beats a lower-ranked player, THE ELO_Engine SHALL award fewer points than beating a higher-ranked player

### Requirement 9: 俱乐部管理

**User Story:** As a user, I want to create, join, and manage clubs, so that I can organize regular Guandan activities with a community.

#### Acceptance Criteria

1. WHEN a user creates a club, THE Club_Module SHALL validate that the club name is between 2 and 20 characters
2. WHEN a user views the club list, THE Mobile_App SHALL display club cards with logo, name, member count, location, tags, and description
3. WHEN a user taps a club card, THE Mobile_App SHALL navigate to the club detail page with tabs for notices, activities, achievements, and stats
4. THE Club_Module SHALL maintain member count consistency: club.memberCount equals the count of active members in that club
5. WHEN a club owner publishes a notice, THE Club_Module SHALL mark it with a pin option and display it prominently

### Requirement 10: 俱乐部聊天

**User Story:** As a club member, I want to chat with other members in real-time, so that I can coordinate activities and socialize.

#### Acceptance Criteria

1. WHEN a user enters the club chat, THE Club_Module SHALL establish a WebSocket connection and load recent message history
2. WHEN a user sends a message, THE Club_Module SHALL broadcast the message to all online members in real-time
3. WHEN the WebSocket connection is lost, THE Club_Module SHALL attempt automatic reconnection with exponential backoff (1s, 2s, 4s, 8s, max 30s)
4. WHEN reconnection succeeds, THE Club_Module SHALL fetch messages that were sent during the disconnection period
5. THE Club_Module SHALL display each message with sender avatar, nickname, content, and timestamp

### Requirement 11: 资讯内容展示

**User Story:** As a user, I want to read news, tutorials, and cultural content about Guandan, so that I can improve my skills and stay informed.

#### Acceptance Criteria

1. WHEN a user opens the News_Module, THE Mobile_App SHALL display article cards with title, thumbnail, source, publish time, view count, and category
2. WHEN a user selects a category tab (推荐, 新闻, 教程, 文化, 体育), THE News_Module SHALL filter articles by that category
3. WHEN a user taps an article card, THE Mobile_App SHALL navigate to the article detail page with full rich-text content
4. WHEN a user likes or bookmarks an article, THE News_Module SHALL persist the action and update the count display
5. WHEN a user pulls down on the article list, THE News_Module SHALL refresh the data and reset pagination

### Requirement 12: 个人中心

**User Story:** As a user, I want to view my profile, stats, orders, and settings, so that I can manage my account and track my activity.

#### Acceptance Criteria

1. WHEN a user opens the Profile_Module, THE Mobile_App SHALL display user avatar, nickname, points, match count, win count, and honor score
2. THE Profile_Module SHALL provide a grid menu with quick access to wallet, orders, badges, favorites, and history
3. WHEN a user navigates to the orders page, THE Profile_Module SHALL display order history with status, amount, and type
4. WHEN a user navigates to settings, THE Profile_Module SHALL provide options for profile editing, notification preferences, privacy, and logout

### Requirement 13: 管理后台

**User Story:** As an administrator, I want a comprehensive backend panel, so that I can manage users, events, merchants, clubs, content, and finances.

#### Acceptance Criteria

1. WHEN an administrator logs in, THE Admin_Panel SHALL display a dashboard with key metrics (users, events, revenue, active clubs)
2. THE Admin_Panel SHALL provide CRUD interfaces for managing users, events, merchants, clubs, and content
3. WHEN an organizer logs into their portal, THE Admin_Panel SHALL display event management, check-in, scoreboard, and reports views
4. WHEN a merchant logs into their portal, THE Admin_Panel SHALL display package management, dashboard, and settlement views
5. THE Admin_Panel SHALL support role-based access control with distinct permissions for admin, organizer, and merchant roles

### Requirement 14: 性能与用户体验

**User Story:** As a user, I want fast page loads and smooth interactions, so that the app feels responsive and enjoyable to use.

#### Acceptance Criteria

1. THE Mobile_App SHALL display skeleton screens during initial page loads to improve perceived performance
2. THE Mobile_App SHALL implement image lazy loading for list pages to reduce initial load time
3. THE Mobile_App SHALL achieve first contentful paint (FCP) within 1.5 seconds
4. THE Mobile_App SHALL maintain list scrolling frame rate at 55fps or above
5. THE Platform SHALL achieve API response time (P95) under 200 milliseconds
6. THE Mobile_App SHALL use sub-packages (分包加载) to reduce the main package size

### Requirement 15: 安全与数据保护

**User Story:** As a platform operator, I want secure authentication and data protection, so that user data and financial transactions are safe.

#### Acceptance Criteria

1. THE Platform SHALL authenticate users with JWT tokens (access_token: 2 hours, refresh_token: 7 days)
2. THE Platform SHALL enforce role-based access control (user, merchant, organizer, admin) on all API endpoints
3. WHEN a payment callback is received, THE Payment_System SHALL verify the WeChat Pay signature before processing
4. THE Platform SHALL use parameterized queries to prevent SQL injection attacks
5. THE Platform SHALL filter rich-text content to prevent XSS attacks
6. WHEN displaying user phone numbers, THE Platform SHALL mask the middle digits for privacy
7. THE Payment_System SHALL ensure idempotent processing of payment callbacks to prevent duplicate transactions
