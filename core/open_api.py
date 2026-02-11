from openai import OpenAI

from config.setting import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_API_BASE
)

completion = client.chat.completions.create(
    model=settings.OPENAI_API_NAME,  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"}
    ]
)

print(completion.choices[0].message.content)