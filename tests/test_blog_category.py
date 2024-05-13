import pytest
import starlette.status

BASE_URL = "/blog_categories"

# blog_category件数
async def get_blog_categories_count(async_client):
    return await async_client.get("/blog_categories_count")

# blog_category一覧取得
async def get_blog_categories(async_client, url: str):
    return await async_client.get(url)

# blog_categorykeyvalue取得
async def get_blog_categories_keyvalue(async_client):
    return await async_client.get("/blog_categories_keyvalue")

# blog_category詳細
async def get_blog_category(async_client, id: int):
    url = f"{BASE_URL}/{id}"
    return await async_client.get(url)

# blog_category作成
async def create_blog_category(async_client, name: str):
    return await async_client.post(BASE_URL, json = { "name": name })

# blog_category更新
async def update_blog_category(async_client, id: int, name: str):
    url = f"{BASE_URL}/{id}"
    return await async_client.put(url, json = { "name": name })

# blog_category削除
async def delete_blog_category(async_client, id: int):
    url = f"{BASE_URL}/{id}"
    return await async_client.delete(url)

# CRUDテスト
@pytest.mark.asyncio
async def test_blog_category(async_client):
    test_name_1 = "test_name_1"
    test_name_2 = "test_name_2"

    # 作成
    response = await create_blog_category(async_client, test_name_1)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["name"] == test_name_1

    id = response_obj["id"]

    # 取得
    response = await get_blog_categories(async_client, BASE_URL)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["id"] == id
    assert response_obj[0]["name"] == test_name_1

    # 詳細
    response = await get_blog_category(async_client, id)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == id
    assert response_obj["name"] == test_name_1

    # 更新
    response = await update_blog_category(async_client, id, test_name_2)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == id
    assert response_obj["name"] == test_name_2

    # 削除
    response = await delete_blog_category(async_client, id)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj == None

# 入力チェックテスト
@pytest.mark.asyncio
async def test_input_length(async_client):
    test_name_ng = (
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "a"
    )
    test_name_ok = "test_name_ok"

    # 作成(name)
    response = await create_blog_category(async_client, test_name_ng)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 作成
    response = await create_blog_category(async_client, test_name_ok)
    response_obj = response.json()
    
    id = response_obj["id"]

    # 更新(name)
    response = await update_blog_category(async_client, id, test_name_ng)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

# 存在テスト
@pytest.mark.asyncio
async def test_id_exist(async_client):
    test_name_ok = "test_name_ok"

    # 作成
    response = await create_blog_category(async_client, test_name_ok)
    response_obj = response.json()
    id = response_obj["id"]

    no_exist_id = id + 1

    # 詳細
    response = await get_blog_category(async_client, no_exist_id)
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND

    # 更新
    response = await update_blog_category(async_client, no_exist_id, test_name_ok)
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND

    # 削除
    response = await delete_blog_category(async_client, no_exist_id)
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND

# 件数テスト
@pytest.mark.asyncio
async def test_count(async_client):
    test_name_ok = "test_name_ok"

    # 件数
    response = await get_blog_categories_count(async_client)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["count"] == 0

    # 作成
    await create_blog_category(async_client, test_name_ok)

    # 件数
    response = await get_blog_categories_count(async_client)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["count"] == 1

# ページネーションテスト
@pytest.mark.asyncio
async def test_count(async_client):
    test_name_1 = "test_name_1"
    test_name_2 = "test_name_2"
    test_name_3 = "test_name_3"
    test_name_4 = "test_name_4"
    test_name_5 = "test_name_5"

    # 0件
    response = await get_blog_categories(async_client, BASE_URL)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 0

    # 作成
    await create_blog_category(async_client, test_name_1)
    await create_blog_category(async_client, test_name_2)
    await create_blog_category(async_client, test_name_3)
    await create_blog_category(async_client, test_name_4)
    await create_blog_category(async_client, test_name_5)

    # ページにつき2件、1ページ目
    url = f"{BASE_URL}?page=1&limit=2"
    response = await get_blog_categories(async_client, url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 2
    assert response_obj[0]["name"] == test_name_1
    assert response_obj[1]["name"] == test_name_2

    # ページにつき3件、2ページ目
    url = f"{BASE_URL}?page=2&limit=3"
    response = await get_blog_categories(async_client, url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 2
    assert response_obj[0]["name"] == test_name_4
    assert response_obj[1]["name"] == test_name_5

# keyvalueテスト
@pytest.mark.asyncio
async def test_keyvalue(async_client):
    test_name_1 = "ccc"
    test_name_2 = "bbb"
    test_name_3 = "aaa"

    # 作成
    await create_blog_category(async_client, test_name_1)
    await create_blog_category(async_client, test_name_2)
    await create_blog_category(async_client, test_name_3)

    response = await get_blog_categories_keyvalue(async_client)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()

    assert response_obj[0]["name"] == test_name_3
    assert response_obj[1]["name"] == test_name_2
    assert response_obj[2]["name"] == test_name_1