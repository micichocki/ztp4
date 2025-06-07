from fastapi import FastAPI, HTTPException, Request, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import os
from datetime import datetime

app = FastAPI(
    title="API Gateway",
    description="API Gateway for Product Service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


API_ENDPOINT = os.getenv("API_ENDPOINT", "http://127.0.0.1:5000").rstrip('/')


@app.options("/products")
async def options_products():
    try:
        response = requests.options(
            f"{API_ENDPOINT}/products",
            timeout=10
        )
        response.raise_for_status()

        allowed_methods = response.headers.get("Allow", "GET, OPTIONS")

        return {
            "allowed_methods": allowed_methods,
            "endpoints": {
                "get_all_products": f"{API_ENDPOINT}/products",
                "get_product_by_id": f"{API_ENDPOINT}/products/{{product_id}}"
            }
        }
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Gateway timeout")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@app.get("/products/")
async def get_products():
    try:
        response = requests.get(
            f"{API_ENDPOINT}/products/",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Gateway timeout")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    try:
        response = requests.get(
            f"{API_ENDPOINT}/products/{product_id}",
            timeout=10
        )

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Gateway timeout")
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        response = requests.get(f"{API_ENDPOINT}/health", timeout=5)
        response_data = response.json()
        backend_status = "healthy" if response.status_code == 200 else "unhealthy"
        backend_info = {
            "status": backend_status,
            "service": response_data.get("service", "unknown"),
            "timestamp": response_data.get("timestamp")
        }
    except Exception as e:
        backend_status = "unavailable"
        backend_info = {
            "status": backend_status,
            "error": str(e)
        }

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "backend_status": backend_status,
        "backend_info": backend_info
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
