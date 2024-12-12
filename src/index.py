import requests
from datetime import datetime
from playwright.sync_api import sync_playwright
import logging

from load_env_vars import load_env_vars
from entities.merchant_open_delivery import Menu, Merchant, Status
from transform import (
    UUID5,
    transform_basic_info,
    transform_service,
    transform_menu,
)


MERCHANT_OPEN_DELIVERY: Merchant

# Carrega as variaveis de ambiente da aplicação
LATITUDE, LONGITUDE, URL_SITE, URL_WEBHOOK = load_env_vars()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run():
    try:
        with sync_playwright() as p:
            logger.info("Iniciando automação do navegador")

            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # Modifica a URL para incluir latitude e longitude nas requisições de merchant-info
            def handle_route_merchant(route, request):
                if (
                    "https://marketplace.ifood.com.br/v1/merchant-info/graphql"
                    in request.url
                ):
                    new_url = f"https://marketplace.ifood.com.br/v1/merchant-info/graphql?latitude={LATITUDE}&longitude={LONGITUDE}&channel=IFOOD"

                    route.continue_(url=new_url)

            # Modifica a URL para incluir o merchantId, latitude e longitude nas requisições de catalog
            def handle_route_catalog(route, request):
                if "https://marketplace.ifood.com.br/v1/merchants/" in request.url:
                    merchantId = request.url.split("/")[5]

                    new_url = f"https://marketplace.ifood.com.br/v1/merchants/{merchantId}/catalog?latitude={LATITUDE}&longitude={LONGITUDE}"

                    route.continue_(url=new_url)

            # Intercepta a URL em questão e aplica as funções de modificação de url
            page.route("**/v1/merchant-info/graphql*", handle_route_merchant)
            page.route("**/v1/merchants/*/catalog", handle_route_catalog)

            logger.info("configuração das url concluidas")

            # Função que lida com o response das requisições feitas pelo site
            def handle_response(response):
                global MERCHANT_OPEN_DELIVERY

                # Verica se e a URL que tem as informações do merchant-info
                if (
                    "https://marketplace.ifood.com.br/v1/merchant-info/graphql"
                    in response.url
                ):
                    logger.info("Iniciando extração de dados")

                    # Recupero as informações que preciso
                    merchant = response.json().get("data").get("merchant")
                    merchantExtra = response.json().get("data").get("merchantExtra")
                    cnpj = merchantExtra.get("documents").get("CNPJ").get("value")
                    catalogGroup = merchant.get("contextSetup").get("catalogGroup")

                    logger.info(
                        "Iniciando transformação dos dados para o padrão Open Delivery"
                    )

                    menu = Menu(
                        id=UUID5(catalogGroup),
                        name="IFood",
                        description="Menu importado do IFood",
                        externalCode=catalogGroup,
                        categoryId=[],
                    )

                    # Chama as função de transformação transform_basic_info() e transform_service()
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
                            merchant=merchant,
                            merchantExtra=merchantExtra,
                            menuId=menu.id,
                        ),
                    )

                # Verica se e a URL que tem as informações do catalogo
                if "https://marketplace.ifood.com.br/v1/merchants/" in response.url:

                    # Recupero as informações que preciso
                    catalogIfood = response.json().get("data").get("menu")

                    # Chama a função de transformação transform_menu()
                    result = transform_menu(
                        catalogIfood, menus=MERCHANT_OPEN_DELIVERY.menus
                    )

                    # Repaso o retorno da função transform_menu() para a variavel global MERCHANT_OPEN_DELIVERY
                    MERCHANT_OPEN_DELIVERY.categories = result.get("categories")
                    MERCHANT_OPEN_DELIVERY.itemOffers = result.get("itemOffers")
                    MERCHANT_OPEN_DELIVERY.items = result.get("items")
                    MERCHANT_OPEN_DELIVERY.optionGroups = result.get("optionGroups")

                    logger.info(
                        "Transformação dos dados para o padrão Open Delivery concluida"
                    )
                    logger.info("Extração de dados concluida")

            # Recupera o response de cada requisição e a repasa para a função handle_response()
            page.on("response", handle_response)

            logger.info("Carregando site do ifood")
            page.goto(URL_SITE)

            page.wait_for_load_state("networkidle")

            context.close()
    except KeyError as e:
        print(f"Erro ao acessar dados da resposta: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    try:
        logger.info("Iniciando envio para webhook")

        result = requests.post(URL_WEBHOOK, json=MERCHANT_OPEN_DELIVERY.model_dump())
        result.raise_for_status()

        logger.info("Webhook enviado com sucesso!")

    except requests.RequestException as e:
        print(f"Erro ao enviar para o webhook: {e}")


run()
