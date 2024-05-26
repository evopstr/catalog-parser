from pathlib import Path
from string import Template
from typing import Dict

from catalog_parser.models import CatalogItem, Category, SourceInfo, SourceType


class CatalogRenderer:
    templates = {
        SourceType.GITHUB: "github",
    }

    components = {
        SourceType.GITHUB: "GitHub",
    }

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def _render_attributes(self, attributes: Dict[str, str]) -> str:
        return " ".join(
            f"{k}={v!r}" for k, v in attributes.items() if v is not None
        )

    def _get_source_attributes(
        self, source_type: SourceType, source_info: SourceInfo
    ) -> str:
        attributes = {}
        for key, value in dict(source_info).items():
            if value is None:
                continue

            attributes[f"{source_type.value}_{key}"] = value

        return attributes

    def _render_component_attributes(self, catalog_item: CatalogItem) -> str:
        attributes = {}
        catalog_item_props = dict(catalog_item)
        catalog_item_props.pop("description")
        source_type = catalog_item_props.pop("source_type")
        source_info = catalog_item_props.pop("source_info")
        source_attributes = self._get_source_attributes(source_type, source_info)
        attributes.update(catalog_item_props)
        attributes.update(source_attributes)

        return self._render_attributes(attributes)

    def render_imports(self, components: set) -> str:
        return "\n".join(
            f"import {component} from '@site/src/components/{component}';"
            for component in components
        )

    def render_catalog_item(self, catalog_item: CatalogItem) -> str:
        template_name = self.templates.get(catalog_item.source_type, "catalog_item")
        template_file = Path("catalog_parser") / "templates" / f"{template_name}.mdx"
        with template_file.open() as f:
            template = Template(f.read())

        return template.substitute(
            description=catalog_item.description,
            attributes=self._render_component_attributes(catalog_item),
        )

    def render_category(self, category: Category, order: int) -> str:
        category_file = Path("catalog_parser") / "templates" / "category.mdx"
        with category_file.open() as f:
            template = Template(f.read())

        category_imports = set()
        catalog_items = []
        for item in category.items:
            category_imports.add(self.components.get(item.source_type, "Project"))
            catalog_items.append(self.render_catalog_item(item))

        return template.substitute(
            order=order,
            imports=self.render_imports(category_imports),
            category_name=category.name,
            catalog_items="".join(catalog_items),
        )

    def render_catalog(self, categories: Dict[str, Category]) -> str:
        categories_index_file = Path("catalog_parser") / "templates" / "catalog.mdx"
        with categories_index_file.open() as f:
            template = Template(f.read())

        return template.substitute(
            categories="\n".join(
                f"- [{category.name}]({category.slug})"
                for category in categories.values()
            )
        )

    def render_and_save(self, categories: Dict[str, Category]):
        for order, slug in enumerate(categories, 1):
            category_file = Path(self.output_dir) / f"{slug}.mdx"
            category_file.parent.mkdir(parents=True, exist_ok=True)
            category = self.render_category(categories[slug], order)

            with category_file.open("w") as f:
                f.write(category)

        catalog_file = Path(self.output_dir) / "katalog.mdx"
        with catalog_file.open("w") as f:
            f.write(self.render_catalog(categories))
