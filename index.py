import json
from playwright.sync_api import sync_playwright
from pydantic import TypeAdapter


from entities.merchant_ifood import MerchantIfood
from transform import transform

latitude = -16.6201783
longitude = -49.3436878
urlSite = "https://www.ifood.com.br/delivery/goiania-go/subway---jardim-curitiba-jardim-curitiba/ad7accaa-afb7-443c-bb5e-7a924f3ad137"


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
                try:
                    responseData = response.json()
                    adapter = TypeAdapter(MerchantIfood)
                    merchantIfood = adapter.validate_python(responseData)

                    merchant = transform(merchantIfood=merchantIfood)

                    formatted_json = json.dumps(merchant.model_dump(), indent=2)
                    print(formatted_json)

                except json.JSONDecodeError:
                    print("Erro: A resposta não está em formato JSON.")
                except Exception as e:
                    print("Erro ao validar a resposta JSON:", str(e))

            if "https://marketplace.ifood.com.br/v1/merchants/" in response.url:
                try:
                    formatted_json = json.dumps(response.json(), indent=4)
                    ##print("Resposta JSON:", formatted_json)
                except:
                    print("A resposta não está em formato JSON.")

        page.on("response", handle_response)

        page.goto(urlSite)

        page.wait_for_load_state("networkidle")

        context.close()


run()
