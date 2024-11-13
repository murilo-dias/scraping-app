import json
from playwright.sync_api import sync_playwright

latitude = -16.7266117
longitude = -49.2745076
urlSite = "https://www.ifood.com.br/delivery/goiania-go/subway---parque-amazonia-parque-amazonia/55c9bff8-f810-42d6-9242-421a82a8754e"


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

        def hadle_response(response):
            if (
                "https://marketplace.ifood.com.br/v1/merchant-info/graphql"
                in response.url
            ):
                print("URL da API:", response.url)
                print("Status:", response.status)

                try:
                    formatted_json = json.dumps(response.json(), indent=4)
                    print("Resposta JSON:", formatted_json)
                except:
                    print("A resposta não está em formato JSON.")

            if "https://marketplace.ifood.com.br/v1/merchants/" in response.url:
                print("URL da API:", response.url)
                print("Status:", response.status)

                try:
                    formatted_json = json.dumps(response.json(), indent=4)
                    print("Resposta JSON:", formatted_json)
                except:
                    print("A resposta não está em formato JSON.")

        page.on("response", hadle_response)

        page.goto(urlSite)

        page.wait_for_load_state("networkidle")

        context.close()


run()
