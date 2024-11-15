from datetime import datetime
import uuid

from entities.merchant_ifood import MerchantIfood
from entities.merchant_open_delivery import MerchantOpenDelivery
from enums.merchant import MerchantStatus


def generate_uuid(value: str):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, value))


def transform(merchantIfood: MerchantIfood) -> MerchantOpenDelivery:
    merchant = merchantIfood.data.merchant
    merchantExtra = merchantIfood.data.merchantExtra

    return MerchantOpenDelivery(
        lastUpdate=datetime.now().isoformat(),
        TTL=86400,
        id=generate_uuid(merchantExtra.documents["CNPJ"].value),
        status=(
            MerchantStatus.AVAILABLE.value
            if merchant.available
            else MerchantStatus.UNAVAILABLE.value
        ),
    )
