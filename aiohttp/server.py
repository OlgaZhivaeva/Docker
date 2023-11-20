import json
from typing import Type

from aiohttp import web
from aiohttp.typedefs import Handler
from sqlalchemy.exc import IntegrityError

from models import Session, Advertisement, engine

app = web.Application()


async def orm_context(app: web.Application):
    print("START")
    async with engine.begin() as conn:
        await conn.run_sync(Advertisement.metadata.create_all)
    yield
    await engine.dispose()
    print("FINISH")


@web.middleware
async def session_middleware(request: web.Request, handler: Handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_http_error(error_class: Type[web.HTTPClientError], message):
    return error_class(
        text=json.dumps({"error": message}), content_type="application/json"
    )


async def get_adv_by_id(session: Session, adv_id: int) -> Advertisement:
    adv = await session.get(Advertisement, adv_id)
    if adv is None:
        raise get_http_error(web.HTTPNotFound, f"Advertisement with id {adv_id} not found")
    return adv


async def add_adv(session: Session, adv: Advertisement):
    try:
        session.add(adv)
        await session.commit()
    except IntegrityError as error:
        print(error)
        raise get_http_error(web.HTTPConflict, "Advertisement already exists")
    print(adv)
    return adv


class AdvView(web.View):
    @property
    def adv_id(self):
        return int(self.request.match_info["adv_id"])

    @property
    def session(self) -> Session:
        return self.request.session

    async def get(self):
        adv = await get_adv_by_id(self.session, self.adv_id)
        return web.json_response(adv.dict)

    async def post(self):
        adv_data = await self.request.json()
        adv = Advertisement(**adv_data)
        adv = await add_adv(self.session, adv)
        return web.json_response({"id": adv.id})

    async def patch(self):
        adv = await get_adv_by_id(self.session, self.adv_id)
        adv_data = await self.request.json()
        for field, value in adv_data.items():
            setattr(adv, field, value)
            await add_adv(self.session, adv)
        return web.json_response({"id": adv.id})

    async def delete(self):
        adv = await get_adv_by_id(self.session, self.adv_id)
        await self.session.delete(adv)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.get("/advertisements/{adv_id:\d+}", AdvView),
        web.patch("/advertisements/{adv_id:\d+}", AdvView),
        web.delete("/advertisements/{adv_id:\d+}", AdvView),
        web.post("/advertisements", AdvView),
    ]
)

web.run_app(app)
