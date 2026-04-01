import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Настройка
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# Цвета
COLORS = {
    'source': '#E3F2FD',      # светло-голубой
    'dwh': '#FFF3E0',         # светло-оранжевый
    'mart': '#E8F5E9',        # светло-зеленый
    'process': '#F3E5F5',     # светло-фиолетовый
    'border': '#2C3E50',
    'arrow': '#E74C3C',
    'text': '#2C3E50'
}

def draw_box(x, y, width, height, text, color, fontsize=11, bold=False):
    rect = FancyBboxPatch((x, y), width, height,
                          boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor=COLORS['border'],
                          linewidth=2, alpha=0.9)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    ax.text(x + width/2, y + height/2, text, ha='center', va='center',
            fontsize=fontsize, fontweight=weight, color=COLORS['text'])

# ========== 1. ИСТОЧНИКИ ДАННЫХ ==========
# CRM
draw_box(0.5, 7, 2.5, 1.2, 'CRM\n(система продаж)', COLORS['source'], fontsize=10)
# LMS
draw_box(0.5, 5.5, 2.5, 1.2, 'LMS\n(платформа обучения)', COLORS['source'], fontsize=10)
# 1С
draw_box(0.5, 4, 2.5, 1.2, '1С\n(финансовая система)', COLORS['source'], fontsize=10)
# Google Sheets
draw_box(0.5, 2.5, 2.5, 1.2, 'Google Sheets\n(справочник продуктов)', COLORS['source'], fontsize=10)

# ========== 2. ХРАНИЛИЩЕ ДАННЫХ (DWH) ==========
draw_box(5, 4.5, 2.8, 3, 'Хранилище данных\n(DWH)', COLORS['dwh'], fontsize=12, bold=True)

# ========== 3. ВИТРИНА ДАННЫХ ==========
draw_box(9, 4.5, 2.8, 3, 'Витрина данных\ncompany_readiness_for_pro', COLORS['mart'], fontsize=11, bold=True)

# ========== 4. ПОТРЕБИТЕЛИ (бизнес-процессы) ==========
draw_box(13, 7, 2.2, 1.2, 'Процесс: Продажи\n(оценка потенциала)', COLORS['process'], fontsize=10)
draw_box(13, 5.5, 2.2, 1.2, 'Процесс: Продукт\n(анализ готовности)', COLORS['process'], fontsize=10)
draw_box(13, 4, 2.2, 1.2, 'Процесс: Финансы\n(прогноз выручки)', COLORS['process'], fontsize=10)

# ========== СТРЕЛКИ (основные потоки) ==========
arrow_style = '->, head_width=0.15, head_length=0.2'

# Источники → Хранилище
ax.annotate('', xy=(5, 7.6), xytext=(3, 7.6),
            arrowprops=dict(arrowstyle=arrow_style, color=COLORS['arrow'], lw=2))
ax.text(4, 7.8, 'company_id, сделки', ha='center', fontsize=8, color=COLORS['arrow'])

ax.annotate('', xy=(5, 6.1), xytext=(3, 6.1),
            arrowprops=dict(arrowstyle=arrow_style, color=COLORS['arrow'], lw=2))
ax.text(4, 6.3, 'company_id, события', ha='center', fontsize=8, color=COLORS['arrow'])

ax.annotate('', xy=(5, 4.6), xytext=(3, 4.6),
            arrowprops=dict(arrowstyle=arrow_style, color=COLORS['arrow'], lw=2))
ax.text(4, 4.8, 'company_id, платежи', ha='center', fontsize=8, color=COLORS['arrow'])

ax.annotate('', xy=(5, 3.1), xytext=(3, 3.1),
            arrowprops=dict(arrowstyle=arrow_style, color=COLORS['arrow'], lw=2))
ax.text(4, 3.3, 'product_id, цены', ha='center', fontsize=8, color=COLORS['arrow'])

# Хранилище → Витрина
ax.annotate('', xy=(9, 6), xytext=(7.8, 6),
            arrowprops=dict(arrowstyle=arrow_style, color=COLORS['arrow'], lw=2))
ax.text(8.4, 6.2, 'агрегация', ha='center', fontsize=9, color=COLORS['arrow'])

