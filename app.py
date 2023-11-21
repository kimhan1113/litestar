from litestar import Litestar, get, post, status_codes, Controller
from litestar.exceptions import HTTPException
from pydantic import BaseModel

'''
pydantic은 파이썬 타입 어노테이션을 사용해서 데이터 유효성 검사와 설정 관리를 하는 라이브러리다. 
런타임때 타입 힌트를 강제하고, 데이터가 유효하지 않을때 유저 친화적인 에러를 제공한다.
'''

BANDS = [
    {'id' : 1, 'name' : 'the queen', 'genre' : 'rock'},
    {'id' : 2, 'name' : 'the muse', 'genre' : 'pop'},
]

class Band(BaseModel):
    id: int | None = None
    name: str
    genre: str


class BandController(Controller):
    path = '/bands'

    @get()
    async def bands(self) -> list[Band]:
        return [Band(**b) for b in BANDS]

    @get('/{band_id: int}')
    async def band(self,band_id: int) -> Band:
        band = next((Band(**b) for b in BANDS if b['id'] == band_id), None)

        if not band:
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail = f"No band with ID {band_id}"
            )
        return band

    @post()
    async def create_band(self, data:Band) -> Band:
        next_id = max(BANDS,  key=lambda x: x['id'])['id'] + 1
        data.id = next_id
        BANDS.append(data.model_dump())
        return data

app = Litestar([BandController])