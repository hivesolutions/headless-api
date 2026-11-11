from typing import Literal, TypedDict
from appier import API as BaseAPI

BASE_URL: str = ...

Format = Literal["pdf", "png", "jpeg", "webp", "bmp", "tiff", "gif"]

WaitUntil = Literal["load", "domcontentloaded", "networkidle0", "networkidle2"]

class Info(TypedDict):
    name: str
    version: str
    node: str
    engines: list[list[str]]

class API(BaseAPI):
    def render(
        self,
        url: str,
        format: Format | None = ...,
        page_format: str | None = ...,
        prefer_css_page_size: bool | None = ...,
        print_background: bool | None = ...,
        wait_until: WaitUntil | None = ...,
        full_page: bool | None = ...,
        trim: bool | None = ...,
        width: int | None = ...,
        height: int | None = ...,
        scale_factor: int | None = ...,
        timeout: int | None = ...,
        cookie: str | list[str] | None = ...,
        method: str | None = ...,
        reload: bool | None = ...,
        engine: str | None = ...,
    ) -> bytes: ...
    def render_contents(
        self,
        contents: str | bytes,
        mime: str = ...,
        format: Format | None = ...,
        page_format: str | None = ...,
        prefer_css_page_size: bool | None = ...,
        print_background: bool | None = ...,
        wait_until: WaitUntil | None = ...,
        full_page: bool | None = ...,
        trim: bool | None = ...,
        width: int | None = ...,
        height: int | None = ...,
        scale_factor: int | None = ...,
        timeout: int | None = ...,
        reload: bool | None = ...,
    ) -> bytes: ...
    def info(self) -> Info: ...
