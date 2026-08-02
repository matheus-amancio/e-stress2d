import marimo

__generated_with = "0.23.15"
app = marimo.App(app_title="e-Stress2D")


@app.cell
def _():
    import marimo as mo
    import numpy as np

    from plot_stress_2d.plotting import (
        ExtremeShearStressState,
        ExtremeShearStressStatePlotter,
        PrincipalStressState,
        PrincipalStressStatePlotter,
    )

    return (
        ExtremeShearStressState,
        ExtremeShearStressStatePlotter,
        PrincipalStressState,
        PrincipalStressStatePlotter,
        mo,
        np,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # e-Stress2D

    Desenvolvido por:
    - Matheus Amancio Miranda
    - Eduardo Nobre Lages
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Entrada de dados
    """)
    return


@app.cell
def _(mo, np):
    initial_values = {
        "s_xx": round(np.random.uniform(-100, 100), 2),
        "s_yy": round(np.random.uniform(-100, 100), 2),
        "s_xy": round(np.random.uniform(-100, 100), 2),
    }

    s_xx_input = mo.ui.number(value=initial_values["s_xx"], label=r"$\sigma_{xx}$")
    s_yy_input = mo.ui.number(value=initial_values["s_yy"], label=r"$\sigma_{yy}$")
    s_xy_input = mo.ui.number(value=initial_values["s_xy"], label=r"$\sigma_{xy}$")

    mo.vstack(
        [
            s_xx_input,
            s_yy_input,
            s_xy_input,
        ]
    )
    return s_xx_input, s_xy_input, s_yy_input


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Equacionamento

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
    return


@app.cell
def _(mo, np, s_xx_input, s_xy_input, s_yy_input):
    mo.stop(
        s_xx_input.value is None
        or s_yy_input.value is None
        or s_xy_input.value is None,
        mo.md("Aguardando valores serem preenchidos..."),
    )

    sxx = s_xx_input.value
    syy = s_yy_input.value
    sxy = s_xy_input.value

    if sxx is not None and syy is not None and sxy is not None:
        # Cálculo das tensões principais
        s_med = (sxx + syy) / 2
        R = np.sqrt(((sxx - syy) / 2) ** 2 + sxy**2)
        s1 = s_med + R
        s2 = s_med - R

        # Cálculo das direções principais
        theta_p = 0.5 * np.arctan2(2 * sxy, sxx - syy)

        # Para garantir que estamos trabalhando com números positivos
        if theta_p < 0:
            theta_p += np.pi / 2
        theta_p_deg = np.degrees(theta_p)

        if sxy >= 0:
            theta1 = theta_p
        else:
            theta1 = theta_p + np.pi / 2
        theta2 = theta1 + np.pi / 2

        theta1_deg = np.degrees(theta1)
        theta2_deg = np.degrees(theta2)
    return (
        R,
        s1,
        s2,
        s_med,
        theta1,
        theta1_deg,
        theta2,
        theta2_deg,
        theta_p_deg,
    )


@app.cell
def _(
    R,
    mo,
    s1,
    s2,
    s_med,
    s_xx_input,
    s_xy_input,
    s_yy_input,
    theta1_deg,
    theta2_deg,
    theta_p_deg,
):
    mo.stop(
        s_xx_input.value is None
        or s_yy_input.value is None
        or s_xy_input.value is None,
        mo.md("Aguardando valores serem preenchidos..."),
    )

    mo.md(
        rf"""
    ## Resultados

    $\sigma_{{\text{{med}}}} = {round(s_med, 2)}$

    $R = {round(R, 2)}$

    $\sigma_{{1}} = {round(s1, 2)}$

    $\sigma_{{2}} = {round(s2, 2)}$

    $\theta_{{p}} = {round(theta_p_deg, 2)}^\circ$

    $\theta_{{1}} = {round(theta1_deg, 2)}^\circ$

    $\theta_{{2}} = {round(theta2_deg, 2)}^\circ$

    """
    )
    return


@app.cell
def _(mo, s_xx_input, s_xy_input, s_yy_input):
    mo.stop(
        s_xx_input.value is None
        or s_yy_input.value is None
        or s_xy_input.value is None,
        mo.md("Aguardando valores serem preenchidos..."),
    )
    mo.md(
        "## Representação gráfica dos elementos com orientação adequada na presença das tensões principais"
    )
    return


@app.cell
def _(
    PrincipalStressState,
    PrincipalStressStatePlotter,
    mo,
    s1,
    s2,
    s_xx_input,
    s_xy_input,
    s_yy_input,
    theta1,
    theta2,
):
    mo.stop(
        s_xx_input.value is None
        or s_yy_input.value is None
        or s_xy_input.value is None,
        mo.md("Aguardando valores serem preenchidos..."),
    )

    principal_state_plotter = PrincipalStressStatePlotter(
        PrincipalStressState(
            sigma_1=s1, sigma_2=s2, theta_1_rad=theta1, theta_2_rad=theta2
        )
    )
    principal_state_plotter.plot()

    principal_state_plotter.ax
    return


@app.cell
def _(mo, s_xx_input, s_xy_input, s_yy_input):
    mo.stop(
        s_xx_input.value is None or s_yy_input.value is None or s_xy_input.value is None,
        mo.md("Aguardando valores serem preenchidos..."),
    )
    mo.md(
        "## Representação gráfica dos elementos com orientação adequada na presença das tensões de cisalhamento extremas"
    )
    return


@app.cell
def _(
    ExtremeShearStressState,
    ExtremeShearStressStatePlotter,
    R,
    mo,
    s_med,
    s_xx_input,
    s_xy_input,
    s_yy_input,
    theta1,
    theta2,
):
    mo.stop(
        s_xx_input.value is None
        or s_yy_input.value is None
        or s_xy_input.value is None,
        mo.md("Aguardando valores serem preenchidos..."),
    )

    extreme_shear_state_plotter = ExtremeShearStressStatePlotter(
        ExtremeShearStressState(
            sigma_med=s_med, radius=R, theta_1_rad=theta1, theta_2_rad=theta2
        )
    )
    extreme_shear_state_plotter.plot()

    extreme_shear_state_plotter.ax
    return


if __name__ == "__main__":
    app.run()
