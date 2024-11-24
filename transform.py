import uuid
from typing import List
from datetime import datetime, timedelta

from entities.merchant_open_delivery import (
    Address,
    BasicInfo,
    ContactPhones,
    Currecy,
    Image,
    MerchantCategories,
    MerchantType,
    MinOrderValue,
    Service,
    Status,
)


def UUID4() -> str:
    return str(uuid.uuid4())


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
            currency=Currecy.BRL.value,
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
                    Status.AVAILABLE.value
                    if deliveryMethod.get("state") == "ELIGIBLE"
                    else Status.UNAVAILABLE.value
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
