from typing import List, Dict, Optional
from pydantic import BaseModel


class ContextSetup(BaseModel):
    catalogGroup: str
    context: str
    regionGroup: str


class DeliveryFee(BaseModel):
    originalValue: float
    type: str
    value: float


class Shift(BaseModel):
    dayOfWeek: int | str
    startTime: str
    endTime: str
    interval: int


class TimeSlot(BaseModel):
    availableLoad: int
    date: str
    endDateTime: int
    endTime: str
    id: str
    isAvailable: bool
    originalPrice: int
    price: int
    startDateTime: int
    startTime: str


class Schedule(BaseModel):
    now: bool
    shifts: List[Shift]
    timeSlots: List[TimeSlot]


class DeliveryMethod(BaseModel):
    catalogGroup: str
    deliveredBy: str
    id: str
    maxTime: int
    minTime: int
    mode: str
    originalValue: Optional[float] = None
    priority: int
    schedule: Schedule
    state: str
    subtitle: str
    title: str
    type: str
    value: float


class MainCategory(BaseModel):
    code: str
    name: str


class MainCategoryMerchantExtra(BaseModel):
    code: str
    description: str
    friendlyName: str


class Resource(BaseModel):
    fileName: str
    type: str


class Address(BaseModel):
    city: str
    country: str
    district: str
    latitude: float
    longitude: float
    state: str
    streetName: Optional[str] = None
    streetNumber: Optional[str] = None
    timezone: Optional[str] = None
    zipCode: Optional[str] = None


class Category(BaseModel):
    code: str
    description: str
    friendlyName: str


class Configs(BaseModel):
    bagItemNoteLength: str
    chargeDifferentToppingsMode: str
    nationalIdentificationNumberRequired: bool
    orderNoteLength: str


class Document(BaseModel):
    type: str
    value: str


class Group(BaseModel):
    externalId: str
    id: str
    name: str
    type: str


class MetadataBanner(BaseModel):
    action: str
    image: str
    priority: str
    title: str


class Metadata(BaseModel):
    ifoodClub: Dict[str, MetadataBanner]


class ShiftMerchantExtra(BaseModel):
    dayOfWeek: str
    duration: int
    start: str


class MerchantExtra(BaseModel):
    address: Address
    categories: List[Category]
    companyCode: str
    configs: Configs
    deliveryTime: int
    description: str
    documents: Dict[str, Document]
    enabled: bool
    features: List[str]
    groups: List[Group]
    id: str
    locale: str
    mainCategory: MainCategoryMerchantExtra
    merchantChain: Dict[str, str]
    metadata: Metadata
    minimumOrderValue: int
    minimumOrderValueV2: int
    name: str
    phoneIf: str
    priceRange: str
    resources: List[Resource]
    shifts: List[ShiftMerchantExtra]
    shortId: int
    tags: List[str]
    takeoutTime: int
    userRatingCount: float


class Merchant(BaseModel):
    available: bool
    availableForScheduling: bool
    contextSetup: ContextSetup
    currency: str
    deliveryFee: DeliveryFee
    deliveryMethods: List[DeliveryMethod]
    deliveryTime: int
    distance: float
    features: List[str]
    id: str
    mainCategory: MainCategory
    minimumOrderValue: int
    name: str
    paymentCodes: List[str]
    preparationTime: int
    priceRange: str
    resources: List[Resource]
    slug: str
    tags: List[str]
    takeoutTime: int
    userRating: float


class Data(BaseModel):
    merchant: Merchant
    merchantExtra: MerchantExtra


class MerchantIfood(BaseModel):
    data: Data
