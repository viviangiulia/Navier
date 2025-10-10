import sys
import os
import math

from dataclasses import dataclass


@dataclass
class DadosViga:
    mk: float
    vk: float
    bw: float
    h: float
    d: float
    fck: float
    fyk: float
    fcd: float
    fyd: float
    vsd: float
    theta_transversal: int = 45
    modelo_calculo: str = "Modelo I"
    xis_dominio: float = 0.450

    def validar_dados(self) -> tuple[bool, str]:
        """Valida se todos os dados necessários para cálculo foram preenchidos."""
        campos = {
            "Momento Fletor (Mk)": self.mk,
            "Largura da Viga (bw)": self.bw,
            "Altura Total (h)": self.h,
            "Altura Útil (d)": self.d,
            "Concreto (fck)": self.fck,
            "Aço (fyk)": self.fyk,
            "Concreto (fcd)": self.fcd,
            "Aço (fyd)": self.fyd,
        }

        for nome, valor in campos.items():
            if valor is None or valor <= 0:
                return False, f"O valor de '{nome}' está ausente ou inválido."

        return True, "Todos os dados válidos."


class CalculadoraViga:

    @staticmethod
    def calcular_viga_cortante(dados_viga: DadosViga) -> dict:

        alfa_transversal = (
            90  # Estribos verticais (ãngulo de 90° com relação ao eixo da barra)
        )

        alfa_transversal = (alfa_transversal / 180) * math.pi
        fator_cotangentes_transversal = (
            (math.cos(alfa_transversal) / math.sin(alfa_transversal))
        ) + (
            math.cos(dados_viga.theta_transversal)
            / math.sin(dados_viga.theta_transversal)
        )
        fator_cotangentes_transversal = 1

        vrd2 = (
            # -------------- TENSÃO MÁXIMA CONVENCIONAL DE CISALHAMENTO
            0.27
            * (1 - (dados_viga.fck / 250))  # alfav2
            * dados_viga.fcd
            # -------------- TENSÃO MÁXIMA CONVENCIONAL DE CISALHAMENTO
            * (dados_viga.bw / 100)  # bw em metros
            * (dados_viga.d / 100)  # d em metros
            * (math.sin(2 * dados_viga.theta_transversal))
            * fator_cotangentes_transversal
            * 1000
        )  # Força cortante resistente de cálculo
        vrd2 = round(vrd2, 2)

        print(
            f"[NOTICE] Força Cortante Solicitante de Cálculo Vsd: {dados_viga.vsd:.2f} kN"
        )
        print(
            f"[NOTICE] Força Cortante Resistente de Cálculo (ruína das diagonais comprimidas) VRd2: {vrd2:.2f} kN"
        )

        if vrd2 < dados_viga.vsd:
            print(
                "[ERROR] A seção de concreto não permite gerar bielas resistentes à compressão. "
                "Reveja as dimensões da viga ou esforços de cálculo para a estrutura."
            )
            raise ValueError(
                "A seção de concreto não permite gerar bielas resistentes à compressão. "
                "Reveja as dimensões da viga ou esforços de cálculo para a estrutura."
            )
        else:
            vc_0 = (
                0.09
                * (dados_viga.fck ** (2 / 3))
                * (dados_viga.bw / 100)
                * (dados_viga.d / 100)
                * 1000
            )
            if dados_viga.modelo_calculo == "Modelo II":
                vc_0 = vc_0 * ((vrd2 - dados_viga.vsd) / (vrd2 - vc_0))

            vsw = dados_viga.vsd - vc_0

            as_transversal = (
                vsw
                / (0.9 * (dados_viga.d / 100) * dados_viga.fyd)
                * math.tan(dados_viga.theta_transversal)
            ) * 1000

            taxa_aco_cortante_retangular = (
                0.2 * (0.3 * dados_viga.fck ** (2 / 3)) / dados_viga.fyk
            )

            as_min_transversal = (
                (dados_viga.bw * 10) * taxa_aco_cortante_retangular
            ) * 1000  # para deixar em mm²

            print(f"[NOTICE] Força Cortante Vk: {dados_viga.vk:.2f} kN")
            print(
                f"[NOTICE] Força Cortante Mecanismos Complementares (ângulo = 45)° Vc0: {vc_0:.2f} kN"
            )
            print(
                f"[NOTICE] Força Cortante parcela resistida pela armadura transversal Vsw: {vsw:.2f} kN"
            )
            print(
                f"[NOTICE] Área da Seção Transversão dos Estribos Asw: {as_transversal:.2f} mm²"
            )
            print(
                f"[NOTICE] Área de aço transversal mínima por metro linear Aswmin/s: {as_min_transversal:.2f} mm²/m"
            )

            # TODO verificar se vou usar essa informação
            if dados_viga.vsd <= 0.67 * vrd2:
                espass_maximo = 30
            else:
                espass_maximo = 20

        return {
            "vk_viga": dados_viga.vk,
            "vsd": dados_viga.vsd,
            "vrd2": vrd2,
            "vc_0": vc_0,
            "as_transversal": as_transversal,
            "taxa_aco_cortante_retangular": taxa_aco_cortante_retangular,
            "as_min_transversal": as_min_transversal,
            "vsw": vsw,
        }

    @staticmethod
    def calcular_viga_simples(dados_viga: DadosViga) -> dict:
        """Retonar um dicionário com os resultados obtidos após terminar o dimensionamento da viga simplesmente armada."""
        d_linha = dados_viga.h - dados_viga.d
        area_secao_viga = dados_viga.bw * dados_viga.h

        kmd_viga = (dados_viga.mk * 1.4 * 1000) / (
            (dados_viga.bw / 100)
            * ((dados_viga.d / 100) ** 2)
            * (0.85 * dados_viga.fcd * 1000000)
        )

        if kmd_viga > 0.5:
            print(
                "[ERROR] Os esforços especificados não são suportados pela seção de concreto analisada. "
                "Por favor altere as dimensões da seção da viga ou reveja os esforços de cálculo para a estrutura."
            )
            raise ValueError(
                "Os esforços especificados não são suportados pela seção de concreto analisada. "
                "Por favor altere as dimensões da seção da viga ou reveja os esforços de cálculo para a estrutura."
            )
        else:
            kx_viga = (1 - math.sqrt(1 - 2 * kmd_viga)) / 0.8
            kz_viga = 1 - 0.4 * kx_viga
            as_viga = (dados_viga.mk * 1.4 * 1000) / (
                kz_viga * (dados_viga.d / 100) * dados_viga.fyd
            )

            as_sobre_apoio_viga = as_viga / 3
            if dados_viga.h >= 60:
                as_pele = (0.1 / 100) * area_secao_viga * 100
            else:
                as_pele = 0

            as_max_viga = (4 / 100) * area_secao_viga * 100

            # TODO código repetido refatorar
            taxa_aco_por_fck = {
                20: 0.0015,
                25: 0.0015,
                30: 0.00173,
                35: 0.00201,
                40: 0.00203,
                45: 0.00259,
                50: 0.00288,
            }
            taxa_aco_viga_retangular = taxa_aco_por_fck.get(dados_viga.fck)

            if taxa_aco_viga_retangular is None:
                raise ValueError(f"fck inválido: {dados_viga.fck}")

            as_min_viga = taxa_aco_viga_retangular * area_secao_viga * 100

            # TODO melhorar esta estrutura
            if kx_viga < 0:
                dominio_viga = "Domínio 1"
            elif kx_viga > 0 and kx_viga < 0.259:
                dominio_viga = "Domínio 2"
            elif kx_viga > 0.259 and kx_viga < 0.45:
                dominio_viga = "Domínio 3 - Dúctil"
            elif kx_viga > 0.45 and kx_viga < 0.63:
                dominio_viga = "Domínio 3 - Não Dúctil"
            elif kx_viga > 0.628 and kx_viga < 1:
                dominio_viga = "Domínio 4a"
            elif (kx_viga > 0.438 and kx_viga < 1) and (dados_viga.fyk == 600):
                dominio_viga = "Domínio 4a"
            else:
                dominio_viga = "Domínio 4b"

            print(
                f"[NOTICE] Intensidade do momento fletor solicitante Kmd: {kmd_viga:.2f}"
            )
            print(f"[NOTICE] Profundidade da linha neutra Kx: {kx_viga:.2f}")
            print(f"[NOTICE] Altura do braço de alavanca interno Kz: {kz_viga:.2f}")
            print(
                f"[NOTICE] Área da seção transversal da armadura longitudinal de tração As: {as_viga:.2f} mm²"
            )

        resultados_viga = CalculadoraViga.calcular_viga_cortante(dados_viga)

        resultados_viga.update(
            {
                "kmd_viga": kmd_viga,
                "kx_viga": kx_viga,
                "kz_viga": kz_viga,
                "as_viga": as_viga,
                "as_sobre_apoio_viga": as_sobre_apoio_viga,
                "as_max_viga": as_max_viga,
                "as_min_viga": as_min_viga,
                "as_pele": as_pele,
                "d_linha": d_linha,
                "dominio_viga": dominio_viga,
            }
        )

        return resultados_viga

    @staticmethod
    def calcular_viga_dupla(dados_viga: DadosViga) -> dict:

        d_linha = dados_viga.h - dados_viga.d

        xis_dominio = dados_viga.xis_dominio

        d_min_viga = math.sqrt(
            (dados_viga.mk * 1.4 * 1000)
            / (
                (dados_viga.bw / 100)
                * (dados_viga.fcd * 1000000)
                * (0.68 * xis_dominio - 0.272 * (xis_dominio**2))
            )
        )

        x_lim_viga = xis_dominio * (dados_viga.d / 100)

        momento_lim_viga = (
            0.68
            * (dados_viga.bw / 100)
            * (dados_viga.fcd * 1000)
            * x_lim_viga
            * ((dados_viga.d / 100) - 0.4 * x_lim_viga)
        )        

        if d_min_viga < (dados_viga.h / 100):
            print(
                "[NOTICE] A altura atual da viga é maior que a altura útil mínima, calcule como simplesmente armada."
            )
            raise ValueError(
                "A altura atual da viga é maior que a altura útil mínima, calcule como simplesmente armada."
            )

        else:
            momento_lim_viga = (
                0.68
                * (dados_viga.bw / 100)
                * (dados_viga.fcd * 1000)
                * x_lim_viga
                * ((dados_viga.d / 100) - 0.4 * x_lim_viga)
            )
            momento_2_viga = (dados_viga.mk * 1.4) - momento_lim_viga

            as_compressao_viga = (momento_2_viga * 1000) / (
                ((dados_viga.d / 100) - (d_linha / 100)) * (dados_viga.fyd)
            )

            as_tracao_viga = (momento_lim_viga * 1000) / (
                (1 - 0.4 * xis_dominio) * (dados_viga.d / 100) * dados_viga.fyd
            )

            as_tracao_viga = as_tracao_viga + as_compressao_viga

            as_total_viga = as_tracao_viga + as_compressao_viga

            as_sobre_apoio_viga = as_tracao_viga / 3

            area_secao_viga = dados_viga.bw * dados_viga.h
            if dados_viga.h >= 60:
                as_pele = (0.1 / 100) * area_secao_viga * 100
            else:
                as_pele = 0

            # TODO Código repetido refatorar
            taxa_aco_por_fck = {
                20: 0.0015,
                25: 0.0015,
                30: 0.00173,
                35: 0.00201,
                40: 0.00203,
                45: 0.00259,
                50: 0.00288,
            }
            taxa_aco_viga_retangular = taxa_aco_por_fck.get(dados_viga.fck)

            if taxa_aco_viga_retangular is None:
                raise ValueError(f"fck inválido: {dados_viga.fck}")

            as_max_viga = (4 / 100) * area_secao_viga * 100
            as_min_viga = taxa_aco_viga_retangular * area_secao_viga * 100


            print(f"[NOTICE] Altura útil mínima para evitar armadura dupla d_min: {d_min_viga:.2f} m")
            print(f"[NOTICE] Posição limite da linha neutra para domínio 3 x_lim: {x_lim_viga:.2f} m")
            print(f"[NOTICE] Momento resistente último para armadura simples Mlim: {momento_lim_viga:.2f} kN.m")
            print(f"[NOTICE] Momento excedente para armadura dupla Momento2: {momento_2_viga:.2f} kN.m")
            print(f"[NOTICE] Área de aço de compressão As Compressão: {as_compressao_viga:.2f} mm²")
            print(f"[NOTICE] Área de aço de tração As Tração: {as_tracao_viga:.2f} mm²")

        resultados_viga = CalculadoraViga.calcular_viga_cortante(dados_viga)

        resultados_viga.update(
            {
                "d_min_viga": d_min_viga,
                "x_lim_viga": x_lim_viga,
                "momento_lim_viga": momento_lim_viga,
                "momento_2_viga": momento_2_viga,
                "as_compressao_viga": as_compressao_viga,
                "as_tracao_viga": as_tracao_viga,
                "as_sobre_apoio_viga": as_sobre_apoio_viga,
                "as_max_viga": as_max_viga,
                "as_min_viga": as_min_viga,
                "as_pele": as_pele,
                "as_total_viga":as_total_viga,
                "d_linha": d_linha,
            }
        )

        return resultados_viga
