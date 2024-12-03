# tokens_quantity.py

def log_tokens(data):
    """
    Функция для логирования токенов по каждой записи и подсчёта общего количества токенов.

    :param data: Список словарей с информацией о токенах
    :return: Итоговые суммы входящих, исходящих токенов и их общей суммы
    """
    total_input_tokens = 0
    total_output_tokens = 0
    total_sum_tokens = 0

    print("\nДетализация потребления токенов:")
    print("=" * 50)

    for entry in data:
        prompt = entry.get('prompt', 'N/A')
        input_tokens = entry.get('input_tokens', 0)
        output_tokens = entry.get('output_tokens', 0)
        total_tokens = entry.get('total_tokens', 0)

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        total_sum_tokens += total_tokens

        print(f"Промпт: {prompt}")
        print(f"  Входящие токены: {input_tokens}")
        print(f"  Исходящие токены: {output_tokens}")
        print(f"  Всего токенов: {total_tokens}")
        print("-" * 50)

    print("\nОбщий итог:")
    print(f"  Всего входящих токенов: {total_input_tokens}")
    print(f"  Всего исходящих токенов: {total_output_tokens}")
    print(f"  Общая сумма токенов: {total_sum_tokens}")

    return {
        'total_input_tokens': total_input_tokens,
        'total_output_tokens': total_output_tokens,
        'total_sum_tokens': total_sum_tokens
    }

