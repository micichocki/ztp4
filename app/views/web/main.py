from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.services.product_service import ProductService
from app.models.product import Product
from app.viewmodels.product_viewmodel import ProductViewModel
from typing import List
import os
import pathlib

app = FastAPI(
    title="Product API",
    description="API for managing products",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "templates")
templates = Jinja2Templates(directory=templates_dir)
product_service = ProductService()
view_model = ProductViewModel(product_service)

@app.get("/")
async def root(request: Request):
    try:
        view_model.load_products()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "products": view_model.products,
            "error": view_model.error_message
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "products": [],
            "error": str(e)
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
