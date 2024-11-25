from fastapi import Request


class FileMetadata:
    async def __call__(self, request: Request) -> dict:
        form = await request.form()
        file = form.get("file")
        return {"name": file.filename, "format": file.content_type,
                "extension": file.filename.split(".")[-1] if "." in file.filename else None}
