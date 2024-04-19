from fastapi import FastAPI
from api.routers import blog, blog_category

app = FastAPI()

app.include_router(blog.router)
app.include_router(blog_category.router)