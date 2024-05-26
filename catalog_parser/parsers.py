from pathlib import Path
from typing import Dict

import yaml

from catalog_parser.models import (
    SOURCE_INFO_CLASSES,
    CatalogItem,
    Catalog,
    Category,
    SourceType,
)


class CatalogParser:
    categories: Dict[str, Category] = None

    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def get_catalog(self) -> Dict[str, Category]:
        if self.categories is not None:
            return self.categories

        catalog_file = Path(self.data_dir) / "catalog.yaml"
        if not catalog_file.exists():
            raise FileNotFoundError(f"{catalog_file} not found")

        with catalog_file.open() as f:
            self.categories = {
                category.slug: category
                for category in Catalog(**yaml.safe_load(f)).categories
            }

        for slug in self.categories:
            self.get_category(slug)

        return self.categories

    def get_category(self, slug: str) -> Category:
        if self.categories is None:
            self.get_categories()

        if slug not in self.categories:
            raise KeyError(f"Category with slug {slug} not found")

        category_file = Path(self.data_dir) / "category_data" / f"{slug}.yaml"
        if not category_file.exists():
            raise FileNotFoundError(f"{category_file} not found")

        if self.categories[slug].items is not None:
            return self.categories[slug]

        catalog_items = []
        with category_file.open() as f:
            category = yaml.safe_load(f)
            for item in category["items"]:
                source_type = SourceType(item["source_type"])
                source_info = item["source_info"]
                item["source_info"] = SOURCE_INFO_CLASSES[source_type](**source_info)
                catalog_item = CatalogItem(**item)
                catalog_items.append(catalog_item)
            self.categories[slug].items = catalog_items

        return self.categories[slug]
