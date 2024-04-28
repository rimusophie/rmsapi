import pytest
import starlette.status

# blog_category作成
async def create_blog_category(async_client, name: str):
    response = await async_client.post("/blog_categories", json = { "name": name })
    return response.json()

# CRUDテスト
@pytest.mark.asyncio
async def test_blog(async_client):
    base_url = "/blogs"
    test_title_1 = "test_title_1"
    test_title_2 = "test_title_2"
    test_filename_1 = "test_filename_1.html"
    test_filename_2 = "test_filename_2.html"
    test_updated_date_1 = "2024-04-01"
    test_updated_date_2 = "2024-04-02"

    # blog_category作成
    response_obj = await create_blog_category(async_client, "test_name_1")
    blog_category_id_1 = response_obj["id"]

    response_obj = await create_blog_category(async_client, "test_name_2")
    blog_category_id_2 = response_obj["id"]

    # 作成
    response = await async_client.post(
        base_url, 
        json = {
            "title": test_title_1, 
            "blog_category_id": blog_category_id_1, 
            "filename": test_filename_1,
            "updated_date": test_updated_date_1
        }
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == test_title_1
    assert response_obj["blog_category_id"] == blog_category_id_1
    assert response_obj["filename"] == test_filename_1
    assert response_obj["updated_date"] == test_updated_date_1

    id = response_obj["id"]

    # 取得
    response = await async_client.get(base_url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["id"] == id
    assert response_obj[0]["title"] == test_title_1
    assert response_obj[0]["blog_category_id"] == blog_category_id_1
    assert response_obj[0]["filename"] == test_filename_1
    assert response_obj[0]["updated_date"] == test_updated_date_1

    url = f"{base_url}/{id}"

    # 詳細
    response = await async_client.get(url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == id
    assert response_obj["title"] == test_title_1
    assert response_obj["blog_category_id"] == blog_category_id_1
    assert response_obj["filename"] == test_filename_1
    assert response_obj["updated_date"] == test_updated_date_1

    # 更新
    response = await async_client.put(
        url, 
        json = {
            "title": test_title_2,
            "blog_category_id": blog_category_id_2, 
            "filename": test_filename_2,
            "updated_date": test_updated_date_2
        }
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == test_title_2
    assert response_obj["blog_category_id"] == blog_category_id_2
    assert response_obj["filename"] == test_filename_2
    assert response_obj["updated_date"] == test_updated_date_2

    # 削除
    response = await async_client.delete(url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj == None

# 入力チェックテスト
@pytest.mark.asyncio
async def test_input_length(async_client):
    base_url = "/blogs"
    test_title = (
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "a"
    )
    test_filename = (
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "a"
    )
    test_updated_date = "2024-02-31"

    test_title_1 = "test_title_1"
    test_filename_1 = "test_filename_1.html"
    test_updated_date_1 = "2024-04-01"

    # blog_category作成
    response_obj = await create_blog_category(async_client, "test_name_1")
    blog_category_id_1 = response_obj["id"]

    # 作成(title)
    response = await async_client.post(
        base_url, 
        json = {
            "title": test_title, 
            "blog_category_id": blog_category_id_1, 
            "filename": test_filename_1,
            "updated_date": test_updated_date_1
        }
    )
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 作成(filename)
    response = await async_client.post(
        base_url, 
        json = {
            "title": test_title_1, 
            "blog_category_id": blog_category_id_1, 
            "filename": test_filename,
            "updated_date": test_updated_date_1
        }
    )
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 作成(updated_date)
    response = await async_client.post(
        base_url, 
        json = {
            "title": test_title_1, 
            "blog_category_id": blog_category_id_1, 
            "filename": test_filename_1,
            "updated_date": test_updated_date
        }
    )
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 作成
    response = await async_client.post(
        base_url, 
        json = {
            "title": test_title_1, 
            "blog_category_id": blog_category_id_1, 
            "filename": test_filename_1,
            "updated_date": test_updated_date_1
        }
    )
    response_obj = response.json()

    id = response_obj["id"]

    url = f"{base_url}/{id}"

    # 更新(title)
    response = await async_client.put(
        url, 
        json = {
            "title": test_title,
            "blog_category_id": blog_category_id_1, 
            "filename": test_filename_1,
            "updated_date": test_updated_date_1
        }
    )
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 更新(filename)
    response = await async_client.put(
        url, 
        json = {
            "title": test_title_1,
            "blog_category_id": blog_category_id_1, 
            "filename": test_filename,
            "updated_date": test_updated_date_1
        }
    )
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 更新(updated_date)
    response = await async_client.put(
        url, 
        json = {
            "title": test_title_1,
            "blog_category_id": blog_category_id_1, 
            "filename": test_filename_1,
            "updated_date": test_updated_date
        }
    )
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

# 存在テスト
@pytest.mark.asyncio
async def test_id_exist(async_client):
    base_url = "/blogs"
    test_title_1 = "test_title_1"
    test_filename_1 = "test_filename_1.html"
    test_updated_date_1 = "2024-04-01"

    # blog_category作成
    response_obj = await create_blog_category(async_client, "test_name_1")
    blog_category_id_1 = response_obj["id"]

    # 作成
    response = await async_client.post(
        base_url, 
        json = {
            "title": test_title_1, 
            "blog_category_id": blog_category_id_1, 
            "filename": test_filename_1,
            "updated_date": test_updated_date_1
        }
    )
    response_obj = response.json()

    id = response_obj["id"]

    no_exist_id = id + 1

    url = f"{base_url}/{no_exist_id}"

    # 詳細
    response = await async_client.get(url)
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND

    # 更新
    response = await async_client.put(
        url, 
        json = {
            "title": test_title_1,
            "blog_category_id": blog_category_id_1, 
            "filename": test_filename_1,
            "updated_date": test_updated_date_1
        }
    )
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND

    # 削除
    response = await async_client.delete(url)
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND