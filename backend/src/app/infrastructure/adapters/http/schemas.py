from pydantic import BaseModel, Field


class RegisterApplicationRequest(BaseModel):
    client_name: str = Field(min_length=1, max_length=120)


class ApplicationResponse(BaseModel):
    client_id: str
    client_name: str
