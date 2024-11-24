import uuid
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests
from entities.merchant_open_delivery import Merchant, Status
from transform import transform_basic_info, transform_service, transform_menu

latitude = -16.6201783
longitude = -49.3436878
urlSite = "https://www.ifood.com.br/delivery/goiania-go/subway---jardim-curitiba-jardim-curitiba/ad7accaa-afb7-443c-bb5e-7a924f3ad137"


def UUID5(value: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, value))


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
            if (
                "https://marketplace.ifood.com.br/v1/merchant-info/graphql"
                in response.url
            ):
                merchant = response.json().get("data").get("merchant")
                merchantExtra = response.json().get("data").get("merchantExtra")
                cnpj = merchantExtra.get("documents").get("CNPJ").get("value")

                menu = transform_menu(merchant.get("contextSetup").get("catalogGroup"))

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
                    services=transform_service(
                        merchant=merchant,
                        merchantExtra=merchantExtra,
                        menuId=menu.id,
                    ),
                    menus=[menu],
                )

                result = requests.post(
                    "https://webhook.site/59bdf0e1-5f9e-4a81-b6a3-c1d41684642d",
                    data=merchantOpenDelivery.model_dump_json(indent=2),
                    headers={"Content-Type": "application/json"},
                )
                if result.status_code == 200:
                    print(result)

            if "https://marketplace.ifood.com.br/v1/merchants/" in response.url:
                response.json().get("data")

        page.on("response", handle_response)

        page.goto(urlSite)

        page.wait_for_load_state("networkidle")

        context.close()


run()
