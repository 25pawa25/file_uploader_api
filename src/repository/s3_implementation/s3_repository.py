import aioboto3
from botocore.exceptions import ClientError
from fastapi import UploadFile

from core.config import settings
from repository.interfaces.file.abc_s3_repository import AbstractS3Repository


class S3FileRepository(AbstractS3Repository):
    def __init__(self, client: aioboto3.session):
        self.bucket_name = settings.s3.bucket
        self.client = client
        self.upload_chunk_size = settings.project.upload_chunk_size

    async def add_file(self, file: UploadFile, file_name: str) -> int:
        """
        Upload a file to the S3 bucket
        Args:
            file: File-like object to upload
            file_name: Name of the file in the bucket
        Returns:
            int: Size of the uploaded file
        """
        try:
            total_size = 0
            async with self.client.create_multipart_upload(Bucket=self.bucket_name, Key=file_name) as response:
                upload_id = response["UploadId"]
                parts = []
                part_number = 1

                while chunk := await file.read(self.upload_chunk_size):
                    part_response = await self.client.upload_part(
                        Bucket=self.bucket_name,
                        Key=file_name,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=chunk
                    )
                    parts.append({
                        "ETag": part_response["ETag"],
                        "PartNumber": part_number
                    })
                    part_number += 1
                    total_size += len(chunk)

                await self.client.complete_multipart_upload(
                    Bucket=self.bucket_name,
                    Key=file_name,
                    UploadId=upload_id,
                    MultipartUpload={"Parts": parts}
                )
            return total_size

        except ClientError as e:
            await self.client.abort_multipart_upload(
                Bucket=self.bucket_name,
                Key=file_name,
                UploadId=upload_id
            )
            raise RuntimeError(f"Failed to upload file to S3: {e}")

    async def delete_file(self, file_name: str):
        """
        Delete a file from the S3 bucket
        Args:
            file_name: Name of the file to delete
        Returns:
            bool: True if the file was successfully deleted, False otherwise
        """
        try:
            await self.client.delete_object(Bucket=self.bucket_name, Key=file_name)
        except ClientError as e:
            raise RuntimeError(f"Failed to delete file from S3: {e}")
