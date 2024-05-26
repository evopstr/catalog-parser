from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class SourceType(Enum):
    NULL = "null"
    GITHUB = "github"


class SourceInfo(BaseModel):
    pass


class NullSourceInfo(SourceInfo):
    pass


class GitHubSourceInfo(SourceInfo):
    owner: str
    repository: str


class CatalogItem(BaseModel):
    title: str
    description: str
    source_type: SourceType
    source_info: SourceInfo
    docker_image: Optional[str] = None
    website: Optional[str] = None
    demo: Optional[str] = None


class Category(BaseModel):
    name: str
    slug: str
    items: Optional[List[CatalogItem]] = None


class Catalog(BaseModel):
    categories: List[Category]


SOURCE_INFO_CLASSES = {
    SourceType.NULL: NullSourceInfo,
    SourceType.GITHUB: GitHubSourceInfo,
}
