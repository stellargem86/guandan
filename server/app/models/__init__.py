"""SQLAlchemy 数据模型

所有模型从 Base 继承，Alembic 通过 Base.metadata 自动检测表结构变更。
"""

from app.core.database import Base  # noqa: F401

# User
from app.models.user import User  # noqa: F401

# Merchant & Dining Packages
from app.models.merchant import DiningPackage, Merchant  # noqa: F401

# Orders & Revenue Splits
from app.models.order import Order, RevenueSplit  # noqa: F401

# Wallets & Transactions
from app.models.wallet import Wallet, WalletTransaction  # noqa: F401

# Matchmaking
from app.models.matchmaking import MatchmakingParticipant, MatchmakingRequest  # noqa: F401

# Events & Registrations
from app.models.event import Event, EventRegistration  # noqa: F401

# Clubs, Members & Activities
from app.models.club import Club, ClubActivity, ClubMember  # noqa: F401

# Posts, Comments & Likes
from app.models.post import Comment, Like, Post  # noqa: F401

# ELO Scores & Match Results
from app.models.elo import EloScore, MatchResult  # noqa: F401

# Articles & Advertisements
from app.models.content import Advertisement, Article  # noqa: F401
