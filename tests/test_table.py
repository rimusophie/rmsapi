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
    assert len(response_obj) == 2
    assert response_obj[0]["name"] == "blog_categories"
    assert response_obj[1]["name"] == "blogs"
