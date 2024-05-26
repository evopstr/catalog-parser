from argparse import ArgumentParser

from catalog_parser.parsers import CatalogParser
from catalog_parser.renderers import CatalogRenderer


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--data-dir", default="/data")
    parser.add_argument("--output-dir", default="/output")

    args = parser.parse_args()

    catalog_parser = CatalogParser(args.data_dir)
    categories = catalog_parser.get_catalog()

    renderer = CatalogRenderer(args.output_dir)
    renderer.render_and_save(categories)
