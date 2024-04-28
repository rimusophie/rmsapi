import pytest
import starlette.status

# blog_categoryテスト
@pytest.mark.asyncio
async def test_blog_category(async_client):
    base_url = "/blog_categories"
    test_name_1 = "test_name_1"
    test_name_2 = "test_name_2"

    # 作成
    response = await async_client.post(base_url, json = { "name": test_name_1 })
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["name"] == test_name_1

    # 取得
    response = await async_client.get(base_url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["name"] == test_name_1

    # 更新
    id = response_obj[0]["id"]
    url = f"{base_url}/{id}"
    response = await async_client.put(url, json = { "name": test_name_2 })
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == id
    assert response_obj["name"] == test_name_2

    # 削除
    id = response_obj["id"]
    response = await async_client.delete(url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj == None
    