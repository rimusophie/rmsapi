# DB接続のユーザーID
DB_USER_ID: str = ""

# DB接続のパスワード
DB_PASSWORD: str = ""

# DB接続のポート
DB_PORT: str = ""

# DB接続のDB名
DB_NAME: str = ""

# テストDB接続先
ASYNC_DB_URL: str = f"mysql+aiomysql://{DB_USER_ID}:{DB_PASSWORD}@db:{DB_PORT}/{DB_NAME}?charset=utf8"

# マイグレーション用
DB_URL: str = f"mysql+pymysql://{DB_USER_ID}:{DB_PASSWORD}@db:{DB_PORT}/{DB_NAME}?charset=utf8"