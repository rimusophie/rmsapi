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

test_title_tmp = "tmp"
test_title_ok = "test_title_ok"
test_title_ng = ""
for i in range(201):
    test_title_ng += "a"

test_filename_tmp = "tmp.html"
test_filename_ok = "test_filename_ok.html"
test_filename_ng = ""
for i in range(251):
    test_filename_ng += "a"

test_updated_date_ok = "2024-04-01"
test_updated_date_tmp = "2024-01-01"
test_updated_date_ng = "2024-02-31"

test_blog_category_name_tmp = "tmp"

# createテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_title, input_filename, input_updated_date, expect_status, expect_title, expect_filename, expect_updated_date",
    [
        (test_title_ok, test_filename_ok, test_updated_date_ok, starlette.status.HTTP_200_OK, test_title_ok, test_filename_ok, test_updated_date_ok),
        (test_title_ng, test_filename_ok, test_updated_date_ok, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_title_ng, test_filename_ok, test_updated_date_ok),
        (test_title_ok, test_filename_ng, test_updated_date_ok, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_title_ok, test_filename_ng, test_updated_date_ok),
        (test_title_ok, test_filename_ok, test_updated_date_ng, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_title_ok, test_filename_ok, test_updated_date_ng),
    ],
)
async def test_create(input_title, input_filename, input_updated_date, expect_status, expect_title, expect_filename, expect_updated_date, async_client):
    # blog_categoroy作成
    response = await create_blog_category(async_client, test_blog_category_name_tmp)
    response_obj = response.json()
    blog_category_id = response_obj["id"]

    response = await create_blog(async_client, input_title, blog_category_id, input_filename, input_updated_date)
    assert response.status_code == expect_status

    if response.status_code == starlette.status.HTTP_200_OK:
        response_obj = response.json()
        assert response_obj["id"] != None 
        assert response_obj["title"] == expect_title
        assert response_obj["blog_category_id"] == blog_category_id
        assert response_obj["filename"] == expect_filename
        assert response_obj["updated_date"] == expect_updated_date

# updateテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_title, input_filename, input_updated_date, input_create_id, expect_status, expect_title, expect_filename, expect_updated_date",
    [
        (test_title_ok, test_filename_ok, test_updated_date_ok, True, starlette.status.HTTP_200_OK, test_title_ok, test_filename_ok, test_updated_date_ok),
        (test_title_ng, test_filename_ok, test_updated_date_ok, True, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_title_ng, test_filename_ok, test_updated_date_ok),
        (test_title_ok, test_filename_ng, test_updated_date_ok, True, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_title_ok, test_filename_ng, test_updated_date_ok),
        (test_title_ok, test_filename_ok, test_updated_date_ng, True, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_title_ok, test_filename_ok, test_updated_date_ng),
        (test_title_ok, test_filename_ok, test_updated_date_ok, False, starlette.status.HTTP_404_NOT_FOUND, test_title_ok, test_filename_ok, test_updated_date_ok),
    ],
)
async def test_update(input_title, input_filename, input_updated_date, input_create_id, expect_status, expect_title, expect_filename, expect_updated_date, async_client):
    # blog_categoroy作成
    response = await create_blog_category(async_client, test_blog_category_name_tmp)
    response_obj = response.json()
    blog_category_id_1 = response_obj["id"]

    # blog_categoroy作成
    response = await create_blog_category(async_client, test_blog_category_name_tmp)
    response_obj = response.json()
    blog_category_id_2 = response_obj["id"]

    # 作成
    response = await create_blog(async_client, test_title_tmp, blog_category_id_1,  test_filename_tmp, test_updated_date_tmp)
    response_obj = response.json()
    id = response_obj["id"]

    if input_create_id == False:
        id = id + 1

    response = await update_blog(async_client, id, input_title, blog_category_id_2, input_filename, input_updated_date)
    assert response.status_code == expect_status
    
    if response.status_code == starlette.status.HTTP_200_OK:
        response_obj = response.json()
        assert response_obj["id"] == id
        assert response_obj["title"] == expect_title
        assert response_obj["blog_category_id"] == blog_category_id_2
        assert response_obj["filename"] == expect_filename
        assert response_obj["updated_date"] == expect_updated_date

# deleteテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_create_id, expect_status",
    [
        (True, starlette.status.HTTP_200_OK),
        (False, starlette.status.HTTP_404_NOT_FOUND),
    ],
)
async def test_delete(input_create_id, expect_status, async_client):
    # blog_categoroy作成
    response = await create_blog_category(async_client, test_blog_category_name_tmp)
    response_obj = response.json()
    blog_category_id = response_obj["id"]

    # 作成
    response = await create_blog(async_client, test_title_tmp, blog_category_id, test_filename_tmp, test_updated_date_tmp)
    response_obj = response.json()
    id = response_obj["id"]

    if input_create_id == False:
        id = id + 1

    response = await delete_blog(async_client, id)
    assert response.status_code == expect_status

# detailテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_title, input_filename, input_updated_date, input_create_id, expect_status, expect_title, expect_filename, expect_updated_date",
    [
        (test_title_ok, test_filename_ok, test_updated_date_ok, True, starlette.status.HTTP_200_OK, test_title_ok, test_filename_ok, test_updated_date_ok),
        (test_title_ok, test_filename_ok, test_updated_date_ok, False, starlette.status.HTTP_404_NOT_FOUND, test_title_ok, test_filename_ok, test_updated_date_ok),
    ],
)
async def test_detail(input_title, input_filename, input_updated_date, input_create_id, expect_status, expect_title, expect_filename, expect_updated_date, async_client):
    # blog_categoroy作成
    response = await create_blog_category(async_client, test_blog_category_name_tmp)
    response_obj = response.json()
    blog_category_id = response_obj["id"]

    # 作成
    response = await create_blog(async_client, input_title, blog_category_id, input_filename, input_updated_date)
    response_obj = response.json()
    id = response_obj["id"]

    if input_create_id == False:
        id = id + 1

    response = await get_blog(async_client, id)
    assert response.status_code == expect_status
    
    if response.status_code == starlette.status.HTTP_200_OK:
        response_obj = response.json()
        assert response_obj["id"] == id
        assert response_obj["title"] == expect_title
        assert response_obj["blog_category_id"] == blog_category_id
        assert response_obj["filename"] == expect_filename
        assert response_obj["updated_date"] == expect_updated_date

# listテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_page, input_limit, expect_status, expect_len, expect_index",
    [
        (0, 3, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, 0, -1),  # page異常
        (1, 3, starlette.status.HTTP_200_OK, 3, 0),   # 1ページ目3件出力(正常)
        (2, 3, starlette.status.HTTP_200_OK, 2, 3),   # 2ページ目3件出力(2件出力)
        (3, 3, starlette.status.HTTP_200_OK, 0, -1),            # 3ページ目3件出力(0件出力)
        (1, 0, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, 0, -1),  # limit異常
        (1, 10, starlette.status.HTTP_200_OK, 5, 0),  # 1ページ目10件出力(5件出力)
        (2, 10, starlette.status.HTTP_200_OK, 0, -1),  # 2ページ目10件出力(0件出力)
    ],
)
async def test_list(input_page, input_limit, expect_status, expect_len, expect_index, async_client):
    # blog_categoroy作成
    response = await create_blog_category(async_client, test_blog_category_name_tmp)
    response_obj = response.json()
    blog_category_id = response_obj["id"]

    # 作成
    ids = [0] * 5
    for i in range(len(ids)):
        response = await create_blog(async_client, test_title_tmp, blog_category_id, test_filename_tmp, test_updated_date_tmp)
        response_obj = response.json()
        ids[i] = response_obj["id"]

    url = f"{BASE_URL}?page={input_page}&limit={input_limit}"
    response = await get_blogs(async_client, url)
    assert response.status_code == expect_status

    if expect_status == starlette.status.HTTP_200_OK:
        response_obj = response.json()
        assert len(response_obj) == expect_len

        if len(response_obj) > 0:
            assert response_obj[0]["id"] == ids[expect_index]

# countテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_count, expect_status, expect_count",
    [
        (0, starlette.status.HTTP_200_OK, 0),
        (3, starlette.status.HTTP_200_OK, 3),
    ],
)
async def test_count(input_count, expect_status, expect_count, async_client):
    # blog_categoroy作成
    response = await create_blog_category(async_client, test_blog_category_name_tmp)
    response_obj = response.json()
    blog_category_id = response_obj["id"]

    # 作成
    for i in range(input_count):
        await create_blog(async_client, test_title_tmp, blog_category_id, test_filename_tmp, test_updated_date_tmp)

    # 件数
    response = await get_blogs_count(async_client)
    assert response.status_code == expect_status
    response_obj = response.json()
    assert response_obj["count"] == expect_count