import config
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


# 翻訳する関数を定義
def translate_text(llm: str):
    if llm == "gpt-4o-mini":
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    elif llm == "gpt-4o":
        model = ChatOpenAI(model="gpt-4o", temperature=0)
    elif llm == "gemini-1.5-flash":
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    elif llm == "gemini-1.5-pro":
        model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
    else:
        raise ValueError(f"Invalid LLM: {llm}")

    parser = StrOutputParser()
    messages = ChatPromptTemplate(
        [
            ("system", "Translate the following text to {target_language}"),
            ("user", "{text}"),
        ]
    )
    chain = messages | model | parser

    return chain
