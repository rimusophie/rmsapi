import pytest
import starlette.status

# CRUDテスト
@pytest.mark.asyncio
async def test_table(async_client_engine):
    base_url = "/tables"

    # 取得
    response = await async_client_engine.get(base_url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 5
    assert response_obj[0]["name"] == "blog_categories"
    assert response_obj[1]["name"] == "blogs"
    assert response_obj[2]["name"] == "portfolio_skills"
    assert response_obj[3]["name"] == "portfolios"
    assert response_obj[4]["name"] == "skills"


# CRUDテスト
@pytest.mark.asyncio
async def test_dbinfo(async_client_engine):
    base_url = "/dbinfo"

    # 取得
    response = await async_client_engine.get(base_url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["host"] == "db"
    assert response_obj["name"] == "rms_test"
    assert response_obj["port"] == 3306