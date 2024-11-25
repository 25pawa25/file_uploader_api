import aioboto3

from core.config import settings


async def get_async_s3_client():
    session = aioboto3.Session(
        aws_access_key_id=settings.s3.access_key,
        aws_secret_access_key=settings.s3.secret_key,
        region_name=settings.s3.region,
    )
    return session.client("s3")
