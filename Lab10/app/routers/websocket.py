from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, status, Form, WebSocket, WebSocketDisconnect
from app.dependencies import SessionDep, AuthDep
from . import router, templates
from app.services.user_service import UserService
from app.repositories.user import UserRepository
from app.utilities.flash import flash
from app.schemas import UserResponse
from app.services.websocket_service import websocket_service


@router.get("/chats", response_class=HTMLResponse)
async def chats_view(
    request: Request,
    user: AuthDep,
    db:SessionDep
):
    return templates.TemplateResponse(
        request=request, 
        name="chat.html",
        context={
            "user": user
        }
    )


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket_service.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_service.send_personal_message(f"You wrote: {data}", websocket)
            await websocket_service.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        websocket_service.disconnect(websocket)
        await websocket_service.broadcast(f"Client #{client_id} left the chat")