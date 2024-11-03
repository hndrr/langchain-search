# llm

## 仮想環境を作成(venvの場合)

```bash
python -m venv .venv
. venv/bin/activate
```

依存関係をインストール

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

### 参考

- [LangChainとLangGraphによるRAG・AIエージェント［実践］入門](https://gihyo.jp/book/2024/978-4-297-14530-9)
- [Software Design 2024年8月号 第1特集 LangChainではじめるLLMアプリ開発入門](https://gihyo.jp/magazine/SD/archive/2024/202408)
- [LangChain](https://langchain.com/)
- [LangSmith](https://smith.langchain.com/)
- [Gradio](https://www.gradio.app/)
