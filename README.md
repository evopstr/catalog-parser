# Catalog Parser

This project parses [EvOps application catalog](https://github.com/evopstr/evops-web/tree/main/data) in YAML format and generates documentation pages for Docusaurus.

## Usage

```shell
docker run --rm -v /path/to/evops/data:/data -v /path/to/evops/docs:/output ghcr.io/evopstr/catalog-parser
```
