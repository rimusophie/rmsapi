import pytest
import starlette.status

# CRUDテスト
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

    id = response_obj["id"]

    # 取得
    response = await async_client.get(base_url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["id"] == id
    assert response_obj[0]["name"] == test_name_1

    url = f"{base_url}/{id}"

    # 詳細
    response = await async_client.get(url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == id
    assert response_obj["name"] == test_name_1

    # 更新
    response = await async_client.put(url, json = { "name": test_name_2 })
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == id
    assert response_obj["name"] == test_name_2

    # 削除
    response = await async_client.delete(url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj == None

# 入力チェックテスト
@pytest.mark.asyncio
async def test_input_length(async_client):
    base_url = "/blog_categories"
    test_name = (
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "a"
    )
    test_name_1 = "test_name_1"

    # 作成(name)
    response = await async_client.post(base_url, json = { "name": test_name })
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 作成
    response = await async_client.post(base_url, json = { "name": test_name_1 })
    response_obj = response.json()
    
    id = response_obj["id"]

    # 更新(name)
    url = f"{base_url}/{id}"
    response = await async_client.put(url, json = { "name": test_name })
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

# 存在テスト
@pytest.mark.asyncio
async def test_id_exist(async_client):
    base_url = "/blog_categories"
    test_name_1 = "test_name_1"

    # 作成
    response = await async_client.post(base_url, json = { "name": test_name_1 })
    response_obj = response.json()
    id = response_obj["id"]

    no_exist_id = id + 1

    url = f"{base_url}/{no_exist_id}"

    # 詳細
    response = await async_client.get(url)
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND

    # 更新
    response = await async_client.put(url, json = { "name": test_name_1 })
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND

    # 削除
    response = await async_client.delete(url)
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND