from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, status, Form, WebSocket, WebSocketDisconnect, File, UploadFile
from app.dependencies import SessionDep, AuthDep
from . import router, templates
from app.services.user_service import UserService
from app.repositories.user import UserRepository
from app.utilities.flash import flash
from app.schemas import UserResponse
from app.services.upload_service import UploadService


@router.post("/upload")
async def create_upload_file(
    files: list[UploadFile],
    user: AuthDep,
    db: SessionDep,
):
    upload_service = UploadService()
    for file in files:
        await upload_service.store_file(file)
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/upload", response_class=HTMLResponse)
async def upload_view(
    request: Request,
    user: AuthDep,
    db:SessionDep
):
    return templates.TemplateResponse(
        request=request, 
        name="upload.html",
        context={
            "user": user,
        }
    )
    
@router.get("/uploads/{filename}")
async def view_file(
    filename: str,
    user: AuthDep,
    db:SessionDep
):
    upload_service = UploadService()
    file_path = upload_service.views_file(filename)
    return RedirectResponse(url=f"/{file_path}", status_code=status.HTTP_302_FOUND)

@router.delete("/uploads/{filename}")
async def delete_file(
    filename: str,
    user: AuthDep,
    db:SessionDep
):
    upload_service = UploadService()
    upload_service.remove_file(filename)
    return {"message": "File deleted successfully"}