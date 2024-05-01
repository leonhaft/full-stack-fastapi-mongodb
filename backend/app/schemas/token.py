from beanie import PydanticObjectId, Document
from pydantic import BaseModel, ConfigDict, SecretStr


class RefreshTokenBase(BaseModel):
    token: SecretStr
    authenticates: Document | None = None


class RefreshTokenCreate(RefreshTokenBase):
    authenticates: Document


class RefreshTokenUpdate(RefreshTokenBase):
    pass


class RefreshToken(RefreshTokenUpdate):
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: SecretStr
    refresh_token: SecretStr | None = None
    token_type: str


class TokenPayload(BaseModel):
    sub: PydanticObjectId | None = None
    refresh: bool | None = False
    totp: bool | None = False


class MagicTokenPayload(BaseModel):
    sub: PydanticObjectId | None = None
    fingerprint: PydanticObjectId | None = None


class WebToken(BaseModel):
    claim: str
