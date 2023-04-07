# Nike Flask Backend

## 系統需求
### Python
- Version: >= `3.10`

### 建立 python virtual environment
在 project 目錄下執行下面的 command

```bash
python3 -m venv venv
. venv/bin/activate
```

### 安裝 dependency
```bash
pip install -r requirements.txt
pip install -e '.[dev]' --index-url https://tv-pypi:Leadinfo@dev.tradingvalley.com/pypi
```

### 設定檔 Config
複製 `config/sample_api_config.py` 到 `config/api_config.py`，接著修改 `config/api_config.py` 配置內容

複製  `alembic.ini_sample` 到 `alembic.ini`

### Docker
若需要起 Local docker server

- redis
- mysql

在 project 目錄下執行

```bash
docker-compose down && docker-compose up
```