# llm

## 仮想環境を作成(dockerの場合)
```bash
docker compose build
```

## 仮想環境を作成(venvの場合)
```bash
python -m venv .venv
. venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt
```

---

### Config

 `.env` ファイルに以下を設定してください。langchainのAPIキーは[こちら](https://smith.langchain.com/settings)から取得。

```python
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=""
LANGCHAIN_PROJECT=""
OPENAI_API_KEY=""
GOOGLE_API_KEY=""
```

## 実行
### dockerの場合

```bash
docker compose up
```

#### container内に入る

```bash
docker container exec -it <container> /bin/bash
```

#### db containerに入る
```bash
docker-compose exec db mysql demo
```

#### db migration
```bash
docker-compose exec demo-app python migrate_db.py
```

#### test実行
```bash
docker-compose run --entrypoint pytest demo-app
```

### ローカル環境の場合
```bash
uvicorn api.main:app --reload
```

`http://127.0.0.1:8000/docs` にアクセスして、APIを試すことができます。

langserveのapp_routesでendpointを定義していれば `http://127.0.0.1:8000/translate/playground/` などで動作を試せます

## cloud upload

### GCP
#### build
```bash
docker build -t gcr.io/trans-proposal-441803-v6/demo-app:latest --platform linux/amd64 -f Dockerfile.cloud .
```
#### push
```bash
docker push gcr.io/trans-proposal-441803-v6/demo-app:latest
```
Artifact Registry API を有効化している必要がある

#### confirm
```bash
gcloud container images list
```

### 参考
- [FastAPI](https://fastapi.tiangolo.com/ja/)
- [Zenn books FastAPI入門](https://zenn.dev/sh0nk/books/537bb028709ab9)
- [動かして学ぶ！Python FastAPI開発入門](https://www.shoeisha.co.jp/book/detail/9784798177229)
- [LangChain](https://langchain.com/)
- [LangSmith](https://smith.langchain.com/)
