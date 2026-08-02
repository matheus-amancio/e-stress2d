import math

import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch


def rotacionar_pontos(pontos: np.ndarray, angulo: float) -> np.ndarray:
    R = np.array([[np.cos(angulo), -np.sin(angulo)], [np.sin(angulo), np.cos(angulo)]])
    return pontos @ R.T


def desenhar_seta(ax, inicio, fim, cor="#6f2da8", espessura=4):
    seta = FancyArrowPatch(
        posA=inicio,
        posB=fim,
        arrowstyle="->",
        mutation_scale=22,
        linewidth=espessura,
        color=cor,
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_patch(seta)


def desenhar_arco(
    ax,
    angulo_inicial,
    angulo_final,
    raio=0.75,
    cor="#c00000",
    espessura=1,
    label="",
    text_color="black",
    text_size=11,
):
    angulo_meio = (angulo_inicial + angulo_final) / 2
    arco = Arc(
        (0, 0),
        2 * raio,
        2 * raio,
        angle=0,
        theta1=np.degrees(angulo_inicial),
        theta2=np.degrees(angulo_final),
        color=cor,
        linewidth=espessura,
        linestyle="--",
    )
    ax.add_patch(arco)

    # Seta no ponto final do arco usando FancyArrowPatch
    eps = 1e-3
    tip_x = raio * np.cos(angulo_final)
    tip_y = raio * np.sin(angulo_final)
    # Tangente no ponto final (sentido anti-horário)
    dx = -np.sin(angulo_final)
    dy = np.cos(angulo_final)
    arrow = FancyArrowPatch(
        posA=(tip_x - dx * eps, tip_y - dy * eps),
        posB=(tip_x + dx * eps, tip_y + dy * eps),
        arrowstyle="->",
        color=cor,
        mutation_scale=10,
        linewidth=espessura,
    )
    ax.add_patch(arrow)

    raio_texto = raio + 0.07  # um pouco fora do arco

    pos_texto = np.array(
        [raio_texto * np.cos(angulo_meio), raio_texto * np.sin(angulo_meio)]
    )

    ax.text(
        *pos_texto,
        label,
        fontsize=text_size,
        color=text_color,
        ha="center",
        va="center",
        zorder=5,
    )


def is_close_to_zero(value, tol=1e-6):
    return math.isclose(value, 0.0, abs_tol=tol)


def add_coordinate_system(ax):
    comprimento_eixo = 0.3
    origem = (-1.45, -1.45)
    ax.plot(
        [origem[0], origem[0] + comprimento_eixo],
        [origem[1], origem[1]],
        color="black",
        linewidth=1,
    )
    ax.plot(
        [origem[0], origem[0]],
        [origem[1], origem[1] + comprimento_eixo],
        color="black",
        linewidth=1,
    )
    ax.text(
        origem[0] + comprimento_eixo + 0.05,
        origem[1],
        "x",
        fontsize=10,
        color="black",
        ha="center",
        va="center",
    )
    ax.text(
        origem[0],
        origem[1] + comprimento_eixo + 0.05,
        "y",
        fontsize=10,
        color="black",
        ha="center",
        va="center",
    )
