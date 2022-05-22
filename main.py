import bot_web_scraping
import bot_registro_excel
import bot_envio_email
import bot_envio_whatsapp
#import wbs_v2
from PyQt6 import uic,QtWidgets
from datetime import datetime
from PyQt6 import QtCore, QtWidgets,QtGui
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
import sys, time

class G3WS_threads(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('interfaceV1.ui',self)
        self.label_resultado.setText("")
        self.thread = {}
        self.pushButton_start.clicked.connect(self.start_worker_1)

    def start_worker_1(self):
        flag_email_ok = False
        flag_software_ok = False
        flag_intervalo_ok = False

        #todo verifica os emails -----------------------------------------------------------------------------------------------------
        ListaEmails_previa=[]
        ListaEmails_previa.append(self.lineEdit_email1.text())
        ListaEmails_previa.append(self.lineEdit_email2.text())
        ListaEmails_previa.append(self.lineEdit_email3.text())
        ListaEmails_previa.append(self.lineEdit_email4.text())
        ListaEmails_previa.append(self.lineEdit_email5.text())
        ListaEmails = ListaEmails_previa.copy()
        for i in range(4,-1,-1):
            if ListaEmails_previa[i] == "":
                ListaEmails.pop(i)
            elif ('@' not in ListaEmails_previa[i]) or ('.' not in ListaEmails_previa[i]):
                QMessageBox.critical(G3Scraping,"Email inválido!","O email "+str(i+1)+" está incorreto, por gentileza digite-o novamente.")
                # self.label_resultado.setText("O email "+str(i+1)+" está incorreto, por gentileza digite-o novamente.")
                break
            else:
                flag_email_ok = True
        
        if ListaEmails == []:
            QMessageBox.critical(G3Scraping,"Email em branco!","Por favor insira ao menos 1 endereço de email.")
            # self.label_resultado.setText("Por favor insira ao menos 1 endereço de email.")
            flag_email_ok = False

        #todo verifica o software ----------------------------------------------------------------------------------------------------
        sw_sch = self.lineEdit_software.text()
        if sw_sch == "":
            QMessageBox.critical(G3Scraping,"Software Inválido!","Você precisa digitar um software para somente então clicar em START.")
            # self.label_resultado.setText("Você precisa digitar um software para somente então clicar em START.")
        else:
            flag_software_ok = True

        #todo verifica o intervalo de tempo -----------------------------------------------------------------------------------------
        data_busca = self.dateEdit_inicial.text()
        data_busca = data_busca.replace("/", "")
        aday = self.dateEdit_final.text()
        aday = aday.replace("/", "")
        dia_inicial = int(data_busca[:2])
        mes_inicial = int(data_busca[2:4])
        ano_inicial = int(data_busca[4:])
        dia_final = int(aday[:2])
        mes_final = int(aday[2:4])
        ano_final = int(aday[4:])
        d_inicio = datetime.strptime(data_busca[:2]+data_busca[2:4]+data_busca[4:], '%d%m%Y')
        d_final = datetime.strptime(aday[:2]+aday[2:4]+aday[4:], '%d%m%Y')
        d_hoje = datetime.strptime(datetime.today().strftime("%d%m%Y"),"%d%m%Y")
        if ano_inicial > ano_final:
            QMessageBox.critical(G3Scraping,"Período de tempo inválido!","Ano inicial maior que o Ano final. Tente outro intervalo de tempo.")
            # self.label_resultado.setText("Ano inicial maior que o Ano final. Tente outro intervalo de tempo.")
        elif (d_hoje - d_final).days < 0:
            QMessageBox.critical(G3Scraping,"Período de tempo inválido!","Data final não pode ser maior que a data de hoje. Tente outro intervalo de tempo")
            # self.label_resultado.setText("Data final não pode ser maior que a data de hoje. Tente outro intervalo de tempo")
        elif (d_hoje - d_inicio).days < 0:
            QMessageBox.critical(G3Scraping,"Período de tempo inválido!","Data inicial não pode ser maior que a data de hoje. Tente outro intervalo de tempo")
            # self.label_resultado.setText("Data inicial não pode ser maior que a data de hoje. Tente outro intervalo de tempo")
        elif mes_inicial > mes_final:
            QMessageBox.critical(G3Scraping,"Período de tempo inválido!","Mês inicial maior que o Mês final. Para os anos selecionados isso é inválido. Tente outro intervalo de tempo.")
            # self.label_resultado.setText("Mês inicial maior que o Mês final. Para os anos selecionados isso é inválido. Tente outro intervalo de tempo")
        elif (mes_inicial == mes_final) and (dia_inicial > dia_final):
            QMessageBox.critical(G3Scraping,"Período de tempo inválido!","O dia inicial é maior que o dia final. Para mesmos meses isso é inválido. Tente outro intervalo de tempo.")
            # self.label_resultado.setText("O dia inicial é maior que o dia final. Para mesmos meses isso é inválido. Tente outro intervalo de tempo.")
        elif abs((d_final - d_inicio).days) >= 120:
            QMessageBox.critical(G3Scraping,"Período de tempo inválido!","O site da NIST não suporta intervalos de tempo maiores que 120 dias. Tente outro intervalo de tempo.")
            # self.label_resultado.setText("O site da NIST não suporta intervalos de tempo maiores que 120 dias. Tente outro intervalo de tempo")
        else:
            aday = aday[2:4]+aday[:2]+aday[4:]
            data_busca = data_busca[2:4]+data_busca[:2]+data_busca[4:]
            flag_intervalo_ok = True

        #todo Se tudo estiver ok - inicia a busca.
        num_wpp = self.lineEdit_whatsapp.text().replace(" ","").replace("(","").replace(")","").replace("+55","")
        if flag_email_ok and flag_software_ok and flag_intervalo_ok:
            self.label_resultado.setText("---------Carregando ---------")
            self.pushButton_start.setEnabled(False)
            envio_dt = []
            envio_dt.append(sw_sch)
            envio_dt.append(data_busca)
            envio_dt.append(aday)
            envio_dt.append(ListaEmails)
            envio_dt.append(num_wpp)
            self.thread[1] = ThreadClass(parent=None, envio_dt = envio_dt)
            self.thread[1].start()
            self.thread[1].any_signal.connect(self.micropross)

        #todo caso contrario não
        else:
            #self.label_resultado.setText("---------Carregando ---------")
            self.pushButton_start.setEnabled(True)
    
    def stop_worker_1(self):
        self.thread[1].stop()
        self.pushButton_start.setEnabled(True)
        
    def micropross(self, counter = [0,0,0]):
        status_bar = counter
        envio_dt = self.sender().envio_dt
        if status_bar[2] == 1:
            self.label_resultado.setText("--------- Realizando Busca ---------")
            
        elif status_bar[2] == 2:
            self.label_resultado.setText("--------- Coletando dados ---------")
            self.progressBar.setMaximum(status_bar[1])
            self.progressBar.setValue(status_bar[0])
        elif status_bar[2] == 3:
            self.progressBar.setValue(0)
            self.pushButton_start.setEnabled(True)
            self.label_resultado.setText("--------- E-MAIL ENVIADO ---------")
            self.stop_worker_1

class ThreadClass(QtCore.QThread):

    any_signal = QtCore.pyqtSignal(list)
    def __init__(self,parent=None,envio_dt=[]):
        super(ThreadClass, self).__init__(parent)
        self.envio_dt=envio_dt
        self.is_running = True
    
    def run(self):
        #print(self.envio_dt[0])
        que_dt = [0,0,0]
        #result_busca = bot_web_scraping.web_sc(self.envio_dt[0],self.envio_dt[1],self.envio_dt[2])
        que_dt[2] = 1
        self.any_signal.emit(que_dt)
        result_busca = bot_web_scraping.web_sc(self.envio_dt[0],self.envio_dt[1],self.envio_dt[2])
        if result_busca[0] == 0:
            cnt = 0
            dt_pes = []
            result_auto = []
            que_dt[0] = cnt
            que_dt[1] = result_busca[2]
            que_dt[2] = 2
            self.any_signal.emit(que_dt)
            for i in range(0,len(result_busca[1])):
                dt_pes.append(bot_web_scraping.web_cole(self.envio_dt[0], result_busca[1][i]))
                cnt += 1
                #print(cnt)
                que_dt[0] = cnt
                self.any_signal.emit(que_dt)
            result_auto.append(0)
            result_auto.append(dt_pes)
        if result_auto[0] == 0:
            felps_gel = bot_registro_excel.montaPlanilha(result_auto[1])            
        bot_envio_email.send_email(self.envio_dt[3], felps_gel)
        bot_envio_whatsapp.send_wpp(self.envio_dt[4],self.envio_dt[0])
        que_dt[2] = 3
        self.any_signal.emit(que_dt)
    
    def stop(self):
        self.is_running = False
        self.terminate()

app = QtWidgets.QApplication(sys.argv)
G3Scraping = G3WS_threads()
G3Scraping.show()
sys.exit(app.exec())