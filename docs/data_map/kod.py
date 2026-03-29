import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import numpy as np

# Настройка стиля
plt.style.use('default')
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# Цветовая схема
COLORS = {
    'domain_bg': '#E8F4F8',
    'source_bg': '#FFFFFF',
    'title': '#2C3E50',
    'source_title': '#2980B9',
    'field': '#7F8C8D',
    'arrow': '#E74C3C',
    'key_field': '#27AE60'
}

# Позиции доменов (x, y, width, height)
DOMAINS = {
    'Клиенты': {'x': 1, 'y': 7, 'width': 3, 'height': 4},
    'Продажи': {'x': 5, 'y': 7, 'width': 3, 'height': 4},
    'Обучение': {'x': 9, 'y': 7, 'width': 3, 'height': 4},
    'Финансы': {'x': 1, 'y': 1.5, 'width': 3, 'height': 4},
    'Продукты': {'x': 12.5, 'y': 1.5, 'width': 3, 'height': 4}
}

# Источники внутри доменов
SOURCES = {
    'Клиенты': {
        'name': 'CRM (Companies)',
        'fields': ['company_id*', 'company_name', 'industry', 'region', 'employee_count', 'status'],
        'file': '01_crm_companies.csv'
    },
    'Продажи': {
        'name': 'CRM (Transactions)',
        'fields': ['transaction_id', 'company_id*', 'product_id', 'total_amount', 'transaction_stage', 'manager'],
        'file': '02_crm_transactions.csv'
    },
    'Обучение': {
        'name': 'LMS (Events)',
        'fields': ['event_id', 'company_id*', 'user_id', 'event_type', 'event_date'],
        'file': '03_lms_events.csv'
    },
    'Финансы': {
        'name': '1С (Payments)',
        'fields': ['payment_id', 'company_id*', 'amount', 'payment_date', 'payment_type'],
        'file': '05_finance_payments.csv'
    },
    'Продукты': {
        'name': 'Google Sheets (Products)',
        'fields': ['product_id*', 'product_name', 'price', 'category'],
        'file': '09_products.csv'
    }
}

# Связи между источниками (от, до, ключ связи)
LINKS = [
    {'from': 'Клиенты', 'to': 'Продажи', 'key': 'company_id'},
    {'from': 'Клиенты', 'to': 'Обучение', 'key': 'company_id'},
    {'from': 'Клиенты', 'to': 'Финансы', 'key': 'company_id'},
    {'from': 'Продажи', 'to': 'Продукты', 'key': 'product_id'}
]

# Отрисовка доменов
for domain_name, pos in DOMAINS.items():
    # Прямоугольник домена
    rect = plt.Rectangle(
        (pos['x'], pos['y']), pos['width'], pos['height'],
        facecolor=COLORS['domain_bg'], edgecolor='#BDC3C7', linewidth=2, alpha=0.7
    )
    ax.add_patch(rect)
    
    # Заголовок домена
    ax.text(
        pos['x'] + pos['width']/2, pos['y'] + pos['height'] - 0.3,
        domain_name, ha='center', va='top', fontsize=14, fontweight='bold', color=COLORS['title']
    )
    
    # Источник данных
    source = SOURCES[domain_name]
    source_rect = plt.Rectangle(
        (pos['x'] + 0.2, pos['y'] + 0.5), pos['width'] - 0.4, pos['height'] - 1.2,
        facecolor=COLORS['source_bg'], edgecolor=COLORS['source_title'], linewidth=1.5, linestyle='--'
    )
    ax.add_patch(source_rect)
    
    # Название источника
    ax.text(
        pos['x'] + pos['width']/2, pos['y'] + pos['height'] - 0.8,
        source['name'], ha='center', va='top', fontsize=11, fontweight='bold', color=COLORS['source_title']
    )
    
    # Имя файла
    ax.text(
        pos['x'] + pos['width']/2, pos['y'] + pos['height'] - 1.1,
        source['file'], ha='center', va='top', fontsize=8, style='italic', color='#95A5A6'
    )
    
    # Поля
    y_offset = pos['y'] + pos['height'] - 1.6
    for field in source['fields']:
        if field.endswith('*'):
            color = COLORS['key_field']
            field_display = field.replace('*', ' (PK/FK)')
        else:
            color = COLORS['field']
            field_display = field
        ax.text(
            pos['x'] + 0.4, y_offset,
            f'• {field_display}', ha='left', va='top', fontsize=8, color=color
        )
        y_offset -= 0.3

