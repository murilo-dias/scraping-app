from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class MerchantType(str, Enum):
    RESTAURANT = "RESTAURANT"


class Currecy(str, Enum):
    BRL = "BRL"


class Status(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"


class MerchantCategories(str, Enum):
    BURGERS = "BURGERS"
    PIZZA = "PIZZA"
    FAST_FOOD = "FAST_FOOD"
    HOT_DOG = "HOT_DOG"
    JAPANESE = "JAPANESE"
    DESSERTS = "DESSERTS"
    AMERICAN = "AMERICAN"
    ICE_CREAM = "ICE_CREAM"
    BBQ = "BBQ"
    SANDWICH = "SANDWICH"
    MEXICAN = "MEXICAN"
    BRAZILIAN = "BRAZILIAN"
    PASTRY = "PASTRY"
    ARABIAN = "ARABIAN"
    COMFORT_FOOD = "COMFORT_FOOD"
    VEGETARIAN = "VEGETARIAN"
    VEGAN = "VEGAN"
    BAKERY = "BAKERY"
    HEALTHY = "HEALTHY"
    ITALIAN = "ITALIAN"
    CHINESE = "CHINESE"
    JUICE_SMOOTHIES = "JUICE_SMOOTHIES"
    SEAFOOD = "SEAFOOD"
    CAFE = "CAFE"
    SALADS = "SALADS"
    COFFEE_TEA = "COFFEE_TEA"
    PASTA = "PASTA"
    BREAKFAST_BRUNCH = "BREAKFAST_BRUNCH"
    LATIN_AMERICAN = "LATIN_AMERICAN"
    CONVENIENCE = "CONVENIENCE"
    PUB = "PUB"
    HAWAIIAN = "HAWAIIAN"
    EUROPEAN = "EUROPEAN"
    FAMILY_MEALS = "FAMILY_MEALS"
    FRENCH = "FRENCH"
    INDIAN = "INDIAN"
    PORTUGUESE = "PORTUGUESE"
    SPANISH = "SPANISH"
    GOURMET = "GOURMET"
    KIDS_FRIENDLY = "KIDS_FRIENDLY"
    SOUTH_AMERICAN = "SOUTH_AMERICAN"
    SPECIALTY_FOODS = "SPECIALTY_FOODS"
    ARGENTINIAN = "ARGENTINIAN"
    PREMIUM = "PREMIUM"
    AFFORDABLE_MEALS = "AFFORDABLE_MEALS"


class MinOrderValue(BaseModel):
    value: float
    currency: Currecy


class Address(BaseModel):
    country: str
    state: str
    city: str
    district: str
    street: str
    number: str
    postalCode: str
    complement: Optional[str] = None
    reference: Optional[str] = None
    latitude: float
    longitude: float


class ContactPhones(BaseModel):
    commercialNumber: str
    whatsappNumber: Optional[str] = None


class Image(BaseModel):
    URL: str
    CRC_32: Optional[str] = None


class BasicInfo(BaseModel):
    name: str
    document: str
    corporateName: Optional[str] = None
    description: str
    averageTicket: Optional[float] = None
    averagePreparationTime: int
    minOrderValue: MinOrderValue
    merchantType: MerchantType
    merchantCategories: List[MerchantCategories]
    address: Address
    contactEmails: Optional[List[str]] = None
    contactPhones: ContactPhones
    logoImage: Image
    bannerImage: Image
    createdAt: datetime


class Merchant(BaseModel):
    lastUpdate: datetime
    TTL: int
    id: str
    status: Status
    basicInfo: BasicInfo
