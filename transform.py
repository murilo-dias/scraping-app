import uuid
from typing import List
from datetime import datetime, timedelta

from entities.merchant_open_delivery import (
    Address,
    BasicInfo,
    Category,
    ContactPhones,
    Currency,
    Image,
    Item,
    MerchantCategories,
    MerchantType,
    MinOrderValue,
    Price,
    Service,
    Status,
    Menu,
    ItemOffer,
)


def UUID4() -> str:
    return str(uuid.uuid4())


def UUID5(value: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, value))


def transform_basic_info(merchant, merchantExtra) -> BasicInfo:
    address = merchantExtra.get("address")
    resources = merchant.get("resources")
    logo = next((res for res in resources if res["type"] == "LOGO"), None)
    banner = next((res for res in resources if res["type"] == "HEADER"), None)

    return BasicInfo(
        name=merchantExtra.get("name"),
        document=merchantExtra.get("documents").get("CNPJ").get("value"),
        description=merchantExtra.get("description"),
        averagePreparationTime=merchant.get("preparationTime"),
        minOrderValue=MinOrderValue(
            currency=Currency.BRL.value,
            value=merchant.get("minimumOrderValue"),
        ),
        merchantType=MerchantType.RESTAURANT.value,
        merchantCategories=[MerchantCategories.FAST_FOOD.value],
        address=Address(
            country=address.get("country"),
            state=address.get("state"),
            city=address.get("city"),
            district=address.get("district"),
            street=address.get("streetName"),
            number=address.get("streetNumber"),
            postalCode=address.get("zipCode"),
            latitude=address.get("latitude"),
            longitude=address.get("longitude"),
        ),
        contactPhones=ContactPhones(commercialNumber=merchantExtra.get("phoneIf")),
        logoImage=Image(URL=logo.get("fileName")),
        bannerImage=Image(URL=banner.get("fileName")),
        createdAt=datetime.now().isoformat(),
    )


def transform_service(merchant, merchantExtra, menuId) -> List[Service]:
    deliveryMethods = merchant.get("deliveryMethods")
    shifts = merchantExtra.get("shifts")

    def getEndTime(shift):
        startTime = datetime.strptime(shift.get("start"), "%H:%M:%S")
        endTime = startTime + timedelta(minutes=shift.get("duration"))

        return endTime.strftime("%H:%M:%S")

    timePeriods = list(
        {
            (shift.get("start"), getEndTime(shift=shift)): {
                "startTime": shift.get("start"),
                "endTime": getEndTime(shift=shift),
            }
            for shift in shifts
        }.values()
    )

    return list(
        map(
            lambda deliveryMethod: {
                "id": UUID4(),
                "status": (
                    Status.AVAILABLE
                    if deliveryMethod.get("state") == "ELIGIBLE"
                    else Status.UNAVAILABLE
                ),
                "serviceType": deliveryMethod.get("mode"),
                "menuId": menuId,
                "serviceHours": {
                    "id": UUID4(),
                    "weekHours": [
                        {
                            "dayOfWeek": list(
                                map(lambda shift: shift.get("dayOfWeek"), shifts)
                            ),
                            "timePeriods": timePeriods[0] if timePeriods else None,
                        }
                    ],
                },
            },
            deliveryMethods,
        )
    )


def transform_menu(catalogIfood, menus: List[Menu]):
    categories = []
    itemOffers = []
    items = []

    for index, catalog in enumerate(catalogIfood, start=0):
        categoryObj = Category(
            id=UUID5(catalog.get("code")),
            index=index,
            name=catalog.get("name"),
            externalCode=catalog.get("code"),
            itemOfferId=[],
        )

        for index, item in enumerate(catalog.get("itens"), start=0):
            itemObj = Item(
                id=UUID5(item.get("id")),
                name=item.get("description"),
                description=item.get("details", ""),
                externalCode=item.get("id"),
                image=Image(URL=item.get("logoUrl")),
            )

            itemOfferObj = ItemOffer(
                id=UUID5(itemObj.id),
                index=index,
                itemId=itemObj.id,
                price=Price(
                    value=item.get("unitMinPrice", 0.0),
                    originalValue=item.get("unitOriginalPrice", 0.0),
                    currency=Currency.BRL.value,
                ),
            )

            categoryObj.itemOfferId.append(itemOfferObj.id)
            items.append(itemObj.model_dump())
            itemOffers.append(itemOfferObj.model_dump())

        categories.append(categoryObj.model_dump())
        menus[0]["categoryId"] = [category.get("id") for category in categories]

    return {
        "menus": menus,
        "categories": categories,
        "itemOffers": itemOffers,
        "items": items,
    }
