import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Создаем фигуру
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# Цвета
COLOR_BOX = '#E8F4F8'
COLOR_BORDER = '#2C3E50'
COLOR_ARROW = '#E74C3C'
COLOR_SOURCE = '#2980B9'
COLOR_FIELD = '#7F8C8D'
COLOR_KEY = '#27AE60'

def draw_rect(x, y, w, h, title):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                          facecolor=COLOR_BOX, edgecolor=COLOR_BORDER, linewidth=2)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 0.35, title, ha='center', va='top',
            fontsize=13, fontweight='bold', color=COLOR_BORDER)

# Рисуем 5 доменов
draw_rect(0.5, 5.8, 4.2, 4.8, 'ДОМЕН 1: КЛИЕНТЫ')
draw_rect(5.2, 6.5, 3.2, 4, 'ДОМЕН 2: ПРОДАЖИ')
draw_rect(8.8, 5.8, 4.2, 4.8, 'ДОМЕН 3: ОБУЧЕНИЕ')
draw_rect(0.5, 0.8, 4, 3.5, 'ДОМЕН 4: ФИНАНСЫ')
draw_rect(11, 0.8, 3.5, 3.5, 'ДОМЕН 5: ПРОДУКТЫ')

# ========== ДОМЕН 1: КЛИЕНТЫ (3 источника) ==========
y_start = 10.2

# Источник 1: CRM
ax.text(0.9, y_start, 'CRM (Companies)', fontsize=9, fontweight='bold', color=COLOR_SOURCE)
ax.text(0.9, y_start - 0.25, '01_crm_companies.csv', fontsize=6, style='italic', color='gray')
ax.text(0.9, y_start - 0.5, '• company_id*', fontsize=7, color=COLOR_KEY)
ax.text(0.9, y_start - 0.75, '• company_name', fontsize=7, color=COLOR_FIELD)
ax.text(0.9, y_start - 1.0, '• industry, region', fontsize=7, color=COLOR_FIELD)
ax.text(0.9, y_start - 1.25, '• employee_count, status', fontsize=7, color=COLOR_FIELD)

# Источник 2: 1С
ax.text(0.9, y_start - 1.7, '1С (Payments)', fontsize=9, fontweight='bold', color=COLOR_SOURCE)
ax.text(0.9, y_start - 1.95, '05_finance_payments.csv', fontsize=6, style='italic', color='gray')
ax.text(0.9, y_start - 2.2, '• payment_id*', fontsize=7, color=COLOR_KEY)
ax.text(0.9, y_start - 2.45, '• company_id*', fontsize=7, color=COLOR_KEY)
ax.text(0.9, y_start - 2.7, '• amount', fontsize=7, color=COLOR_FIELD)

# Источник 3: LMS Events
ax.text(0.9, y_start - 3.2, 'LMS (Events)', fontsize=9, fontweight='bold', color=COLOR_SOURCE)
ax.text(0.9, y_start - 3.45, '03_lms_events.csv', fontsize=6, style='italic', color='gray')
ax.text(0.9, y_start - 3.7, '• event_id*', fontsize=7, color=COLOR_KEY)
ax.text(0.9, y_start - 3.95, '• company_id*', fontsize=7, color=COLOR_KEY)
ax.text(0.9, y_start - 4.2, '• user_id, event_type', fontsize=7, color=COLOR_FIELD)

# ========== ДОМЕН 2: ПРОДАЖИ (1 источник) ==========
ax.text(5.5, 10.0, 'CRM (Transactions)', fontsize=9, fontweight='bold', color=COLOR_SOURCE)
ax.text(5.5, 9.75, '02_crm_transactions.csv', fontsize=6, style='italic', color='gray')
ax.text(5.5, 9.5, '• transaction_id*', fontsize=7, color=COLOR_KEY)
ax.text(5.5, 9.25, '• company_id*', fontsize=7, color=COLOR_KEY)
ax.text(5.5, 9.0, '• product_id', fontsize=7, color=COLOR_FIELD)
ax.text(5.5, 8.75, '• total_amount', fontsize=7, color=COLOR_FIELD)
ax.text(5.5, 8.5, '• transaction_stage', fontsize=7, color=COLOR_FIELD)

