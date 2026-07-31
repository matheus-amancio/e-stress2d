import marimo

__generated_with = "0.23.14"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Polygon

    from plot_stress_2d.utils import desenhar_seta, rotacionar_pontos, posicao_rotulo, desenhar_arco

    return (
        Polygon,
        desenhar_arco,
        desenhar_seta,
        mo,
        np,
        plt,
        posicao_rotulo,
        rotacionar_pontos,
    )


@app.cell
def _(mo):
    theta_1_input = mo.ui.number(value=30, label=r"$\theta_1$")
    theta_2_input = mo.ui.number(value=120, label=r"$\theta_2$")
    mo.vstack([
        theta_1_input,
        theta_2_input,
    ])
    return (theta_1_input,)


@app.cell
def _(theta_1_input):
    type(theta_1_input.value)
    return


@app.cell
def _(np, theta_1_input):
    # Tensões e direções principais
    theta_1 = np.deg2rad(theta_1_input.value)
    sigma_1 = 100
    theta_2 = np.deg2rad(theta_1_input.value + 90)
    sigma_2 = 50
    return theta_1, theta_2


@app.cell
def _(np, rotacionar_pontos, theta_1):
    # Construção dos vértices do quadrado
    lado: float = 1.0

    vertices: np.ndarray = np.array(
        [
            [-lado / 2, -lado / 2],
            [lado / 2, -lado / 2],
            [lado / 2, lado / 2],
            [-lado / 2, lado / 2],
        ]
    )

    vertices_rotacionados: np.ndarray = rotacionar_pontos(vertices, theta_1)
    vertices_rotacionados
    return lado, vertices_rotacionados


@app.cell
def _(np, rotacionar_pontos, theta_1, theta_2):
    # Construção dos pontos das retas auxiliares das direções principais

    comprimento_reta: float = 2.0
    reta_1 = np.array([
        [-comprimento_reta, 0],
        [comprimento_reta, 0],
    ])
    reta_2 = np.array([
        [0, -comprimento_reta],
        [0, comprimento_reta],
    ])

    # rotacionar as retas auxiliares
    reta_1_rotacionada = rotacionar_pontos(reta_1, theta_1)
    reta_2_rotacionada = rotacionar_pontos(reta_1, theta_2)
    return reta_1_rotacionada, reta_2_rotacionada


@app.cell
def _(
    Polygon,
    desenhar_arco,
    desenhar_seta,
    lado: float,
    np,
    plt,
    posicao_rotulo,
    reta_1_rotacionada,
    reta_2_rotacionada,
    theta_1,
    theta_2,
    vertices_rotacionados: "np.ndarray",
):
    # Construção da figura
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set_aspect("equal")

    # adicionando retas
    ax.plot(
        reta_1_rotacionada[:, 0],
        reta_1_rotacionada[:, 1],
        color="gray",
        linestyle="--",
        linewidth=1,
        zorder=1,
    )
    ax.plot(
        reta_2_rotacionada[:, 0],
        reta_2_rotacionada[:, 1],
        color="gray",
        linestyle="--",
        linewidth=1,
        zorder=1,
    )

    # linha horizontal auxiliar
    ax.plot([0.0, 2.0], [0.0, 0.0], color="gray", linestyle="--", linewidth=1, zorder=1)

    quadrado = Polygon(
        vertices_rotacionados,
        closed=True,
        edgecolor="black",
        facecolor="lightgray",
        zorder=2,
    )
    # Construção das setas
    direcao_1 = np.array([np.cos(theta_1), np.sin(theta_1)])
    direcao_2 = np.array([np.cos(theta_2), np.sin(theta_2)])

    centro = np.array([0.0, 0.0])

    comprimento_seta = 0.50
    afastamento = lado / 2

    ponto_base_positivo_1 = centro + afastamento * direcao_1
    ponta_positiva_1 = ponto_base_positivo_1 + comprimento_seta * direcao_1

    ponto_base_negativo_1 = centro - afastamento * direcao_1
    ponta_negativa_1 = ponto_base_negativo_1 - comprimento_seta * direcao_1

    desenhar_seta(ax, ponto_base_positivo_1, ponta_positiva_1)
    desenhar_seta(ax, ponto_base_negativo_1, ponta_negativa_1)

    ponto_base_positivo_2 = centro + afastamento * direcao_2
    ponta_positiva_2 = ponto_base_positivo_2 + comprimento_seta * direcao_2

    ponto_base_negativo_2 = centro - afastamento * direcao_2
    ponta_negativa_2 = ponto_base_negativo_2 - comprimento_seta * direcao_2

    desenhar_seta(ax, ponto_base_positivo_2, ponta_positiva_2)
    desenhar_seta(ax, ponto_base_negativo_2, ponta_negativa_2)

    p_rotulo_sigma_1_positivo = posicao_rotulo(ponta_positiva_1, direcao_1, 0.01)
    p_rotulo_sigma_1_negativo = posicao_rotulo(ponta_negativa_1, direcao_1, -0.1)
    ax.text(
        *p_rotulo_sigma_1_positivo,
        r"$\sigma_1$",
        fontsize=16,
        ha="left",
        va="bottom",
    )
    ax.text(
        *p_rotulo_sigma_1_negativo,
        r"$\sigma_1$",
        fontsize=16,
        ha="left",
        va="bottom",
    )

    p_rotulo_sigma_2_positivo = posicao_rotulo(ponta_positiva_2, direcao_2, 0.01)
    p_rotulo_sigma_2_negativo = posicao_rotulo(ponta_negativa_2, direcao_2, -0.1)
    ax.text(
        *p_rotulo_sigma_2_positivo,
        r"$\sigma_2$",
        fontsize=16,
        ha="left",
        va="bottom",
    )
    ax.text(
        *p_rotulo_sigma_2_negativo,
        r"$\sigma_2$",
        fontsize=16,
        ha="left",
        va="bottom",
    )

    desenhar_arco(ax, 0.0, theta_1, raio=1.0, label=r"$\theta_1$")
    desenhar_arco(ax, 0.0, theta_2, raio=1.225, label=r"$\theta_2$")

    ax.add_patch(quadrado)
    limit = 1.50
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_xticks([])
    ax.set_yticks([])
    ax
    return


if __name__ == "__main__":
    app.run()
