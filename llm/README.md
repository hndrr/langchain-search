# llm

## 仮想環境を作成(dockerの場合)
```bashd
docker compose build
```

## 仮想環境を作成(venvの場合)

```bash
python -m venv .venv
. venv/bin/activate
```

### 依存関係をインストール

```bash
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

```
docker compose up
```

### ローカル環境の場合
```bash
uvicorn api.main:app --reload
```

`http://127.0.0.1:8000/docs` にアクセスして、APIを試すことができます。

langserveのapp_routesでendpointを定義していれば `http://127.0.0.1:8000/translate/playground/` などで動作を試せます

### 参考

- [LangChainとLangGraphによるRAG・AIエージェント［実践］入門](https://gihyo.jp/book/2024/978-4-297-14530-9)
- [Software Design 2024年8月号 第1特集 LangChainではじめるLLMアプリ開発入門](https://gihyo.jp/magazine/SD/archive/2024/202408)
- [LangChain](https://langchain.com/)
- [LangSmith](https://smith.langchain.com/)
- [Gradio](https://www.gradio.app/)
