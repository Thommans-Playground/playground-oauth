from fastapi import APIRouter, HTTPException, status

from app.application.use_cases.register_application import (
    RegisterApplication,
    RegisterApplicationCommand,
)
from app.infrastructure.adapters.http.schemas import (
    ApplicationResponse,
    RegisterApplicationRequest,
)


def build_router(register_application: RegisterApplication) -> APIRouter:
    router = APIRouter(prefix="/applications", tags=["applications"])

    @router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
    def register(payload: RegisterApplicationRequest) -> ApplicationResponse:
        try:
            application = register_application.execute(
                RegisterApplicationCommand(client_name=payload.client_name)
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=str(exc),
            ) from exc

        return ApplicationResponse(
            client_id=application.client_id,
            client_name=application.client_name,
        )

    return router
