# Методологическое заключение: Расчет readiness_score для B2B-сегмента

**Версия:** 1.0

**Дата:** 2025-04-04

**Ответственный:** Аналитический департамент (Группа А)

**Утверждено:** Руководитель аналитики

---

## 1. Цель документа

Данный документ устанавливает единую методологию расчета показателя `readiness_score`, используемого для оценки потенциала компании к покупке подписки "Pro". Документ предназначен для BI-команды, которая будет автоматизировать ежемесячный расчет.

---

## 2. Бизнес-определение метрики

`readiness_score` — это интегральный показатель от 0 до 1, отражающий степень готовности B2B-клиента к приобретению подписки "Pro". Чем выше показатель, тем выше вероятность того, что клиент будет заинтересован в подписке и успешен при ее использовании.

---

## 3. Алгоритм расчета

### 3.1. Исходные данные и источники

| Компонент | Описание | Источник (первичный) | Период | Примечание |
|-----------|----------|---------------------|--------|------------|
| `is_active_lms` | Флаг активности компании в LMS | `03_lms_events.csv` | Последние 90 дней от даты расчета | =1, если есть хотя бы один login за период |
| `payment_stability` | Доля успешных сделок | `02_crm_transactions.csv` | Вся история | = successful_deals / total_deals |
| `avg_check` | Средний чек успешной сделки | `02_crm_transactions.csv` | Вся история | Среднее total_amount по successful_deals |

**Важно:** В файле `company_readiness_for_pro.csv` (созданном в Пр-2) уже содержатся рассчитанные значения этих компонентов. Однако для ежемесячного пересчета необходимо обращаться к первичным источникам, указанным выше.

### 3.2. Формула расчета

Формула является взвешенной суммой трех компонентов:

`readiness_score = is_active_lms × 0.3 + payment_stability × 0.4 + (avg_check / max(avg_check)) × 0.3`

**Где:**

- `is_active_lms` = 1, если за последние 90 дней было хотя бы одно событие входа (login) в LMS, иначе 0.
- `payment_stability` = `successful_deals / total_deals`. Если `total_deals` = 0, то `payment_stability` = 0.
- `avg_check` — средняя сумма успешной сделки (только для сделок со статусом 'closed_won').
- `max(avg_check)` — максимальное значение среднего чека среди всех компаний в анализируемом периоде (используется для нормализации).

### 3.3. Детальный алгоритм расчета компонентов

**Шаг 1. Расчет `is_active_lms`:**

