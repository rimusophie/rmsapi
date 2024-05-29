import pytest
import starlette.status

BASE_URL = "/portfolios"

# portfolio件数
async def get_portfolios_count(async_client):
    return await async_client.get("/portfolios_count")

# portfolio一覧取得
async def get_portfolios(async_client, url: str):
    return await async_client.get(url)

# portfolio詳細
async def get_portfolio(async_client, id: int):
    url = f"{BASE_URL}/{id}"
    return await async_client.get(url)

# portfolio作成
async def create_portfolio(async_client, name: str, remark: str):
    return await async_client.post(
        BASE_URL, 
        json = { 
            "name": name,
            "remark": remark
        }
    )

# portfolio更新
async def update_portfolio(async_client, id: int, name: str, remark: str):
    url = f"{BASE_URL}/{id}"
    return await async_client.put(
        url, 
        json = {
            "name": name,
            "remark": remark
        }
    )

# portfolio削除
async def delete_portfolio(async_client, id: int):
    url = f"{BASE_URL}/{id}"
    return await async_client.delete(url)

test_name_tmp = "tmp"
test_name_ok = "test_name_ok"
test_name_ng = ""
for i in range(201):
    test_name_ng += "a"

test_remark_tmp = "tmp"
test_remark_ok = "test_remark_ok"
test_remark_ng = ""
for i in range(501):
        test_remark_ng += "a"

# createテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_name, input_remark, expect_status, expect_name, expect_remark",
    [
        (test_name_ok, test_remark_ok, starlette.status.HTTP_200_OK, test_name_ok, test_remark_ok),
        (test_name_ng, test_remark_ok, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_name_ng, test_remark_ok),
        (test_name_ok, test_remark_ng, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_name_ok, test_remark_ng),
    ],
)
async def test_create(input_name, input_remark, expect_status, expect_name, expect_remark, async_client):
    response = await create_portfolio(async_client, input_name, input_remark)
    assert response.status_code == expect_status

    if response.status_code == starlette.status.HTTP_200_OK:
        response_obj = response.json()
        assert response_obj["id"] != None 
        assert response_obj["name"] == expect_name
        assert response_obj["remark"] == expect_remark

# updateテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_name, input_remark, input_create_id, expect_status, expect_name, expect_remark",
    [
        (test_name_ok, test_remark_ok, True, starlette.status.HTTP_200_OK, test_name_ok, test_remark_ok),
        (test_name_ng, test_remark_ok, True, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_name_ng, test_remark_ok),
        (test_name_ok, test_remark_ng, True, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, test_name_ok, test_remark_ng),
        (test_name_ok, test_remark_ok, False, starlette.status.HTTP_404_NOT_FOUND, test_name_ok, test_remark_ok),
    ],
)
async def test_update(input_name, input_remark, input_create_id, expect_status, expect_name, expect_remark, async_client):
    # 作成
    response = await create_portfolio(async_client, test_name_tmp, test_remark_tmp)
    response_obj = response.json()
    id = response_obj["id"]

    if input_create_id == False:
        id = id + 1

    response = await update_portfolio(async_client, id, input_name, input_remark)
    assert response.status_code == expect_status
    
    if response.status_code == starlette.status.HTTP_200_OK:
        response_obj = response.json()
        assert response_obj["id"] == id
        assert response_obj["name"] == expect_name
        assert response_obj["remark"] == expect_remark

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
    response = await create_portfolio(async_client, test_name_tmp, test_remark_tmp)
    response_obj = response.json()
    id = response_obj["id"]

    if input_create_id == False:
        id = id + 1

    response = await delete_portfolio(async_client, id)
    assert response.status_code == expect_status

# detailテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_name, input_remark, input_create_id, expect_status, expect_name, expect_remark",
    [
        (test_name_ok, test_remark_ok, True, starlette.status.HTTP_200_OK, test_name_ok, test_remark_ok),
        (test_name_ok, test_remark_ok, False, starlette.status.HTTP_404_NOT_FOUND, test_name_ok, test_remark_ok),
    ],
)
async def test_detail(input_name, input_remark, input_create_id, expect_status, expect_name, expect_remark, async_client):
    # 作成
    response = await create_portfolio(async_client, input_name, input_remark)
    response_obj = response.json()
    id = response_obj["id"]

    if input_create_id == False:
        id = id + 1

    response = await get_portfolio(async_client, id)
    assert response.status_code == expect_status
    
    if response.status_code == starlette.status.HTTP_200_OK:
        response_obj = response.json()
        assert response_obj["id"] == id
        assert response_obj["name"] == expect_name
        assert response_obj["remark"] == expect_remark

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
        response = await create_portfolio(async_client, test_name_tmp, test_remark_tmp)
        response_obj = response.json()
        ids[i] = response_obj["id"]

    url = f"{BASE_URL}?page={input_page}&limit={input_limit}"
    response = await get_portfolios(async_client, url)
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
        await create_portfolio(async_client, test_name_tmp, test_remark_tmp)

    # 件数
    response = await get_portfolios_count(async_client)
    assert response.status_code == expect_status
    response_obj = response.json()
    assert response_obj["count"] == expect_count