# ========== ДОМЕН 3: ОБУЧЕНИЕ (2 источника) ==========
y_start3 = 10.2

# Источник 1: LMS Events
ax.text(9.2, y_start3, 'LMS (Events)', fontsize=9, fontweight='bold', color=COLOR_SOURCE)
ax.text(9.2, y_start3 - 0.25, '03_lms_events.csv', fontsize=6, style='italic', color='gray')
ax.text(9.2, y_start3 - 0.5, '• event_id*', fontsize=7, color=COLOR_KEY)
ax.text(9.2, y_start3 - 0.75, '• company_id*', fontsize=7, color=COLOR_KEY)
ax.text(9.2, y_start3 - 1.0, '• user_id', fontsize=7, color=COLOR_FIELD)
ax.text(9.2, y_start3 - 1.25, '• course_id*', fontsize=7, color=COLOR_KEY)

# Источник 2: LMS Courses
ax.text(9.2, y_start3 - 1.75, 'LMS (Courses)', fontsize=9, fontweight='bold', color=COLOR_SOURCE)
ax.text(9.2, y_start3 - 2.0, '04_lms_courses.csv', fontsize=6, style='italic', color='gray')
ax.text(9.2, y_start3 - 2.25, '• course_id*', fontsize=7, color=COLOR_KEY)
ax.text(9.2, y_start3 - 2.5, '• course_name', fontsize=7, color=COLOR_FIELD)
ax.text(9.2, y_start3 - 2.75, '• category, difficulty', fontsize=7, color=COLOR_FIELD)

# ========== ДОМЕН 4: ФИНАНСЫ (1 источник) ==========
ax.text(0.9, 3.8, '1С (Payments)', fontsize=9, fontweight='bold', color=COLOR_SOURCE)
ax.text(0.9, 3.55, '05_finance_payments.csv', fontsize=6, style='italic', color='gray')
ax.text(0.9, 3.3, '• payment_id*', fontsize=7, color=COLOR_KEY)
ax.text(0.9, 3.05, '• company_id*', fontsize=7, color=COLOR_KEY)
ax.text(0.9, 2.8, '• amount', fontsize=7, color=COLOR_FIELD)
ax.text(0.9, 2.55, '• payment_date', fontsize=7, color=COLOR_FIELD)
ax.text(0.9, 2.3, '• payment_type', fontsize=7, color=COLOR_FIELD)

# ========== ДОМЕН 5: ПРОДУКТЫ (1 источник) ==========
ax.text(11.3, 3.8, 'Google Sheets', fontsize=9, fontweight='bold', color=COLOR_SOURCE)
ax.text(11.3, 3.55, '09_products.csv', fontsize=6, style='italic', color='gray')
ax.text(11.3, 3.3, '• product_id*', fontsize=7, color=COLOR_KEY)
ax.text(11.3, 3.05, '• product_name', fontsize=7, color=COLOR_FIELD)
ax.text(11.3, 2.8, '• price', fontsize=7, color=COLOR_FIELD)
ax.text(11.3, 2.55, '• category', fontsize=7, color=COLOR_FIELD)

# ========== СТРЕЛКИ ==========
# Клиенты -> Продажи
ax.annotate('', xy=(5.2, 8.5), xytext=(4.7, 8.5), arrowprops=dict(arrowstyle='->', color=COLOR_ARROW, lw=2))
ax.text(4.95, 8.7, 'company_id', ha='center', fontsize=8, color=COLOR_ARROW)

