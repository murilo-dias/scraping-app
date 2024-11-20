from datetime import datetime
from entities.merchant_open_delivery import (
    Address,
    BasicInfo,
    ContactPhones,
    Currecy,
    Image,
    MerchantCategories,
    MerchantType,
    MinOrderValue,
)


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
