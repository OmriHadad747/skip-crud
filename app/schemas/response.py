from typing import Any

from app.schemas import CustomRespBaseModel


class MsgResp(CustomRespBaseModel):
    entity: dict[str, Any] | None
    msg: str


class EntityResp(CustomRespBaseModel):
    entity: dict[str, Any] | list[dict[str, Any]]
    msg: str | None = "no message"
