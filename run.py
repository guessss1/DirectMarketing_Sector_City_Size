from dotenv import load_dotenv
import os
import openai
import pandas as pd
from tokens_quantity import log_tokens
from tiktoken import encoding_for_model

# Загрузка переменных окружения из .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Проверка API-ключа
if not openai.api_key:
    raise ValueError("API ключ OpenAI не найден. Проверьте файл .env.")

# Настройка модели и энкодинга
MODEL_NAME = "gpt-3.5-turbo"
ENCODING = encoding_for_model(MODEL_NAME)

# Функция для подсчёта токенов
def count_tokens(text, encoding):
    return len(encoding.encode(text))

# Функция для вызова ChatCompletion и подсчёта токенов
def chat_completion(prompt, model=MODEL_NAME, temperature=0):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        completion_text = response['choices'][0]['message']['content']

        # Подсчёт токенов
        input_tokens = count_tokens(prompt, ENCODING)
        output_tokens = count_tokens(completion_text, ENCODING)
        total_tokens = input_tokens + output_tokens

        return completion_text.strip(), input_tokens, output_tokens, total_tokens
    except Exception as e:
        print(f"Ошибка запроса к OpenAI: {e}")
        return None, 0, 0, 0

# Исходные данные
sectors = ['Продуктовые магазины', 'Рестораны', 'Фастфуды']
cities = ['Брюссель', 'Париж', 'Берлин']
sizes = ['маленькие', 'средние', 'большие']

# Шаблон промпта
prompt_template = """
Роль: Вы эксперт в маркетинговых текстах для директ-маркетинга.
Контекст: Напишите короткое сообщение для продвижения нового сервиса электронной коммерции для магазинов. 
Целевые магазины:
- Сектор: {sector}
- Город: {city}
- Размер: {size}
"""

# Сбор данных
data = []
for sector in sectors:
    for city in cities:
        for size in sizes:
            prompt = prompt_template.format(sector=sector, city=city, size=size)
            completion, input_tokens, output_tokens, total_tokens = chat_completion(
                prompt, model=MODEL_NAME, temperature=0.7
            )
            if completion:
                data.append({
                    'prompt': f"{sector}, {city}, {size}",
                    'completion': completion,
                    'input_tokens': input_tokens,
                    'output_tokens': output_tokens,
                    'total_tokens': total_tokens
                })
            print(f"Обработано: {sector}, {city}, {size}")
            print(f"Входящие токены: {input_tokens}, Исходящие токены: {output_tokens}, Всего: {total_tokens}")

# Сохранение данных в CSV
df = pd.DataFrame(data)
output_csv_path = "out_openai_completion.csv"
df.to_csv(output_csv_path, index=False, encoding="utf-8")
print(f"Результаты сохранены в {output_csv_path}")

# Логирование итогов токенов
log_results = log_tokens(data)

# Сохранение итогов в файл
with open("tokens_summary.txt", "w", encoding="utf-8") as summary_file:
    summary_file.write("Общий итог потребления токенов:\n")
    summary_file.write(f"Всего входящих токенов: {log_results['total_input_tokens']}\n")
    summary_file.write(f"Всего исходящих токенов: {log_results['total_output_tokens']}\n")
    summary_file.write(f"Общая сумма токенов: {log_results['total_sum_tokens']}\n")

print("Итоговое потребление токенов сохранено в tokens_summary.txt")


