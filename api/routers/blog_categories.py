from fastapi import APIRouter

router = APIRouter()

@router.get("/blog_categories")
async def list_blog_categories():
    pass

@router.get("/blog_categories/{id}")
async def detail_blog_category():
    pass

@router.post("/blog_categories")
async def create_blog_category():
    pass

@router.put("/blog_categories/{id}")
async def update_blog_category():
    pass

@router.delete("/blog_categories/{id}")
async def delete_blog_category():
    pass