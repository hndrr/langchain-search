from typing import List

import httpx
from pydantic import BaseModel


class ZipCodeRequest(BaseModel):
    zip_codes: List[str]

async def fetch_address(zip_code: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://zipcloud.ibsnet.co.jp/api/search?zipcode={zip_code}"
            )
        return response.json()