# Витрина → Потребители
ax.annotate('', xy=(13, 7.6), xytext=(11.8, 7.6),
            arrowprops=dict(arrowstyle=arrow_style, color=COLORS['arrow'], lw=2))
ax.text(12.4, 7.8, 'сегментация', ha='center', fontsize=8, color=COLORS['arrow'])

ax.annotate('', xy=(13, 6.1), xytext=(11.8, 6.1),
            arrowprops=dict(arrowstyle=arrow_style, color=COLORS['arrow'], lw=2))
ax.text(12.4, 6.3, 'активность', ha='center', fontsize=8, color=COLORS['arrow'])

ax.annotate('', xy=(13, 4.6), xytext=(11.8, 4.6),
            arrowprops=dict(arrowstyle=arrow_style, color=COLORS['arrow'], lw=2))
ax.text(12.4, 4.8, 'прогноз', ha='center', fontsize=8, color=COLORS['arrow'])

# ========== ОБРАТНЫЕ СВЯЗИ (пунктирные) ==========
ax.annotate('', xy=(2.8, 7.9), xytext=(2.8, 8.2),
            arrowprops=dict(arrowstyle=arrow_style, color='#9E9E9E', lw=1.5, linestyle='dashed'))
ax.text(3.2, 8.1, 'управление', ha='left', fontsize=8, color='#9E9E9E')

ax.annotate('', xy=(2.8, 6.4), xytext=(2.8, 6.7),
            arrowprops=dict(arrowstyle=arrow_style, color='#9E9E9E', lw=1.5, linestyle='dashed'))
ax.text(3.2, 6.6, 'настройка курсов', ha='left', fontsize=8, color='#9E9E9E')

ax.annotate('', xy=(2.8, 4.9), xytext=(2.8, 5.2),
            arrowprops=dict(arrowstyle=arrow_style, color='#9E9E9E', lw=1.5, linestyle='dashed'))
ax.text(3.2, 5.1, 'бюджетирование', ha='left', fontsize=8, color='#9E9E9E')

# ========== ЗАГОЛОВОК ==========
ax.text(8, 11.5, 'Карта данных Группы А: Оценка потенциала подписки "Pro"',
        ha='center', va='center', fontsize=16, fontweight='bold', color=COLORS['text'])
ax.text(8, 11.0, 'EdTech-холдинг "Образование Будущего" (B2B-сегмент)',
        ha='center', va='center', fontsize=11, color='#7F8C8D')

# ========== ЛЕГЕНДА ==========
ax.text(0.5, 0.5, 'Легенда:', fontsize=10, fontweight='bold')
ax.text(1.2, 0.5, '→', fontsize=11, color=COLORS['arrow'])
ax.text(1.5, 0.5, 'Основной поток данных', fontsize=8, color=COLORS['text'])
ax.text(4, 0.5, '⇢', fontsize=11, color='#9E9E9E')
ax.text(4.3, 0.5, 'Обратная связь (управление)', fontsize=8, color='#9E9E9E')

# Цветовые метки
ax.add_patch(plt.Rectangle((7, 0.4), 0.4, 0.3, facecolor=COLORS['source'], edgecolor=COLORS['border']))
ax.text(7.5, 0.55, 'Источники данных (OLTP)', fontsize=8, va='center')
ax.add_patch(plt.Rectangle((10, 0.4), 0.4, 0.3, facecolor=COLORS['dwh'], edgecolor=COLORS['border']))
ax.text(10.5, 0.55, 'Хранилище данных (DWH)', fontsize=8, va='center')
ax.add_patch(plt.Rectangle((12.8, 0.4), 0.4, 0.3, facecolor=COLORS['mart'], edgecolor=COLORS['border']))
ax.text(13.3, 0.55, 'Витрина данных', fontsize=8, va='center')

plt.tight_layout()
plt.savefig('data_map_group_A.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()

print("✅ Карта данных сохранена как data_map_group_A.png")
print("\n📊 НА КАРТЕ ОТОБРАЖЕНЫ:")
print("  • Источники: CRM, LMS, 1С, Google Sheets")
print("  • Хранилище данных (DWH)")
print("  • Витрина данных: company_readiness_for_pro")
print("  • Потребители: Процессы Продаж, Продукта, Финансов")
print("  • Основные потоки данных и обратные связи")