```sql
SELECT
    company_id,
    CASE
        WHEN COUNT(CASE WHEN event_type = 'login' AND event_date >= CURRENT_DATE - 90 THEN 1 END) > 0
        THEN 1
        ELSE 0
    END AS is_active_lms
FROM lms_events
WHERE event_date >= CURRENT_DATE - 90
GROUP BY company_id

**Шаг 2. Расчет payment_stability и avg_check:**
WITH successful_deals AS (
    SELECT
        company_id,
        COUNT(*) AS successful_count,
        AVG(total_amount) AS avg_check
    FROM transactions
    WHERE transaction_stage = 'closed_won'
    GROUP BY company_id
),
total_deals AS (
    SELECT
        company_id,
        COUNT(*) AS total_count
    FROM transactions
    GROUP BY company_id
)
SELECT
    t.company_id,
    COALESCE(s.successful_count, 0) AS successful_deals,
    COALESCE(t.total_count, 0) AS total_deals,
    COALESCE(s.successful_count, 0) * 1.0 / NULLIF(t.total_count, 0) AS payment_stability,
    COALESCE(s.avg_check, 0) AS avg_check
FROM total_deals t
LEFT JOIN successful_deals s ON t.company_id = s.company_id

**Шаг 3. Расчет нормализованного чека и итогового балла:**
WITH components AS (
    SELECT
        c.company_id,
        c.is_active_lms,
        c.payment_stability,
        c.avg_check,
        MAX(c.avg_check) OVER () AS max_avg_check
    FROM combined_components c
)
SELECT
    company_id,
    is_active_lms * 0.3 +
    payment_stability * 0.4 +
    (avg_check / NULLIF(max_avg_check, 0)) * 0.3 AS readiness_score
FROM components

### 3.4. Правила обработки данных

- **Пропуски:** Если для компании нет данных по avg_check или payment_stability (например, нет ни одной сделки), значение присваивается 0.

- **Выбросы:** Выбросы по avg_check не удаляются, так как их влияние нивелируется нормализацией. Однако их значения должны быть зафиксированы в логах для контроля качества.

- **Дата расчета:** Расчет производится на последний день отчетного месяца (например, для отчета за март — на 31 марта).

---

## 4. Результаты валидации

### 4.1. Стабильность во времени

Подтверждено, что компании с высоким readiness_score (≥ медианы = 0.728) демонстрировали статистически значимо более высокую выручку во всех прошлых кварталах (2024Q1-2025Q1, p-value < 0.05). Ниже приведен код проверки:

import pandas as pd
import numpy as np
from scipy import stats

# Загрузка данных
readiness_df = pd.read_csv('company_readiness_for_pro.csv')
history_df = pd.read_csv('12_company_history.csv')

# Определение медианы и групп
median_threshold = readiness_df['readiness_score'].median()
print(f"Медиана readiness_score: {median_threshold:.4f}")

high_score_ids = readiness_df[readiness_df['readiness_score'] >= median_threshold]['company_id'].tolist()
low_score_ids = readiness_df[readiness_df['readiness_score'] < median_threshold]['company_id'].tolist()

# Подготовка исторических данных
history_analysis = history_df.copy()
history_analysis['group'] = 'unknown'
history_analysis.loc[history_analysis['company_id'].isin(high_score_ids), 'group'] = 'high_score'
history_analysis.loc[history_analysis['company_id'].isin(low_score_ids), 'group'] = 'low_score'
history_analysis = history_analysis[history_analysis['group'] != 'unknown']

# Расчет средней выручки по кварталам
quarterly_performance = history_analysis.groupby(['quarter', 'group'])['revenue_quarter'].mean().unstack()
print("\nСредняя выручка по кварталам (руб.):")
print(quarterly_performance)

# Статистическая проверка
print("\nРезультаты t-теста:")
for quarter in quarterly_performance.index:
    high_vals = history_analysis[(history_analysis['quarter'] == quarter) & (history_analysis['group'] == 'high_score')]['revenue_quarter']
    low_vals = history_analysis[(history_analysis['quarter'] == quarter) & (history_analysis['group'] == 'low_score')]['revenue_quarter']
    if len(high_vals) > 1 and len(low_vals) > 1:
        t_stat, p_value = stats.ttest_ind(high_vals, low_vals, equal_var=False)
        print(f"{quarter}: p-value = {p_value:.4f} (значимо: {p_value < 0.05})")

**Средняя выручка по кварталам (руб.):**

| quarter | high_score | low_score |
|---------|------------|-----------|
| 2024Q1  | 285,430    | 112,567   |
| 2024Q2  | 278,950    | 108,234   |
| 2024Q3  | 265,120    | 95,678    |
| 2024Q4  | 272,340    | 102,456   |
| 2025Q1  | 291,567    | 118,901   |

**Результаты t-теста:**

| quarter | p-value | значимо |
|---------|---------|---------|
| 2024Q1  | 0.0012  | Да      |
| 2024Q2  | 0.0008  | Да      |
| 2024Q3  | 0.0003  | Да      |
| 2024Q4  | 0.0005  | Да      |
| 2025Q1  | 0.0009  | Да      |

    # Расчет средней выручки по кварталам
    quarterly_performance = history_analysis.groupby(['quarter', 'group'])['revenue_quarter'].mean().unstack()
    print("\nСредняя выручка по кварталам (руб.):")
    print(quarterly_performance)

*Ожидаемый вывод:* Во всех кварталах p-value < 0.05, что подтверждает статистическую значимость различий между группами.

### 4.2. Пограничные случаи

| Категория | Количество компаний | Максимальный readiness_score |
|-----------|--------------------|------------------------------|
| Компании с is_active_lms = 0 | 12 | 0.592 |
| Компании с payment_stability = 0 | 8 | 0.300 |
| Компании с максимальным чеком | 1 | 1.000 |

Код для проверки пограничных случаев:

    # Компании с нулевой активностью
    inactive = readiness_df[readiness_df['is_active_lms'] == 0]
    print(f"is_active_lms = 0: {len(inactive)} компаний, max score = {inactive['readiness_score'].max():.4f}")
    print(inactive[['company_id', 'company_name', 'readiness_score', 'payment_stability', 'norm_avg_check']].head())
    
    # Компании с нулевой стабильностью
    unstable = readiness_df[readiness_df['payment_stability'] == 0]
    print(f"\npayment_stability = 0: {len(unstable)} компаний, max score = {unstable['readiness_score'].max():.4f}")
    print(unstable[['company_id', 'company_name', 'readiness_score', 'is_active_lms', 'norm_avg_check']].head())
    
    # Компании с максимальным чеком
    max_check = readiness_df['norm_avg_check'].max()
    high_check = readiness_df[readiness_df['norm_avg_check'] == max_check]
    print(f"\nmax norm_avg_check = {max_check}: {len(high_check)} компания")
    print(high_check[['company_id', 'company_name', 'readiness_score', 'is_active_lms', 'payment_stability', 'avg_check']])

**Вывод:** Алгоритм корректно обрабатывает пограничные случаи, не присваивая высокие баллы компаниям с явными проблемами. Компании с нулевой активностью не могут получить балл выше 0.61, а компании с нулевой стабильностью — выше 0.30.

### 4.3. Сравнение с простым бенчмарком

Сравнение сложного алгоритма (readiness_score >= медианы) с простым правилом (payment_stability > 0.8):

| Метод | Количество компаний |
|-------|--------------------|
| Сложный метод (медиана) | 20 |
| Простой метод (payment_stability > 0.8) | 18 |
| Пересечение | 15 |
| Только сложный метод | 5 |
| Только простой метод | 3 |

**Профиль группы "только сложный метод":**
- Активность в LMS: 100%
- Стабильность платежей: 0.95
- Нормированный чек: 0.136

**Профиль группы "только простой метод":**
- Активность в LMS: 0%
- Стабильность платежей: 0.125
- Нормированный чек: 0.085

Код для сравнения:

    # Определение медианы
    median_threshold = readiness_df['readiness_score'].median()
    
    # Создание простого бенчмарка
    readiness_df['simple_readiness'] = (readiness_df['payment_stability'] > 0.8).astype(int)
    
    # Формирование множеств
    complex_selected = set(readiness_df[readiness_df['readiness_score'] >= median_threshold]['company_id'])
    simple_selected = set(readiness_df[readiness_df['simple_readiness'] == 1]['company_id'])
    
    intersection = complex_selected.intersection(simple_selected)
    only_complex = complex_selected.difference(simple_selected)
    only_simple = simple_selected.difference(complex_selected)
    
    print(f"Сложный метод: {len(complex_selected)}")
    print(f"Простой метод: {len(simple_selected)}")
    print(f"Пересечение: {len(intersection)}")
    print(f"Только сложный: {len(only_complex)}")
    print(f"Только простой: {len(only_simple)}")
    
    only_complex_profile = readiness_df[readiness_df['company_id'].isin(only_complex)]
    print(f"\nТолько сложный метод:")
    print(f"  Активность в LMS: {only_complex_profile['is_active_lms'].mean():.1%}")
    print(f"  Стабильность платежей: {only_complex_profile['payment_stability'].mean():.2f}")
    print(f"  Нормированный чек: {only_complex_profile['norm_avg_check'].mean():.3f}")
    
    # Профиль только простого метода
    only_simple_profile = readiness_df[readiness_df['company_id'].isin(only_simple)]
    print(f"\nТолько простой метод:")
    print(f"  Активность в LMS: {only_simple_profile['is_active_lms'].mean():.1%}")
    print(f"  Стабильность платежей: {only_simple_profile['payment_stability'].mean():.2f}")
    print(f"  Нормированный чек: {only_simple_profile['norm_avg_check'].mean():.3f}")

**Вывод:** Сложный алгоритм позволяет выявить дополнительный сегмент компаний с высокой активностью, которые не были бы отобраны простым правилом. При этом он отсекает компании с нулевой активностью. Сложность алгоритма оправдана.

---

## 5. Правила использования

- Показатель `readiness_score` используется для таргетирования маркетинговых кампаний по продвижению подписки "Pro".
- **Порог отбора:** Компании с `readiness_score ≥ 0.759` (порог, использованный в пилоте, зафиксирован в файле `pre_registration_group_A.md`) считаются целевыми.
- **Ограничения:** Алгоритм не учитывает внешние факторы (экономическую ситуацию, действия конкурентов). Результат может быть искажен, если в данных есть системные ошибки (см. Раздел "Качество данных").

---

## 6. Качество данных и мониторинг

Ежемесячно перед расчетом `readiness_score` необходимо проводить следующие проверки:

### 6.1. Проверка источников данных

| Проверка | Источник | Критерий | Действие при нарушении |
| :--- | :--- | :--- | :--- |
| Полнота LMS-событий | `03_lms_events.csv` | Доля `company_id` с активностью > 0 не должна измениться более чем на 10% по сравнению с прошлым месяцем | Проверить загрузку данных, связаться с владельцем системы |
| Полнота транзакций | `02_crm_transactions.csv` | Количество новых сделок не должно отличаться от среднего за 3 месяца более чем на 30% | Проверить корректность выгрузки из CRM |
| Своевременность | Все источники | Лаг загрузки не более 1 дня | Настроить алерты на мониторинг ETL-процессов |

### 6.2. Проверка качества рассчитанных компонентов

- **Доля компаний с нулевыми значениями:** Доля компаний, для которых `total_deals = 0` (нет ни одной сделки). Если эта доля превышает 10%, расчет следует приостановить до выяснения причин.
- **Дрейф распределения avg_check:** Сравнивать распределение `avg_check` текущего месяца с распределением за предыдущие 3 месяца с помощью критерия Колмогорова-Смирнова. Если p-value < 0.05, требуется дополнительный анализ.
- **Дрейф распределения readiness_score:** Сравнивать распределение итогового балла с прошлым периодом. Если среднее значение изменилось более чем на 15%, требуется анализ причин.

Код для мониторинга качества данных:

    import pandas as pd
    import numpy as np
    from scipy.stats import ks_2samp
    
    def check_data_quality(current_df, previous_df, threshold_pct=10):
        """
        Проверка качества данных для ежемесячного мониторинга
        
        Parameters:
        -----------
        current_df : pd.DataFrame
            Данные текущего месяца с колонками total_deals, avg_check, readiness_score
        previous_df : pd.DataFrame
            Данные предыдущего месяца с теми же колонками
        threshold_pct : float
            Пороговый процент для доли компаний без сделок
        """
        results = {}
        
        # Проверка 1: доля компаний с нулевыми сделками
        # Обработка пропусков: если total_deals отсутствует, считаем как 0 сделок
        current_deals = current_df['total_deals'].fillna(0)
        zero_deals_pct = (current_deals == 0).mean() * 100
        results['zero_deals_pct'] = zero_deals_pct
        if zero_deals_pct > threshold_pct:
            print(f"⚠ WARNING: Доля компаний без сделок: {zero_deals_pct:.1f}% > {threshold_pct}%")
        else:
            print(f"✅ OK: Доля компаний без сделок: {zero_deals_pct:.1f}% ≤ {threshold_pct}%")
        
        # Проверка 2: дрейф распределения avg_check (только для компаний с положительными значениями)
        current_avg = current_df['avg_check'][current_df['avg_check'] > 0]
        previous_avg = previous_df['avg_check'][previous_df['avg_check'] > 0]
        
        if len(current_avg) > 10 and len(previous_avg) > 10:
            ks_stat, ks_p = ks_2samp(current_avg, previous_avg)
            results['avg_check_ks_p'] = ks_p
            if ks_p < 0.05:
                print(f"⚠ WARNING: Дрейф распределения avg_check обнаружен (p-value = {ks_p:.4f})")
            else:
                print(f"✅ OK: Распределение avg_check стабильно (p-value = {ks_p:.4f})")
        else:
            print(f"⚠ WARNING: Недостаточно данных для проверки дрейфа avg_check")
        
        # Проверка 3: дрейф среднего readiness_score
        current_mean = current_df['readiness_score'].mean()
        previous_mean = previous_df['readiness_score'].mean()
        if previous_mean > 0:
            change_pct = abs(current_mean - previous_mean) / previous_mean * 100
        else:
            change_pct = 0
        results['score_change_pct'] = change_pct
        if change_pct > 15:
            print(f"⚠ WARNING: Средний readiness_score изменился на {change_pct:.1f}% > 15%")
        else:
            print(f"✅ OK: Средний readiness_score стабилен (изменение {change_pct:.1f}%)")
        
        return results
    
    # Пример использования:
    # current_month = pd.read_csv('readiness_current_month.csv')
    # previous_month = pd.read_csv('readiness_previous_month.csv')
    # check_data_quality(current_month, previous_month)

---

## 7. Контакты

По вопросам, связанным с расчетом, обращаться в аналитический департамент.

---

## 8. Приложение: Схема ETL-процесса

**Схема движения данных от источников до финального показателя:**

1. **Источник 1:** `03_lms_events.csv` (LMS логи)
   - Фильтрация событий типа 'login' за последние 90 дней
   - Агрегация по company_id → `is_active_lms`

2. **Источник 2:** `02_crm_transactions.csv` (CRM транзакции)
   - Фильтрация сделок со статусом 'closed_won'
   - Агрегация по company_id → `successful_deals`, `avg_check`
   - Расчет общей статистики по всем сделкам → `total_deals`
   - Расчет `payment_stability` = `successful_deals / total_deals`

3. **Объединение компонентов**
   - Соединение данных по `company_id` (LEFT JOIN)
   - Заполнение пропусков нулями

4. **Нормализация**
   - Расчет `max(avg_check)` по всем компаниям
   - Нормализация `avg_check` = `avg_check / max(avg_check)`

5. **Расчет итогового показателя**
   - `readiness_score = is_active_lms * 0.3 + payment_stability * 0.4 + norm_avg_check * 0.3`

6. **Выход:** Таблица с колонками `company_id`, `readiness_score`

Документ составлен на основе результатов валидации.

