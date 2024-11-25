import uuid

from fastapi import APIRouter, Depends, Request, status, UploadFile
from fastapi.responses import Response
from loguru import logger
from starlette.responses import StreamingResponse

from common.dependencies.file_metadata import FileMetadata
from schemas.request.file_data import FileDataSchema
from schemas.response.file_data import FileDataResponse
from services.file.adc_file import AbstractFileService
from services.file_data.abc_file_data import AbstractFileDataService

router = APIRouter(prefix="/file", tags=["Upload actions"])


@router.post(
    "/upload",
    summary="Upload file",
    description="Uploading files to the system and S3 storage",
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
        file: UploadFile,
        file_metadata: dict = Depends(FileMetadata()),
        file_data_service: AbstractFileDataService = Depends(),
) -> uuid.UUID:
    """
    Uploading files to the system and S3 storage
    Args:
        file_data_service: FileDataService
    Returns:
        id of the uploaded file
    """
    logger.info(f"Uploading file: {file_metadata.get('file_name')}")
    file_data = await file_data_service.add_file_data(file, FileDataSchema(**file_metadata))
    return file_data.id


@router.get(
    "",
    summary="Get file",
    description="Get file by id",
    status_code=status.HTTP_200_OK,
)
async def upload_file(
        file_id: uuid.UUID,
        file_data_service: AbstractFileDataService = Depends(),
        file_service: AbstractFileService = Depends(),
) -> StreamingResponse:
    """
    Get file by id
    Args:
        file_id: id of the file
        file_data_service: FileDataService
        file_service: FileService
    Returns:
        file to download
    """
    logger.info(f"Get file: {file_id}")
    file_data = await file_data_service.get_file_data(file_id)
    file_stream = file_service.get_file(file_data.name)

    return StreamingResponse(
        file_stream,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_data.name}"},
    )


@router.patch(
    "",
    summary="Update file data",
    description="Update file data (set to delete) by id",
    status_code=status.HTTP_200_OK,
)
async def upload_file(
        file_id: uuid.UUID,
        file_data_service: AbstractFileDataService = Depends(),
) -> FileDataResponse:
    """
    Update file data (set to delete) by id
    Args:
        file_id: id of the file
        file_data_service: FileDataService
    Returns:
        FileDataResponse
    """
    logger.info(f"Set file: {file_id} to delete")
    return await file_data_service.set_file_to_delete(file_id=file_id)