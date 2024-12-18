import requests
from playwright.sync_api import sync_playwright

latitude = -16.6201783
longitude = -49.3436878
urlSite = "https://www.ifood.com.br/delivery/goiania-go/subway---jardim-curitiba-jardim-curitiba/ad7accaa-afb7-443c-bb5e-7a924f3ad137"


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        merchantData = []

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
                merchantData.append(
                    {
                        "merchantId": 1,
                        "type": "ifoodMerchant",
                        "data": response.json().get("data"),
                    }
                )

            if "https://marketplace.ifood.com.br/v1/merchants/" in response.url:
                merchantData.append(
                    {
                        "merchantId": 1,
                        "type": "ifoodCatalog",
                        "data": response.json().get("data"),
                    }
                )

        page.on("response", handle_response)

        page.goto(urlSite)

        page.wait_for_load_state("networkidle")

        if len(merchantData) == 2:
            result = requests.post(
                "https://webhook.site/dc42a828-d61e-4184-aae8-22a8d4e99d3d",
                json=merchantData,
            )
            if result.status_code == 200:
                print(result)

        context.close()


run()
