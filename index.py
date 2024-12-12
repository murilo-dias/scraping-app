import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from entities.merchant_open_delivery import Menu, Merchant, Status

from transform import (
    UUID5,
    transform_basic_info,
    transform_service,
    transform_menu,
)


load_dotenv()

LATITUDE = os.getenv("LATITUDE")
LONGITUDE = os.getenv("LONGITUDE")
URL_SITE = os.getenv("URL_SITE")
URL_WEBHOOK = os.getenv("URL_WEBHOOK")

MERCHANT_OPEN_DELIVERY: Merchant

if not LATITUDE or not LONGITUDE or not URL_SITE or not URL_WEBHOOK:
    raise ValueError("Uma ou mais variáveis de ambiente estão ausentes.")


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        def handle_route_merchant(route, request):
            if (
                "https://marketplace.ifood.com.br/v1/merchant-info/graphql"
                in request.url
            ):
                new_url = f"https://marketplace.ifood.com.br/v1/merchant-info/graphql?latitude={LATITUDE}&longitude={LONGITUDE}&channel=IFOOD"

                route.continue_(url=new_url)

        def handle_route_catalog(route, request):
            if "https://marketplace.ifood.com.br/v1/merchants/" in request.url:
                merchantId = request.url.split("/")[5]

                new_url = f"https://marketplace.ifood.com.br/v1/merchants/{merchantId}/catalog?latitude={LATITUDE}&longitude={LONGITUDE}"

                route.continue_(url=new_url)

        page.route("**/v1/merchant-info/graphql*", handle_route_merchant)
        page.route("**/v1/merchants/*/catalog", handle_route_catalog)

        def handle_response(response):
            global MERCHANT_OPEN_DELIVERY

            if (
                "https://marketplace.ifood.com.br/v1/merchant-info/graphql"
                in response.url
            ):
                merchant = response.json().get("data").get("merchant")
                merchantExtra = response.json().get("data").get("merchantExtra")
                cnpj = merchantExtra.get("documents").get("CNPJ").get("value")
                catalogGroup = merchant.get("contextSetup").get("catalogGroup")

                menu = Menu(
                    id=UUID5(catalogGroup),
                    name="IFood",
                    description="Menu importado do IFood",
                    externalCode=catalogGroup,
                    categoryId=[],
                )

                MERCHANT_OPEN_DELIVERY = Merchant(
                    id=UUID5(cnpj),
                    lastUpdate=datetime.now().isoformat(),
                    TTL=86400,
                    status=(
                        Status.AVAILABLE
                        if merchant.get("available") == True
                        else Status.UNAVAILABLE
                    ),
                    basicInfo=transform_basic_info(
                        merchant=merchant, merchantExtra=merchantExtra
                    ),
                    menus=[menu],
                    services=transform_service(
                        merchant=merchant, merchantExtra=merchantExtra, menuId=menu.id
                    ),
                )

            if "https://marketplace.ifood.com.br/v1/merchants/" in response.url:
                catalogIfood = response.json().get("data").get("menu")

                result = transform_menu(
                    catalogIfood, menus=MERCHANT_OPEN_DELIVERY.menus
                )

                MERCHANT_OPEN_DELIVERY.categories = result.get("categories")
                MERCHANT_OPEN_DELIVERY.itemOffers = result.get("itemOffers")
                MERCHANT_OPEN_DELIVERY.items = result.get("items")
                MERCHANT_OPEN_DELIVERY.optionGroups = result.get("optionGroups")

        page.on("response", handle_response)

        page.goto(URL_SITE)

        page.wait_for_load_state("networkidle")

        context.close()

        result = requests.post(
            URL_WEBHOOK,
            json=MERCHANT_OPEN_DELIVERY.model_dump(),
        )
        if result.status_code == 200:
            print(result)


run()
