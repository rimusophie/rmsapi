from fastapi import FastAPI
from api.routers import blogs, blog_categories

app = FastAPI()

app.include_router(blogs.router)
app.include_router(blog_categories.router)