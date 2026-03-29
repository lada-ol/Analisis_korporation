import pandas as pd

# Данные для инвентаризационной матрицы
data = [
    # Домен, Атрибут, Тип данных, Файл-источник, Система-источник, Владелец, Частота обновления, Правила ETL, Целевая витрина, Качество
    ["Клиенты", "company_id", "int", "01_crm_companies.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Приведение к единому формату int. Проверка на уникальность.", "company_readiness_for_pro", "100% заполнено, дубликатов нет"],
    ["Клиенты", "company_name", "string", "01_crm_companies.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Очистка от лишних пробелов (strip). Замена кавычек.", "company_readiness_for_pro", "100% заполнено"],
    ["Клиенты", "inn", "int", "01_crm_companies.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Оставить как есть (может быть NaN). Для аналитики не используется.", "company_readiness_for_pro", "~20% пропусков (8 из 40 компаний без ИНН)"],
    ["Клиенты", "industry", "string", "01_crm_companies.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Привести к единому регистру (Capitalize). Проверить на допустимые значения.", "company_readiness_for_pro", "100% заполнено"],
    ["Клиенты", "region", "string", "01_crm_companies.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Привести к единому формату (ЦФО, СЗФО, ЮФО, ПФО).", "company_readiness_for_pro", "100% заполнено"],
    ["Клиенты", "employee_count", "int", "01_crm_companies.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Проверить на аномалии (от 1 до 1000).", "company_readiness_for_pro", "100% заполнено"],
    ["Клиенты", "created_date", "date", "01_crm_companies.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Преобразовать из string в datetime (формат YYYY-MM-DD).", "company_readiness_for_pro", "100% заполнено"],
    ["Клиенты", "status", "string", "01_crm_companies.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Привести к единому формату (active/lead/inactive).", "company_readiness_for_pro", "100% заполнено"],
    ["Продажи", "transaction_id", "string", "02_crm_transactions.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Проверить на уникальность.", "company_readiness_for_pro (промежуточный)", "100% заполнено, дубликатов нет"],
    ["Продажи", "company_id", "int", "02_crm_transactions.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Привести к int. Проверить наличие в справочнике companies.", "company_readiness_for_pro (промежуточный)", "100% заполнено"],
    ["Продажи", "transaction_date", "datetime", "02_crm_transactions.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Преобразовать из string в datetime (формат YYYY-MM-DD).", "company_readiness_for_pro (промежуточный)", "100% заполнено"],
    ["Продажи", "product_id", "string", "02_crm_transactions.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Оставить как есть. Используется для фильтрации аналогов.", "company_readiness_for_pro (промежуточный)", "100% заполнено"],
    ["Продажи", "quantity", "int", "02_crm_transactions.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Проверить на положительность (>0).", "company_readiness_for_pro (промежуточный)", "100% заполнено"],
    ["Продажи", "unit_price", "int", "02_crm_transactions.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Проверить на аномалии.", "company_readiness_for_pro (промежуточный)", "100% заполнено"],
    ["Продажи", "total_amount", "int", "02_crm_transactions.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Проверить на положительность (>0).", "company_readiness_for_pro (avg_check, total_revenue)", "100% заполнено"],
    ["Продажи", "transaction_stage", "string", "02_crm_transactions.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Привести к единому формату (closed_won, negotiation, lead).", "company_readiness_for_pro (avg_check, total_revenue)", "100% заполнено"],
    ["Продажи", "manager", "string", "02_crm_transactions.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Оставить как есть.", "company_readiness_for_pro", "100% заполнено"],
    ["Продажи", "probability", "int", "02_crm_transactions.csv", "CRM", "Департамент продаж (Козлов Д.В.)", "Еженедельно", "Для closed_won = 100, иначе 0-99.", "company_readiness_for_pro", "100% заполнено"],
    ["Обучение", "event_id", "string", "03_lms_events.csv", "LMS", "Платформа (Новиков А.А.)", "Ежедневно", "Проверить на уникальность.", "company_readiness_for_pro (промежуточный)", "100% заполнено"],
    ["Обучение", "company_id", "int", "03_lms_events.csv", "LMS", "Платформа (Новиков А.А.)", "Ежедневно", "Привести к int. Проверить наличие в справочнике companies.", "company_readiness_for_pro (промежуточный)", "100% заполнено"],
    ["Обучение", "user_id", "int", "03_lms_events.csv", "LMS", "Платформа (Новиков А.А.)", "Ежедневно", "Оставить как есть.", "company_readiness_for_pro (промежуточный)", "100% заполнено"],
    ["Обучение", "course_id", "string", "03_lms_events.csv", "LMS", "Платформа (Новиков А.А.)", "Ежедневно", "Оставить как есть.", "company_readiness_for_pro (промежуточный)", "100% заполнено"],
    ["Обучение", "event_type", "string", "03_lms_events.csv", "LMS", "Платформа (Новиков А.А.)", "Ежедневно", "Привести к единому формату (login, lesson_start, lesson_complete).", "company_readiness_for_pro (is_active_lms)", "100% заполнено"],
    ["Обучение", "event_date", "datetime", "03_lms_events.csv", "LMS", "Платформа (Новиков А.А.)", "Ежедневно", "Преобразовать из string в datetime. Извлечь дату.", "company_readiness_for_pro (is_active_lms)", "100% заполнено"],
    ["Обучение", "completion_pct", "int", "03_lms_events.csv", "LMS", "Платформа (Новиков А.А.)", "Ежедневно", "Для event_type='login' = NULL (заполнить 0).", "company_readiness_for_pro", "~60% пропусков"],
    ["Финансы", "payment_id", "string", "05_finance_payments.csv", "1С", "Департамент финансов (Григорьев Г.Г.)", "Ежедневно", "Проверить на уникальность.", "company_readiness_for_pro (промежуточный)", "100% заполнено"],
    ["Финансы", "company_id", "int", "05_finance_payments.csv", "1С", "Департамент финансов (Григорьев Г.Г.)", "Ежедневно", "Привести к int. Проверить наличие в справочнике companies.", "company_readiness_for_pro (промежуточный)", "100% заполнено"],
    ["Финансы", "amount", "int", "05_finance_payments.csv", "1С", "Департамент финансов (Григорьев Г.Г.)", "Ежедневно", "Для payment_type='refund' - отрицательные суммы. Фильтровать.", "company_readiness_for_pro (payment_stability)", "100% заполнено"],
    ["Финансы", "payment_date", "datetime", "05_finance_payments.csv", "1С", "Департамент финансов (Григорьев Г.Г.)", "Ежедневно", "ВАЖНО: Преобразовать из формата ДД.ММ.ГГГГ в datetime (%d.%m.%Y).", "company_readiness_for_pro (промежуточный)", "100% заполнено"],
    ["Финансы", "payment_type", "string", "05_finance_payments.csv", "1С", "Департамент финансов (Григорьев Г.Г.)", "Ежедневно", "Привести к единому формату (payment, refund).", "company_readiness_for_pro (payment_stability)", "100% заполнено"],
]

# Создание DataFrame
columns = ["Домен", "Атрибут (Поле)", "Тип данных", "Файл-источник", "Система-источник", "Владелец (из org_structure)", "Частота обновления", "Правила ETL", "Целевая витрина", "Качество (пропуски, дубликаты)"]
df = pd.DataFrame(data, columns=columns)

# Сохранение в Excel
file_path = "inventory_matrix_group_A.xlsx"
df.to_excel(file_path, index=False, sheet_name="Inventory_Matrix")

print(f"Файл успешно создан: {file_path}")
print(f"Всего записей: {len(df)}")
print(f"Колонки: {', '.join(columns)}")