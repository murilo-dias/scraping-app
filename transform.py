from datetime import datetime
from typing import List
import uuid

from entities.merchant_ifood import MerchantIfood
from entities.merchant_open_delivery import (
    ContactPhones,
    Image,
    MerchantOpenDelivery,
    BasicInfo,
    MinOrderValue,
    Address,
    Menu,
)
from enums.merchant import MerchantCategories, MerchantStatus, Currency, MerchantType


def generate_uuid(value: str):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, value))


def transformBaseInfo(merchantIfood: MerchantIfood) -> BasicInfo:
    merchant = merchantIfood.data.merchant
    merchantExtra = merchantIfood.data.merchantExtra
    return BasicInfo(
        name=merchantExtra.name,
        document=merchantExtra.documents["CNPJ"].value,
        corporateName=None,
        description=merchantExtra.description,
        averageTicket=None,
        averagePreparationTime=merchant.preparationTime,
        minOrderValue=MinOrderValue(
            currency=Currency.BRL, value=merchant.minimumOrderValue
        ),
        merchantType=MerchantType.RESTAURANTE,
        merchantCategories=[MerchantCategories.FAST_FOOD],
        address=Address(
            country=merchantExtra.address.country,
            state=merchantExtra.address.state,
            city=merchantExtra.address.city,
            district=merchantExtra.address.district,
            street=merchantExtra.address.streetName,
            number=merchantExtra.address.streetNumber,
            postalCode=merchantExtra.address.zipCode,
            complement=None,
            reference=None,
            latitude=merchantExtra.address.latitude,
            longitude=merchantExtra.address.longitude,
        ),
        contactEmails=[],
        contactPhones=ContactPhones(
            commercialNumber=merchantExtra.phoneIf, whatsappNumber=None
        ),
        logoImage=Image(
            CRC_32=None,
            URL=next(
                (r for r in merchant.resources if r.type == "LOGO"), None
            ).fileName,
        ),
        bannerImage=Image(
            CRC_32=None,
            URL=next(
                (r for r in merchant.resources if r.type == "HEADER"), None
            ).fileName,
        ),
        createdAt=None,
    )


def transformMenu(merchantIfoo: MerchantIfood) -> List[Menu]:
    merchant = merchantIfoo.data.merchant
    return [
        Menu(
            name="IFOOD",
            externalCode=merchant.contextSetup.catalogGroup,
        )
    ]


def transform(merchantIfood: MerchantIfood) -> MerchantOpenDelivery:
    merchant = merchantIfood.data.merchant
    merchantExtra = merchantIfood.data.merchantExtra

    menus = transformMenu(merchantIfoo=merchantIfood)

    return MerchantOpenDelivery(
        lastUpdate=datetime.now().isoformat(),
        TTL=86400,
        id=generate_uuid(merchantExtra.documents["CNPJ"].value),
        status=(
            MerchantStatus.AVAILABLE.value
            if merchant.available
            else MerchantStatus.UNAVAILABLE.value
        ),
        basicInfo=transformBaseInfo(merchantIfood=merchantIfood),
        menus=menus,
    )
