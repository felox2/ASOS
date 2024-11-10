from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .middlewares.session import SessionMiddleware

from .routers import (
    auth,
    users,
    categories,
    products,
    brands,
    cart
)

origins = ["http://localhost:5173"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(brands.router)
app.include_router(brands.router)
app.include_router(cart.router)