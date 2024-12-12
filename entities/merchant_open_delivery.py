from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class MerchantType(str, Enum):
    RESTAURANT = "RESTAURANT"


class Currency(str, Enum):
    BRL = "BRL"


class Status(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"


class ServiceType(str, Enum):
    DELIVERY = "DELIVERY"
    TAKEOUT = "TAKEOUT"


class DayOfWeek(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class Unit(str, Enum):
    UN = "UN"
    KG = "KG"
    OZ = "OZ"
    LB = "LB"
    GAL = "GAL"


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
    currency: Currency


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
    createdAt: str


class TimePeriods(BaseModel):
    startTime: str
    endTime: str


class WeekHour(BaseModel):
    dayOfWeek: List[DayOfWeek] = None
    timePeriods: TimePeriods


class ServiceHour(BaseModel):
    id: str
    weekHours: List[WeekHour]


class Service(BaseModel):
    id: str
    status: Status
    serviceType: ServiceType
    menuId: str
    serviceHours: ServiceHour


class Menu(BaseModel):
    id: str
    name: str
    description: str
    externalCode: str
    disclaimer: Optional[str] = None
    categoryId: Optional[List[str]] = None


class Category(BaseModel):
    id: str
    index: Optional[int] = None
    name: str
    description: Optional[str] = None
    image: Optional[Image] = None
    externalCode: str
    status: Optional[Status] = Status.AVAILABLE
    availabilityId: Optional[List[str]] = []
    itemOfferId: Optional[List[str]] = []


class Price(BaseModel):
    value: float
    originalValue: float
    currency: Currency


class ItemOffer(BaseModel):
    id: str
    itemId: str
    index: Optional[int] = None
    status: Optional[Status] = Status.AVAILABLE
    price: Price
    availabilityId: Optional[List[str]] = []
    optionGroupsId: Optional[List[str]] = []


class Item(BaseModel):
    id: str
    name: str
    description: str
    externalCode: str
    status: Optional[Status] = Status.AVAILABLE
    image: Optional[Image] = None
    serving: Optional[int] = None
    unit: Optional[Unit] = Unit.UN
    ean: Optional[str] = None


class Option(BaseModel):
    id: str
    itemId: Optional[str]
    index: Optional[int]
    status: Optional[Status] = Status.AVAILABLE
    price: Price
    maxPermitted: int


class OptionGroup(BaseModel):
    id: str
    index: int
    name: str
    description: Optional[str] = None
    externalCode: str
    status: Optional[Status] = Status.AVAILABLE
    minPermitted: int
    maxPermitted: int
    options: Optional[List[Option]] = []


class Merchant(BaseModel):
    lastUpdate: str
    TTL: int
    id: str
    status: Status
    basicInfo: BasicInfo
    menus: List[Menu]
    services: List[Service]
    categories: Optional[List[Category]] = []
    itemOffers: Optional[List[ItemOffer]] = []
    items: Optional[List[Item]] = []
    optionGroups: Optional[List[OptionGroup]] = []