# Клиенты -> Обучение
ax.annotate('', xy=(8.8, 8.5), xytext=(4.7, 8.5), arrowprops=dict(arrowstyle='->', color=COLOR_ARROW, lw=2))
ax.text(6.75, 8.7, 'company_id', ha='center', fontsize=8, color=COLOR_ARROW)

# Клиенты -> Финансы
ax.annotate('', xy=(0.5, 4.3), xytext=(2.5, 5.8), arrowprops=dict(arrowstyle='->', color=COLOR_ARROW, lw=2, connectionstyle="arc3,rad=-0.3"))
ax.text(2, 5.0, 'company_id', ha='center', fontsize=8, color=COLOR_ARROW)

# Продажи -> Продукты
ax.annotate('', xy=(11, 2.5), xytext=(8.4, 6.5), arrowprops=dict(arrowstyle='->', color=COLOR_ARROW, lw=2, connectionstyle="arc3,rad=0.2"))
ax.text(9.7, 4.5, 'product_id', ha='center', fontsize=8, color=COLOR_ARROW)

# Обучение -> Продукты
ax.annotate('', xy=(11, 2.5), xytext=(11.5, 5.8), arrowprops=dict(arrowstyle='->', color=COLOR_ARROW, lw=2, connectionstyle="arc3,rad=0.2"))
ax.text(11.8, 4.2, 'course_id', ha='center', fontsize=8, color=COLOR_ARROW)

# ========== ЗАГОЛОВОК ==========
ax.text(8, 11.7, 'Карта данных Группы А: Оценка потенциала подписки "Pro"',
        ha='center', va='center', fontsize=16, fontweight='bold', color=COLOR_BORDER)
ax.text(8, 11.3, 'EdTech-холдинг "Образование Будущего" (B2B-сегмент)',
        ha='center', va='center', fontsize=10, color='gray')

# ========== ЛЕГЕНДА ==========
ax.text(0.5, 0.3, 'Легенда:', fontsize=8, fontweight='bold')
ax.text(1.2, 0.3, '→', fontsize=10, color=COLOR_ARROW)
ax.text(1.5, 0.3, 'Связь между доменами', fontsize=7)
ax.text(4, 0.3, '*', fontsize=9, color=COLOR_KEY)
ax.text(4.3, 0.3, 'Ключевое поле (PK/FK)', fontsize=7)
ax.text(7, 0.3, '📦 Домен = группа источников данных', fontsize=7, style='italic', color='gray')

plt.tight_layout()
plt.savefig('data_map_group_A.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()

print("✅ Карта данных сохранена как data_map_group_A.png")
print("\n📊 СТРУКТУРА ДОМЕНОВ:")
print("=" * 50)
print("ДОМЕН 1: КЛИЕНТЫ (3 источника)")
print("  ├── CRM (Companies) — 01_crm_companies.csv")
print("  ├── 1С (Payments) — 05_finance_payments.csv")
print("  └── LMS (Events) — 03_lms_events.csv")
print()
print("ДОМЕН 2: ПРОДАЖИ (1 источник)")
print("  └── CRM (Transactions) — 02_crm_transactions.csv")
print()
print("ДОМЕН 3: ОБУЧЕНИЕ (2 источника)")
print("  ├── LMS (Events) — 03_lms_events.csv")
print("  └── LMS (Courses) — 04_lms_courses.csv")
print()
print("ДОМЕН 4: ФИНАНСЫ (1 источник)")
print("  └── 1С (Payments) — 05_finance_payments.csv")
print()
print("ДОМЕН 5: ПРОДУКТЫ (1 источник)")
print("  └── Google Sheets — 09_products.csv")
print()
print("🔗 СВЯЗИ МЕЖДУ ДОМЕНАМИ:")
print("  • Клиенты → Продажи: company_id")
print("  • Клиенты → Обучение: company_id")
print("  • Клиенты → Финансы: company_id")
print("  • Продажи → Продукты: product_id")
print("  • Обучение → Продукты: course_id")