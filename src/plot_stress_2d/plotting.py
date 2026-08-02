from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

from plot_stress_2d.utils import (
    desenhar_arco,
    desenhar_seta,
    is_close_to_zero,
    rotacionar_pontos,
)


@dataclass
class PrincipalStressState:
    sigma_1: float
    sigma_2: float
    theta_1_rad: float
    theta_2_rad: float


class PrincipalStressStatePlotter:
    def __init__(self, principal_stress_state: PrincipalStressState):
        self.principal_stress_state = principal_stress_state

    def criar_figura(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect("equal")
        self.fig = fig
        self.ax = ax
        self.configurar_eixos()

    def configurar_eixos(self):
        limit = 1.50
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

    def desenhar_quadrado(self):
        self.lado_quadrado = 1.0
        lado = 1.0
        vertices = np.array(
            [
                [-lado / 2, -lado / 2],
                [lado / 2, -lado / 2],
                [lado / 2, lado / 2],
                [-lado / 2, lado / 2],
            ]
        )
        vertices_rotacionados = rotacionar_pontos(
            vertices, self.principal_stress_state.theta_1_rad
        )
        quadrado = Polygon(
            vertices_rotacionados,
            closed=True,
            edgecolor="#ff9999",
            facecolor="#ffcccc",
            zorder=2,
        )
        self.ax.add_patch(quadrado)

    def desenhar_setas(self):
        lado = self.lado_quadrado
        theta_1 = self.principal_stress_state.theta_1_rad
        theta_2 = self.principal_stress_state.theta_2_rad

        sigma_1 = self.principal_stress_state.sigma_1
        sigma_2 = self.principal_stress_state.sigma_2

        # Construção das setas
        direcao_1 = np.array([np.cos(theta_1), np.sin(theta_1)])
        direcao_2 = np.array([np.cos(theta_2), np.sin(theta_2)])

        centro = np.array([0.0, 0.0])

        comprimento_seta = 0.50
        afastamento = lado / 2 + 0.05

        ponto_base_positivo_1 = centro + afastamento * direcao_1
        ponta_positiva_1 = ponto_base_positivo_1 + comprimento_seta * direcao_1

        ponto_base_negativo_1 = centro - afastamento * direcao_1
        ponta_negativa_1 = ponto_base_negativo_1 - comprimento_seta * direcao_1

        if not is_close_to_zero(sigma_1):
            if sigma_1 > 0:
                desenhar_seta(self.ax, ponto_base_positivo_1, ponta_positiva_1)
                desenhar_seta(self.ax, ponto_base_negativo_1, ponta_negativa_1)
            if sigma_1 < 0:
                desenhar_seta(self.ax, ponta_positiva_1, ponto_base_positivo_1)
                desenhar_seta(self.ax, ponta_negativa_1, ponto_base_negativo_1)

        ponto_base_positivo_2 = centro + afastamento * direcao_2
        ponta_positiva_2 = ponto_base_positivo_2 + comprimento_seta * direcao_2

        ponto_base_negativo_2 = centro - afastamento * direcao_2
        ponta_negativa_2 = ponto_base_negativo_2 - comprimento_seta * direcao_2

        if not is_close_to_zero(sigma_2):
            if sigma_2 > 0:
                desenhar_seta(self.ax, ponto_base_negativo_2, ponta_negativa_2)
                desenhar_seta(self.ax, ponto_base_positivo_2, ponta_positiva_2)
            if sigma_2 < 0:
                desenhar_seta(self.ax, ponta_positiva_2, ponto_base_positivo_2)
                desenhar_seta(self.ax, ponta_negativa_2, ponto_base_negativo_2)

    def desenhar_angulos(self):
        theta_1 = self.principal_stress_state.theta_1_rad
        theta_2 = self.principal_stress_state.theta_2_rad

        if not is_close_to_zero(theta_1):
            desenhar_arco(
                self.ax,
                0,
                theta_1,
                raio=0.75,
                espessura=1,
                label=rf"$\theta_1 = {np.degrees(theta_1):.1f}^\circ$",
            )
        if not is_close_to_zero(theta_2):
            desenhar_arco(
                self.ax,
                0,
                theta_2,
                raio=0.95,
                espessura=1,
                label=rf"$\theta_2 = {np.degrees(theta_2):.1f}^\circ$",
            )

    def adicionar_rotulos(self):
        lado = self.lado_quadrado
        theta_1 = self.principal_stress_state.theta_1_rad
        theta_2 = self.principal_stress_state.theta_2_rad

        sigma_1 = self.principal_stress_state.sigma_1
        sigma_2 = self.principal_stress_state.sigma_2

        direcao_1 = np.array([np.cos(theta_1), np.sin(theta_1)])
        direcao_2 = np.array([np.cos(theta_2), np.sin(theta_2)])

        centro = np.array([0.0, 0.0])

        comprimento_seta = 0.50
        afastamento = lado / 2 + 0.05

        ponto_base_positivo_1 = centro + afastamento * direcao_1
        ponta_positiva_1 = ponto_base_positivo_1 + comprimento_seta * direcao_1

        ponto_base_negativo_1 = centro - afastamento * direcao_1
        ponta_negativa_1 = ponto_base_negativo_1 - comprimento_seta * direcao_1

        ponto_base_positivo_2 = centro + afastamento * direcao_2
        ponta_positiva_2 = ponto_base_positivo_2 + comprimento_seta * direcao_2

        ponto_base_negativo_2 = centro - afastamento * direcao_2
        ponta_negativa_2 = ponto_base_negativo_2 - comprimento_seta * direcao_2

        if not is_close_to_zero(sigma_1):
            pos_rotulo_pos_1 = ponta_positiva_1 + 0.07 * direcao_1
            pos_rotulo_neg_1 = ponta_negativa_1 - 0.07 * direcao_1
            self.ax.text(
                *pos_rotulo_pos_1,
                rf"$\sigma_1 = {sigma_1:.2f}$",
                fontsize=11,
                color="black",
                ha="center",
                va="center",
                zorder=5,
            )
            self.ax.text(
                *pos_rotulo_neg_1,
                rf"$\sigma_1 = {sigma_1:.2f}$",
                fontsize=11,
                color="black",
                ha="center",
                va="center",
                zorder=5,
            )

        if not is_close_to_zero(sigma_2):
            pos_rotulo_pos_2 = ponta_positiva_2 + 0.07 * direcao_2
            pos_rotulo_neg_2 = ponta_negativa_2 - 0.07 * direcao_2
            self.ax.text(
                *pos_rotulo_pos_2,
                rf"$\sigma_2 = {sigma_2:.2f}$",
                fontsize=11,
                color="black",
                ha="center",
                va="center",
                zorder=5,
            )
            self.ax.text(
                *pos_rotulo_neg_2,
                rf"$\sigma_2 = {sigma_2:.2f}$",
                fontsize=11,
                color="black",
                ha="center",
                va="center",
                zorder=5,
            )

    def desenhar_auxiliares(self):
        # linha horizontal auxiliar
        self.ax.plot(
            [0.0, 2.0], [0.0, 0.0], color="gray", linestyle="--", linewidth=1, zorder=1
        )

    def plot(self):
        self.criar_figura()
        self.desenhar_quadrado()
        self.desenhar_setas()
        self.desenhar_angulos()
        self.desenhar_auxiliares()
        self.adicionar_rotulos()
