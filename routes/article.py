from typing import Annotated

from fastapi import Query, Path, APIRouter

router = APIRouter(prefix="/article", tags=["文章管理"])


@router.get("/list")
async def get_article_list(page: Annotated[int, Query(ge=1, alias="page")] = 1,
                           size: Annotated[int, Query(ge=1, le=20, alias="size")] = 10):
    return {"page": page, "size": size}


@router.get("/{article_id}")
# async def get_article(article_id: Annotated[int, Path(ge=2)]): # ge=2 表示article_id必须大于等于2,第二个是校验path参数
async def get_article(article_id: int = Path(ge=2)):  # 跟上述写法等价
    return {"article_id": article_id}
