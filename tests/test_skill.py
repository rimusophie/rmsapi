import pytest
import starlette.status

BASE_URL = "/skills"

# skill件数
async def get_skills_count(async_client):
    return await async_client.get("/skills_count")

# skill一覧取得
async def get_skills(async_client, url: str):
    return await async_client.get(url)

# skillkeyvalue取得
async def get_skills_keyvalue(async_client):
    return await async_client.get("/skills_keyvalue")

# skill詳細
async def get_skill(async_client, id: int):
    url = f"{BASE_URL}/{id}"
    return await async_client.get(url)

# skill作成
async def create_skill(async_client, name: str, category: int):
    return await async_client.post(
        BASE_URL, 
        json = { 
            "name": name,
            "category": category
        }
    )

# skill更新
async def update_skill(async_client, id: int, name: str, category: int):
    url = f"{BASE_URL}/{id}"
    return await async_client.put(
        url, 
        json = {
            "name": name,
            "category": category
        }
    )

# skill削除
async def delete_skill(async_client, id: int):
    url = f"{BASE_URL}/{id}"
    return await async_client.delete(url)

test_name_tmp = "tmp"
test_name_ok = "test_name_ok"
test_name_ng = ""
for i in range(101):
    test_name_ng += "a"

test_category_tmp = 1
test_category_ok = 2
test_category_ng = -1

test_name_1 = "test_name_1"
test_name_2 = "test_name_2"
test_name_3 = "test_name_3"

test_category_1 = 1
test_category_2 = 2

# createテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_name, input_category, expect_status, expect_name, expect_category",
    [
        (test_name_ok, test_category_ok, starlette.status.HTTP_200_OK, test_name_ok, test_category_ok),
        (test_name_ng, test_category_ok, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_name_ng, test_category_ok),
        (test_name_ok, test_category_ng, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_name_ok, test_category_ng),
    ],
)
async def test_create(input_name, input_category, expect_status, expect_name, expect_category, async_client):
    response = await create_skill(async_client, input_name, input_category)
    assert response.status_code == expect_status

    if response.status_code == starlette.status.HTTP_200_OK:
        response_obj = response.json()
        assert response_obj["id"] != None 
        assert response_obj["name"] == expect_name
        assert response_obj["category"] == expect_category

# updateテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_name, input_category, input_create_id, expect_status, expect_name, expect_category",
    [
        (test_name_ok, test_category_ok, True, starlette.status.HTTP_200_OK, test_name_ok, test_category_ok),
        (test_name_ng, test_category_ok, True, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_name_ng, test_category_ok),
        (test_name_ok, test_category_ng, True, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_name_ok, test_category_ng),
        (test_name_ok, test_category_ok, False, starlette.status.HTTP_404_NOT_FOUND, test_name_ok, test_category_ok),
    ],
)
async def test_update(input_name, input_category, input_create_id, expect_status, expect_name, expect_category, async_client):
    # 作成
    response = await create_skill(async_client, test_name_tmp, test_category_tmp)
    response_obj = response.json()
    id = response_obj["id"]

    if input_create_id == False:
        id = id + 1

    response = await update_skill(async_client, id, input_name, input_category)
    assert response.status_code == expect_status
    
    if response.status_code == starlette.status.HTTP_200_OK:
        response_obj = response.json()
        assert response_obj["id"] == id
        assert response_obj["name"] == expect_name
        assert response_obj["category"] == expect_category

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
    # 作成
    response = await create_skill(async_client, test_name_tmp, test_category_tmp)
    response_obj = response.json()
    id = response_obj["id"]

    if input_create_id == False:
        id = id + 1

    response = await delete_skill(async_client, id)
    assert response.status_code == expect_status

# detailテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_name, input_category, input_create_id, expect_status, expect_name, expect_category",
    [
        (test_name_ok, test_category_ok, True, starlette.status.HTTP_200_OK, test_name_ok, test_category_ok),
        (test_name_ok, test_category_ok, False, starlette.status.HTTP_404_NOT_FOUND, test_name_ok, test_category_ok),
    ],
)
async def test_detail(input_name, input_category, input_create_id, expect_status, expect_name, expect_category, async_client):
    # 作成
    response = await create_skill(async_client, input_name, input_category)
    response_obj = response.json()
    id = response_obj["id"]

    if input_create_id == False:
        id = id + 1

    response = await get_skill(async_client, id)
    assert response.status_code == expect_status
    
    if response.status_code == starlette.status.HTTP_200_OK:
        response_obj = response.json()
        assert response_obj["id"] == id
        assert response_obj["name"] == expect_name
        assert response_obj["category"] == expect_category

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
    # 作成
    ids = [0] * 5
    for i in range(len(ids)):
        response = await create_skill(async_client, test_name_tmp, test_category_tmp)
        response_obj = response.json()
        ids[i] = response_obj["id"]

    url = f"{BASE_URL}?page={input_page}&limit={input_limit}"
    response = await get_skills(async_client, url)
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
    # 作成
    for i in range(input_count):
        await create_skill(async_client, test_name_tmp, test_category_tmp)

    # 件数
    response = await get_skills_count(async_client)
    assert response.status_code == expect_status
    response_obj = response.json()
    assert response_obj["count"] == expect_count

# keyvalueテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_names, input_categories, expect_status, expect_names",
    [
        (
            [test_name_1, test_name_2, test_name_3], 
            [test_category_1, test_category_1, test_category_2],
            starlette.status.HTTP_200_OK, 
            [test_name_1, test_name_2, test_name_3]
        ),
        (
            [test_name_3, test_name_1, test_name_2], 
            [test_category_1, test_category_2, test_category_2],
            starlette.status.HTTP_200_OK, 
            [test_name_3, test_name_1, test_name_2]
        ),
    ],
)
async def test_keyvalue(input_names, input_categories, expect_status, expect_names, async_client):
    # 作成
    for i in range(len(input_names)):
        await create_skill(async_client, input_names[i], input_categories[i])

    response = await get_skills_keyvalue(async_client)
    assert response.status_code == expect_status
    response_obj = response.json()

    for i in range(len(expect_names)):
        assert response_obj[i]["name"] == expect_names[i]