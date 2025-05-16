import os
from dotenv import load_dotenv
from langfuse import Langfuse
from openai import OpenAI

# .env 파일 로드
load_dotenv()

# Langfuse 및 OpenAI 초기화
langfuse = Langfuse()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 문서 로딩
with open("data/chat_text.txt", "r", encoding="utf-8") as f:
    document = f.read()

# 프롬프트 템플릿 로딩
with open("data/prompt_v1.txt", "r", encoding="utf-8") as f:
    prompt_template = f.read()

# 최종 프롬프트 구성
prompt_text = prompt_template.format(document=document)

# Langfuse trace 생성
trace = langfuse.trace(name="contract-trace")

# GPT 호출
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_text}]
    )

    # 응답 내용
    output_text = response.choices[0].message.content

    # Langfuse generation 기록 (Prompt는 dict로 전달)
    trace.generation(
        name="date-extraction",
        prompt={
            "name": "extract-date",
            "input": prompt_text
        },
        output=output_text
    )

    # 결과 출력
    print(output_text)

except Exception as e:
    print("[ERROR] GPT 호출 중 문제가 발생했습니다:")
    print(e)