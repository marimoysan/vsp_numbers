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

data_servicios_vsp["año"] = data_servicios_vsp["fecha_evento"].dt.year


# # --- SIDEBAR ---

# Filtro por año
año_seleccionado = st.sidebar.multiselect(
    "Selecciona el año",
    options=sorted(data_servicios_vsp["año"].dropna().unique()),
    default=[2025],
    key="año_multiselect"
)

# # Filtro por cliente
# cliente_seleccionado = st.sidebar.multiselect(
#     "Selecciona el cliente",
#     options=sorted(data_servicios_vsp['cliente_vsp'].unique()),
#     key="cliente_multiselect"
# )


# Aplicar los filtros
df_servicios = data_servicios_vsp[
    (data_servicios_vsp['año'].isin(año_seleccionado))
].copy()



# --- MAIN PAGE ---

st.title("Overview de Clientes")

# --- GRAFICAS ---

# --- MÉTRICAS PRINCIPALES ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Clientes VSP", value=df_servicios["cliente_vsp"].nunique())

with col2:
    if "cliente_final" in df_servicios.columns:
        st.metric("Clientes Finales", value=df_servicios["cliente_final"].nunique())
    else:
        st.metric("Clientes Finales", value="N/A")

with col3:
    st.metric("Total Eventos", value=len(df_servicios))

with col4:
    eventos_por_cliente = len(df_servicios) / df_servicios["cliente_vsp"].nunique() if df_servicios["cliente_vsp"].nunique() > 0 else 0
    st.metric("Eventos por Cliente VSP", value=f"{eventos_por_cliente:.2f}")


# Primer fila
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Eventos por Cliente VSP")
    client_counts = df_servicios["cliente_vsp"].value_counts()
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(x=client_counts.index, y=client_counts.values, color=vsp_palette[1], ax=ax1)
    ax1.set_title("Eventos / Actividades por Cliente VSP", fontsize=14)
    ax1.set_xlabel("Cliente", fontsize=12)
    ax1.set_ylabel("Eventos", fontsize=12)
    ax1.tick_params(axis='x', rotation=90)
    st.pyplot(fig1)

with col2:
    st.markdown("### Eventos por Cliente Final")
    client_counts = df_servicios["cliente_final"].value_counts()
    fig2, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(x=client_counts.index, y=client_counts.values, color=vsp_palette[1], ax=ax1)
    ax1.set_title("Eventos / Actividades por Cliente final", fontsize=14)
    ax1.set_xlabel("Cliente", fontsize=12)
    ax1.set_ylabel("Eventos", fontsize=12)
    ax1.tick_params(axis='x', rotation=90)
    st.pyplot(fig2)

st.divider()
# # Segunda fila as
# Fila completa para el gráfico vertical por cliente
st.markdown("### Cobros, Pagos y Margen por Cliente VSP")
df_servicios["margen"] = df_servicios["cobros"] + df_servicios["pagos"]


# --- Agrupar y preparar datos ---
cliente_summary = df_servicios.groupby('cliente_vsp')[['cobros', 'pagos', 'margen']].sum()

# Ordenar por margen descendente (de mayor a menor)
cliente_summary = cliente_summary.sort_values(by='margen', ascending=False)

# --- Checkboxes para seleccionar qué mostrar ---
show_cobros = st.checkbox("Cobros", value=True)
show_pagos = st.checkbox("Pagos", value=True)
show_margen = st.checkbox("Margen", value=True)


# --- Determinar columnas seleccionadas ---
categorias = []
colores = []
if show_margen:
    categorias.append('margen')
    colores.append(vsp_palette[2])
if show_cobros:
    categorias.append('cobros')
    colores.append(vsp_palette[0])
if show_pagos:
    categorias.append('pagos')
    colores.append(vsp_palette[1])


# --- Mostrar gráfico si hay algo seleccionado ---
if categorias:
    fig, ax = plt.subplots(figsize=(14, 6))  # Ancho grande para fila completa

    cliente_summary[categorias].plot(
        kind='bar',
        stacked=True,
        ax=ax,
        color=colores,
        width=0.6
    )

    ax.set_xlabel('Cliente VSP', fontsize=13)
    ax.set_ylabel('Euros', fontsize=13)
    ax.set_title('Cobros, Pagos y Margen por Cliente VSP', fontsize=16, pad=15)
    ax.tick_params(axis='x', rotation=45, labelsize=11)
    ax.tick_params(axis='y', labelsize=11)

    # Añadir anotaciones solo para margen (si está seleccionado)
    if show_margen:
        for p in ax.patches:
            if p.get_facecolor() == (0, 0, 0, 1):  # Negro = margen
                height = p.get_height()
                if height != 0:
                    x = p.get_x() + p.get_width() / 2
                    y = p.get_y() + height
                    ax.text(x, y + 100, f'{height:,.0f} €', ha='center', va='bottom', fontsize=9)

    ax.legend(title='Categorías', loc='upper right', fontsize=10)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("Selecciona al menos una categoría para mostrar el gráfico.")


# col3, col4 = st.columns(2)

# with col3:
#     st.markdown("### Cobros, Pagos y Margen por Tipo de Actividad")
#     actividad_summary = df_servicios.groupby('tipo_actividad')[['cobros', 'pagos', 'margen']].sum().sort_values(by='margen')
#     fig3, ax3 = plt.subplots(figsize=(8, 6))
#     actividad_summary.plot(kind='barh', stacked=True, ax=ax3, color=['green', 'red', 'black'])
#     ax3.set_xlabel("Euros")
#     ax3.set_ylabel("Tipo de Actividad")
#     ax3.set_title("Por Tipo de Actividad")
#     st.pyplot(fig3)

# with col4:
#     st.markdown("### Margen Real vs Estimado")
#     if "margen_est_eur" in df_servicios.columns:
#         margen_comparacion = df_servicios.groupby('tipo_actividad')[['margen', 'margen_est_eur']].sum().sort_values(by='margen')
#         fig4, ax4 = plt.subplots(figsize=(8, 6))
#         y_pos = np.arange(len(margen_comparacion)) * 2
#         bar_width = 0.8
#         ax4.barh(y_pos - bar_width/2, margen_comparacion['margen'], bar_width, label='Margen Real', color='#1f77b4')
#         ax4.barh(y_pos + bar_width/2, margen_comparacion['margen_est_eur'], bar_width, label='Margen Estimado', color='#ff7f0e')
#         ax4.set_yticks(y_pos)
#         ax4.set_yticklabels(margen_comparacion.index)
#         ax4.set_xlabel("Euros")
#         ax4.set_title("Margen Real vs Estimado")
#         ax4.legend()
#         st.pyplot(fig4)
#     else:
#         st.info("No hay datos de margen estimado disponibles.")


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
