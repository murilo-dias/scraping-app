import json
from playwright.sync_api import sync_playwright

urlSite = "https://www.ifood.com.br/delivery/goiania-go/subway---parque-amazonia-parque-amazonia/55c9bff8-f810-42d6-9242-421a82a8754e"


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context()

        page = context.new_page()

        def handle_route(route, request):
            if (
                "https://marketplace.ifood.com.br/v1/merchant-info/graphql"
                in request.url
            ):
                new_url = "https://marketplace.ifood.com.br/v1/merchant-info/graphql?latitude=-16.7266117&longitude=-49.2745076&channel=IFOOD"

                print("Modificando a URL da requisição para:", new_url)

                route.continue_(url=new_url)

        page.route("**/v1/merchant-info/graphql*", handle_route)

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

        page.on("response", hadle_response)

        page.goto(urlSite)

        page.wait_for_load_state("networkidle")

        context.close()


run()
