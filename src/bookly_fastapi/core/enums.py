from enum import Enum


class CatalogStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class UserRole(str, Enum):
    READER = "reader"
    MODERATOR = "moderator"
    ADMIN = "admin"


class UserStatus(str, Enum):
    PENDING = "pending"       
    ACTIVE = "active"         
    BANNED = "banned"         
    DEACTIVATED = "deactivated"   

class ReviewStatus(str, Enum):
    PUBLISHED = "published"
    FLAGGED = "flagged"
    HIDDEN = "hidden"
    DELETED = "deleted"
