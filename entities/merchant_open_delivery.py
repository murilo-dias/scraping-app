from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from enums.merchant import MerchantStatus


class MinOrderValue(BaseModel):
    value: float
    currency: str


class Address(BaseModel):
    country: str
    state: str
    city: str
    district: str
    street: str
    number: str
    postalCode: str
    complement: str
    reference: str
    latitude: float
    longitude: float


class ContactPhones(BaseModel):
    commercialNumber: str
    whatsappNumber: str


class Image(BaseModel):
    URL: str
    CRC_32: str


class BasicInfo(BaseModel):
    name: str
    document: str
    corporateName: str
    description: str
    averageTicket: int
    averagePreparationTime: int
    minOrderValue: MinOrderValue
    merchantType: str
    merchantCategories: List[str]
    address: Address
    contactEmails: List[str]
    contactPhones: ContactPhones
    logoImage: Image
    bannerImage: Image
    createdAt: datetime


class Price(BaseModel):
    value: float
    currency: str


class GeoCoordinate(BaseModel):
    latitude: float
    longitude: float


class ServiceAreaPolygon(BaseModel):
    geoCoordinates: List[GeoCoordinate]
    price: Price
    estimateDeliveryTime: int


class Radius(BaseModel):
    size: float
    price: Price
    estimateDeliveryTime: int


class GeoRadius(BaseModel):
    geoMidpointLatitude: float
    geoMidpointLongitude: float
    radius: List[Radius]


class ServiceArea(BaseModel):
    id: str
    polygon: List[ServiceAreaPolygon]
    geoRadius: GeoRadius


class TimePeriod(BaseModel):
    startTime: str
    endTime: str


class WeekHours(BaseModel):
    dayOfWeek: List[str]
    timePeriods: TimePeriod


class HolidayHours(BaseModel):
    date: str
    timePeriods: TimePeriod


class ServiceHours(BaseModel):
    id: str
    weekHours: List[WeekHours]
    holidayHours: List[HolidayHours]


class Service(BaseModel):
    id: str
    status: str
    serviceType: str
    menuId: str
    serviceArea: ServiceArea
    serviceHours: ServiceHours


class ImageItem(BaseModel):
    URL: str
    CRC_32: str


class NutritionalInfo(BaseModel):
    description: str
    calories: str
    allergen: List[str]


class Item(BaseModel):
    id: str
    name: str
    description: str
    externalCode: str
    image: ImageItem
    serving: int
    unit: str
    nutritionalInfo: Optional[NutritionalInfo]


class Menu(BaseModel):
    id: str
    name: str
    description: str
    externalCode: str
    disclaimer: str
    categoryId: List[str]


class Category(BaseModel):
    id: str
    index: int
    name: str
    description: str
    image: Image
    externalCode: str
    status: str
    availabilityId: List[str]
    itemOfferId: List[str]


class AvailabilityHours(BaseModel):
    dayOfWeek: List[str]
    timePeriods: TimePeriod


class Availability(BaseModel):
    id: str
    startDate: str
    endDate: str
    hours: List[AvailabilityHours]


# Classe principal Merchant
class MerchantOpenDelivery(BaseModel):
    lastUpdate: str
    TTL: int
    id: str
    status: str
    basicInfo: Optional[BasicInfo] = None
    services: Optional[List[Service]] = None
    items: Optional[List[Item]] = None
    menus: Optional[List[Menu]] = None
    categories: Optional[List[Category]] = None
    availabilities: Optional[List[Availability]] = None
