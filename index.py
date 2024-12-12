from datetime import datetime
from playwright.sync_api import sync_playwright
import requests
from entities.merchant_open_delivery import Menu, Merchant, Status
from transform import (
    UUID5,
    transform_basic_info,
    transform_service,
    transform_menu,
)

latitude = -16.6201783
longitude = -49.3436878
urlSite = "https://www.ifood.com.br/delivery/goiania-go/subway-vera-cruz-conjunto-vera-cruz/8bf33c63-8572-4dd2-8281-c216d82c1116"


merchantOpenDelivery: Merchant


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
                new_url = f"https://marketplace.ifood.com.br/v1/merchant-info/graphql?latitude={latitude}&longitude={longitude}&channel=IFOOD"

                route.continue_(url=new_url)

        def handle_route_catalog(route, request):
            if "https://marketplace.ifood.com.br/v1/merchants/" in request.url:
                merchantId = request.url.split("/")[5]

                new_url = f"https://marketplace.ifood.com.br/v1/merchants/{merchantId}/catalog?latitude={latitude}&longitude={longitude}"

                route.continue_(url=new_url)

        page.route("**/v1/merchant-info/graphql*", handle_route_merchant)
        page.route("**/v1/merchants/*/catalog", handle_route_catalog)

        def handle_response(response):
            global merchantOpenDelivery

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

                merchantOpenDelivery = Merchant(
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
                ).model_dump()

            if "https://marketplace.ifood.com.br/v1/merchants/" in response.url:
                catalogIfood = response.json().get("data").get("menu")

                result = transform_menu(
                    catalogIfood, menus=merchantOpenDelivery.get("menus")
                )

                result = requests.post(
                    "https://webhook.site/b6ce4482-ef3f-467e-b4fa-fceb2cd3c89a",
                    json=merchantOpenDelivery,
                )
                if result.status_code == 200:
                    print(result)

        page.on("response", handle_response)

        page.goto(urlSite)

        page.wait_for_load_state("networkidle")

        context.close()


run()
