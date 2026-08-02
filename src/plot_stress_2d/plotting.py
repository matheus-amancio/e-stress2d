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
                raio=0.9,
                espessura=1,
                label=rf"$\theta_1 = {np.degrees(theta_1):.1f}^\circ$",
            )
        if not is_close_to_zero(theta_2):
            desenhar_arco(
                self.ax,
                0,
                theta_2,
                raio=0.75,
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
                rf"$\sigma_1 = {abs(sigma_1):.2f}$",
                fontsize=11,
                color="black",
                ha="center",
                va="center",
                zorder=5,
            )
            self.ax.text(
                *pos_rotulo_neg_1,
                rf"$\sigma_1 = {abs(sigma_1):.2f}$",
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
                rf"$\sigma_2 = {abs(sigma_2):.2f}$",
                fontsize=11,
                color="black",
                ha="center",
                va="center",
                zorder=5,
            )
            self.ax.text(
                *pos_rotulo_neg_2,
                rf"$\sigma_2 = {abs(sigma_2):.2f}$",
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


@dataclass
class ExtremeShearStressState:
    sigma_med: float
    radius: float
    theta_1_rad: float
    theta_2_rad: float


class ExtremeShearStressStatePlotter:
    def __init__(self, extreme_shear_stress_state: ExtremeShearStressState):
        self.extreme_shear_stress_state = extreme_shear_stress_state

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
            vertices, self.extreme_shear_stress_state.theta_1_rad + np.pi / 4
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
        theta_1 = self.extreme_shear_stress_state.theta_1_rad
        theta_2 = self.extreme_shear_stress_state.theta_2_rad
        aux_theta_1 = theta_1 + np.pi / 4
        aux_theta_2 = theta_2 + np.pi / 4

        sigma_med = self.extreme_shear_stress_state.sigma_med
        R = self.extreme_shear_stress_state.radius

        # Construção das setas
        direcao_1 = np.array([np.cos(aux_theta_1), np.sin(aux_theta_1)])
        direcao_2 = np.array([np.cos(aux_theta_2), np.sin(aux_theta_2)])

        tangente_1 = np.array([-direcao_1[1], direcao_1[0]])
        tangente_2 = np.array([-direcao_2[1], direcao_2[0]])

        centro = np.array([0.0, 0.0])

        centro_face_positiva_1 = centro + (lado / 2 + 0.05) * direcao_1
        centro_face_negativa_1 = centro - (lado / 2 + 0.05) * direcao_1
        centro_face_positiva_2 = centro + (lado / 2 + 0.05) * direcao_2
        centro_face_negativa_2 = centro - (lado / 2 + 0.05) * direcao_2

        comprimento_seta = 0.50
        afastamento = lado / 2 + 0.05

        ponto_base_positivo_1 = centro + afastamento * direcao_1
        ponta_positiva_1 = ponto_base_positivo_1 + comprimento_seta * direcao_1

        ponto_base_negativo_1 = centro - afastamento * direcao_1
        ponta_negativa_1 = ponto_base_negativo_1 - comprimento_seta * direcao_1

        if not is_close_to_zero(sigma_med):
            if sigma_med > 0:
                desenhar_seta(
                    self.ax, ponto_base_positivo_1, ponta_positiva_1, cor="#c00000"
                )
                desenhar_seta(
                    self.ax, ponto_base_negativo_1, ponta_negativa_1, cor="#c00000"
                )
            if sigma_med < 0:
                desenhar_seta(
                    self.ax, ponta_positiva_1, ponto_base_positivo_1, cor="#c00000"
                )
                desenhar_seta(
                    self.ax, ponta_negativa_1, ponto_base_negativo_1, cor="#c00000"
                )

        ponto_base_positivo_2 = centro + afastamento * direcao_2
        ponta_positiva_2 = ponto_base_positivo_2 + comprimento_seta * direcao_2

        ponto_base_negativo_2 = centro - afastamento * direcao_2
        ponta_negativa_2 = ponto_base_negativo_2 - comprimento_seta * direcao_2

        if not is_close_to_zero(sigma_med):
            if sigma_med > 0:
                desenhar_seta(
                    self.ax, ponto_base_negativo_2, ponta_negativa_2, cor="#c00000"
                )
                desenhar_seta(
                    self.ax, ponto_base_positivo_2, ponta_positiva_2, cor="#c00000"
                )
            if sigma_med < 0:
                desenhar_seta(
                    self.ax, ponta_positiva_2, ponto_base_positivo_2, cor="#c00000"
                )
                desenhar_seta(
                    self.ax, ponta_negativa_2, ponto_base_negativo_2, cor="#c00000"
                )

        comprimento_seta = 0.50

        inicio_pos = centro_face_positiva_1 - (comprimento_seta / 2) * tangente_1
        fim_pos = centro_face_positiva_1 + (comprimento_seta / 2) * tangente_1

        inicio_neg = centro_face_negativa_1 + (comprimento_seta / 2) * tangente_1
        fim_neg = centro_face_negativa_1 - (comprimento_seta / 2) * tangente_1

        if not is_close_to_zero(R):
            if R > 0:
                desenhar_seta(self.ax, fim_pos, inicio_pos, cor="#c00000")
                desenhar_seta(self.ax, fim_neg, inicio_neg, cor="#c00000")
            else:
                desenhar_seta(self.ax, inicio_pos, fim_pos, cor="#c00000")
                desenhar_seta(self.ax, inicio_neg, fim_neg, cor="#c00000")

        inicio_pos_2 = centro_face_positiva_2 + (comprimento_seta / 2) * tangente_2
        fim_pos_2 = centro_face_positiva_2 - (comprimento_seta / 2) * tangente_2

        inicio_neg_2 = centro_face_negativa_2 - (comprimento_seta / 2) * tangente_2
        fim_neg_2 = centro_face_negativa_2 + (comprimento_seta / 2) * tangente_2

        if not is_close_to_zero(R):
            if R > 0:
                desenhar_seta(self.ax, fim_pos_2, inicio_pos_2, cor="#c00000")
                desenhar_seta(self.ax, fim_neg_2, inicio_neg_2, cor="#c00000")
            else:
                desenhar_seta(self.ax, inicio_pos_2, fim_pos_2, cor="#c00000")
                desenhar_seta(self.ax, inicio_neg_2, fim_neg_2, cor="#c00000")

    def desenhar_angulos(self):
        theta_1 = self.extreme_shear_stress_state.theta_1_rad

        if not is_close_to_zero(theta_1):
            desenhar_arco(
                self.ax,
                0,
                theta_1,
                raio=1.0,
                espessura=1,
                label=rf"$\theta_1 = {np.degrees(theta_1):.1f}^\circ$",
            )
        if not is_close_to_zero(theta_1 + np.pi / 4):
            desenhar_arco(
                self.ax,
                theta_1,
                theta_1 + np.pi / 4,
                raio=0.9,
                espessura=1,
                label=r"$45^\circ$",
                cor="red",
                text_color="red",
            )
        if not is_close_to_zero(theta_1 + 3 * np.pi / 4):
            desenhar_arco(
                self.ax,
                theta_1,
                theta_1 + 3 * np.pi / 4,
                raio=0.75,
                espessura=1,
                label=r"$135^\circ$",
                cor="red",
                text_color="red",
            )

    def adicionar_rotulos(self):
        lado = self.lado_quadrado
        theta_1 = self.extreme_shear_stress_state.theta_1_rad
        theta_2 = self.extreme_shear_stress_state.theta_2_rad
        aux_theta_1 = theta_1 + np.pi / 4
        aux_theta_2 = theta_2 + np.pi / 4

        sigma_med = self.extreme_shear_stress_state.sigma_med
        R = self.extreme_shear_stress_state.radius

        # Construção das setas
        direcao_1 = np.array([np.cos(aux_theta_1), np.sin(aux_theta_1)])
        direcao_2 = np.array([np.cos(aux_theta_2), np.sin(aux_theta_2)])

        tangente_1 = np.array([-direcao_1[1], direcao_1[0]])
        tangente_2 = np.array([-direcao_2[1], direcao_2[0]])

        centro = np.array([0.0, 0.0])

        centro_face_positiva_1 = centro + (lado / 2 + 0.05) * direcao_1
        centro_face_negativa_1 = centro - (lado / 2 + 0.05) * direcao_1
        centro_face_positiva_2 = centro + (lado / 2 + 0.05) * direcao_2
        centro_face_negativa_2 = centro - (lado / 2 + 0.05) * direcao_2

        comprimento_seta = 0.50
        afastamento = lado / 2 + 0.05

        # Tensões normais
        ponto_base_positivo_1 = centro + afastamento * direcao_1
        ponta_positiva_1 = ponto_base_positivo_1 + comprimento_seta * direcao_1

        ponto_base_negativo_1 = centro - afastamento * direcao_1
        ponta_negativa_1 = ponto_base_negativo_1 - comprimento_seta * direcao_1

        ponto_base_positivo_2 = centro + afastamento * direcao_2
        ponta_positiva_2 = ponto_base_positivo_2 + comprimento_seta * direcao_2

        ponto_base_negativo_2 = centro - afastamento * direcao_2
        ponta_negativa_2 = ponto_base_negativo_2 - comprimento_seta * direcao_2

        if not is_close_to_zero(sigma_med):
            offset = 0.07
            s_med_positions = [
                ponta_positiva_1 + offset * direcao_1,
                ponta_negativa_1 - offset * direcao_1,
                ponta_positiva_2 + offset * direcao_2,
                ponta_negativa_2 - offset * direcao_2,
            ]
            for pos in s_med_positions:
                self.ax.text(
                    *pos,
                    rf"$\sigma_{{med}} = {abs(sigma_med):.2f}$",
                    fontsize=11,
                    color="black",
                    ha="center",
                    va="center",
                    zorder=5,
                )

        # Tensões de cisalhamento
        inicio_pos = centro_face_positiva_1 - (comprimento_seta / 2) * tangente_1
        fim_pos = centro_face_positiva_1 + (comprimento_seta / 2) * tangente_1

        inicio_neg = centro_face_negativa_1 + (comprimento_seta / 2) * tangente_1
        fim_neg = centro_face_negativa_1 - (comprimento_seta / 2) * tangente_1

        inicio_pos_2 = centro_face_positiva_2 + (comprimento_seta / 2) * tangente_2
        fim_pos_2 = centro_face_positiva_2 - (comprimento_seta / 2) * tangente_2

        inicio_neg_2 = centro_face_negativa_2 - (comprimento_seta / 2) * tangente_2
        fim_neg_2 = centro_face_negativa_2 + (comprimento_seta / 2) * tangente_2

        offset = 0.25
        s_cis_positions = [
            inicio_pos - offset * tangente_1,
            inicio_pos_2 + offset * tangente_2,
        ]
        for pos in s_cis_positions:
            self.ax.text(
                *pos,
                rf"$R = {abs(R):.2f}$",
                fontsize=11,
                color="black",
                ha="center",
                va="center",
                zorder=5,
            )

    def desenhar_auxiliares(self):
        theta_1 = self.extreme_shear_stress_state.theta_1_rad
        # linha horizontal auxiliar
        self.ax.plot(
            [0.0, 2.0], [0.0, 0.0], color="gray", linestyle="--", linewidth=1, zorder=1
        )
        self.ax.plot(
            [0.0, 3.0 * np.cos(theta_1)],
            [0.0, 3.0 * np.sin(theta_1)],
            color="gray",
            linestyle="--",
            linewidth=1,
            zorder=1,
        )

    def plot(self):
        self.criar_figura()
        self.desenhar_quadrado()
        self.desenhar_setas()
        self.desenhar_angulos()
        self.adicionar_rotulos()
        self.desenhar_auxiliares()
