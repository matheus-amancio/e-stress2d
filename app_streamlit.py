import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from src.plot_stress_2d.plotting import (
    ExtremeShearStressState,
    ExtremeShearStressStatePlotter,
    PrincipalStressState,
    PrincipalStressStatePlotter,
    StressState,
    StressStatePlotter,
)

st.set_page_config(
    page_title="e-Stress2D",
    page_icon="📊",
    layout="wide",
)

st.title("e-Stress2D")
st.markdown("""
Desenvolvido por:
- Matheus Amancio Miranda
- Eduardo Nobre Lages
""")

st.divider()

# Sidebar para entrada de dados
st.sidebar.header("Entrada de dados")

# Gerar valores iniciais aleatórios para a sessão
if "initial_values" not in st.session_state:
    st.session_state.initial_values = {
        "s_xx": round(np.random.uniform(-100, 100), 2),
        "s_yy": round(np.random.uniform(-100, 100), 2),
        "s_xy": round(np.random.uniform(-100, 100), 2),
    }

# Inputs na sidebar com labels em LaTeX
st.sidebar.markdown("$\\sigma_{xx}$")
s_xx = st.sidebar.number_input(
    "s_xx (label oculto)",
    value=st.session_state.initial_values["s_xx"],
    step=0.01,
    label_visibility="collapsed",
)

st.sidebar.markdown("$\\sigma_{yy}$")
s_yy = st.sidebar.number_input(
    "s_yy (label oculto)",
    value=st.session_state.initial_values["s_yy"],
    step=0.01,
    label_visibility="collapsed",
)

st.sidebar.markdown("$\\sigma_{xy}$")
s_xy = st.sidebar.number_input(
    "s_xy (label oculto)",
    value=st.session_state.initial_values["s_xy"],
    step=0.01,
    label_visibility="collapsed",
)

# Botão para gerar valores aleatórios
if st.sidebar.button("🎲 Gerar valores aleatórios"):
    st.session_state.initial_values = {
        "s_xx": round(np.random.uniform(-100, 100), 2),
        "s_yy": round(np.random.uniform(-100, 100), 2),
        "s_xy": round(np.random.uniform(-100, 100), 2),
    }
    st.rerun()

# Equacionamento
with st.expander("📐 Equacionamento"):
    st.markdown(r"""
    $\sigma_{\text{med}} = \dfrac{\sigma_{xx} + \sigma_{yy}}{2}$

    $R = \sqrt{(\dfrac{\sigma_{xx} - \sigma_{yy}}{2})^2 + \sigma_{xy}^2}$

    ### Tensões principais

    $\sigma_{1} = \sigma_{\text{med}} + R$

    $\sigma_{2} = \sigma_{\text{med}} - R$

    ### Direções principais

    Os ângulos $\theta_1$ e $\theta_2$ são definidos a partir de

    $\theta_p = \dfrac{1}{2} \arctan \left( \dfrac{2 \sigma_{xy}}{\sigma_{xx} - \sigma_{yy}} \right)$

    Considerando só ângulos positivos como solução, o menor dos ângulos é $\theta_1$ quando $\sigma_{xy}$ for positivo.

    Definido $\theta_1$, $\theta_2$ é igual a $\theta_1$ mais 90° (ou $\pi/2$ radianos).
    """)

# Observação sobre unidades
with st.expander("⚠️ Observação sobre as unidades e homogeneidade"):
    st.markdown("""
    Este sistema não impõe um sistema de unidades fixo. Portanto, é fundamental manter a **homogeneidade das unidades** entre os dados de entrada e os resultados.

    A unidade adotada para os componentes cartesianos de tensão (σ_xx, σ_yy e σ_xy) determina diretamente a unidade dos valores calculados. Não há conversão automática de unidades pela aplicação. Assim, deve haver total consistência para os resultados:

    - σ_med
    - R
    - σ_1
    - σ_2

    **Exemplo:** Se as tensões de entrada forem inseridas em **MPa**, todos os valores de saída serão calculados e apresentados em **MPa**. O mesmo se aplica para **kPa**, **kgf/cm²**, **psi** ou qualquer outra unidade de tensão, desde que seja mantida a mesma base em todos os campos de entrada.

    Os ângulos, por outro lado, são expressos em **graus** (°), salvo indicação contrária na interface.
    """)

# Cálculos
sxx = s_xx
syy = s_yy
sxy = s_xy

# Cálculo das tensões principais
s_med = (sxx + syy) / 2
R = np.sqrt(((sxx - syy) / 2) ** 2 + sxy**2)
s1 = s_med + R
s2 = s_med - R

# Cálculo das direções principais
theta_p = 0.5 * np.arctan2(2 * sxy, sxx - syy)

# Para garantir que estamos trabalhando com números positivos
theta_p_adjusted = theta_p
if theta_p_adjusted < 0:
    theta_p_adjusted += np.pi / 2
theta_p_deg = np.degrees(theta_p_adjusted)

if sxy >= 0:
    theta1 = theta_p
else:
    theta1 = theta_p + np.pi / 2
theta2 = theta1 + np.pi / 2

theta1_deg = np.degrees(theta1)
theta2_deg = np.degrees(theta2)

# Resultados
st.header("Resultados")

col = st.columns(1)
with col[0]:
    st.markdown(f"**$\\sigma_{{\\text{{med}}}}$** = {round(s_med, 2)}")
    st.markdown(f"**$R$** = {round(R, 2)}")
    st.markdown(f"**$\\sigma_{{1}}$** = {round(s1, 2)}")
    st.markdown(f"**$\\sigma_{{2}}$** = {round(s2, 2)}")
    st.markdown(f"""
**$\\theta_{{p1}}$** = {round(theta_p_deg, 2)}° e **$\\theta_{{p2}}$** = {round(theta_p_deg + 90, 2)}°
""")
    st.markdown(f"**$\\theta_{{1}}$** = {round(theta1_deg, 2)}°")
    st.markdown(f"**$\\theta_{{2}}$** = {round(theta2_deg, 2)}°")

st.divider()

# Representação gráfica planificada do estado de tensões
st.header("Representação gráfica planificada do estado de tensões")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    stress_state_plotter = StressStatePlotter(
        StressState(sigma_x=sxx, sigma_y=syy, sigma_xy=sxy)
    )
    stress_state_plotter.plot()
    st.pyplot(stress_state_plotter.fig)
    plt.close(stress_state_plotter.fig)

st.divider()

# Representação gráfica dos elementos com orientação adequada na presença das tensões principais
st.header("Elementos com orientação adequada (Tensões Principais)")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    principal_state_plotter = PrincipalStressStatePlotter(
        PrincipalStressState(
            sigma_1=s1, sigma_2=s2, theta_1_rad=theta1, theta_2_rad=theta2
        )
    )
    principal_state_plotter.plot()
    st.pyplot(principal_state_plotter.fig)
    plt.close(principal_state_plotter.fig)

st.divider()

# Representação gráfica dos elementos com orientação adequada na presença das tensões de cisalhamento extremas
st.header("Elementos com orientação adequada (Tensões de Cisalhamento Extremas)")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    extreme_shear_state_plotter = ExtremeShearStressStatePlotter(
        ExtremeShearStressState(
            sigma_med=s_med, radius=R, theta_1_rad=theta1, theta_2_rad=theta2
        )
    )
    extreme_shear_state_plotter.plot()
    st.pyplot(extreme_shear_state_plotter.fig)
    plt.close(extreme_shear_state_plotter.fig)
