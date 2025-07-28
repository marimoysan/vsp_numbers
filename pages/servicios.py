import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_loader import load_service_data
from vsp_palette import vsp_palette
import time
import random

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(
    page_title="Servicios",
    page_icon="📊",
    layout="wide"
)
sns.set_palette(vsp_palette)

plt.rcParams['axes.prop_cycle'] = plt.cycler(color=vsp_palette)
orden_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
               "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# --- SINCRONIZACIÓN CON GOOGLE SHEETS ---
success_placeholder = st.empty()
with st.spinner("Cargando muchos meses de curro..."):
    data_servicios_vsp = load_service_data(sheet_name="Planning_Tracker_VSP", worksheet_name="Eventos")
success_placeholder.success("Aquí estan todos los eventos!")
time.sleep(3)
success_placeholder.empty()


# # --- SIDEBAR ---
st.sidebar.header("Opciones de visualización")
año_seleccionado = st.sidebar.multiselect(
"Selecciona el cliente",
options=sorted(data_servicios_vsp['cliente_vsp'].unique()),
default="AMEX"
)

# filtrar datos por año
if año_seleccionado:
    df_servicios = data_servicios_vsp[data_servicios_vsp['cliente_vsp'].isin(año_seleccionado)].copy()
else:
    df_servicios = data_servicios_vsp.copy()



# --- MAIN PAGE ---

st.title("Overview de Eventos")

st.dataframe(df_servicios)

# Always start fresh: convert and filter first
# data_servicios_vsp['fecha'] = pd.to_datetime(data_servicios_vsp['fecha'], format='%d/%m/%Y')
# data_filtrada = data_servicios_vsp[data_servicios_vsp['fecha'] >= pd.Timestamp('2023-09-01')]

# balance_mensual = (
#     data_filtrada
#     .groupby(pd.Grouper(key='fecha', freq='M'))['cantidad']
#     .sum()
#     .reset_index()
# )

# Step 1: Cumulative liquid account
# saldo_inicial = 6701.61 + 2183.76  # banco sept 23 + diferencia por entradas manuales
# saldo_total = balance_mensual['cantidad'].cumsum() + saldo_inicial
# saldo_actual = saldo_total.iloc[-1]
# fecha_actual = balance_mensual['fecha'].iloc[-1]

# Step 2–3: Create matplotlib chart
# fig, ax = plt.subplots(figsize=(14, 6))
# bar_width = 25
# colors = [vsp_palette[2] if val >= 0 else vsp_palette[1] for val in balance_mensual['cantidad']]
# ax.bar(balance_mensual["fecha"], balance_mensual["cantidad"], width=bar_width, color=colors, align='center', label='Balance mensual')
# ax.plot(balance_mensual["fecha"], saldo_total, color=vsp_palette[3], linewidth=1.5, marker='o', label='Saldo acumulado')

# # Annotation
# ax.text(
#     fecha_actual + pd.Timedelta(days=10),
#     saldo_actual,
#     f'Saldo actual: €{saldo_actual:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
#     fontsize=12,
#     color=vsp_palette[3],
#     va='center',
#     fontweight='bold'
# )

# for x, y in zip(balance_mensual["fecha"], saldo_total):
#     ax.text(
#         x, y,
#         f'€{y:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
#         fontsize=9,
#         ha='center',
#         va='bottom',
#         color=vsp_palette[3],
#         fontweight='regular'
#     )

# # Custom axes
# ax.get_yaxis().set_major_formatter(
#     plt.FuncFormatter(lambda x, _: f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))
# )

# ticks = balance_mensual["fecha"]
# shifted_labels = (ticks - pd.DateOffset(months=0)).dt.strftime('%b\n%Y')
# ax.set_xticks(ticks)
# ax.set_xticklabels(shifted_labels)

# ax.set_xlim(pd.Timestamp('2023-09-01'), balance_mensual['fecha'].max())

# for year in balance_mensual['fecha'].dt.year.unique():
#     ax.axvline(pd.Timestamp(f'{year}-01-01'), color='gray', linestyle='--', linewidth=0.5)

