# Gem

## 專案架構
```bash
.
├── alembic             # database migration
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions        # migration version
├── alembic.ini_sample  # database migration config
├── application                 # api
├── domain           
├── interface
│   ├── api     
│   ├── open-api-spec   # open api spec
│   ├── dbmodels
├── config              # config
│   └── sample_api_config.py
├── docker              # docker mysql redis config
│   ├── mysql-conf
│   ├── mysql-dumps
│   └── redis-conf
├── docker-compose.yaml # docker-compose config
├── Dockerfile
├── logs                # log
├── mainapp.py          # Flask app entry point
├── tests               # test         
├── pyproject.toml
├── README.md
├── requirements.txt
├── scripts
├── setup.cfg
├── setup.py
├── start-dev.py
└── poetry.lock
```

## 系統需求
### Python
- Version: >= `3.10`

### 使用Poetry 管理套件與環境
在 project 目錄下執行下面的 command
[Poetry](https://blog.kyomind.tw/python-poetry/)

安裝完成Poetry後，執行下面的指令修改設定檔
- 虛擬環境的路徑改為「專案的根目錄」
- 名稱固定為`.venv`。
```bash
poetry config virtualenvs.in-project true
```

### 安裝 dependency
```bash
poetry init  # 初始化，建立 pyproject.toml
poetry env use python  # 建立專案虛擬環境並使用
poetry shell  # 啟用虛擬環境，若沒有虛擬環境自動幫你建立並使用
poetry install  # 依poetry.lock記載的套件版本安裝到虛擬環境中，類似npm install \
poetry add xxx  # == pip install xxx
poetry add --group dev xxx  # == pip install in dev
poetry remove xxx  # == pip uninstall xxx  
```

### 設定檔 Config
複製 `config/sample_api_config.py` 到 `config/api_config.py`，接著修改 `config/api_config.py` 配置內容
```bash
cp config/sample_api_config.py config/api_config.py
```


複製  `alembic.ini_sample` 到 `alembic.ini` 並配置sqlalchemy.url
```bash
cp alembic.ini_sample alembic.ini
```
### Docker
若需要起 Local docker server

- redis
- mysql

在 project 目錄下執行

```bash
docker-compose down && docker-compose up -d
```

### mysql資料庫 migration
```bash
alembic upgrade heads # 進版
alembic downgrade base # 回版
alembic revision -m "message" # 產生migration檔案
```