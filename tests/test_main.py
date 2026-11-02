import pytest

# pytest-asyncio требует явно указывать, что тест асинхронный
@pytest.mark.asyncio
async def test_health_check(async_client):
    # Имитируем GET-запрос
    response = await async_client.get("/health")
    
    # Проверяем статус-код (должен быть 200)
    assert response.status_code == 200
    
    # Проверяем тело ответа
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_create_link(async_client):
    # Имитируем POST-запрос с валидными данными
    payload = {"url": "https://example.com/test"}
    response = await async_client.post("/links", json=payload)
    
    # Проверяем, что ссылка создалась
    assert response.status_code == 201
    data = response.json()
    
    # Проверяем, что в ответе есть код и оригинальный URL
    assert "code" in data
    assert data["url"] == "https://example.com/test"
