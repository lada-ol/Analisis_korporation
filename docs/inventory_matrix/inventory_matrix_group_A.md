# Инвентаризационная матрица источников данных
## Группа А. Оценка потенциала подписки "Pro"

### Общая информация

| Домен | Атрибут (Поле) | Тип данных | Файл-источник | Система-источник | Владелец (из org_structure) | Частота обновления | Правила ETL (какие преобразования нужны) | Целевая витрина | Качество (пропуски, дубликаты) |
|-------|----------------|------------|----------------|------------------|----------------------------|--------------------|-------------------------------------------|-----------------|-------------------------------|
| **Клиенты** | company_id | int | 01_crm_companies.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Приведение к единому формату int. Проверка на уникальность. | company_readiness_for_pro | 100% заполнено, дубликатов нет |
| **Клиенты** | company_name | string | 01_crm_companies.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Очистка от лишних пробелов (strip). Замена кавычек на стандартные. | company_readiness_for_pro | 100% заполнено |
| **Клиенты** | inn | int | 01_crm_companies.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Оставить как есть (может быть NaN). Для аналитики не используется. | company_readiness_for_pro | ~20% пропусков (8 из 40 компаний без ИНН) |
| **Клиенты** | industry | string | 01_crm_companies.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Привести к единому регистру (Capitalize). Проверить на допустимые значения (Retail, IT, Services, Logistics, Construction, Finance, Industry, Media, Energy). | company_readiness_for_pro | 100% заполнено |
| **Клиенты** | region | string | 01_crm_companies.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Привести к единому формату (ЦФО, СЗФО, ЮФО, ПФО). | company_readiness_for_pro | 100% заполнено |
| **Клиенты** | employee_count | int | 01_crm_companies.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Проверить на аномалии (от 1 до 1000). Выбросы оставить для анализа. | company_readiness_for_pro | 100% заполнено |
| **Клиенты** | created_date | date | 01_crm_companies.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Преобразовать из string в datetime (формат YYYY-MM-DD). | company_readiness_for_pro | 100% заполнено |
| **Клиенты** | status | string | 01_crm_companies.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Привести к единому формату (active/lead/inactive). | company_readiness_for_pro | 100% заполнено |
| **Продажи** | transaction_id | string | 02_crm_transactions.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Проверить на уникальность. Оставить как есть. | company_readiness_for_pro (промежуточный расчет) | 100% заполнено, дубликатов нет |
| **Продажи** | company_id | int | 02_crm_transactions.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Привести к int. Проверить наличие в справочнике companies. | company_readiness_for_pro (промежуточный расчет) | 100% заполнено |
| **Продажи** | transaction_date | datetime | 02_crm_transactions.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Преобразовать из string в datetime (формат YYYY-MM-DD). | company_readiness_for_pro (промежуточный расчет) | 100% заполнено |
| **Продажи** | product_id | string | 02_crm_transactions.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Оставить как есть. Используется для фильтрации аналогов. | company_readiness_for_pro (промежуточный расчет) | 100% заполнено |
| **Продажи** | quantity | int | 02_crm_transactions.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Проверить на положительность (>0). | company_readiness_for_pro (промежуточный расчет) | 100% заполнено |
| **Продажи** | unit_price | int | 02_crm_transactions.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Проверить на аномалии. Может использоваться для верификации total_amount. | company_readiness_for_pro (промежуточный расчет) | 100% заполнено |
| **Продажи** | total_amount | int | 02_crm_transactions.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Проверить на положительность (>0). Рассчитать как quantity × unit_price (для верификации). | company_readiness_for_pro (avg_check, total_revenue) | 100% заполнено |
| **Продажи** | transaction_stage | string | 02_crm_transactions.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Привести к единому формату (closed_won, negotiation, lead). Для avg_check использовать только closed_won. | company_readiness_for_pro (avg_check, total_revenue) | 100% заполнено |
| **Продажи** | manager | string | 02_crm_transactions.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Оставить как есть. Для аналитики не используется. | company_readiness_for_pro | 100% заполнено |
| **Продажи** | probability | int | 02_crm_transactions.csv | CRM | Департамент продаж (Козлов Д.В.) | Еженедельно | Для closed_won = 100, иначе 0-99. Для аналитики не используется. | company_readiness_for_pro | 100% заполнено |
| **Обучение** | event_id | string | 03_lms_events.csv | LMS | Платформа (Новиков А.А.) | Ежедневно | Проверить на уникальность. Оставить как есть. | company_readiness_for_pro (промежуточный расчет) | 100% заполнено |
| **Обучение** | company_id | int | 03_lms_events.csv | LMS | Платформа (Новиков А.А.) | Ежедневно | Привести к int. Проверить наличие в справочнике companies. | company_readiness_for_pro (промежуточный расчет) | 100% заполнено |
| **Обучение** | user_id | int | 03_lms_events.csv | LMS | Платформа (Новиков А.А.) | Ежедневно | Оставить как есть. Для агрегации на уровне компании не используется напрямую. | company_readiness_for_pro (промежуточный расчет) | 100% заполнено |
| **Обучение** | course_id | string | 03_lms_events.csv | LMS | Платформа (Новиков А.А.) | Ежедневно | Оставить как есть. Для аналитики не используется (нет связи с products). | company_readiness_for_pro (промежуточный расчет) | 100% заполнено |
| **Обучение** | event_type | string | 03_lms_events.csv | LMS | Платформа (Новиков А.А.) | Ежедневно | Привести к единому формату (login, lesson_start, lesson_complete). Для is_active_lms использовать только login. | company_readiness_for_pro (is_active_lms, login_count_90d) | 100% заполнено |
| **Обучение** | event_date | datetime | 03_lms_events.csv | LMS | Платформа (Новиков А.А.) | Ежедневно | Преобразовать из string в datetime. Извлечь дату из строки с временем (YYYY-MM-DD). | company_readiness_for_pro (is_active_lms, login_count_90d) | 100% заполнено |
| **Обучение** | completion_pct | int | 03_lms_events.csv | LMS | Платформа (Новиков А.А.) | Ежедневно | Для event_type='login' = NULL (заполнить 0). Для аналитики не используется в Группе А. | company_readiness_for_pro | ~60% пропусков (только для lesson_start) |
| **Финансы** | payment_id | string | 05_finance_payments.csv | 1С | Департамент финансов (Григорьев Г.Г.) | Ежедневно | Проверить на уникальность. Оставить как есть. | company_readiness_for_pro (промежуточный расчет) | 100% заполнено |
| **Финансы** | company_id | int | 05_finance_payments.csv | 1С | Департамент финансов (Григорьев Г.Г.) | Ежедневно | Привести к int. Проверить наличие в справочнике companies. | company_readiness_for_pro (промежуточный расчет) | 100% заполнено |
| **Финансы** | amount | int | 05_finance_payments.csv | 1С | Департамент финансов (Григорьев Г.Г.) | Ежедневно | Для payment_type='refund' - отрицательные суммы. Оставить как есть, но при расчете payment_stability использовать ABS(amount) или фильтровать. | company_readiness_for_pro (payment_stability, total_payments_count) | 100% заполнено |
| **Финансы** | payment_date | datetime | 05_finance_payments.csv | 1С | Департамент финансов (Григорьев Г.Г.) | Ежедневно | **ВАЖНО:** Преобразовать из формата ДД.ММ.ГГГГ в datetime (format='%d.%m.%Y'). | company_readiness_for_pro (промежуточный расчет) | 100% заполнено |
| **Финансы** | payment_type | string | 05_finance_payments.csv | 1С | Департамент финансов (Григорьев Г.Г.) | Ежедневно | Привести к единому формату (payment, refund). Для payment_stability использовать только payment. | company_readiness_for_pro (payment_stability, total_payments_count) | 100% заполнено |

### Итого по качеству данных

| Файл | Всего записей | Пропуски в ключевых полях | Дубликаты | Особые проблемы |
|------|---------------|---------------------------|-----------|-----------------|
| 01_crm_companies.csv | 40 | inn: 8 пропусков (20%) | Нет | Одинаковые ИНН у разных компаний |
| 02_crm_transactions.csv | 42 | Нет | Нет | Разные unit_price для одного product_id |
| 03_lms_events.csv | 50 | completion_pct: ~30 пропусков | Нет | completion_pct похож на минуты, а не проценты |
| 05_finance_payments.csv | (данных нет в файлах) | - | - | Формат дат ДД.ММ.ГГГГ (требует преобразования) |

### Правила ETL (подробное описание)

#### 1. Преобразование дат
```python
# Для 01_crm_companies.csv и 02_crm_transactions.csv
df['date_column'] = pd.to_datetime(df['date_column'])  # формат YYYY-MM-DD

# Для 05_finance_payments.csv (критически важно!)
df['payment_date'] = pd.to_datetime(df['payment_date'], format='%d.%m.%Y')

# Для 03_lms_events.csv
df['event_date'] = pd.to_datetime(df['event_date'].str.split().str[0])  # извлекаем дату