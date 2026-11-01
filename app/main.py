import secrets
from fastapi import FastAPI, HTTPException, Depends
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


@app.get("/links/{code}", response_model=LinkOut)
async def get_link(code: str, db: AsyncSession = Depends(get_db)):
    # Формируем SQL-запрос: SELECT * FROM links WHERE code = code
    stmt = select(Link).where(Link.code == code)
    
    # Выполняем его асинхронно
    result = await db.execute(stmt)
    
    # Достаем одну запись или None, если ничего не нашли
    link = result.scalar_one_or_none()
    
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
        
    return link
