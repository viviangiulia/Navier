import sys
import os
import math

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QStatusBar,
    QToolBar,
    QLineEdit,
    QComboBox,
    QSpinBox,
)
from PyQt6.QtGui import QPixmap, QIcon, QImage
from PyQt6 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
from calculos.vigas import DadosViga, CalculadoraViga

# import marcus

tabela_marcus = "tabela_marcus.pdf"
abaco_normal = "abaco_normal.pdf"
abaco_obliqua = "abaco_obliqua.pdf"


class Inicio(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Navier - Início")
        self.ui = None
        self.load_ui()
        self.load_signals()

    def load_ui(self):
        self.ui = loadUi("inicio_alt.ui", self)
        self.label.setStyleSheet("Background-Color: #ddebff;")

        self.pushButton.setIcon(QtGui.QIcon("images/btn_inicio_vigas.png"))
        self.pushButton.setIconSize(QtCore.QSize(52, 52))
        self.pushButton_3.setIcon(QtGui.QIcon("images/btn_inicio_pilares.png"))
        self.pushButton_3.setIconSize(QtCore.QSize(42, 42))
        self.pushButton_9.setIcon(QtGui.QIcon("images/btn_inicio_lajes.png"))
        self.pushButton_9.setIconSize(QtCore.QSize(42, 42))
        self.pushButton_11.setIcon(QtGui.QIcon("images/btn_inicio_fundacoes.png"))
        self.pushButton_11.setIconSize(QtCore.QSize(45, 45))

        self.label_5.setStyleSheet("Background-Color: #ddebff;")
        self.label_10.setStyleSheet("Background-Color: #ddebff;")
        self.label_9.setStyleSheet("Background-Color: #ddebff;")
        self.label_11.setStyleSheet("Background-Color: #ddebff;")

        self.pushButton_2.setIcon(QtGui.QIcon("images/btn_caa.png"))
        self.pushButton_2.setIconSize(QtCore.QSize(45, 45))
        self.pushButton_5.setIcon(QtGui.QIcon("images/btn_cadicional.png"))
        self.pushButton_5.setIconSize(QtCore.QSize(45, 45))
        self.pushButton_6.setIcon(QtGui.QIcon("images/btn_tabbitolas.png"))
        self.pushButton_6.setIconSize(QtCore.QSize(45, 45))
        self.pushButton_7.setIcon(QtGui.QIcon("images/btn_tabmarcus.png"))
        self.pushButton_7.setIconSize(QtCore.QSize(45, 45))
        self.pushButton_8.setIcon(QtGui.QIcon("images/btn_flexaosimples.png"))
        self.pushButton_8.setIconSize(QtCore.QSize(45, 45))
        self.pushButton_23.setIcon(QtGui.QIcon("images/btn_flexaocomposta.png"))
        self.pushButton_23.setIconSize(QtCore.QSize(45, 45))

        self.label_21.setToolTip(
            "Brunel - programa de cálculo e verificação de perfis metálicos para perfis brasileiros"
        )
        self.label_22.setToolTip(
            "EngTool - aplicação mobile para cálculo de vigas de concreto armado"
        )

        self.setFixedSize(570, 450)

        self.setWindowIcon(QtGui.QIcon("images/logo.ico"))

        self.show()

    def load_signals(self):
        self.pushButton.clicked.connect(self.iniciar_vigas)
        self.pushButton_3.clicked.connect(self.iniciar_pilares)
        self.pushButton_9.clicked.connect(self.iniciar_lajes)
        self.pushButton_11.clicked.connect(self.iniciar_fundacoes)

        self.pushButton_2.clicked.connect(self.iniciar_classe_agressividade)
        self.pushButton_5.clicked.connect(self.iniciar_carga_adicional)
        self.pushButton_6.clicked.connect(self.iniciar_tabela_bitolas)

        self.pushButton_7.clicked.connect(
            lambda: self.abrirTabelaAuxiliar(tabela_marcus)
        )
        self.pushButton_23.clicked.connect(
            lambda: self.abrirTabelaAuxiliar(abaco_normal)
        )
        self.pushButton_8.clicked.connect(
            lambda: self.abrirTabelaAuxiliar(abaco_obliqua)
        )

    def abrirTabelaAuxiliar(self, file):
        os.startfile(file)

    def iniciar_vigas(self) -> None:
        """Exibe a janela de dimensiomaneto de vigas."""
        print("[INFO] Janela de Dimensionamento de Vigas carregada corretamente!")
        vigas.show()

    def iniciar_pilares(self):
        print("pilares")
        pilares.show()

    def iniciar_lajes(self):
        print("lajes")
        lajes.show()

    def iniciar_fundacoes(self):
        print("fundações")
        sapatas.show()

    # --------------------------- forms complementares -----------------------------
    def iniciar_carga_adicional(self):
        print("carga adicional")
        carga_adicional.show()

    def iniciar_tabela_bitolas(self):
        print("carga adicional")
        tabela_bitolas.show()

    def iniciar_classe_agressividade(self):
        print("classe de agressividade")
        tabela_classe_agressividade.show()


class Vigas(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi("vigas_alt.ui", self)
        self.load_signals()

        self.setWindowIcon(QtGui.QIcon("images/logo.ico"))

        self.setWindowTitle("Navier - Vigas")
        self.setFixedSize(860, 620)

    def load_signals(self):
        self.btn_viga_armacao_simples.clicked.connect(
            lambda: self.stacked_viga_modelo_armacao.setCurrentIndex(1)
        )
        self.btn_viga_armacao_dupla.clicked.connect(
            lambda: self.stacked_viga_modelo_armacao.setCurrentIndex(0)
        )
        self.btn_viga_gerar_detalhamento.clicked.connect(lambda: detalhar_vigas.show())

        self.btn_viga_calcular.clicked.connect(self.calcular_viga_index)
        self.btn_viga_limpar.clicked.connect(self.limpar_preenchimento_janela_vigas)

        self.radio_viga_dominio_2.clicked.connect(
            lambda: self.ledit_viga_linha_neutra.setText("0.450")
        )
        self.radio_viga_dominio_3.clicked.connect(
            lambda: self.ledit_viga_linha_neutra.setText("0.628")
        )

    def calcular_viga_index(self) -> None:
        """Define o tipo de cálculo a ser realizado para dimensionamento da viga.
        Viga simplesmente ou duplamente armada.
        """
        indice = self.stacked_viga_modelo_armacao.currentIndex()

        if indice == 1:
            print("[INFO] Calculando Viga Simplesmente armada.")
            try:
                dados_viga = self._coletar_dados_interface(tipo_armacao_viga="Simples")
                calculos_viga = CalculadoraViga()
                dicionario_resultados = calculos_viga.calcular_viga_simples(dados_viga)
                self._atualizar_dados_interface(
                    dicionario_resultados, tipo_armacao_viga="Simples"
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    str(e) or "Dados inconsistentes — verifique os campos.",
                )
                return
        else:
            print("[INFO] Calculando Viga Duplamente armada.")
            try:
                dados_viga = self._coletar_dados_interface(tipo_armacao_viga="Dupla")
                calculos_viga = CalculadoraViga()
                dicionario_resultados = calculos_viga.calcular_viga_dupla(dados_viga)
                self._atualizar_dados_interface(
                    dicionario_resultados, tipo_armacao_viga="Dupla"
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    str(e) or "Dados inconsistentes — verifique os campos.",
                )
                return    

    def limpar_preenchimento_janela_vigas(self) -> None:
        """Retorna todos os widgets da janela para seus valores default."""

        for widget in self.findChildren(QLineEdit):
            widget.clear()

        for widget in self.findChildren(QComboBox):
            widget.setCurrentIndex(0)

        for spin in self.findChildren(QSpinBox):
            if spin.objectName() == "spin_viga_angulo_theta":
                spin.setValue(30)

        self.radio_viga_dominio_3.setChecked(False)
        self.radio_viga_dominio_2.setChecked(True)
        self.radio_viga_modelo_calculo_1.setChecked(True)
        self.radio_viga_modelo_calculo_2.setChecked(False)

    def _verificar_modelo_calculo_viga(self) -> str:
        """Retorna o modelo de cálculo que será utilizado para verificação ao cisalhamento no ELU.

        Modelo I: Diagonais de compressão inclinadas a 45° em relação ao eixo longitudinal do elemento estrutural e
        parcela complementar Vc de valor constante, independente de VSd.

        Modelo II: Diagonais de compressão inclinadas em relação ao eixo longitudinal da peça, variando livremente entre 30° e 45°. Admite ainda
        que a parcela complementar Vc sofra redução com o aumento de VSd.

        """
        if self.radio_viga_modelo_calculo_2.isChecked():
            modelo_calculo = "Modelo II"
        else:
            modelo_calculo = "Modelo I"
        return modelo_calculo

    def _coletar_dados_interface(self, tipo_armacao_viga: str) -> DadosViga:
        """Coleta e converte dados da interface para DTO para serem utilizados no dimensionamento das vigas."""

        modelo_calculo = self._verificar_modelo_calculo_viga()

        if modelo_calculo == "Modelo I":
            theta_transversal = 45
        else:
            theta_transversal = self.spin_viga_angulo_theta.value()

        if tipo_armacao_viga == "Simples":

            dados_calculo_viga = DadosViga(
                mk=float(self.ledit_viga_momento_fletor.text()),
                vk=float(self.ledit_viga_cortante.text()),
                bw=float(self.ledit_viga_armacao_simples_largura.text()),
                h=float(self.ledit_viga_armacao_simples_altura.text()),
                d=float(self.ledit_viga_armacao_simples_altura_util.text()),
                fck=float(self.combo_viga_concreto_fck.currentText()),
                fyk=float(self.combo_viga_aco_classe.currentText()),
                fcd=float(self.combo_viga_concreto_fck.currentText()) / 1.4,
                fyd=float(self.combo_viga_aco_classe.currentText()) / 1.15,
                vsd=float(self.ledit_viga_cortante.text()) * 1.4,
                theta_transversal=(theta_transversal / 180) * math.pi,
                modelo_calculo=modelo_calculo,
            )

            validacao, mensagem = dados_calculo_viga.validar_dados()
            if not validacao:
                raise ValueError(mensagem)

            return dados_calculo_viga

        else:
            dados_calculo_viga = DadosViga(
                mk=float(self.ledit_viga_momento_fletor.text()),
                vk=float(self.ledit_viga_cortante.text()),
                bw=float(self.ledit_viga_armacao_dupla_lagura.text()),
                h=float(self.ledit_viga_armacao_dupla_altura.text()),
                d=float(self.ledit_viga_armacao_dupla_altura_util.text()),
                fck=float(self.combo_viga_concreto_fck.currentText()),
                fyk=float(self.combo_viga_aco_classe.currentText()),
                fcd=float(self.combo_viga_concreto_fck.currentText()) / 1.4,
                fyd=float(self.combo_viga_aco_classe.currentText()) / 1.15,
                vsd=float(self.ledit_viga_cortante.text()) * 1.4,
                theta_transversal=(theta_transversal / 180) * math.pi,
                modelo_calculo=modelo_calculo,
                xis_dominio=float(self.ledit_viga_linha_neutra.text()),
            )
        
            validacao, mensagem = dados_calculo_viga.validar_dados()
            if not validacao:
                raise ValueError(mensagem)

            return dados_calculo_viga

    def _atualizar_dados_interface(
        self, resultados_viga: dict, tipo_armacao_viga: str
    ) -> None:
        """Atualiza a interface com os resultados do cálculo do dimensionamento da viga."""

        dados_viga = self._coletar_dados_interface(tipo_armacao_viga)

        self.ledit_viga_vsd.setText(
            str(round(resultados_viga["vk_viga"] * 1.4, ndigits=4))
        )
        self.ledit_viga_vrd2.setText(str(round(resultados_viga["vrd2"], ndigits=4)))
        self.ledit_viga_vc.setText(str(round(resultados_viga["vc_0"], ndigits=4)))
        self.ledit_viga_vsw.setText(str(round(resultados_viga["vsw"], ndigits=4)))
        self.ledit_viga_as_s.setText(
            str(round(resultados_viga["as_transversal"], ndigits=4))
        )
        self.ledit_viga_as_min_s.setText(
            str(round(resultados_viga["as_min_transversal"], ndigits=4))
        )

        if tipo_armacao_viga == "Simples":

            self.ledit_viga_armacao_simples_md.setText(
                str(round(dados_viga.mk * 1.4, ndigits=4))
            )
            self.ledit_viga_armacao_simples_kmd.setText(
                str(round(resultados_viga["kmd_viga"], 4))
            )
            self.ledit_viga_armacao_simples_kx.setText(
                str(round(resultados_viga["kx_viga"], 4))
            )
            self.ledit_viga_armacao_simples_kz.setText(
                str(round(resultados_viga["kz_viga"], 4))
            )

            self.ledit_viga_armacao_simples_as.setText(
                str(round(resultados_viga["as_viga"], ndigits=4))
            )
            self.ledit_viga_armacao_simples_area_sobre_apoio.setText(
                str(round(resultados_viga["as_sobre_apoio_viga"], ndigits=4))
            )
            self.ledit_viga_armacao_simples_as_pele.setText(
                str(round(resultados_viga["as_pele"], ndigits=4))
            )
            self.ledit_viga_armacao_simples_as_max.setText(
                str(round(resultados_viga["as_max_viga"], ndigits=4))
            )
            self.ledit_viga_armacao_simples_as_min.setText(
                str(round(resultados_viga["as_min_viga"], ndigits=4))
            )

            self.ledit_viga_armacao_simples_dominio_ruptura.setText(
                resultados_viga["dominio_viga"]
            )

            self.ledit_viga_armacao_simples_d_linha.setText(
                str(round(resultados_viga["d_linha"], ndigits=2))
            )

            if (resultados_viga["dominio_viga"] == "Domínio 4a") or (
                resultados_viga["dominio_viga"] == "Domínio 4b"
            ):
                QMessageBox.about(
                    self,
                    "Atenção",
                    "Domínio de Cálculo 4: recomenda-se utilizar, em seção retangular, armadura dupla ou seção tê para contenção dos esforços de compressão do concreto.",
                )

            if resultados_viga["as_viga"] > resultados_viga["as_max_viga"]:
                QMessageBox.about(
                    self,
                    "Atenção",
                    "Área Total calculada superior a Área Máxima especificada para a seção da viga.",
                )
            if resultados_viga["as_viga"] < resultados_viga["as_min_viga"]:
                QMessageBox.about(
                    self,
                    "Atenção",
                    "Área Total calculada inferior a Área Mínima especificada para a seção da viga.",
                )

        else:

            self.ledit_viga_d_limite.setText(
                str(round(resultados_viga["d_min_viga"], ndigits=5))
            )
            self.ledit_viga_x_limite.setText(
                str(round(resultados_viga["x_lim_viga"], ndigits=5))
            )
            self.ledit_viga_momento_limite.setText(
                str(round(resultados_viga["momento_lim_viga"], ndigits=5))
            )
            self.ledit_viga_momento_2.setText(
                str(round(resultados_viga["momento_2_viga"], ndigits=5))
            )

            self.ledit_viga_as_compressao.setText(
                str(round(resultados_viga["as_compressao_viga"], ndigits=5))
            )
            self.ledit_viga_as_tracao.setText(
                str(round(resultados_viga["as_tracao_viga"], ndigits=5))
            )
            self.ledit_viga_area_sobre_apoio.setText(
                str(round(resultados_viga["as_sobre_apoio_viga"], ndigits=5))
            )
            self.ledit_viga_as_pele.setText(
                str(round(resultados_viga["as_pele"], ndigits=5))
            )
            self.ledit_viga_as_total.setText(
                str(round(resultados_viga["as_total_viga"], ndigits=2))
            )
            self.ledit_viga_as_max.setText(
                str(round(resultados_viga["as_max_viga"], ndigits=2))
            )
            self.ledit_viga_as_min.setText(
                str(round(resultados_viga["as_min_viga"], ndigits=2))
            )

            self.ledit_viga_armacao_dupla_d_linha.setText(
                str(round(resultados_viga["d_linha"], ndigits=2))
            )

            if resultados_viga["as_total_viga"] > resultados_viga["as_max_viga"]:
                QMessageBox.about(
                    self,
                    "Atenção",
                    "Área Total calculada superior a Área Máxima especificada para a seção da viga.",
                )
            if resultados_viga["as_total_viga"] < resultados_viga["as_min_viga"]:
                QMessageBox.about(
                    self,
                    "Atenção",
                    "Área Total calculada inferior a Área Mínima especificada para a seção da viga.",
                )


tabela_bitolas_ferro = [
    [6.3, 31.17],
    [8, 50.26],
    [10, 78.53],
    [12.5, 122.71],
    [16, 201.06],
    [20, 314.15],
    [25, 490.87],
    [32, 804.24],
    [40, 1256.63],
]


class Detalhar_viga(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.load_signals()

    def load_ui(self):
        self.ui = loadUi("detalhamento_vigas_alt.ui", self)

        # scriptDir = os.path.dirname(os.path.realpath(__file__))
        # self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo.ico'))
        self.setWindowIcon(QtGui.QIcon("images/logo.ico"))

        self.setWindowTitle("Navier - Vigas - Detalhamento")
        self.setFixedSize(845, 600)

    def load_signals(self):
        print("inicializado")
        self.pushButton.clicked.connect(self.calcular_area)
        # self.pushButton.clicked.connect(self.calcular_estribos)
        self.pushButton_2.clicked.connect(self.limpar_detalhamento)
        self.pushButton_3.clicked.connect(self.recuperarValores)

        # pg.plot(x=[0,1,2,3,4], y=[0,1,2,3,4]**2 )
        header = self.tableWidget.horizontalHeader()
        # FIXME Verificar a propriedade atualizada caso necessário
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

        self.widget.setTitle("nº barras/Bitola")
        self.widget.showGrid(x=True, y=True, alpha=1)

        # if '0' not in info_viga:
        # 	self.recuperarValores()

    def calcular_estribos(self):
        vsw = self.lineEdit_14.text()
        fyk_estribo = self.comboBox_2.currentText()
        tramos = self.lineEdit_15.text()

        if vsw != "0" and tramos != "0":
            vsw = float(self.lineEdit_14.text())
            bitola_estribo = float(self.comboBox.currentText())
            fyk_estribo = float(self.comboBox_2.currentText())
            tramos = float(self.lineEdit_15.text())
            d = float(self.lineEdit_13.text())

            espass_horizontal = info_viga_cortante[1]

            area_bitola = 3.14 * ((bitola_estribo / 1000) ** 2) / 4

            print(vsw)
            print(bitola_estribo)
            print(tramos)
            print(fyk_estribo)
            print(area_bitola)

            s_estribo = (
                (tramos * area_bitola * 0.9 * (d / 100) * (fyk_estribo * 100000 / 1.15))
                / vsw
                * 1000
            ) / 100
            s_estribo = round(s_estribo, ndigits=3)

            if s_estribo < espass_horizontal:
                self.lineEdit.setText(str(espass_horizontal))
            else:
                self.lineEdit.setText(str(s_estribo))

        else:
            QMessageBox.about(
                self,
                "Falta de Dados",
                "Por favor insira dados consistentes para o cálculo dos Estribos!",
            )

    def recuperarValores(self):
        area_aco = info_viga[0]
        base = info_viga[1]
        altura = info_viga[2]
        d = info_viga[3]
        d_agreg = info_viga[4]

        vsw = info_viga_cortante[0]

        self.lineEdit_11.setText(area_aco)
        self.lineEdit_10.setText(base)
        self.lineEdit_9.setText(altura)
        self.lineEdit_12.setText(d_agreg)
        self.lineEdit_13.setText(d)
        self.lineEdit_14.setText(vsw)

    def calcular_area(self):
        area_aco = self.lineEdit_11.text()
        base = self.lineEdit_10.text()
        altura = self.lineEdit_9.text()
        d_agreg = self.lineEdit_12.text()
        d = self.lineEdit_13.text()

        if (
            area_aco != "0"
            and base != "0"
            and altura != "0"
            and d_agreg != "0"
            and d != "0"
        ):

            self.widget.clear()
            area_aco = float(self.lineEdit_11.text())
            base = float(self.lineEdit_10.text())
            altura = float(self.lineEdit_9.text())
            cobrimento = float(self.comboBox_3.currentText())
            bitola_estribo = float(self.comboBox.currentText())
            x = []
            y = []
            z = []
            cont = 0
            for i in tabela_bitolas_ferro:
                n_barras = float(area_aco / i[1])
                print("bitola: ", i[0], " - nº barras: ", n_barras)

                self.tableWidget.setItem(
                    cont, 2, QTableWidgetItem(str(round(n_barras, ndigits=2)))
                )
                self.tableWidget.setItem(
                    cont, 3, QTableWidgetItem(str(round(n_barras + 0.5) + 1))
                )

                x.append(i[0])
                y.append(round(n_barras + 0.5) + 1)

                bitola = x[cont]
                n_barras = round(n_barras + 0.5) + 1

                espass_horizontal = (
                    round(
                        base
                        - 2 * (cobrimento + bitola_estribo / 10)
                        - n_barras * (bitola / 10),
                        ndigits=2,
                    )
                ) / (n_barras - 1)

                z.append(round(espass_horizontal, ndigits=2))
                self.tableWidget.setItem(
                    cont, 4, QTableWidgetItem(str(espass_horizontal))
                )

                print("base:", base)
                print("cobrimento:", cobrimento)
                print("bitola_estribo:", bitola_estribo)
                print("n_barras:", n_barras)

                cont += 1

            # print(x)
            # print(y)
            # print(z)

            self.widget.plot(x=x, y=y, pen=(3))

            self.calcular_espacamentos()
            self.calcular_estribos()

        else:
            QMessageBox.about(
                self, "Falta de Dados", "Por favor insira dados consistentes!"
            )

    def calcular_espacamentos(self):
        bitola = float(self.comboBox_4.currentText())
        d_agreg = float(self.lineEdit_12.text())

        s_horizontal = max(2, (bitola / 10), 1.2 * d_agreg)
        s_vertical = max(2, (bitola / 10), 0.5 * d_agreg)

        # ------------------------------- saida de dados ----------------------------------
        self.lineEdit_7.setText(str(s_horizontal))
        self.lineEdit_8.setText(str(s_vertical))

    def limpar_detalhamento(self):
        self.widget.clear()
        self.lineEdit_11.setText(str("0"))
        self.lineEdit_9.setText(str("0"))
        self.lineEdit_10.setText(str("0"))
        self.lineEdit_7.setText(str("0"))
        self.lineEdit_8.setText(str("0"))


class Tabela_Bitolas(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi("bitolas_ferros.ui", self)

        # scriptDir = os.path.dirname(os.path.realpath(__file__))
        # self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo.ico'))
        self.setWindowIcon(QtGui.QIcon("images/logo.ico"))

        header = self.tableWidget.horizontalHeader()
        # FIXME Verificar a propriedade atualizada caso necessário
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        self.setWindowTitle("Navier - Tabela de Bitolas")
        self.setFixedSize(456, 372)


global pilares_info
pilares_info = [0, 0, 0, 0]

global pilares_info_aco
pilares_info_aco = [0, 0, 0, 0, 0, 0, 0]


class Pilares(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi("pilares_alt.ui", self)
        self.load_signals()

        # scriptDir = os.path.dirname(os.path.realpath(__file__))
        # self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo.ico'))
        self.setWindowIcon(QtGui.QIcon("images/logo.ico"))

        self.setWindowTitle("Navier - Pilares")
        self.setFixedSize(997, 670)

    def load_signals(self):
        print("pilares carregado")
        self.cont_x = 0
        self.cont_y = 0

        self.pushButton_6.clicked.connect(self.calcular_pilares)
        self.pushButton_7.clicked.connect(self.limpar_pilares)

        self.pushButton.clicked.connect(self.gerar_envoltoria)
        self.pushButton_3.clicked.connect(lambda: pilares_areas_aco.show())

    def calcular_pilares(self):
        x_pilar = self.lineEdit.text()
        y_pilar = self.lineEdit_2.text()
        altura_pilar = self.lineEdit_3.text()
        altura_lance = self.lineEdit_4.text()

        nk_pilar = self.lineEdit_5.text()
        momento_x_topo = self.lineEdit_6.text()
        momento_x_base = self.lineEdit_7.text()
        momento_y_topo = self.lineEdit_8.text()
        momento_y_base = self.lineEdit_9.text()

        if (
            x_pilar != "0"
            and y_pilar != "0"
            and altura_pilar != "0"
            and altura_lance != "0"
            and nk_pilar != "0"
        ):
            fck_pilar = float(self.comboBox_3.currentText())
            fcd_pilar = fck_pilar / 1.4
            fyk_pilar = float(self.comboBox_4.currentText())
            fyd_pilar = fyk_pilar / 1.15
            cobrimento_pilar = float(self.comboBox_5.currentText())

            x_pilar = float(self.lineEdit.text())
            y_pilar = float(self.lineEdit_2.text())
            altura_pilar = float(self.lineEdit_3.text())
            altura_lance = float(self.lineEdit_4.text())

            nk_pilar = float(self.lineEdit_5.text())
            momento_x_topo = float(self.lineEdit_6.text())
            momento_x_base = float(self.lineEdit_7.text())
            momento_y_topo = float(self.lineEdit_8.text())
            momento_y_base = float(self.lineEdit_9.text())

            area_secao_pilar = (x_pilar / 100) * (y_pilar / 100)

            # nd_pilar = (nk_pilar + ((x_pilar/100)*(y_pilar/100)*altura_pilar*25)) * 1.4
            nd_pilar = (nk_pilar) * 1.4
            md_x_topo = 1.4 * momento_x_topo
            md_x_base = 1.4 * momento_x_base
            md_y_topo = 1.4 * momento_y_topo
            md_y_base = 1.4 * momento_y_base

            tipo_apoio_x = "AA"

            if (
                momento_x_topo == 0
                and momento_x_base == 0
                and momento_y_topo == 0
                and momento_y_base == 0
            ):
                self.tipo_pilar = "intermediario"
            elif momento_x_topo == 0 and momento_x_base == 0:
                self.tipo_pilar = "extremidade-x"
            elif momento_y_topo == 0 and momento_y_base == 0:
                self.tipo_pilar = "extremidade-y"
            else:
                self.tipo_pilar = "canto"

            self.lineEdit_13.setText(str(round(md_x_topo, ndigits=5)))
            self.lineEdit_14.setText(str(round(md_x_base, ndigits=5)))
            self.lineEdit_22.setText(str(round(md_y_topo, ndigits=5)))
            self.lineEdit_28.setText(str(round(md_y_base, ndigits=5)))

            # -Eixo-X----------------------------------------------------------------------
            b = y_pilar
            h = x_pilar

            m_a = max(md_x_topo, md_x_base)
            m_b = min(md_x_topo, md_x_base)

            if self.tipo_pilar == "intermediario" or self.tipo_pilar == "extremidade-x":
                alfa_b_x = 1.0
            else:
                alfa_b_x = 0.6 + 0.4 * (m_b / m_a)

            if alfa_b_x < 0.4:
                alfa_b_x = 0.4

            # excen_min_x = (1.5+0.03*h)
            momento_min_x = (nd_pilar * (1.5 + 0.03 * h)) / 100
            excen_min_x = momento_min_x / nd_pilar

            if md_x_topo < momento_min_x:
                md_x_topo = momento_min_x
                print("momento topo - mínimo")
                alfa_b_x = 1.0
            if md_x_base < momento_min_x:
                md_x_base = momento_min_x
                print("momento base - mínimo")
                alfa_b_x = 1.0

            compr_efetivo_x = (altura_pilar * 100) + h
            if altura_lance * 100 < compr_efetivo_x:
                compr_efetivo_x = altura_lance * 100

            excen_x_acidental = compr_efetivo_x / 400
            v_0 = (nd_pilar * 1000) / (area_secao_pilar * fcd_pilar * 1000000)

            excentricidade_relativa = (
                max(md_x_topo, md_x_base, momento_min_x) / nd_pilar
            ) / h

            lambda_pilar_x = 3.46 * (compr_efetivo_x / h)
            lambda_pilar_x_limite = (25 + 12.5 * (excentricidade_relativa)) / alfa_b_x
            if lambda_pilar_x_limite < 35:
                lambda_pilar_x_limite = 35

            excen_2_x = (compr_efetivo_x**2) / 10 * (0.005 / ((v_0 + 0.5) * h))

            md2_x = nd_pilar * (excen_2_x / 100)

            if lambda_pilar_x > lambda_pilar_x_limite:
                print("efeitos de 2 ordem considerados")
                excen_2 = (compr_efetivo_x**2) / 10 * (0.005 / ((v_0 + 0.5) * h))
                md2_x_relativo = nd_pilar * (excen_2 / 100)
            else:
                md2_x_relativo = 0
                print("efeitos de 2 ordem desconsiderados")

            msd_x_intermediario = (
                alfa_b_x * max(abs(md_x_topo), abs(md_x_base), abs(momento_min_x))
                + md2_x_relativo
            )
            # msd_x_intermediario = alfa_b_x * abs(momento_min_x) + md2_x_relativo

            mi_x = msd_x_intermediario / (h * area_secao_pilar * fcd_pilar) / 10
            delta_x = cobrimento_pilar / h

            # -Eixo-Y----------------------------------------------------------------------
            h = y_pilar
            b = x_pilar

            m_a = max(md_y_topo, md_y_base)
            m_b = min(md_y_topo, md_y_base)

            if self.tipo_pilar == "intermediario" or self.tipo_pilar == "extremidade-y":
                alfa_b_y = 1.0
            else:
                alfa_b_y = 0.6 + 0.4 * (m_b / m_a)

            if alfa_b_y < 0.4:
                alfa_b_y = 0.4

            momento_min_y = (nd_pilar * (1.5 + 0.03 * h)) / 100
            excen_min_y = momento_min_y / nd_pilar

            if md_y_topo < momento_min_y:
                md_y_topo = momento_min_y
                print("momento topo - mínimo")
                alfa_b_y = 1.0
            if md_y_base < momento_min_y:
                md_y_base = momento_min_y
                print("momento base - mínimo")
                alfa_b_y = 1.0

            compr_efetivo_y = (altura_pilar * 100) + h
            if altura_lance * 100 < compr_efetivo_y:
                compr_efetivo_y = altura_lance * 100

            excen_y_acidental = compr_efetivo_y / 400
            v_0 = (nd_pilar * 1000) / (area_secao_pilar * fcd_pilar * 1000000)

            excentricidade_relativa = (
                max(md_y_topo, md_y_base, momento_min_y) / nd_pilar
            ) / h

            lambda_pilar_y = 3.46 * (compr_efetivo_y / h)
            lambda_pilar_y_limite = (25 + 12.5 * (excentricidade_relativa)) / alfa_b_y
            if lambda_pilar_y_limite < 35:
                lambda_pilar_y_limite = 35

            excen_2_y = (compr_efetivo_y**2) / 10 * (0.005 / ((v_0 + 0.5) * h))

            md2_y = nd_pilar * (excen_2_y / 100)

            if lambda_pilar_y > lambda_pilar_y_limite:
                print("efeitos de 2 ordem considerados")
                excen_2 = (compr_efetivo_y**2) / 10 * (0.005 / ((v_0 + 0.5) * h))
                md2_y_relativo = nd_pilar * (excen_2 / 100)
            else:
                md2_y_relativo = 0
                print("efeitos de 2 ordem desconsiderados")

            msd_y_intermediario = (
                alfa_b_y * max(abs(md_y_topo), abs(md_y_base), abs(momento_min_y))
                + md2_y_relativo
            )
            # msd_y_intermediario = alfa_b_y * abs(momento_min_y) + md2_y_relativo

            mi_y = msd_y_intermediario / (h * area_secao_pilar * fcd_pilar) / 10
            delta_y = cobrimento_pilar / h

            # --------------------------------------------- saida de dados ---------------------------------------------
            self.lineEdit_10.setText(str(round(nd_pilar, ndigits=4)))
            self.lineEdit_11.setText(str(round(area_secao_pilar, ndigits=4)))
            self.lineEdit_12.setText(str(round(v_0, ndigits=4)))

            self.lineEdit_15.setText(str(round(momento_min_x, ndigits=5)))
            self.lineEdit_16.setText(str(round(excen_min_x * 100, ndigits=5)))
            self.lineEdit_17.setText(str(round(lambda_pilar_x, ndigits=5)))
            self.lineEdit_18.setText(str(round(lambda_pilar_x_limite, ndigits=5)))
            self.lineEdit_19.setText(str(round(excen_2_x, ndigits=5)))
            self.lineEdit_20.setText(str(round(md2_x, ndigits=5)))
            self.lineEdit_21.setText(str(round(msd_x_intermediario, ndigits=5)))

            self.lineEdit_24.setText(str(round(momento_min_y, ndigits=5)))
            self.lineEdit_25.setText(str(round(excen_min_y * 100, ndigits=5)))
            self.lineEdit_26.setText(str(round(lambda_pilar_y, ndigits=5)))
            self.lineEdit_23.setText(str(round(lambda_pilar_y_limite, ndigits=5)))
            self.lineEdit_30.setText(str(round(excen_2_y, ndigits=5)))
            self.lineEdit_29.setText(str(round(md2_y, ndigits=5)))
            self.lineEdit_27.setText(str(round(msd_y_intermediario, ndigits=5)))

            self.lineEdit_31.setText(str(round(mi_x, ndigits=2)))
            self.lineEdit_32.setText(str(round(mi_y, ndigits=2)))
            self.lineEdit_33.setText(str(round(delta_x, ndigits=2)))
            self.lineEdit_34.setText(str(round(delta_y, ndigits=2)))

            global pilares_info
            pilares_info = [
                msd_x_intermediario,
                msd_y_intermediario,
                momento_min_x,
                momento_min_y,
            ]

            if md2_x_relativo == 0:
                self.label_39.setText("não considera 2º ordem")
            else:
                self.label_39.setText("considera 2º ordem")

            if md2_y_relativo == 0:
                self.label_44.setText("não considera 2º ordem")
            else:
                self.label_44.setText("considera 2º ordem")

            if self.tipo_pilar == "intermediario":
                self.label.setText("PILAR INTERMEDIÁRIO")
            elif (self.tipo_pilar == "extremidade-x") or (
                self.tipo_pilar == "extremidade-y"
            ):
                self.label.setText("PILAR DE EXTREMIDADE")
            else:
                self.label.setText("PILAR DE CANTO")

            global pilares_info_aco
            pilares_info_aco = [
                mi_x,
                delta_x,
                mi_y,
                delta_y,
                fck_pilar,
                area_secao_pilar,
                nk_pilar,
            ]

        else:
            QMessageBox.about(
                self, "Falta de Dados", "Por favor insira dados consistentes!"
            )

    def gerar_envoltoria(self):
        msd_x_intermediario = pilares_info[0]
        msd_y_intermediario = pilares_info[1]
        momento_min_x = pilares_info[2]
        momento_min_y = pilares_info[3]

        x = []
        y = []
        for i in range(360):
            theta = i
            theta_conv = (theta * math.pi) / 180

            seno = math.sin(theta_conv)
            seno = momento_min_y * seno

            cosseno = math.cos(theta_conv)
            cosseno = momento_min_x * cosseno

            x.append(seno)
            y.append(cosseno)

        z = []
        w = []
        for j in range(360):
            theta = j
            theta_conv = (theta * math.pi) / 180

            seno = math.sin(theta_conv)
            seno = msd_y_intermediario * seno

            cosseno = math.cos(theta_conv)
            cosseno = msd_x_intermediario * cosseno

            z.append(seno)
            w.append(cosseno)

        # create plot
        """plt = pg.plot(x, y, title='theTitle', pen='r')
		plt.showGrid(x=True,y=True)
		"""
        # create plot
        plt = pg.plot()
        plt.clear()
        plt.showGrid(x=True, y=True)
        plt.addLegend()
        plt.setTitle("Envoltória de Momentos")

        # set properties
        plt.setLabel("left", "Momentos Y", units="KN.m")
        plt.setLabel("bottom", "Momentos X", units="KN.m")
        plt.setXRange(0, 10)
        plt.setYRange(0, 20)

        plt.enableAutoRange()
        plt.setWindowTitle("pyqtgraph plot")
        # plot
        c1 = plt.plot(x, y, pen="r", name="Envoltória Momentos min")
        c2 = plt.plot(z, w, pen="b", name="Envoltória Momentos máx")

    def limpar_pilares(self):
        print("limpar")
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)

        self.lineEdit.setText("0")
        self.lineEdit_2.setText("0")
        self.lineEdit_3.setText("0")
        self.lineEdit_4.setText("0")
        self.lineEdit_5.setText("0")
        self.lineEdit_6.setText("0")
        self.lineEdit_7.setText("0")
        self.lineEdit_8.setText("0")
        self.lineEdit_9.setText("0")

        self.lineEdit_10.setText("")
        self.lineEdit_11.setText("")
        self.lineEdit_12.setText("")
        self.lineEdit_13.setText("")
        self.lineEdit_14.setText("")
        self.lineEdit_15.setText("")
        self.lineEdit_16.setText("")
        self.lineEdit_17.setText("")
        self.lineEdit_18.setText("")
        self.lineEdit_19.setText("")
        self.lineEdit_20.setText("")
        self.lineEdit_21.setText("")
        self.lineEdit_22.setText("")
        self.lineEdit_23.setText("")
        self.lineEdit_24.setText("")
        self.lineEdit_25.setText("")
        self.lineEdit_26.setText("")
        self.lineEdit_27.setText("")
        self.lineEdit_28.setText("")
        self.lineEdit_29.setText("")
        self.lineEdit_30.setText("")

        self.lineEdit_31.setText("")
        self.lineEdit_32.setText("")
        self.lineEdit_33.setText("")
        self.lineEdit_34.setText("")


class Pilar_area_aco(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.load_signals()

    def load_ui(self):
        self.ui = loadUi("pilares_areas_aco.ui", self)

        # scriptDir = os.path.dirname(os.path.realpath(__file__))
        # self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo.ico'))
        self.setWindowIcon(QtGui.QIcon("images/logo.ico"))

        self.setWindowTitle("Navier - Pilares - Áreas de Aço")
        self.setFixedSize(484, 300)

        self.pushButton_4.setIcon(QtGui.QIcon("images/btn_flexaosimples.png"))
        self.pushButton_4.setIconSize(QtCore.QSize(50, 60))
        self.pushButton_5.setIcon(QtGui.QIcon("images/btn_flexaocomposta.png"))
        self.pushButton_5.setIconSize(QtCore.QSize(50, 60))

    def load_signals(self):
        print("inicializado")
        self.pushButton_2.clicked.connect(self.calcular_area_aco)
        self.pushButton.clicked.connect(self.recuperar_dados)
        self.pushButton_3.clicked.connect(self.limpar)
        self.pushButton_4.clicked.connect(
            lambda: self.abrirTabelaAuxiliar(abaco_normal)
        )
        self.pushButton_5.clicked.connect(
            lambda: self.abrirTabelaAuxiliar(abaco_obliqua)
        )

    def recuperar_dados(self):
        self.lineEdit_2.setText(str(round(pilares_info_aco[0], ndigits=2)))
        self.lineEdit_3.setText(str(round(pilares_info_aco[1], ndigits=2)))
        self.lineEdit_5.setText(str(round(pilares_info_aco[2], ndigits=2)))
        self.lineEdit_6.setText(str(round(pilares_info_aco[3], ndigits=2)))
        self.lineEdit_12.setText(str(round(pilares_info_aco[4], ndigits=2)))
        self.lineEdit_13.setText(str(round(pilares_info_aco[5], ndigits=2)))
        self.lineEdit_14.setText(str(round(pilares_info_aco[6], ndigits=2)))

    def calcular_area_aco(self):
        fck = float(self.lineEdit_12.text())
        fcd = fck / 1.4
        fyd = 500 / 1.15
        area_concreto = float(self.lineEdit_13.text())
        nk = float(self.lineEdit_14.text())
        nd = 1.4 * nk

        mi_x = float(self.lineEdit_2.text())
        delta_x = float(self.lineEdit_3.text())

        mi_y = float(self.lineEdit_5.text())
        delta_y = float(self.lineEdit_6.text())

        omega_x = float(self.lineEdit_4.text())
        omega_y = float(self.lineEdit_7.text())

        as_x = (omega_x * (area_concreto * 1000000) * fcd) / fyd
        as_y = (omega_y * (area_concreto * 1000000) * fcd) / fyd

        as_x = round(as_x, ndigits=3)
        as_y = round(as_y, ndigits=3)

        as_pilar_min = 0.15 * (nd / fyd)
        if as_pilar_min < (0.004 * area_concreto * 100000):
            as_pilar_min = round((0.004 * area_concreto * 100000), ndigits=3)

        as_pilar_max = round((0.08 * area_concreto * 1000000), ndigits=3)

        # -------------------------------------- saída de dados ----------------------------------------------------
        self.lineEdit_8.setText(str(as_x))
        self.lineEdit_9.setText(str(as_y))
        self.lineEdit_10.setText(str(as_pilar_max))
        self.lineEdit_11.setText(str(as_pilar_min))

    def teste(self):
        print("teste")

    def limpar(self):
        self.lineEdit_2.setText("0")
        self.lineEdit_3.setText("0")
        self.lineEdit_4.setText("1")
        self.lineEdit_5.setText("0")
        self.lineEdit_6.setText("0")
        self.lineEdit_7.setText("1")
        self.lineEdit_8.setText("0")
        self.lineEdit_9.setText("0")
        self.lineEdit_10.setText("0")
        self.lineEdit_11.setText("0")
        self.lineEdit_12.setText("0")
        self.lineEdit_13.setText("0")
        self.lineEdit_14.setText("0")

    def abrirTabelaAuxiliar(self, file):
        if sys.platform == "linux2":
            subprocess.call(["xdg-open", file])
        else:
            os.startfile(file)


class Lajes(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi("lajes_alt.ui", self)

        self.lado1 = "livre"
        self.lado2 = "livre"
        self.lado3 = "livre"
        self.lado4 = "livre"
        self.label_37.hide()
        self.label_38.hide()
        self.label_40.hide()
        self.label_41.hide()
        global caso
        caso = "1"
        global lx_lage
        lx_lage = "l_menor"
        self.lineEdit.setReadOnly(True)

        self.load_signals()

        # scriptDir = os.path.dirname(os.path.realpath(__file__))
        # self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo.ico'))
        self.setWindowIcon(QtGui.QIcon("images/logo.ico"))

        self.setWindowTitle("Navier - Lajes")
        self.setFixedSize(1245, 587)

    def load_signals(self):
        print("lajes iniciado")
        self.pushButton.clicked.connect(self.estado_l1)
        self.pushButton_2.clicked.connect(self.estado_l2)
        self.pushButton_3.clicked.connect(self.estado_l3)
        self.pushButton_4.clicked.connect(self.estado_l4)
        self.pushButton.clicked.connect(self.situacao_laje)
        self.pushButton_2.clicked.connect(self.situacao_laje)
        self.pushButton_3.clicked.connect(self.situacao_laje)
        self.pushButton_4.clicked.connect(self.situacao_laje)

        self.pushButton_5.clicked.connect(
            lambda: self.abrirTabelaAuxiliar(tabela_marcus)
        )
        self.pushButton_6.clicked.connect(self.calcular_laje)
        self.pushButton_7.clicked.connect(self.limpar_lajes)

        self.toolButton.clicked.connect(self.revelar_carg_acidental)

    def abrirTabelaAuxiliar(self, file):
        if sys.platform == "linux2":
            subprocess.call(["xdg-open", file])
        else:
            os.startfile(file)

    def teste(self):
        lado1 = float(self.lineEdit_3.text())
        lado2 = float(self.lineEdit_4.text())
        espes = float(self.lineEdit_5.text())

        pp = (espes * 25) / 100
        self.lineEdit.setText(str(pp))

    def revelar_carg_acidental(self):
        print("oi--")
        carga_adicional.show()

    def estado_l1(self):
        if self.lado1 == "livre":
            self.lado1 = "engastado"
            pixmap = QPixmap("images/engv.png")
            self.pushButton.setIcon(QIcon(pixmap))
        else:
            self.lado1 = "livre"
            pixmap = QPixmap("images/livv.png")
            self.pushButton.setIcon(QIcon(pixmap))

    def estado_l2(self):
        if self.lado2 == "livre":
            self.lado2 = "engastado"
            pixmap = QPixmap("images/engh.png")
            self.pushButton_2.setIcon(QIcon(pixmap))
        else:
            self.lado2 = "livre"
            pixmap = QPixmap("images/livh.png")
            self.pushButton_2.setIcon(QIcon(pixmap))

    def estado_l3(self):
        if self.lado3 == "livre":
            self.lado3 = "engastado"
            pixmap = QPixmap("images/engh.png")
            self.pushButton_3.setIcon(QIcon(pixmap))
        else:
            self.lado3 = "livre"
            pixmap = QPixmap("images/livh.png")
            self.pushButton_3.setIcon(QIcon(pixmap))

    def estado_l4(self):
        if self.lado4 == "livre":
            self.lado4 = "engastado"
            pixmap = QPixmap("images/engv.png")
            self.pushButton_4.setIcon(QIcon(pixmap))
        else:
            self.lado4 = "livre"
            pixmap = QPixmap("images/livv.png")
            self.pushButton_4.setIcon(QIcon(pixmap))

    def situacao_laje(self):
        l1 = self.lado1
        l2 = self.lado2
        l3 = self.lado3
        l4 = self.lado4

        cota_v1 = self.label_37
        cota_v2 = self.label_40
        cota_h1 = self.label_38
        cota_h2 = self.label_41

        if l1 == "livre" and l2 == "livre" and l3 == "livre" and l4 == "livre":
            global caso
            caso = "1"

            cota_v1.show()
            cota_v2.show()
            cota_h1.hide()
            cota_h2.hide()

            global lx_lage
            lx_lage = "l_menor"
        elif (
            l1 == "engastado" and l2 == "livre" and l3 == "livre" and l4 == "livre"
        ) or (l1 == "livre" and l2 == "livre" and l3 == "livre" and l4 == "engastado"):
            caso = "2"

            cota_v1.hide()
            cota_v2.hide()
            cota_h1.show()
            cota_h2.show()

            lx_lage = "l_maior"
        elif (
            l1 == "livre" and l2 == "engastado" and l3 == "livre" and l4 == "livre"
        ) or (l1 == "livre" and l2 == "livre" and l3 == "engastado" and l4 == "livre"):
            caso = "2"

            cota_v1.show()
            cota_v2.show()
            cota_h1.hide()
            cota_h2.hide()

            lx_lage = "l_menor"
        elif (
            (
                l1 == "engastado"
                and l2 == "engastado"
                and l3 == "livre"
                and l4 == "livre"
            )
            or (
                l1 == "engastado"
                and l2 == "livre"
                and l3 == "engastado"
                and l4 == "livre"
            )
            or (
                l1 == "livre"
                and l2 == "engastado"
                and l3 == "livre"
                and l4 == "engastado"
            )
            or (
                l1 == "livre"
                and l2 == "livre"
                and l3 == "engastado"
                and l4 == "engastado"
            )
        ):
            caso = "3"

            cota_v1.show()
            cota_v2.show()
            cota_h1.hide()
            cota_h2.hide()

            lx_lage = "l_menor"
        elif (
            l1 == "engastado" and l2 == "livre" and l3 == "livre" and l4 == "engastado"
        ):
            caso = "4"

            cota_v1.hide()
            cota_v2.hide()
            cota_h1.show()
            cota_h2.show()

            lx_lage = "l_maior"
        elif (
            l1 == "livre" and l2 == "engastado" and l3 == "engastado" and l4 == "livre"
        ):
            caso = "4"

            cota_v1.show()
            cota_v2.show()
            cota_h1.hide()
            cota_h2.hide()

            lx_lage = "l_menor"
        elif (
            l1 == "engastado"
            and l2 == "livre"
            and l3 == "engastado"
            and l4 == "engastado"
        ) or (
            l1 == "engastado"
            and l2 == "engastado"
            and l3 == "livre"
            and l4 == "engastado"
        ):
            caso = "5"

            cota_v1.hide()
            cota_v2.hide()
            cota_h1.show()
            cota_h2.show()

            lx_lage = "l_maior"
        elif (
            l1 == "livre"
            and l2 == "engastado"
            and l3 == "engastado"
            and l4 == "engastado"
        ) or (
            l1 == "engastado"
            and l2 == "engastado"
            and l3 == "engastado"
            and l4 == "livre"
        ):
            caso = "5"

            cota_v1.show()
            cota_v2.show()
            cota_h1.hide()
            cota_h2.hide()

            lx_lage = "l_menor"
        elif (
            l1 == "engastado"
            and l2 == "engastado"
            and l3 == "engastado"
            and l4 == "engastado"
        ):
            caso = "6"

            cota_v1.show()
            cota_v2.show()
            cota_h1.hide()
            cota_h2.hide()

            lx_lage = "l_menor"
        else:
            caso = "ainda não existe, não sei como você chegou até aqui srsrrsrsrsrsrs"

        print(caso)
        self.lineEdit_6.setText(str(caso))

    def calcular_laje(self):
        lado_maior = float(self.lineEdit_3.text())
        lado_menor = float(self.lineEdit_4.text())
        espes = float(self.lineEdit_5.text())
        d = float(self.lineEdit_27.text())

        self.lineEdit_7.setText("")
        self.lineEdit_9.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_10.setText("")
        self.lineEdit_16.setText("")
        self.lineEdit_14.setText("")
        self.lineEdit_15.setText("")
        self.lineEdit_16.setText("")

        if lado_maior != 0 and lado_menor != 0 and espes != 0 and d != 0:
            lado1 = float(self.lineEdit_3.text())
            lado2 = float(self.lineEdit_4.text())
            espes = float(self.lineEdit_5.text())
            d = float(self.lineEdit_27.text())
            carreg_adicional = float(self.lineEdit_2.text())
            # fck_laje = float(self.comboBox.currentText())
            # fcd_laje = fck_laje/1.4
            # fyk_laje = float(self.comboBox_2.currentText())
            # fyd_laje = fyk_laje/1.15

            pp = (espes * 25) / 100
            self.lineEdit.setText(str(pp))

            carreg_total = pp + carreg_adicional
            # print(caso)
            # print(lx_lage)
            # ---------------------------------- cálculo do Lx baseado no caso do tipo de situação da laje -----------------
            global lx
            global lambda_laje
            if lx_lage == "l_menor":
                lx = lado2
                lambda_laje = round((lado1 / lado2), ndigits=2)
            elif lx_lage == "l_maior":
                lx = lado1
                lambda_laje = round((lado2 / lado1), ndigits=2)
            print(lx_lage)

            # ---------------------------------- definição se a laje é unidirecional ou bidirecional baseado no lambda  -----------------
            global tipo_laje
            if float(lambda_laje) > 2.001:
                tipo_laje = "UNIDIRECIONAL"
                self.laje_unidirecional(carreg_total)
            else:
                tipo_laje = "BIDIRECIONAL"
                # self.label_43.setStyleSheet("Background: url('laje_unidirecional_modelo.png') no-repeat")

                mx = my = nx = ny = ""

                if caso == "1":
                    caso1 = marcus.caso1
                    linhas = len(caso1)
                    colunas = len(caso1[0])

                    for i in range(linhas):
                        aux = caso1[i][0]
                        if lambda_laje == aux:
                            print(caso1[i])
                            mx = caso1[i][2]
                            my = caso1[i][3]

                    print("mx: ", mx)
                    print("my: ", my)

                if caso == "2":
                    caso2 = marcus.caso2
                    linhas = len(caso2)
                    colunas = len(caso2[0])

                    for i in range(linhas):
                        aux = caso2[i][0]
                        if lambda_laje == aux:
                            print(caso2[i])
                            mx = caso2[i][2]
                            nx = caso2[i][3]
                            my = caso2[i][4]

                    print("mx: ", mx)
                    print("nx: ", nx)
                    print("my: ", my)

                if caso == "3":
                    caso3 = marcus.caso3
                    linhas = len(caso3)
                    colunas = len(caso3[0])

                    for i in range(linhas):
                        aux = caso3[i][0]
                        if lambda_laje == aux:
                            print(caso3[i])
                            mx = caso3[i][2]
                            nx = caso3[i][3]
                            my = caso3[i][4]
                            ny = caso3[i][5]

                    print("mx: ", mx)
                    print("nx: ", nx)
                    print("my: ", my)
                    print("ny: ", ny)

                if caso == "4":
                    caso4 = marcus.caso4
                    linhas = len(caso4)
                    colunas = len(caso4[0])

                    for i in range(linhas):
                        aux = caso4[i][0]
                        if lambda_laje == aux:
                            print(caso4[i])
                            mx = caso4[i][2]
                            nx = caso4[i][3]
                            my = caso4[i][4]

                    print("mx: ", mx)
                    print("nx: ", nx)
                    print("my: ", my)

                if caso == "5":
                    caso5 = marcus.caso5
                    linhas = len(caso5)
                    colunas = len(caso5[0])

                    for i in range(linhas):
                        aux = caso5[i][0]
                        if lambda_laje == aux:
                            print(caso5[i])
                            mx = caso5[i][2]
                            nx = caso5[i][3]
                            my = caso5[i][4]
                            ny = caso5[i][5]

                    print("mx: ", mx)
                    print("nx: ", nx)
                    print("my: ", my)
                    print("ny: ", ny)

                if caso == "6":
                    caso6 = marcus.caso6
                    linhas = len(caso6)
                    colunas = len(caso6[0])

                    for i in range(linhas):
                        aux = caso6[i][0]
                        if lambda_laje == aux:
                            print(caso6[i])
                            mx = caso6[i][2]
                            nx = caso6[i][3]
                            my = caso6[i][4]
                            ny = caso6[i][5]

                    print("mx: ", mx)
                    print("nx: ", nx)
                    print("my: ", my)
                    print("ny: ", ny)

                print(lx)
                if mx != "":
                    self.lineEdit_7.setText(str(mx))
                    momento_pos_x = (carreg_total * (lx**2)) / mx
                    momento_pos_x = round(momento_pos_x, ndigits=4)

                    self.lineEdit_13.setText(str(momento_pos_x))
                # else:
                # 	self.lineEdit_13.setText('0')
                if nx != "":
                    self.lineEdit_9.setText(str(nx))
                    momento_neg_x = round(((carreg_total * (lx**2)) / nx), ndigits=4)
                    self.lineEdit_14.setText(str(momento_neg_x))
                    # momento_neg_x = round(momento_neg_x,ndigits=2)
                # else:
                # 	self.lineEdit_14.setText('0')
                if my != "":
                    self.lineEdit_8.setText(str(my))
                    momento_pos_y = (carreg_total * (lx**2)) / my
                    momento_pos_y = round(momento_pos_y, ndigits=4)
                    self.lineEdit_15.setText(str(momento_pos_y))
                # else:
                # 	self.lineEdit_15.setText('0')
                if ny != "":
                    self.lineEdit_10.setText(str(ny))
                    momento_neg_y = round(((carreg_total * (lx**2)) / ny), ndigits=4)
                    self.lineEdit_16.setText(str(momento_neg_y))
                    # momento_neg_y = round(momento_neg_y,ndigits=2)

                # ----------------------------------- enviar resultados de saida ao programa ---------------------------------------
                self.lineEdit_11.setText(str(lambda_laje))
                self.label_16.setText(str(tipo_laje))
                self.lineEdit_12.setText(str(carreg_total))

                self.resultados_laje()
        else:
            QMessageBox.about(
                self, "Falta de Dados", "Por favor insira dados consistentes"
            )

    def laje_unidirecional(self, carreg_total):

        self.lado1 = "livre"
        pixmap = QPixmap("images/livv.png")
        self.pushButton.setIcon(QIcon(pixmap))

        self.lado4 = "livre"
        pixmap = QPixmap("images/livv.png")
        self.pushButton_4.setIcon(QIcon(pixmap))

        print("unidirecional")
        # l1 = self.lado1
        l2 = self.lado2
        l3 = self.lado3
        # l4 = self.lado4
        l1 = l4 = "livre"
        print(carreg_total)
        if l2 == "livre" and l3 == "livre":
            self.label_43.setStyleSheet(
                "Background: url('images/laje_unidirecional_ll2.png') no-repeat"
            )
            momento_pos_y = (carreg_total * (lx**2)) / 8
            momento_neg_y = 0
        elif l2 == "engastado" and l3 == "engastado":
            self.label_43.setStyleSheet(
                "Background: url('images/laje_unidirecional_ee2.png') no-repeat"
            )
            momento_pos_y = (carreg_total * (lx**2)) / 24
            momento_neg_y = (carreg_total * (lx**2)) / 12
        elif (l2 == "engastado" and l3 == "livre") or (
            l2 == "livre" and l3 == "engastado"
        ):
            self.label_43.setStyleSheet(
                "Background: url('images/laje_unidirecional_le2.png') no-repeat"
            )
            momento_pos_y = (carreg_total * (lx**2)) / 14.2
            momento_neg_y = (carreg_total * (lx**2)) / 8

        print("momento_pos_y: ", momento_pos_y)
        print("momento_neg_y: ", momento_neg_y)

        # ----------------------------------- enviar resultados de saida ao programa ---------------------------------------
        momento_pos_y = round(momento_pos_y, ndigits=4)
        self.lineEdit_15.setText(str(momento_pos_y))
        momento_neg_y = round(momento_neg_y, ndigits=4)
        self.lineEdit_16.setText(str(momento_neg_y))

        self.lineEdit_13.setText("0")
        self.lineEdit_14.setText("0")

        self.lineEdit_11.setText(str(lambda_laje))
        self.label_16.setText(str(tipo_laje))
        self.lineEdit_12.setText(str(carreg_total))

        self.resultados_laje()

    def truncar(self, x):
        aux = "{:.9f}".format(x)
        return aux

    def resultados_laje(self):
        fck_laje = float(self.comboBox.currentText())
        fcd_laje = fck_laje / 1.4
        fyk_laje = float(self.comboBox_2.currentText())
        fyd_laje = fyk_laje / 1.15
        espes = float(self.lineEdit_5.text())

        area_concreto_laje = round(((espes / 100) * 1000000), ndigits=4)

        ro_armad_minima = 0
        if fck_laje == 20:
            ro_armad_minima = 0.15 / 100
        elif fck_laje == 25:
            ro_armad_minima = 0.15 / 100
        elif fck_laje == 30:
            ro_armad_minima = 0.15 / 100
        elif fck_laje == 35:
            ro_armad_minima = 0.164 / 100
        elif fck_laje == 40:
            ro_armad_minima = 0.179 / 100

        armad_max_laje = (0.4 / 100) * area_concreto_laje
        armad_neg_min = ro_armad_minima * area_concreto_laje
        armad_pos_cruz = round(0.67 * (ro_armad_minima * area_concreto_laje), ndigits=2)
        armad_princ_unid = ro_armad_minima * area_concreto_laje
        armad_secnd_unid = max(
            (0.2 * armad_princ_unid),
            (90),
            (0.5 * (ro_armad_minima * area_concreto_laje)),
        )

        mx = self.lineEdit_13.text()
        if mx == "":
            self.lineEdit_13.setText("0")

        my = self.lineEdit_15.text()
        if my == "":
            self.lineEdit_15.setText("0")

        nx = self.lineEdit_14.text()
        if nx == "":
            self.lineEdit_14.setText("0")

        ny = self.lineEdit_16.text()
        if ny == "":
            self.lineEdit_16.setText("0")

        fck_laje = float(self.comboBox.currentText())
        fyk_laje = float(self.comboBox_2.currentText())
        fcd_laje = fck_laje * 1000000 / 1.4
        fyd_laje = fyk_laje * 1000000 / 1.15
        d_laje = float(self.lineEdit_27.text())
        espes = float(self.lineEdit_5.text())

        # ------------------------------------------enxerto-----------------------

        mx = float(self.lineEdit_13.text())
        my = float(self.lineEdit_15.text())
        nx = float(self.lineEdit_14.text())
        ny = float(self.lineEdit_16.text())
        # print('mx: ',mx)
        # print('nx: ',nx)
        # print('my: ',my)
        # print('ny: ',ny)
        mk_x = mx
        mk_y = my

        nk_x = nx
        nk_y = ny

        md_x = round(1.4 * mk_x, ndigits=4)
        kmd_x_laje = (md_x * 1000) / (1 * ((d_laje / 100) ** 2) * 0.85 * (fcd_laje))
        kx_x_laje = (1 - math.sqrt(1 - 2 * kmd_x_laje)) / 0.8
        kz_x_laje = 1 - 0.4 * kx_x_laje

        as_x_laje = (md_x * 1000 / (kz_x_laje * (d_laje / 100) * fyd_laje)) * 1000000

        print("md_x: ", md_x)
        print("kmd_x_laje: ", kmd_x_laje)
        print("kx_x_laje: ", kx_x_laje)
        print("kz_x_laje: ", kz_x_laje)
        print("as_x_laje: ", as_x_laje)

        md_y = round(1.4 * mk_y, ndigits=4)
        kmd_y_laje = (md_y * 1000) / (1 * ((d_laje / 100) ** 2) * 0.85 * (fcd_laje))
        kx_y_laje = (1 - math.sqrt(1 - 2 * kmd_y_laje)) / 0.8
        kz_y_laje = 1 - 0.4 * kx_y_laje

        as_y_laje = (md_y * 1000 / (kz_y_laje * (d_laje / 100) * fyd_laje)) * 1000000

        print("md_y: ", md_y)
        print("kmd_y_laje: ", kmd_y_laje)
        print("kx_y_laje: ", kx_y_laje)
        print("kz_y_laje: ", kz_y_laje)
        print("as_y_laje: ", as_y_laje)

        nd_x = round(1.4 * nk_x, ndigits=4)
        kmd_x_laje_n = (nd_x * 1000) / (1 * ((d_laje / 100) ** 2) * 0.85 * (fcd_laje))
        kx_x_laje_n = (1 - math.sqrt(1 - 2 * kmd_x_laje_n)) / 0.8
        kz_x_laje_n = 1 - 0.4 * kx_x_laje_n

        as_x_laje_n = (
            nd_x * 1000 / (kz_x_laje_n * (d_laje / 100) * fyd_laje)
        ) * 1000000

        nd_y = round(1.4 * nk_y, ndigits=4)
        kmd_y_laje_n = (nd_y * 1000) / (1 * ((d_laje / 100) ** 2) * 0.85 * (fcd_laje))
        kx_y_laje_n = (1 - math.sqrt(1 - 2 * kmd_y_laje_n)) / 0.8
        kz_y_laje_n = 1 - 0.4 * kx_y_laje_n

        as_y_laje_n = (
            nd_x * 1000 / (kz_y_laje_n * (d_laje / 100) * fyd_laje)
        ) * 1000000

        # ------------------------------------------ saida de dados ------------------------------------
        kmd_x_laje = self.truncar(kmd_x_laje)
        kx_x_laje = self.truncar(kx_x_laje)
        kz_x_laje = self.truncar(kz_x_laje)
        as_x_laje = self.truncar(as_x_laje)

        kmd_y_laje = self.truncar(kmd_y_laje)
        kx_y_laje = self.truncar(kx_y_laje)
        kz_y_laje = self.truncar(kz_y_laje)
        as_y_laje = self.truncar(as_y_laje)

        self.lineEdit_17.setText(str(md_x))
        self.lineEdit_18.setText(str(kmd_x_laje))
        self.lineEdit_19.setText(str(kx_x_laje))
        self.lineEdit_20.setText(str(kz_x_laje))
        self.lineEdit_21.setText(str(as_x_laje))

        self.lineEdit_22.setText(str(md_y))
        self.lineEdit_24.setText(str(kmd_y_laje))
        self.lineEdit_25.setText(str(kx_y_laje))
        self.lineEdit_26.setText(str(kz_y_laje))
        self.lineEdit_23.setText(str(as_y_laje))

        self.lineEdit_38.setText(str(area_concreto_laje))
        self.lineEdit_39.setText(str(ro_armad_minima * 100))
        self.lineEdit_42.setText(str(armad_max_laje))
        self.lineEdit_40.setText(str(armad_neg_min))
        self.lineEdit_41.setText(str(armad_pos_cruz))
        self.lineEdit_43.setText(str(armad_princ_unid))
        self.lineEdit_44.setText(str(armad_secnd_unid))

        if tipo_laje == "UNIDIRECIONAL":
            self.label_44.setText("Distribuição")
            if float(as_y_laje) < armad_princ_unid:
                self.label_45.setText("Mínima")
            else:
                self.label_45.setText("")

        if tipo_laje == "BIDIRECIONAL":
            if float(as_x_laje) < armad_pos_cruz:
                self.label_44.setText("Mínima")
            else:
                self.label_44.setText("")

            if float(as_y_laje) < armad_pos_cruz:
                self.label_45.setText("Mínima")
            else:
                self.label_45.setText("")

    def limpar_lajes(self):
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)

        self.lineEdit.setText("0")
        self.lineEdit_2.setText("0")
        self.lineEdit_3.setText("0")
        self.lineEdit_4.setText("0")
        self.lineEdit_5.setText("0")
        self.lineEdit_27.setText("0")

        self.lineEdit_7.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_9.setText("")
        self.lineEdit_10.setText("")

        self.lineEdit_11.setText("")
        self.lineEdit_12.setText("")
        self.lineEdit_38.setText("")
        self.lineEdit_39.setText("")
        self.lineEdit_42.setText("")
        self.lineEdit_40.setText("")
        self.lineEdit_41.setText("")
        self.lineEdit_43.setText("")
        self.lineEdit_44.setText("")

        self.lineEdit_13.setText("")
        self.lineEdit_14.setText("")
        self.lineEdit_15.setText("")
        self.lineEdit_16.setText("")

        self.lineEdit_16.setText("")
        self.lineEdit_17.setText("")
        self.lineEdit_18.setText("")
        self.lineEdit_19.setText("")
        self.lineEdit_20.setText("")
        self.lineEdit_21.setText("")
        self.lineEdit_22.setText("")
        self.lineEdit_23.setText("")
        self.lineEdit_24.setText("")
        self.lineEdit_25.setText("")
        self.lineEdit_26.setText("")


class Carga_Adicional(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = loadUi("lajes_carg_adicional_atualizada.ui", self)

        header = self.tableWidget.horizontalHeader()
        # FIXME Verificar a propriedade atualizada caso necessário
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.resizeRowsToContents()

        # scriptDir = os.path.dirname(os.path.realpath(__file__))
        # self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo.ico'))
        self.setWindowIcon(QtGui.QIcon("images/logo.ico"))

        self.setWindowTitle("Navier - Cargas Adicionais")
        self.setFixedSize(649, 504)


class Sapatas(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi("sapatas_alt.ui", self)
        self.load_signals()

        # scriptDir = os.path.dirname(os.path.realpath(__file__))
        # self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo.ico'))
        self.setWindowIcon(QtGui.QIcon("images/logo.ico"))

        self.setWindowTitle("Navier - Sapatas")
        self.setFixedSize(946, 574)

    def load_signals(self):
        print("sapatas carregado")
        self.pushButton_6.clicked.connect(self.calcular_sapata)
        self.pushButton_7.clicked.connect(self.limpar_sapatas)
        self.pushButton.clicked.connect(self.gerar_dim_sapata)

    def arredondar_cinco(self, numero):
        numero = round(numero, ndigits=2)
        numero = 100 * numero
        resto = numero % 5
        while resto != 0:
            numero += 1
            resto = numero % 5
            print("numero:", numero, " - resto: ", resto)

        numero = numero / 100
        return numero

    def calcular_sapata(self):

        nk = float(self.lineEdit_3.text())
        momento_x_sapata = float(self.lineEdit_4.text())
        momento_y_sapata = float(self.lineEdit_5.text())
        x_pilar = float(self.lineEdit.text())
        y_pilar = float(self.lineEdit_2.text())
        tensao_adm_solo = float(self.lineEdit_35.text())
        fator_solo = float(self.lineEdit_13.text())

        base_y_sapata = float(self.lineEdit_10.text())
        base_x_sapata = float(self.lineEdit_9.text())
        h_total = float(self.lineEdit_11.text())
        h_0 = float(self.lineEdit_12.text())

        y_sapata = float(self.lineEdit_9.text())
        x_sapata = float(self.lineEdit_10.text())
        h_total = float(self.lineEdit_11.text())
        h_0 = float(self.lineEdit_12.text())

        if (
            nk != 0
            and x_pilar != 0
            and y_pilar != 0
            and tensao_adm_solo != 0
            and fator_solo != 0
            and base_y_sapata != 0
            and base_x_sapata != 0
            and h_total != 0
            and h_0 != 0
        ):
            if x_sapata < 0.6 or y_sapata < 0.6:
                QMessageBox.about(
                    self,
                    "Erro de Entrada",
                    "As sapatas não podem apresentar lados menores de 60 cm, conforme a NBR 6122",
                )
            else:
                fck_sapata = float(self.comboBox.currentText())
                fcd_sapata = fck_sapata / 1.4
                fyk_sapata = float(self.comboBox_2.currentText())
                fyd_sapata = fyk_sapata / 1.15
                nk = float(self.lineEdit_3.text())
                momento_x_sapata = float(self.lineEdit_4.text())
                momento_y_sapata = float(self.lineEdit_5.text())
                tensao_adm_solo = float(self.lineEdit_35.text())
                fator_solo = float(self.lineEdit_13.text())
                angulo_dissp_sapata = float(self.spinBox.value())

                angulo_dissp_sapata = (angulo_dissp_sapata / 180) * 3.14

                x_pilar = float(self.lineEdit.text()) / 100
                y_pilar = float(self.lineEdit_2.text()) / 100

                y_sapata = float(self.lineEdit_9.text())
                x_sapata = float(self.lineEdit_10.text())
                h_total = float(self.lineEdit_11.text())
                h_0 = float(self.lineEdit_12.text())

                if (momento_x_sapata != 0 and momento_y_sapata == 0) or (
                    momento_x_sapata == 0 and momento_y_sapata != 0
                ):
                    fator_acrescimo_dimensoes = 1.05
                elif momento_x_sapata != 0 and momento_y_sapata != 0:
                    fator_acrescimo_dimensoes = 1.103
                else:
                    fator_acrescimo_dimensoes = 1.0

                x_sapata = round(x_sapata * fator_acrescimo_dimensoes, ndigits=4)
                y_sapata = round(y_sapata * fator_acrescimo_dimensoes, ndigits=4)

                wx = x_sapata * (y_sapata**2) / 6
                wy = y_sapata * (x_sapata**2) / 6

                mw_x = (momento_x_sapata / wx) * 1000
                mw_y = (momento_y_sapata / wy) * 1000

                tensao_sapata = (fator_solo * nk * 1000) / (x_sapata * y_sapata)
                tensao_max_sapata = tensao_sapata + mw_x + mw_y
                tensao_min_sapata = tensao_sapata - mw_x - mw_y

                nk_equiv = (x_sapata * y_sapata * tensao_max_sapata) / fator_solo
                area_sapata = round(
                    fator_solo * ((nk * 1000) / (tensao_adm_solo * 1000000)), ndigits=6
                )

                ca_sapata = (x_sapata - x_pilar) / 2
                cb_sapata = (y_sapata - y_pilar) / 2
                h_rig_x = 2 / 3 * ca_sapata
                h_rig_y = 2 / 3 * cb_sapata

                h_mincis = (1.4 * nk_equiv) / (
                    2
                    * (x_pilar + y_pilar)
                    * 0.27
                    * (1 - (fck_sapata / 250))
                    * (fcd_sapata * 1000000)
                )
                if h_mincis < 0.40:
                    h_mincis = 0.40
                if h_total < h_mincis:
                    h_total = h_mincis

                braco_alavanca_sapata = h_total - 0.05

                h0a = h_total - ca_sapata * math.tan(angulo_dissp_sapata)
                h0b = h_total - cb_sapata * math.tan(angulo_dissp_sapata)

                # h0 = round(h0a, ndigits=2)
                # if h0a < h0b:
                # 	h0 = round(h0b, ndigits=2)

                volume_concreto_sapata = (h_total - h_0) / (
                    3
                    * (
                        x_sapata * y_sapata
                        + x_pilar * y_pilar
                        + math.sqrt(x_sapata * y_sapata * x_pilar * y_pilar)
                    )
                    + x_sapata * y_sapata * h_0
                )

                tracao_x_sapata = (
                    1.1 * nk_equiv * (x_sapata - x_pilar) / (8 * braco_alavanca_sapata)
                )
                tracao_y_sapata = (
                    1.1 * nk_equiv * (y_sapata - y_pilar) / (8 * braco_alavanca_sapata)
                )
                as_x_sapata = (1.4 * tracao_x_sapata) / (fyd_sapata)
                as_y_sapata = (1.4 * tracao_y_sapata) / fyd_sapata

                taxa_aco_sapata = (0.078 * (fck_sapata) ** (2 / 3)) / fyd_sapata

                if taxa_aco_sapata <= 0.0015:
                    taxa_aco_sapata = 0.0015

                as_x_min_laje = 0.67 * taxa_aco_sapata * h_mincis * x_sapata
                as_y_min_laje = 0.67 * taxa_aco_sapata * h_mincis * y_sapata

                print("x_sapata: ", x_sapata)
                print("y_sapata: ", y_sapata)

                print("wx: ", wx)
                print("wy: ", wy)
                print("mw_x: ", mw_x)
                print("mw_y: ", mw_y)
                print("tensao_max_sapata: ", tensao_max_sapata)
                print("tensao_min_sapata: ", tensao_min_sapata)
                print("nk_equiv: ", nk_equiv)
                print("ca_sapata: ", ca_sapata)
                print("cb_sapata: ", cb_sapata)
                print("h0a: ", h0a)
                print("h0b: ", h0b)
                print("h_mincis: ", h_mincis)
                # print('h0: ',h0)
                print("h_total", h_total)
                print("-------------------------------------\n")

                # -------------------------------------- saida dos dados --------------------------------------------------
                self.lineEdit_11.setText(str(h_total))
                # self.lineEdit_12.setText(str(h0))

                self.lineEdit_15.setText(str(area_sapata))
                self.lineEdit_16.setText(str(round(wx, ndigits=6)))
                self.lineEdit_17.setText(str(round(wy, ndigits=6)))
                self.lineEdit_18.setText(str(round(nk_equiv, ndigits=4)))
                self.lineEdit_19.setText(
                    str(round(tensao_max_sapata / 1000000, ndigits=4))
                )
                self.lineEdit_20.setText(
                    str(round(tensao_min_sapata / 1000000, ndigits=4))
                )
                self.lineEdit_21.setText(str(round(ca_sapata * 100, ndigits=4)))
                self.lineEdit_22.setText(str(round(cb_sapata * 100, ndigits=4)))

                self.lineEdit_23.setText(str(round(h_rig_x * 100, ndigits=4)))
                self.lineEdit_24.setText(str(round(h_rig_y * 100, ndigits=4)))
                self.lineEdit_25.setText(str(round(h_mincis * 100, ndigits=4)))
                self.lineEdit_26.setText(str(round(h0a * 100, ndigits=4)))
                self.lineEdit_28.setText(str(round(h0b * 100, ndigits=4)))
                self.lineEdit_27.setText(str(round(volume_concreto_sapata, ndigits=4)))

                self.lineEdit_14.setText(str(round(tracao_x_sapata / 1000, ndigits=4)))
                self.lineEdit_29.setText(str(round(tracao_y_sapata / 1000, ndigits=4)))
                self.lineEdit_30.setText(str(round(as_x_sapata, ndigits=4)))
                self.lineEdit_31.setText(str(round(as_y_sapata, ndigits=4)))

                self.lineEdit_32.setText(str(round(taxa_aco_sapata, ndigits=7)))
                self.lineEdit_33.setText(str(round(as_x_min_laje * 1000000, ndigits=4)))
                self.lineEdit_34.setText(str(round(as_y_min_laje * 1000000, ndigits=4)))

        else:
            QMessageBox.about(
                self, "Falta de Dados", "Por favor insira dados consistentes"
            )

    def gerar_dim_sapata(self):

        nk = float(self.lineEdit_3.text())
        momento_x_sapata = float(self.lineEdit_4.text())
        momento_y_sapata = float(self.lineEdit_5.text())
        x_pilar = float(self.lineEdit.text())
        y_pilar = float(self.lineEdit_2.text())
        tensao_adm_solo = float(self.lineEdit_35.text())
        fator_solo = float(self.lineEdit_13.text())

        if (
            nk != 0
            and x_pilar != 0
            and y_pilar != 0
            and tensao_adm_solo != 0
            and fator_solo != 0
        ):

            fck_sapata = float(self.comboBox.currentText())
            fcd_sapata = fck_sapata / 1.4
            fyk_sapata = float(self.comboBox_2.currentText())
            fyd_sapata = fyk_sapata / 1.15
            nk = float(self.lineEdit_3.text())
            momento_x_sapata = float(self.lineEdit_4.text())
            momento_y_sapata = float(self.lineEdit_5.text())
            tensao_adm_solo = float(self.lineEdit_35.text())
            fator_solo = float(self.lineEdit_13.text())
            angulo_dissp_sapata = float(self.spinBox.value())

            angulo_dissp_sapata = (angulo_dissp_sapata / 180) * 3.14

            x_pilar = float(self.lineEdit.text()) / 100
            y_pilar = float(self.lineEdit_2.text()) / 100

            area_sapata = round(
                fator_solo * ((nk * 1000) / (tensao_adm_solo * 1000000)), ndigits=6
            )

            y_sapata = 0.5 * (y_pilar - x_pilar) + math.sqrt(
                0.25 * ((y_pilar - x_pilar) ** 2) + area_sapata
            )

            x_sapata = area_sapata / y_sapata

            if (momento_x_sapata != 0 and momento_y_sapata == 0) or (
                momento_x_sapata == 0 and momento_y_sapata != 0
            ):
                fator_acrescimo_dimensoes = 1.05
            elif momento_x_sapata != 0 and momento_y_sapata != 0:
                fator_acrescimo_dimensoes = 1.103
            else:
                fator_acrescimo_dimensoes = 1.0

            x_sapata = round(x_sapata * fator_acrescimo_dimensoes, ndigits=4)
            y_sapata = round(y_sapata * fator_acrescimo_dimensoes, ndigits=4)

            if x_sapata < 0.6:
                x_sapata = 0.6
            if y_sapata < 0.6:
                y_sapata = 0.6
            print(x_sapata, "<--------------------------------------------------")
            wx = x_sapata * (y_sapata**2) / 6
            wy = y_sapata * (x_sapata**2) / 6

            mw_x = (momento_x_sapata / wx) * 1000
            mw_y = (momento_y_sapata / wy) * 1000

            tensao_sapata = (fator_solo * nk * 1000) / (x_sapata * y_sapata)
            tensao_max_sapata = tensao_sapata + mw_x + mw_y
            tensao_min_sapata = tensao_sapata - mw_x - mw_y

            x_sapata = self.arredondar_cinco(x_sapata)
            y_sapata = self.arredondar_cinco(y_sapata)
            if x_sapata < 0.6:
                x_sapata = 0.6
            if y_sapata < 0.6:
                y_sapata = 0.6

            nk_equiv = (x_sapata * y_sapata * tensao_max_sapata) / fator_solo

            ca_sapata = (x_sapata - x_pilar) / 2
            cb_sapata = (y_sapata - y_pilar) / 2
            h_rig_x = 2 / 3 * ca_sapata
            h_rig_y = 2 / 3 * cb_sapata

            h_total = h_rig_x
            if h_total < h_rig_y:
                h_total = h_rig_y

            h_mincis = (1.4 * nk_equiv) / (
                2
                * (x_pilar + y_pilar)
                * 0.27
                * (1 - (fck_sapata / 250))
                * (fcd_sapata * 1000000)
            )
            if h_mincis < 0.40:
                h_mincis = 0.40
            h_mincis = round(h_mincis, ndigits=4)

            if h_total < h_mincis:
                h_total = h_mincis

            h_total = self.arredondar_cinco(h_total)

            h0a = h_total - ca_sapata * math.tan(angulo_dissp_sapata)
            h0b = h_total - cb_sapata * math.tan(angulo_dissp_sapata)
            h0_prerrogativo = h_total / 3
            tangente_angulo = math.tan(angulo_dissp_sapata)
            h0 = round(h0a, ndigits=2)
            if h0a < h0b:
                h0 = round(h0b, ndigits=2)
            elif h0b < h0_prerrogativo:
                h0 = h0_prerrogativo
            if h0 < 0.25:
                h0 = 0.25
            h0 = self.arredondar_cinco(h0)

            volume_concreto_sapata = (
                (h_total - h0)
                / 3
                * (
                    x_sapata * y_sapata
                    + x_pilar * y_pilar
                    + math.sqrt(x_sapata * y_sapata * x_pilar * y_pilar)
                )
            ) + (x_sapata * y_sapata * h0)

            braco_alavanca_sapata = h_total - 0.05

            tracao_x_sapata = (
                1.1 * nk_equiv * (x_sapata - x_pilar) / (8 * braco_alavanca_sapata)
            )
            tracao_y_sapata = (
                1.1 * nk_equiv * (y_sapata - y_pilar) / (8 * braco_alavanca_sapata)
            )
            as_x_sapata = (1.4 * tracao_x_sapata) / (fyd_sapata)
            as_y_sapata = (1.4 * tracao_y_sapata) / fyd_sapata

            taxa_aco_sapata = (0.078 * (fck_sapata) ** (2 / 3)) / fyd_sapata

            if taxa_aco_sapata <= 0.0015:
                taxa_aco_sapata = 0.0015

            as_x_min_laje = 0.67 * taxa_aco_sapata * h_total * x_sapata
            as_y_min_laje = 0.67 * taxa_aco_sapata * h_total * y_sapata

            print("x_sapata: ", x_sapata)
            print("y_sapata: ", y_sapata)

            print("wx: ", wx)
            print("wy: ", wy)
            print("mw_x: ", mw_x)
            print("mw_y: ", mw_y)
            print("tensao_max_sapata: ", tensao_max_sapata)
            print("tensao_min_sapata: ", tensao_min_sapata)
            print("nk_equiv: ", nk_equiv)
            print("ca_sapata: ", ca_sapata)
            print("cb_sapata: ", cb_sapata)
            print("h0a: ", h0a)
            print("h0b: ", h0b)
            print("h_mincis: ", h_mincis)
            print("h0: ", h0)
            print("tangente_angulo: ", tangente_angulo)
            print("----------")
            print("h_total: ", h_total)
            print("tracao_x_sapata: ", tracao_x_sapata)
            print("tracao_y_sapata: ", tracao_y_sapata)
            print("as_x_sapata: ", as_x_sapata)
            print("as_y_sapata: ", as_y_sapata)
            print("taxa_aco_sapata: ", taxa_aco_sapata)
            print("as_x_min_laje: ", as_x_min_laje)
            print("as_y_min_laje: ", as_y_min_laje)
            print("-------------------------------------\n")
            # ------------------------------ saida de dados ---------------------------------------------
            self.lineEdit_9.setText(str(y_sapata))
            self.lineEdit_10.setText(str(x_sapata))
            self.lineEdit_15.setText(str(area_sapata))

            self.lineEdit_11.setText(str(round(h_total, ndigits=4)))
            self.lineEdit_12.setText(str(round(h0, ndigits=4)))

            self.lineEdit_15.setText(str(area_sapata))
            self.lineEdit_16.setText(str(round(wx, ndigits=6)))
            self.lineEdit_17.setText(str(round(wy, ndigits=6)))
            self.lineEdit_18.setText(str(round(nk_equiv, ndigits=4)))
            self.lineEdit_19.setText(str(round(tensao_max_sapata / 1000000, ndigits=4)))
            self.lineEdit_20.setText(str(round(tensao_min_sapata / 1000000, ndigits=4)))
            self.lineEdit_21.setText(str(round(ca_sapata * 100, ndigits=4)))
            self.lineEdit_22.setText(str(round(cb_sapata * 100, ndigits=4)))

            self.lineEdit_23.setText(str(round(h_rig_x * 100, ndigits=4)))
            self.lineEdit_24.setText(str(round(h_rig_y * 100, ndigits=4)))
            self.lineEdit_25.setText(str(round(h_mincis * 100, ndigits=4)))
            self.lineEdit_26.setText(str(round(h0a * 100, ndigits=4)))
            self.lineEdit_28.setText(str(round(h0b * 100, ndigits=4)))
            self.lineEdit_27.setText(str(round(volume_concreto_sapata, ndigits=4)))

            self.lineEdit_14.setText(str(round(tracao_x_sapata / 1000, ndigits=4)))
            self.lineEdit_29.setText(str(round(tracao_y_sapata / 1000, ndigits=4)))
            self.lineEdit_30.setText(str(round(as_x_sapata, ndigits=4)))
            self.lineEdit_31.setText(str(round(as_y_sapata, ndigits=4)))

            self.lineEdit_32.setText(str(round(taxa_aco_sapata, ndigits=7)))
            self.lineEdit_33.setText(str(round(as_x_min_laje * 1000000, ndigits=4)))
            self.lineEdit_34.setText(str(round(as_y_min_laje * 1000000, ndigits=4)))

        else:
            QMessageBox.about(
                self, "Falta de Dados", "Por favor insira dados consistentes"
            )

    def limpar_sapatas(self):
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)

        self.lineEdit.setText("0")
        self.lineEdit_2.setText("0")
        self.lineEdit_3.setText("0")
        self.lineEdit_4.setText("0")
        self.lineEdit_5.setText("0")

        self.lineEdit_35.setText("0")
        self.lineEdit_13.setText("1.1")
        self.spinBox.setValue(30)

        self.lineEdit_9.setText("0")
        self.lineEdit_10.setText("0")
        self.lineEdit_11.setText("0")
        self.lineEdit_12.setText("0")

        self.lineEdit_15.setText("")
        self.lineEdit_16.setText("")
        self.lineEdit_17.setText("")
        self.lineEdit_18.setText("")
        self.lineEdit_19.setText("")
        self.lineEdit_20.setText("")
        self.lineEdit_21.setText("")
        self.lineEdit_22.setText("")
        self.lineEdit_23.setText("")
        self.lineEdit_24.setText("")
        self.lineEdit_25.setText("")
        self.lineEdit_26.setText("")
        self.lineEdit_27.setText("")
        self.lineEdit_28.setText("")

        self.lineEdit_14.setText("")
        self.lineEdit_29.setText("")
        self.lineEdit_30.setText("")
        self.lineEdit_31.setText("")
        self.lineEdit_32.setText("")
        self.lineEdit_33.setText("")
        self.lineEdit_34.setText("")


# ---------------------------------------------- Janelas Adicionais ----------------------------------------------------


class Tabela_Classe_Agressividade(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.load_signals()

    def load_ui(self):
        self.ui = loadUi("class_agres.ui", self)

        # scriptDir = os.path.dirname(os.path.realpath(__file__))
        # self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo.ico'))
        self.setWindowIcon(QtGui.QIcon("images/logo.ico"))

        self.setWindowTitle("Navier - Classes de Agressividade e Cobrimentos Mínimos")
        self.setFixedSize(579, 520)

    def load_signals(self):
        print("inicializado")
        header = self.tableWidget.horizontalHeader()
        # FIXME Verificar a propriedade atualizada caso necessário
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.tableWidget.setSpan(0, 0, 1, 4)

        header_2 = self.tableWidget_2.horizontalHeader()
        # FIXME Verificar a propriedade atualizada caso necessário
        # header_2.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header_2.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # header_2.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        # header_2.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        self.tableWidget_2.setSpan(0, 0, 2, 1)
        self.tableWidget_2.setSpan(0, 1, 2, 1)
        self.tableWidget_2.setSpan(0, 3, 2, 1)

        self.tableWidget_2.setSpan(3, 0, 2, 1)
        self.tableWidget_2.setSpan(3, 1, 2, 1)
        self.tableWidget_2.setSpan(3, 3, 2, 1)

        self.tableWidget_2.setSpan(5, 0, 2, 1)
        self.tableWidget_2.setSpan(5, 1, 2, 1)
        self.tableWidget_2.setSpan(5, 3, 2, 1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    inicio = Inicio()
    vigas = Vigas()
    detalhar_vigas = Detalhar_viga()
    pilares = Pilares()
    pilares_areas_aco = Pilar_area_aco()
    lajes = Lajes()
    sapatas = Sapatas()
    carga_adicional = Carga_Adicional()
    tabela_classe_agressividade = Tabela_Classe_Agressividade()
    tabela_bitolas = Tabela_Bitolas()

    inicio.show()
    sys.exit(app.exec())

    # app.exec_()
