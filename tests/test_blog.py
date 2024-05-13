import pytest
import starlette.status
from datetime import date
from tests.test_blog_category import create_blog_category

BASE_URL = "/blogs"

# blog件数
async def get_blogs_count(async_client):
    return await async_client.get("/blogs_count")

# blog一覧取得
async def get_blogs(async_client, url: str):
    return await async_client.get(url)

# blog詳細
async def get_blog(async_client, id: int):
    url = f"{BASE_URL}/{id}"
    return await async_client.get(url)

# blog作成
async def create_blog(async_client, title: str, blog_category_id: int, filename: str, updated_date: date):
    return await async_client.post(
        BASE_URL, 
        json = {
            "title": title, 
            "blog_category_id": blog_category_id, 
            "filename": filename,
            "updated_date": updated_date
        }
    )

# blogs更新
async def update_blog(async_client, id: int, title: str, blog_category_id: int, filename: str, updated_date: date):
    url = f"{BASE_URL}/{id}"
    return await async_client.put(
        url, 
        json = { 
            "title": title, 
            "blog_category_id": blog_category_id, 
            "filename": filename,
            "updated_date": updated_date 
        }
    )

# blogs削除
async def delete_blog(async_client, id: int):
    url = f"{BASE_URL}/{id}"
    return await async_client.delete(url)

# CRUDテスト
@pytest.mark.asyncio
async def test_blog(async_client):
    test_name_1 = "test_name_1"
    test_name_2 = "test_name_2"

    test_title_1 = "test_title_1"
    test_title_2 = "test_title_2"
    test_filename_1 = "test_filename_1.html"
    test_filename_2 = "test_filename_2.html"
    test_updated_date_1 = "2024-04-01"
    test_updated_date_2 = "2024-04-02"

    # blog_category作成
    response = await create_blog_category(async_client, test_name_1)
    response_obj = response.json()
    blog_category_id_1 = response_obj["id"]

    response = await create_blog_category(async_client, test_name_2)
    response_obj = response.json()
    blog_category_id_2 = response_obj["id"]

    # 作成
    response = await create_blog(async_client, test_title_1, blog_category_id_1, test_filename_1, test_updated_date_1)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == test_title_1
    assert response_obj["blog_category_id"] == blog_category_id_1
    assert response_obj["filename"] == test_filename_1
    assert response_obj["updated_date"] == test_updated_date_1

    id = response_obj["id"]

    # 取得
    response = await get_blogs(async_client, BASE_URL)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["id"] == id
    assert response_obj[0]["title"] == test_title_1
    assert response_obj[0]["blog_category_id"] == blog_category_id_1
    assert response_obj[0]["filename"] == test_filename_1
    assert response_obj[0]["updated_date"] == test_updated_date_1

    # 詳細
    response = await get_blog(async_client, id)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == id
    assert response_obj["title"] == test_title_1
    assert response_obj["blog_category_id"] == blog_category_id_1
    assert response_obj["filename"] == test_filename_1
    assert response_obj["updated_date"] == test_updated_date_1

    # 更新
    response = await update_blog(async_client, id, test_title_2, blog_category_id_2, test_filename_2, test_updated_date_2)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == test_title_2
    assert response_obj["blog_category_id"] == blog_category_id_2
    assert response_obj["filename"] == test_filename_2
    assert response_obj["updated_date"] == test_updated_date_2

    # 削除
    response = await delete_blog(async_client, id)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj == None

# 入力チェックテスト
@pytest.mark.asyncio
async def test_input_length(async_client):
    test_title_ng = (
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "a"
    )
    test_filename_ng = (
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "a"
    )
    test_updated_date_ng = "2024-02-31"

    test_name_ok = "test_name_ok"

    test_title_ok = "test_title_ok"
    test_filename_ok = "test_filename_ok.html"
    test_updated_date_ok = "2024-04-01"

    # blog_category作成
    response = await create_blog_category(async_client, test_name_ok)
    response_obj = response.json()
    blog_category_id_1 = response_obj["id"]

    # 作成(title)
    response = await create_blog(async_client, test_title_ng, blog_category_id_1, test_filename_ok, test_updated_date_ok)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 作成(filename)
    response = await create_blog(async_client, test_title_ok, blog_category_id_1, test_filename_ng, test_updated_date_ok)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 作成(updated_date)
    response = await create_blog(async_client, test_title_ok, blog_category_id_1, test_filename_ok, test_updated_date_ng)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 作成
    response = await create_blog(async_client, test_title_ok, blog_category_id_1, test_filename_ok, test_updated_date_ok)
    response_obj = response.json()

    id = response_obj["id"]

    # 更新(title)
    response = await update_blog(async_client, id, test_title_ng, blog_category_id_1, test_filename_ok, test_updated_date_ok)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 更新(filename)
    response = await update_blog(async_client, id, test_title_ok, blog_category_id_1, test_filename_ng, test_updated_date_ok)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 更新(updated_date)
    response = await update_blog(async_client, id, test_title_ok, blog_category_id_1, test_filename_ok, test_updated_date_ng)

    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

