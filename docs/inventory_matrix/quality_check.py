"""
Код для оценки качества данных источников
Запустить перед построением витрины
"""

import pandas as pd
import numpy as np

# 1. Загрузка данных
companies = pd.read_csv('01_crm_companies.csv')
transactions = pd.read_csv('02_crm_transactions.csv')
lms_events = pd.read_csv('03_lms_events.csv')
finance = pd.read_csv('05_finance_payments.csv')

# 2. Функция для анализа качества
def quality_report(df, name):
    print(f"\n{'='*50}")
    print(f"Отчет по качеству: {name}")
    print(f"{'='*50}")
    print(f"Количество записей: {len(df)}")
    print(f"Количество колонок: {len(df.columns)}")
    print(f"\nПропуски (%):")
    print((df.isnull().sum() / len(df) * 100).round(2))
    print(f"\nДубликаты по ключевому полю:")
    # Определяем ключевое поле
    key_map = {
        'companies': 'company_id',
        'transactions': 'transaction_id',
        'lms_events': 'event_id',
        'finance': 'payment_id'
    }
    key = key_map.get(name, df.columns[0])
    duplicates = df[key].duplicated().sum()
    print(f"  {key}: {duplicates} дубликатов ({duplicates/len(df)*100:.2f}%)")
    
    print(f"\nОсновные статистики для числовых полей:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(df[numeric_cols].describe())

# 3. Запуск анализа
quality_report(companies, 'companies')
quality_report(transactions, 'transactions')
quality_report(lms_events, 'lms_events')
quality_report(finance, 'finance')

# 4. Дополнительная проверка: связность company_id
print(f"\n{'='*50}")
print("Проверка связности company_id")
print(f"{'='*50}")

companies_ids = set(companies['company_id'])
transactions_ids = set(transactions['company_id'])
lms_ids = set(lms_events['company_id'])
finance_ids = set(finance['company_id'])

print(f"Всего компаний в CRM: {len(companies_ids)}")
print(f"Компаний с транзакциями: {len(transactions_ids)}")
print(f"Компаний с событиями в LMS: {len(lms_ids)}")
print(f"Компаний с платежами: {len(finance_ids)}")

print(f"\nПересечения:")
print(f"  Транзакции ∩ Компании: {len(transactions_ids & companies_ids)}")
print(f"  LMS ∩ Компании: {len(lms_ids & companies_ids)}")
print(f"  Финансы ∩ Компании: {len(finance_ids & companies_ids)}")

# Компании без активности
inactive_companies = companies_ids - lms_ids
print(f"\nКомпании без активности в LMS: {len(inactive_companies)}")
print(f"  Примеры: {list(inactive_companies)[:5]}")

# Компании без платежей
no_payments = companies_ids - finance_ids
print(f"Компании без платежей в 1С: {len(no_payments)}")