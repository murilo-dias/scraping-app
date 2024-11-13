from dataclasses import dataclass
from typing import List, Optional


@dataclass
class GarnishItem:
    id: str
    code: str
    description: str
    details: str
    logoUrl: str
    unitPrice: float


@dataclass
class Choice:
    code: str
    name: str
    min: int
    max: int
    garnishItens: List[GarnishItem]


@dataclass
class ProductInfo:
    id: str
    quantity: int
    unit: str


@dataclass
class SellingOption:
    minimum: int
    incremental: int
    availableUnits: List[str]


@dataclass
class ProductTag:
    group: str
    tags: List[str]


@dataclass
class Item:
    id: str
    code: str
    description: str
    details: str
    logoUrl: str
    needChoices: bool
    choices: List[Choice]
    unitPrice: float
    unitMinPrice: float
    unitOriginalPrice: float
    sellingOption: SellingOption
    productTags: List[ProductTag]
    productInfo: ProductInfo


@dataclass
class Menu:
    code: str
    name: str
    itens: List[Item]


@dataclass
class Data:
    menu: List[Menu]


@dataclass
class CatalogIfood:
    code: str
    data: Data