# 存在テスト
@pytest.mark.asyncio
async def test_id_exist(async_client):
    test_name_ok = "test_name_ok"

    test_title_ok = "test_title_ok"
    test_filename_ok = "test_filename_ok.html"
    test_updated_date_ok = "2024-04-01"

    # blog_category作成
    response = await create_blog_category(async_client, test_name_ok)
    response_obj = response.json()
    blog_category_id_1 = response_obj["id"]

    # 作成
    response = await create_blog(async_client, test_title_ok, blog_category_id_1, test_filename_ok, test_updated_date_ok)
    response_obj = response.json()

    id = response_obj["id"]

    no_exist_id = id + 1

    # 詳細
    response = await get_blog(async_client, no_exist_id)
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND

    # 更新
    response = await update_blog(async_client, no_exist_id, test_title_ok, blog_category_id_1, test_filename_ok, test_updated_date_ok)
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND

    # 削除
    response = await delete_blog(async_client, no_exist_id)
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND

# 件数テスト
@pytest.mark.asyncio
async def test_count(async_client):
    test_name_ok = "test_name_ok"

    test_title_ok = "test_name_ok"
    test_filename_ok = "test_filename_ok.html"
    test_updated_date_ok = "2024-04-01"

    # blog_category作成
    response = await create_blog_category(async_client, test_name_ok)
    response_obj = response.json()
    blog_category_id_1 = response_obj["id"]

    # 件数
    response = await get_blogs_count(async_client)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["count"] == 0

    # 作成
    await create_blog(async_client, test_title_ok, blog_category_id_1, test_filename_ok, test_updated_date_ok)

    # 件数
    response = await get_blogs_count(async_client)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["count"] == 1

# ページネーションテスト
@pytest.mark.asyncio
async def test_count(async_client):
    base_url = "/blogs"

    test_name_ok = "test_name_ok"

    test_title_1 = "test_title_1"
    test_title_2 = "test_title_2"
    test_title_3 = "test_title_3"
    test_title_4 = "test_title_4"
    test_title_5 = "test_title_5"
    test_filename_ok = "test_filename_ok.html"
    test_updated_date_ok = "2024-04-01"

    # blog_category作成
    response = await create_blog_category(async_client, test_name_ok)
    response_obj = response.json()
    blog_category_id_1 = response_obj["id"]

    # 0件
    response = await get_blogs(async_client, BASE_URL)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 0

    # 作成
    await create_blog(async_client, test_title_1, blog_category_id_1, test_filename_ok, test_updated_date_ok)
    await create_blog(async_client, test_title_2, blog_category_id_1, test_filename_ok, test_updated_date_ok)
    await create_blog(async_client, test_title_3, blog_category_id_1, test_filename_ok, test_updated_date_ok)
    await create_blog(async_client, test_title_4, blog_category_id_1, test_filename_ok, test_updated_date_ok)
    await create_blog(async_client, test_title_5, blog_category_id_1, test_filename_ok, test_updated_date_ok)

    # ページにつき2件、1ページ目
    url = f"{base_url}?page=1&limit=2"
    response = await get_blogs(async_client, url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 2
    assert response_obj[0]["title"] == "test_title_1"
    assert response_obj[1]["title"] == "test_title_2"

    # ページにつき3件、2ページ目
    url = f"{base_url}?page=2&limit=3"
    response = await get_blogs(async_client, url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 2
    assert response_obj[0]["title"] == "test_title_4"
    assert response_obj[1]["title"] == "test_title_5"