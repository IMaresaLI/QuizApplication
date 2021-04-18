################################################
################################################
################################################
#########*******###*******####**********########
########**#####**#**#####**###**######**########
########**#####**#**#####**###**######**########
########**#####**#**#####**###**********########
########**#####**#**#####**###**################
########**#####**#**#####**###**################
########**######***######**###**################
########**###############**###**################
########**###############**###**################
################################################
########Copyright © Maresal Programming#########
################################################

from PyQt5 import QtWidgets,QtCore
import os,sys,base64
from QuizAppDesign import Ui_MainWindow
from DatabaseManager import sqliteData


class MainApp(QtWidgets.QMainWindow):
    loginStatus = False
    n = 0
    answer =  []
    def __init__(self):
        super(MainApp,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet(open("style.css","r").read())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.ExitBtn.clicked.connect(self.exitButton)
        self.ui.MinimizeBtn.clicked.connect(self.minimize)

        self.ui.HomeBtn.clicked.connect(self.home)
        self.ui.QuizBtn.clicked.connect(self.startQuiz)
        self.ui.AnswerBtn.clicked.connect(self.answerGo)
        self.ui.NullBtn.clicked.connect(self.nullAnswer)
        self.ui.QuizAddBtn.clicked.connect(self.questionCreatePage)
        self.ui.RegisterBtn.clicked.connect(self.registerPage)
        self.ui.LoginBtn.clicked.connect(self.loginPage)
        self.ui.ProfilBtn.clicked.connect(self.profilPage)
        self.ui.QuestAddingBtn.clicked.connect(self.CreateQuestion)
        self.ui.AttLoginBtn.clicked.connect(self.Login)
        self.ui.RegBtn.clicked.connect(self.Register)
        self.ui.LogOutBtn.clicked.connect(self.logout)
        self.ui.InstagramBtn.clicked.connect(self.instaLink)
        self.ui.FacebookBtn.clicked.connect(self.faceLink)
        self.ui.GithubBtn.clicked.connect(self.githubLink)
        self.ui.SettingBtn.clicked.connect(self.setting)



    def home(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def startQuiz(self):
        if self.loginStatus == True :
            self.ui.stackedWidget.setCurrentIndex(1)
            qData = sqliteData().getData("questions")
            if self.n < len(qData):
                self.answer.append(qData[self.n][0])
                self.ui.QuestPlt.setPlainText(str(self.n+1)+"-)"+qData[self.n][1])
                self.ui.ARadioBtn.setText(qData[self.n][2])
                self.ui.BRadioBtn.setText(qData[self.n][3])
                self.ui.CRadioBtn.setText(qData[self.n][4])
                self.ui.DRadioBtn.setText(qData[self.n][5])
            else :
                QtWidgets.QMessageBox.information(self,"Bildiri","Sorular Bitti Tebrikler.")
                self.n = 0
                self.ui.stackedWidget.setCurrentIndex(0)
        else :
            QtWidgets.QMessageBox.warning(self,"Hata","Lütfen Giriş Yapınız.")

    def answerGo(self):
        x = self.ui.groupBox.findChildren(QtWidgets.QRadioButton)
        for i in x :
            if i.isChecked():
                self.answer.append(i.text())
                qData = sqliteData().getData("questions",id=self.answer[0],all=False)
                if qData[6] == self.answer[1]:
                    username = self.ui.UsernameLbl.text().split(":")[1].strip()
                    sqliteData().pointUpdate(username,qData[-1])
                    self.n+=1
                    self.answer.clear()
                    self.loginStat(self.ui.UsernameLbl.text().split(":")[1].strip())
                    self.startQuiz()
                else :
                    self.n+=1
                    self.answer.clear()
                    self.startQuiz()

    def nullAnswer(self):
        self.answer.clear()
        self.n+=1
        self.startQuiz()
    
    def questionCreatePage(self):
        if self.loginStatus == True:
            self.ui.stackedWidget.setCurrentIndex(2)
            self.ui.AttStacked.setCurrentIndex(0)
        else :
            QtWidgets.QMessageBox.warning(self,"Hata","Lütfen Giriş Yapınız.")

    def registerPage(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.AttStacked.setCurrentIndex(1)

    def loginPage(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.AttStacked.setCurrentIndex(2)

    def profilPage(self):
        if self.loginStatus == True:
            QtWidgets.QMessageBox.warning(self,"Bildirim","Yapım Aşamasında...")
        else :
            QtWidgets.QMessageBox.warning(self,"Hata","Lütfen Giriş Yapınız.")

    def logout(self):
        if self.loginStatus == True:
            self.loginStatus = False
            self.btnHidden()
            QtWidgets.QMessageBox.information(self,"Çıkış İşlemi","Çıkış işlemi başarılı.")
            self.ui.stackedWidget.setCurrentIndex(0)
        else :
            QtWidgets.QMessageBox.warning(self,"Hata","Lütfen Giriş Yapınız.")


    def CreateQuestion(self):
        question = self.ui.QuestTbx.toPlainText()
        a = self.ui.ATbx.text()
        b = self.ui.BTbx.text()
        c = self.ui.CTbx.text()
        d = self.ui.DTbx.text()
        point = self.ui.puanCbx.currentText().split(" ")[0]
        rdb = self.ui.frame_2.findChildren(QtWidgets.QRadioButton)
        for i in rdb :
            if i.isChecked():
                if i.text() == "A-)":
                    answer = self.ui.ATbx.text()
                elif i.text() == "B-)":
                    answer = self.ui.BTbx.text()
                elif i.text() == "C-)":
                    answer = self.ui.CTbx.text()
                elif i.text() == "D-)":
                    answer = self.ui.DTbx.text()
        try :
            result = QtWidgets.QMessageBox.question(self,"Onay","Bu soruyu gerçekten eklemek istediğinize emin misiniz?",QtWidgets.QMessageBox.StandardButton.Ok |QtWidgets.QMessageBox.StandardButton.Cancel)
            if result == QtWidgets.QMessageBox.StandardButton.Ok:
                sqliteData().QuestionAdd(question,a,b,c,d,answer,int(point))
                QtWidgets.QMessageBox.information(self,"Eklenme Bilgisi","Soru veritabanına Eklendi.")
                self.questClearTbx()
        except:
            QtWidgets.QMessageBox.warning(self,"Hata","Soru eklenirken hata oluştu.")

    def questClearTbx(self):
        self.ui.QuestTbx.clear()
        self.ui.ATbx.clear()
        self.ui.BTbx.clear()
        self.ui.CTbx.clear()
        self.ui.DTbx.clear()

    def Login(self):
        username = self.ui.UsernameGTbx.text()
        pw = self.ui.PwGTbx.text()
        try : 
            data = sqliteData().getData("users",username=username,all=False)
            print(base64.b32decode(data[2]).decode())
            if base64.b32decode(data[2]).decode() == pw :
                QtWidgets.QMessageBox.information(self,"Giriş Bilgisi","Giriş Başarılı")
                self.loginStatus = True
                self.loginStat(username)
                self.btnHidden()
                self.ui.UsernameGTbx.clear()
                self.ui.PwGTbx.clear()
                self.ui.stackedWidget.setCurrentIndex(0)
            else:
                QtWidgets.QMessageBox.warning(self,"Hata","Girdiğiniz Şifre Yanlıştır.")
        except : 
            QtWidgets.QMessageBox.warning(self,"Hata","Bilgiler Yanlış.")

    def Register(self):
        username = self.ui.usernameTbx.text()
        pw = self.ui.PwTbx.text().encode("utf-8")
        pw64 = base64.b32encode(pw)
        e_mail = self.ui.emailTbx.text()
        name_lastname = self.ui.nameTbx.text()
        if self.ui.TermCbx.isChecked() == True:
            if username != "" and pw != "" and e_mail != "":
                try:
                    sqliteData().UsersAdd(username,pw64,e_mail,name_lastname)
                    QtWidgets.QMessageBox.information(self,"Kayıt Bilgisi","Kayıt işleminiz tamamlandı. Giriş yapabilirsiniz.")
                    self.ui.AttStacked.setCurrentIndex(2)
                except :
                    QtWidgets.QMessageBox.warning(self,"Hata","Girdiğinizi bilgileri kontrol ederek tekrar deneyiniz.")
            else :
                QtWidgets.QMessageBox.warning(self,"Hata","Doldurulması gereken bölümler doldurulmadı.")
        else :
            QtWidgets.QMessageBox.warning(self,"Hata","Kullanım şartlarını kabul etmelisiniz.")

    def btnHidden(self):
        if self.loginStatus == False :
            self.ui.LoginBtn.setHidden(False)
            self.ui.RegisterBtn.setHidden(False)
            self.ui.ProfilBtn.setHidden(True)
            self.ui.LogOutBtn.setHidden(True)
            self.ui.statusFrame.setHidden(True)
            self.ui.QuizAddBtn.setHidden(True)
        else :
            self.ui.LoginBtn.setHidden(True)
            self.ui.RegisterBtn.setHidden(True)
            self.ui.ProfilBtn.setHidden(False)
            self.ui.LogOutBtn.setHidden(False)
            self.ui.statusFrame.setHidden(False)
            self.ui.QuizAddBtn.setHidden(False)

    def loginStat(self,username):
        data = sqliteData().getData("users",username=username,all=False)
        self.ui.UsernameLbl.setText("Username: %s" %data[1])
        self.ui.PuanLbl.setText("Puan : %s" %data[5])

    def instaLink(self):
        os.startfile("https://www.instagram.com/maresalp/")
    def faceLink(self):
        os.startfile("https://www.facebook.com/maresalprogramming")
    def githubLink(self):
        os.startfile("https://github.com/IMaresaLI")

    def setting(self):
        QtWidgets.QMessageBox.warning(self,"Bildirim","Yapım Aşamasında...")

    def minimize(self):
        self.showMinimized()

    def exitButton(self):
        app.exit()

    def mousePressEvent(self, event):
        try :
            if event.buttons() == QtCore.Qt.LeftButton:
                self.dragPos = event.globalPos()
                event.accept()
        except :
            pass

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        except :
            pass






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainApp()
    main.show()
    app.setStyle("Fusion")
    app.exit(app.exec_())
