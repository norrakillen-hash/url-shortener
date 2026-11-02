import secrets
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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
    stmt = select(Link).where(Link.code == code)
    result = await db.execute(stmt)
    link = result.scalar_one_or_none()
    
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    # Увеличиваем счетчик и сохраняем
    link.clicks += 1
    await db.commit()
    
    # Отдаем HTTP 307 (Temporary Redirect)
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