# Отрисовка связей
arrow_style = '->, head_width=0.1, head_length=0.15'
for link in LINKS:
    from_domain = DOMAINS[link['from']]
    to_domain = DOMAINS[link['to']]
    
    # Координаты для стрелки
    start_x = from_domain['x'] + from_domain['width']
    start_y = from_domain['y'] + from_domain['height']/2
    end_x = to_domain['x']
    end_y = to_domain['y'] + to_domain['height']/2
    
    # Стрелка
    ax.annotate(
        '', xy=(end_x, end_y), xytext=(start_x, start_y),
        arrowprops=dict(arrowstyle=arrow_style, color=COLORS['arrow'], lw=2, alpha=0.8)
    )
    
    # Подпись ключа связи
    mid_x = (start_x + end_x) / 2
    mid_y = start_y
    ax.text(
        mid_x, mid_y + 0.15, link['key'], ha='center', va='bottom',
        fontsize=9, color=COLORS['arrow'], fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.7)
    )

# Дополнительная стрелка от Продажи к Продуктам (длинная связь)
link_products = {'from': 'Продажи', 'to': 'Продукты', 'key': 'product_id'}
from_domain = DOMAINS[link_products['from']]
to_domain = DOMAINS[link_products['to']]
start_x = from_domain['x'] + from_domain['width']
start_y = from_domain['y'] + from_domain['height']/2 - 1
end_x = to_domain['x']
end_y = to_domain['y'] + to_domain['height']/2
ax.annotate(
    '', xy=(end_x, end_y), xytext=(start_x, start_y),
    arrowprops=dict(arrowstyle=arrow_style, color=COLORS['arrow'], lw=2, alpha=0.8)
)
mid_x = (start_x + end_x) / 2 - 1
mid_y = (start_y + end_y) / 2
ax.text(
    mid_x, mid_y + 0.15, 'product_id', ha='center', va='bottom',
    fontsize=9, color=COLORS['arrow'], fontweight='bold',
    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.7)
)

# Заголовок карты
ax.text(
    8, 11.5, 'Карта данных Группы А: Оценка потенциала подписки "Pro"',
    ha='center', va='center', fontsize=18, fontweight='bold', color=COLORS['title']
)
ax.text(
    8, 11.0, 'EdTech-холдинг "Образование Будущего" (B2B-сегмент)',
    ha='center', va='center', fontsize=12, color='#7F8C8D', style='italic'
)

# Легенда
legend_y = 0.5
ax.text(1, legend_y + 1.2, 'Легенда:', fontsize=10, fontweight='bold', color=COLORS['title'])
ax.text(1.5, legend_y + 0.8, '→', fontsize=12, color=COLORS['arrow'])
ax.text(1.8, legend_y + 0.8, 'Поток данных (с ключом связи)', fontsize=9, color=COLORS['field'])
ax.text(1.5, legend_y + 0.4, '*', fontsize=10, color=COLORS['key_field'])
ax.text(1.8, legend_y + 0.4, 'Ключевое поле (PK/FK)', fontsize=9, color=COLORS['field'])

# Примечание
ax.text(
    8, 0.5, 'Примечание: В анализ не включены данные поддержки (Zendesk) и каталог курсов (LMS Courses)',
    ha='center', va='center', fontsize=8, color='#95A5A6', style='italic'
)

plt.tight_layout()

# Сохранение карты в файл
# plt.savefig('docs/data_map/data_map_group_A.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()

# Вывод информации о сохранении
print("=" * 60)
print("Карта данных для Группы А успешно создана!")
print("Файл для сохранения: docs/data_map/data_map_group_A.png")
print("=" * 60)
print("\nОсновные домены данных:")
for domain in DOMAINS.keys():
    print(f"  • {domain}")
print("\nКлючевые связи:")
for link in LINKS:
    print(f"  • {link['from']} → {link['to']} : {link['key']}")
print("\nНовые источники для Группы А (Практическая работа №2):")
print("  • 05_finance_payments.csv (1С - Финансы)")
print("  • 09_products.csv (Google Sheets - Продукты)")