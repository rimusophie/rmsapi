from fastapi import APIRouter

router = APIRouter()

@router.get("/blogs")
async def list_blogs():
    pass

@router.get("/blogs/{id}")
async def detail_blog():
    pass

@router.post("/blogs")
async def create_blog():
    pass

@router.put("/blogs/{id}")
async def update_blog():
    pass

@router.delete("/blogs/{id}")
async def delete_blog():
    pass