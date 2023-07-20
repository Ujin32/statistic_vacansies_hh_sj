from dataclasses import dataclass


@dataclass
class HHSearchSettings:
    search_area: int
    search_field: str
    search_period: int
    per_page_result_count: int


@dataclass
class SJSearchSettings:
    search_town: int
    search_catalogues: str
    per_page_result_count: int
    search_block: int
    search_method: str
