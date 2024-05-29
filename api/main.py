from fastapi import FastAPI
from api.routers import blog, blog_category, skill, portfolio, portfolio_skill, table

app = FastAPI()

app.include_router(blog.router)
app.include_router(blog_category.router)
app.include_router(skill.router)
app.include_router(portfolio.router)
app.include_router(portfolio_skill.router)
app.include_router(table.router)