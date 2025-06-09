import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(
    page_title="VSP en números",
    page_icon="📊",
    layout="wide"
)

# Paleta de colores
vsp_palette = ["#8E9DC8", "#C56F54", "#72846F", "#6F4E89", "#E0B664"]
sns.set_palette(vsp_palette)
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=vsp_palette)


# --- CARGA DE DATOS ---

st.title("Upload your VSP data")

uploaded_file = st.file_uploader("Choose your CSV file", type="csv")

if uploaded_file is not None:
    data_vsp = pd.read_csv(uploaded_file)
    st.success("File loaded successfully!")



# --- CARGA DE DATOS ---
# data_vsp = pd.read_csv("data/data_vsp_final.csv")

orden_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
               "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# --- SIDEBAR ---
st.sidebar.image("vsp_logo_white.png", width=150)
st.sidebar.divider()

st.sidebar.header("Opciones de visualización")
año_seleccionado = st.sidebar.multiselect(
    "Selecciona el año",
    options=sorted(data_vsp['año'].unique()),
    default=2024
)


# --- FILTRAR DATOS ---
if año_seleccionado:
    df_filtrado = data_vsp[data_vsp['año'].isin(año_seleccionado)].copy()
else:
    df_filtrado = data_vsp.copy()


# --- MAIN PAGE ---
#
#
# --- TÍTULO ---
st.title("📈 Visualización financiera VSP")

# --- SECCIÓN 1: BARRAS MENSUALES ---
st.subheader("Balance mensual por categoría")

# Separar positivos y negativos
df_positivos = df_filtrado[df_filtrado['cantidad'] > 0]
df_negativos = df_filtrado[df_filtrado['cantidad'] < 0]

# Agrupar
positivos_mes = df_positivos.groupby(['mes', 'grupo_principal_transferencia'])['cantidad'].sum().unstack(fill_value=0).reindex(orden_meses)
negativos_mes = df_negativos.groupby(['mes', 'grupo_principal_transferencia'])['cantidad'].sum().unstack(fill_value=0).reindex(orden_meses).abs()

# Mostrar gráficos
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Entradas (ingresos)")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    positivos_mes.plot(kind="bar", stacked=True, ax=ax1)
    ax1.set_title("Ingresos por mes")
    ax1.set_ylabel("€")
    ax1.set_xlabel("Mes")
    ax1.tick_params(axis='x', rotation=45)
    st.pyplot(fig1)

with col2:
    st.markdown("#### Salidas (gastos)")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    negativos_mes.plot(kind="bar", stacked=True, ax=ax2)
    ax2.set_title("Gastos por mes")
    ax2.set_ylabel("€")
    ax2.set_xlabel("Mes")
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)

# --- SECCIÓN 2: QUESITOS Y BENEFICIO ---
st.subheader("Distribución anual y beneficio")

# Agrupar por categoría
gastos_totales = df_filtrado[df_filtrado['cantidad'] < 0].groupby('grupo_principal_transferencia')['cantidad'].sum().abs()
ingresos_totales = df_filtrado[df_filtrado['cantidad'] > 0].groupby('grupo_principal_transferencia')['cantidad'].sum()
beneficio_neto = ingresos_totales.sum() - gastos_totales.sum()

# Quesitos
col3, col4 = st.columns(2)

with col3:
    st.markdown("##### Ingresos por categoría")
    fig3, ax3 = plt.subplots()
    ax3.pie(
        ingresos_totales,
        labels=ingresos_totales.index,
        autopct=lambda p: f'{p:.1f}%\n({p/100*sum(ingresos_totales):,.0f} €)'.replace(',', 'X').replace('.', ',').replace('X', '.'),
        startangle=90,
        colors=sns.color_palette("Greens", len(ingresos_totales))
    )
    ax3.axis("equal")
    st.pyplot(fig3)

with col4:
    st.markdown("##### Gastos por categoría")
    fig4, ax4 = plt.subplots()
    ax4.pie(
        gastos_totales,
        labels=gastos_totales.index,
        autopct=lambda p: f'{p:.1f}%\n({p/100*sum(gastos_totales):,.0f} €)'.replace(',', 'X').replace('.', ',').replace('X', '.'),
        startangle=90,
        colors=sns.color_palette("Reds", len(gastos_totales))
    )
    ax4.axis("equal")
    st.pyplot(fig4)

# Beneficio neto centrado
st.markdown("### 💰 Beneficio Neto Anual")
st.markdown(f"""
<div style="text-align:center; padding: 1rem; border-radius: 10px;
     background-color:{'#8E9DC8' if beneficio_neto >= 0 else '#C56F54'};
     font-size:2rem; font-weight:bold; border: 1px solid #aaa;">
    {beneficio_neto:,.2f} €
</div>
""", unsafe_allow_html=True)