# ax.set_title('Balance Mensual y Saldo Acumulado desde Octubre 2023', fontsize=16)
# ax.set_xlabel('Mes', fontsize=14)
# ax.set_ylabel('€', fontsize=14)
# ax.grid(True, axis='y', linestyle='--', alpha=0.6)
# ax.legend()
# fig.tight_layout()

# # Show in Streamlit
# st.pyplot(fig)



# # --- SECCIÓN 1: BARRAS MENSUALES ---
# st.subheader("Balance mensual por categoría")

# # Separar positivos y negativos
# df_positivos = df_filtrado[df_filtrado['cantidad'] > 0]
# df_negativos = df_filtrado[df_filtrado['cantidad'] < 0]

# # Agrupar
# positivos_mes = df_positivos.groupby(['mes', 'grupo_principal_transferencia'])['cantidad'].sum().unstack(fill_value=0).reindex(orden_meses)
# negativos_mes = df_negativos.groupby(['mes', 'grupo_principal_transferencia'])['cantidad'].sum().unstack(fill_value=0).reindex(orden_meses).abs()

# # Mostrar gráficos
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("#### Entradas (ingresos)")
#     fig1, ax1 = plt.subplots(figsize=(10, 5))
#     positivos_mes.plot(kind="bar", stacked=True, ax=ax1)
#     ax1.set_title("Ingresos por mes")
#     ax1.set_ylabel("€")
#     ax1.set_xlabel("Mes")
#     ax1.tick_params(axis='x', rotation=45)
#     st.pyplot(fig1)

# with col2:
#     st.markdown("#### Salidas (gastos)")
#     fig2, ax2 = plt.subplots(figsize=(10, 5))
#     negativos_mes.plot(kind="bar", stacked=True, ax=ax2)
#     ax2.set_title("Gastos por mes")
#     ax2.set_ylabel("€")
#     ax2.set_xlabel("Mes")
#     ax2.tick_params(axis='x', rotation=45)
#     st.pyplot(fig2)

# # --- SECCIÓN 2: QUESITOS Y BENEFICIO ---
# st.subheader("Distribución anual y beneficio")

# # Agrupar por categoría
# gastos_totales = df_filtrado[df_filtrado['cantidad'] < 0].groupby('grupo_principal_transferencia')['cantidad'].sum().abs()
# ingresos_totales = df_filtrado[df_filtrado['cantidad'] > 0].groupby('grupo_principal_transferencia')['cantidad'].sum()
# beneficio_neto = ingresos_totales.sum() - gastos_totales.sum()

# # Quesitos
# col3, col4 = st.columns(2)

# with col3:
#     st.markdown("##### Ingresos por categoría")
#     fig3, ax3 = plt.subplots()
#     ax3.pie(
#         ingresos_totales,
#         labels=ingresos_totales.index,
#         autopct=lambda p: f'{p:.1f}%\n({p/100*sum(ingresos_totales):,.0f} €)'.replace(',', 'X').replace('.', ',').replace('X', '.'),
#         startangle=90,
#         colors=sns.color_palette("Greens", len(ingresos_totales))
#     )
#     ax3.axis("equal")
#     st.pyplot(fig3)

# with col4:
#     st.markdown("##### Gastos por categoría")
#     fig4, ax4 = plt.subplots()
#     ax4.pie(
#         gastos_totales,
#         labels=gastos_totales.index,
#         autopct=lambda p: f'{p:.1f}%\n({p/100*sum(gastos_totales):,.0f} €)'.replace(',', 'X').replace('.', ',').replace('X', '.'),
#         startangle=90,
#         colors=sns.color_palette("Reds", len(gastos_totales))
#     )
#     ax4.axis("equal")
#     st.pyplot(fig4)

# # Beneficio neto centrado
# st.markdown("### 💰 Beneficio Neto Anual")
# st.markdown(f"""
# <div style="text-align:center; padding: 1rem; border-radius: 10px;
#      background-color:{'#8E9DC8' if beneficio_neto >= 0 else '#C56F54'};
#      font-size:2rem; font-weight:bold; border: 1px solid #aaa;">
#     {beneficio_neto:,.2f} €
# </div>
# """, unsafe_allow_html=True)
