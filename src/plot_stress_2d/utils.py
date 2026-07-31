import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch


def rotacionar_pontos(pontos: np.ndarray, angulo: float) -> np.ndarray:
    R = np.array([[np.cos(angulo), -np.sin(angulo)], [np.sin(angulo), np.cos(angulo)]])
    return pontos @ R.T


def desenhar_seta(ax, inicio, fim, cor="#6f2da8", espessura=4):
    seta = FancyArrowPatch(
        posA=inicio,
        posB=fim,
        arrowstyle="-|>",
        mutation_scale=22,
        linewidth=espessura,
        color=cor,
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_patch(seta)


def posicao_rotulo(ponta_seta, direcao, deslocamento=0.05):
    return ponta_seta + deslocamento * direcao


def desenhar_arco(
    ax, angulo_inicial, angulo_final, raio=0.75, cor="gray", espessura=1, label=""
):
    angulo_meio = angulo_final / 2
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
    raio_texto = raio + 0.05  # um pouco fora do arco

    pos_texto = np.array(
        [raio_texto * np.cos(angulo_meio), raio_texto * np.sin(angulo_meio)]
    )

    ax.text(
        *pos_texto,
        label,
        fontsize=14,
        color="red",
        ha="center",
        va="center",
        zorder=5,
    )
