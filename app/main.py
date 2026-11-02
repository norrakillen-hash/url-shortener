import secrets
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.redis_client import redis_client
from app.schemas import LinkCreate, LinkOut
from app.database import get_db
from app.models import Link

app = FastAPI(title="URL Shortener")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"service": "url-shortener", "version": "0.1.0"}

# Внедряем сессию через Depends(get_db)
@app.post("/links", response_model=LinkOut, status_code=201)
async def create_link(payload: LinkCreate, db: AsyncSession = Depends(get_db)):
    code = secrets.token_urlsafe(6)
    
    # Создаем объект модели SQLAlchemy
    new_link = Link(code=code, url=str(payload.url))
    
    # Добавляем в сессию и коммитим (сохраняем в БД)
    db.add(new_link)
    await db.commit()
    
    # Обновляем объект из БД, чтобы получить id и created_at, которые сгенерировала БД
    await db.refresh(new_link)
    
    return new_link


# 1. Эндпоинт-редиректор
@app.get("/links/{code}")
async def redirect_to_url(code: str, db: AsyncSession = Depends(get_db)):
    # 1. Проверяем кэш (Redis)
    cached_url = await redis_client.get(f"link:{code}")
    
    if cached_url:
        # Если нашли в кэше — сразу редирект (и можно асинхронно обновить счетчик в БД, но для простоты пока пропустим обновление счетчика при кэш-хите)
        return RedirectResponse(url=cached_url)

    # 2. Если в кэше нет — идем в БД
    stmt = select(Link).where(Link.code == code)
    result = await db.execute(stmt)
    link = result.scalar_one_or_none()
    
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    # 3. Сохраняем в Redis на 1 час (3600 секунд), чтобы в следующий раз не идти в БД
    await redis_client.set(f"link:{code}", link.url, ex=3600)
    
    # 4. Увеличиваем счетчик в БД
    link.clicks += 1
    await db.commit()
    
    return RedirectResponse(url=link.url)

# 2. Эндпоинт для просмотра статистики
@app.get("/links/{code}/stats", response_model=LinkOut)
async def get_link_stats(code: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Link).where(Link.code == code)
    result = await db.execute(stmt)
    link = result.scalar_one_or_none()
    
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
        
    return link
