# Splendor
![1676534655616](https://user-images.githubusercontent.com/51017677/219304429-1d148690-103b-45b2-82cb-97a13a280baa.jpg)

討論過程:https://miro.com/app/board/uXjVPoRiOXE=/
# Intro your game
[遊戲簡介](https://www.youtube.com/watch?v=-miXa-5tB8A)
# My Practice Stack(使用的軟體方法論)
   1. Event Storming
   2. Example Mapping
   3. OOAD
   4. ATDD
   5. mod programming

### Tech Stack
   1. 前端:React
   2. 後端:Python(flask)
   3. DB:MongoDB

## 專案架構
```bash
.
├── alembic             # database migration
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions        # migration version
├── alembic.ini_sample  # database migration config
├── application         # usercase
├── domain              # domain entity
├── interface           # interface adapter
│   ├── api             # 處理http request
│   ├── repository      # 處理資料庫溝通
├── config              # config
│   └── sample_api_config.py
├── docker              # docker mysql redis config
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
[安裝參考](https://blog.kyomind.tw/python-poetry/)

安裝完成Poetry後，執行下面的指令修改設定檔
- 虛擬環境的路徑改為「專案的根目錄」
- 名稱固定為`.venv`。
```bash
poetry config virtualenvs.in-project true
```
### 下載專案
```bash
git clone https://github.com/Game-as-a-Service/splendor.git
```

### 安裝 dependency
```bash
poetry shell  # 啟用虛擬環境，若沒有虛擬環境自動幫你建立並使用
poetry install  # 依poetry.lock記載的套件版本安裝到虛擬環境中，類似npm install \
```
開發過程需要安裝套件
```bash
poetry add xxx  # 安裝套件至全部環境
poetry add --group dev xxx  # 只在開發環境安裝套件
poetry remove xxx  # 移除套件
```
### 設定檔 Config
複製 `config/sample_api_config.py` 到 `config/api_config.py`，接著修改 `config/api_config.py` 配置內容，目前無需修改
```bash
cp config/sample_api_config.py config/api_config.py
```


複製  `alembic.ini_sample` 到 `alembic.ini` 並把55行的改成`sqlalchemy.url = mysql+pymysql://root:secret@127.0.0.1:3306/splendor`
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
確認 docker container 是否正常運作，執行下面的指令，需看到 `mysql` 與 `redis` 的 container
```bash
docker ps
```
進入 mysql container
```bash
docker exec -it mysql8 mysql -psecret
# 退出
exit
```
### mysql資料庫 migration，無須進入container，在專案目錄下執行即可
```bash
alembic upgrade heads # 進版
```
### 如果開發過程需要修改資料庫結構，可以透過下面指令
```bash
alembic upgrade heads # 進版 往前到最新版本
alembic downgrade base # 回版 往後到最舊版本
alembic revision -m "message" # 產生migration檔案
```
### 啟動專案
- 方法一指令
```bash
export FLASK_APP=mainapp.py
flask run
```
- 方法二vscode launch.json
```
mkdir .vscode
touch .vscode/launch.json
```
把以下參數丟入launch.json
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "mainapp.py",
                "FLASK_ENV": "development"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true
        }
    ]
}
```
按下F5即可啟動

### 專案啟動後，可以透過下面的URL，來確認是否正常運作
`127.0.0.1:5000`
`127.0.0.1:5000/open-api-spec`

## 開發流程
### 建立新的 branch
```bash
git checkout -b feature/xxx
```
### 先寫測試
### 寫程式
### 直到把測試跑過
### 寫swagger文件
### 推上github
```bash
git add .
git commit -m "xxx"
git push origin feature/xxx
```
