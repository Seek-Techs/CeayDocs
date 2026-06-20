from fastapi import HTTPException


def bad_request(detail: str) -> HTTPException:
    return HTTPException(status_code=400, detail=detail)


def unsupported_media_type(detail: str) -> HTTPException:
    return HTTPException(status_code=415, detail=detail)


def internal_error(detail: str) -> HTTPException:
    return HTTPException(status_code=500, detail=detail)

