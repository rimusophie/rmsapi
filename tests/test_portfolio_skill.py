import pytest
from sqlalchemy.exc import IntegrityError
import starlette.status
from tests.test_skill import create_skill
from tests.test_portfolio import create_portfolio

BASE_URL = "/portfolio_skills"

# portfolio_skill件数
async def get_portfolio_skills_count(async_client):
    return await async_client.get("/portfolio_skills_count")

# portfolio_skill一覧取得
async def get_portfolio_skills(async_client, url: str):
    return await async_client.get(url)

# portfolio_skill詳細
async def get_portfolio_skill(async_client, id: int):
    url = f"{BASE_URL}/{id}"
    return await async_client.get(url)

# portfolio_skill作成
async def create_portfolio_skill(async_client, portfolio_id: int, skill_id: int):
    return await async_client.post(
        BASE_URL, 
        json = { 
            "portfolio_id": portfolio_id,
            "skill_id": skill_id
        }
    )

# portfolio_skill更新
async def update_portfolio_skill(async_client, id: int, portfolio_id: int, skill_id: int):
    url = f"{BASE_URL}/{id}"
    return await async_client.put(
        url, 
        json = {
            "portfolio_id": portfolio_id,
            "skill_id": skill_id
        }
    )

# portfolio_skill削除
async def delete_portfolio_skill(async_client, id: int):
    url = f"{BASE_URL}/{id}"
    return await async_client.delete(url)

test_skill_name_tmp = "tmp"
test_skill_category_tmp = 1
test_portfolio_name_tmp = "tmp"
test_portfolio_remark_tmp = "tmp"

# createテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_portfolio_create_id, input_skill_create_id, expect_status, expect_raise_error",
    [
        (True, True, starlette.status.HTTP_200_OK, False),
        (True, False, starlette.status.HTTP_200_OK, True),
        (False, True, starlette.status.HTTP_200_OK, True),
    ],
)
async def test_create(input_portfolio_create_id, input_skill_create_id, expect_status, expect_raise_error, async_client):
    # portfolio作成
    response = await create_portfolio(async_client, test_portfolio_name_tmp, test_portfolio_remark_tmp)
    response_obj = response.json()
    portfolio_id = response_obj["id"]

    # skill作成
    response = await create_skill(async_client, test_skill_name_tmp, test_skill_category_tmp)
    response_obj = response.json()
    skill_id = response_obj["id"]

    if input_portfolio_create_id == False:
        portfolio_id = portfolio_id + 1

    if input_skill_create_id == False:
        skill_id = skill_id + 1

    if input_portfolio_create_id == False or input_skill_create_id == False:
        with pytest.raises(IntegrityError) as e:
            response = await create_portfolio_skill(async_client, portfolio_id, skill_id)
        assert expect_raise_error
    else:
        response = await create_portfolio_skill(async_client, portfolio_id, skill_id)
        assert response.status_code == expect_status

        if response.status_code == starlette.status.HTTP_200_OK:
            response_obj = response.json()
            assert response_obj["id"] != None 
            assert response_obj["portfolio_id"] == portfolio_id
            assert response_obj["skill_id"] == skill_id

# updateテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_portfolio_create_id, input_skill_create_id, input_create_id, expect_status, expect_raise_error",
    [
        (True, True, True, starlette.status.HTTP_200_OK, False),
        (True, False, True, starlette.status.HTTP_200_OK, True),
        (False, True, True, starlette.status.HTTP_200_OK, True),
        (True, True, False, starlette.status.HTTP_404_NOT_FOUND, False),
    ],
)
async def test_update(input_portfolio_create_id, input_skill_create_id, input_create_id, expect_status, expect_raise_error, async_client):
    # portfolio作成
    response = await create_portfolio(async_client, test_portfolio_name_tmp, test_portfolio_remark_tmp)
    response_obj = response.json()
    portfolio_id_1 = response_obj["id"]

    # portfolio作成
    response = await create_portfolio(async_client, test_portfolio_name_tmp, test_portfolio_remark_tmp)
    response_obj = response.json()
    portfolio_id_2 = response_obj["id"]

    # skill作成
    response = await create_skill(async_client, test_skill_name_tmp, test_skill_category_tmp)
    response_obj = response.json()
    skill_id_1 = response_obj["id"]

    # skill作成
    response = await create_skill(async_client, test_skill_name_tmp, test_skill_category_tmp)
    response_obj = response.json()
    skill_id_2 = response_obj["id"]

    # 作成
    response = await create_portfolio_skill(async_client, portfolio_id_1, skill_id_1)
    response_obj = response.json()
    id = response_obj["id"]

    if input_portfolio_create_id == False:
        portfolio_id_2 = portfolio_id_2 + 1

    if input_skill_create_id == False:
        skill_id_2 = skill_id_2 + 1

    if input_create_id == False:
        id = id + 1

    if input_portfolio_create_id == False or input_skill_create_id == False:
        with pytest.raises(IntegrityError) as e:
            response = await update_portfolio_skill(async_client, id, portfolio_id_2, skill_id_2)
        assert expect_raise_error
    else:
        response = await update_portfolio_skill(async_client, id, portfolio_id_2, skill_id_2)
        assert response.status_code == expect_status
        
        if response.status_code == starlette.status.HTTP_200_OK:
            response_obj = response.json()
            assert response_obj["id"] == id
            assert response_obj["portfolio_id"] == portfolio_id_2
            assert response_obj["skill_id"] == skill_id_2

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
    # portfolio作成
    response = await create_portfolio(async_client, test_portfolio_name_tmp, test_portfolio_remark_tmp)
    response_obj = response.json()
    portfolio_id = response_obj["id"]

    # skill作成
    response = await create_skill(async_client, test_skill_name_tmp, test_skill_category_tmp)
    response_obj = response.json()
    skill_id = response_obj["id"]

    # 作成
    response = await create_portfolio_skill(async_client, portfolio_id, skill_id)
    response_obj = response.json()
    id = response_obj["id"]

    if input_create_id == False:
        id = id + 1

    response = await delete_portfolio_skill(async_client, id)
    assert response.status_code == expect_status

# detailテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_create_id, expect_status",
    [
        (True, starlette.status.HTTP_200_OK),
        (False, starlette.status.HTTP_404_NOT_FOUND),
    ],
)
async def test_detail(input_create_id, expect_status, async_client):
    # portfolio作成
    response = await create_portfolio(async_client, test_portfolio_name_tmp, test_portfolio_remark_tmp)
    response_obj = response.json()
    portfolio_id = response_obj["id"]

    # skill作成
    response = await create_skill(async_client, test_skill_name_tmp, test_skill_category_tmp)
    response_obj = response.json()
    skill_id = response_obj["id"]

    # 作成
    response = await create_portfolio_skill(async_client, portfolio_id, skill_id)
    response_obj = response.json()
    id = response_obj["id"]

    if input_create_id == False:
        id = id + 1

    response = await get_portfolio_skill(async_client, id)
    assert response.status_code == expect_status
    
    if response.status_code == starlette.status.HTTP_200_OK:
        response_obj = response.json()
        assert response_obj["id"] == id
        assert response_obj["portfolio_id"] == portfolio_id
        assert response_obj["skill_id"] == skill_id

# listテスト
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_page, input_limit, filter_portfolio_index, filter_skill_index, expect_status, expect_len, expect_index",
    [
        (0, 3, None, None, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, 0, -1),  # page異常
        (1, 3, None, None, starlette.status.HTTP_200_OK, 3, 0),   # 1ページ目3件出力(正常)
        (2, 3, None, None, starlette.status.HTTP_200_OK, 2, 3),   # 2ページ目3件出力(2件出力)
        (3, 3, None, None, starlette.status.HTTP_200_OK, 0, -1),            # 3ページ目3件出力(0件出力)
        (1, 0, None, None, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, 0, -1),  # limit異常
        (1, 10, None, None, starlette.status.HTTP_200_OK, 5, 0),  # 1ページ目10件出力(5件出力)
        (2, 10, None, None, starlette.status.HTTP_200_OK, 0, -1),  # 2ページ目10件出力(0件出力)
        (1, 10, 1, None, starlette.status.HTTP_200_OK, 1, 1),  # portfolio_idのみ絞り
        (1, 10, None, 2, starlette.status.HTTP_200_OK, 1, 2),  # skill_idのみ絞り
        (1, 10, 3, 3, starlette.status.HTTP_200_OK, 1, 3),  # portfolio_id、skill_id絞り
    ],
)
async def test_list(input_page, input_limit, filter_portfolio_index, filter_skill_index, expect_status, expect_len, expect_index, async_client):
    # portfolio作成
    portfolio_ids = [0] * 5
    for i in range(len(portfolio_ids)):
        response = await create_portfolio(async_client, test_portfolio_name_tmp, test_portfolio_remark_tmp)
        response_obj = response.json()
        portfolio_ids[i] = response_obj["id"]

    # skill作成
    skill_ids = [0] * 5
    for i in range(len(skill_ids)):
        response = await create_skill(async_client, test_skill_name_tmp, test_skill_category_tmp)
        response_obj = response.json()
        skill_ids[i] = response_obj["id"]

    # 作成
    ids = [0] * 5
    for i in range(len(ids)):
        response = await create_portfolio_skill(async_client, portfolio_ids[i], skill_ids[i])
        response_obj = response.json()
        ids[i] = response_obj["id"]

    url = f"{BASE_URL}?page={input_page}&limit={input_limit}"
    if filter_portfolio_index != None:
        url = f"{url}&portfolio_id={portfolio_ids[filter_portfolio_index]}"
    
    if filter_skill_index != None:
        url = f"{url}&skill_id={skill_ids[filter_skill_index]}"

    response = await get_portfolio_skills(async_client, url)
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
    # portfolio作成
    response = await create_portfolio(async_client, test_portfolio_name_tmp, test_portfolio_remark_tmp)
    response_obj = response.json()
    portfolio_id = response_obj["id"]

    # skill作成
    response = await create_skill(async_client, test_skill_name_tmp, test_skill_category_tmp)
    response_obj = response.json()
    skill_id = response_obj["id"]

    # 作成
    for i in range(input_count):
        await create_portfolio_skill(async_client, portfolio_id, skill_id)

    # 件数
    response = await get_portfolio_skills_count(async_client)
    assert response.status_code == expect_status
    response_obj = response.json()
    assert response_obj["count"] == expect_count