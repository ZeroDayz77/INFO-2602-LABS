import uvicorn
from fastapi import FastAPI, Request, status
from app.routers import main_router, templates
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

SECRET_KEY = "ThisIsAnExampleOfWhatNotToUseAsTheSecretKeyIRL"

app = FastAPI(middleware=[
    Middleware(SessionMiddleware, secret_key=SECRET_KEY)
])
app.include_router(main_router)

@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized_redirect_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(
        request=request, 
        name="401.html",
    )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
