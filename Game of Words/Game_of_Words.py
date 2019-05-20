from sip import delete
import sys
import pickle
import os
from wordchecker import wordcheck,lastlettercheck,lastwordset
from list_generator import mt_list
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class kekapp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget=QWidget()
        self.setCentralWidget(self.widget)
        
        self.par_wordcheck=parameter("wordcheck")
        self.par_lastlettercheck=parameter("lastlettercheck")
        self.last_phase="init"
        self.widgets=[]
        self.n=0

        self.phase1()

    def phase1(self):
        if self.last_phase=="init":
            self.setWindowTitle("Game of Words")
            self.setWindowIcon(QIcon("logo.png"))

            self.layout=QGridLayout()
            self.widget.setLayout(self.layout)
            self.layout.setSpacing(10)

            self.newgame=QAction(QIcon("attention.png"),"Новая игра")
            self.newgame.triggered.connect(self.phase1)

            self.loadgame=QAction("Загрузить игру")
            self.loadgame.triggered.connect(self.loading)

            self.savegame=QAction(QIcon("save.png"),"Сохранить игру")
            self.savegame.triggered.connect(self.saving)

            self.settings=QAction(QIcon("settings.png"),"Настройки")
            self.settings.triggered.connect(self.settings_phase)

            kekbar=self.menuBar()
            the_game=kekbar.addMenu("Игра")
            the_game.addAction(self.newgame)
            the_game.addAction(self.savegame)
            the_game.addAction(self.loadgame)
            the_game.addAction(self.settings)

            self.show()
        else:
            self.clean_phase()
        
        self.savegame.setDisabled(True)

        self.lbl1=QLabel("Введите количество игроков:")
        self.widgets.append(self.lbl1)
        self.layout.addWidget(self.lbl1,0,0,1,5)

        self.pl_count=QLineEdit()
        self.widgets.append(self.pl_count)
        self.layout.addWidget(self.pl_count,1,1,1,3)

        self.play=QPushButton("Играть")
        self.widgets.append(self.play)
        self.layout.addWidget(self.play,3,3,1,2)
        self.play.clicked.connect(self.pl_count_inserted)

        self.last_phase="phase1"

    def saving(self):
        self.clean_phase()

        self.lbl1=QLabel("Введите название сохранения")
        self.widgets.append(self.lbl1)
        self.layout.addWidget(self.lbl1,0,0,1,5)

        self.save_name=QLineEdit()
        self.widgets.append(self.save_name)
        self.layout.addWidget(self.save_name,1,1,1,3)

        self.save=QPushButton("Сохранить")
        self.widgets.append(self.save)
        self.layout.addWidget(self.save,2,1,1,3)
        self.save.clicked.connect(self.save_clk)

    def save_clk(self):
        try:
            with open("savedgames/"+self.save_name.text()+".wdsave","xb") as file:
                for i in [self.players,self.player,self.used_words,self.lastletter]:
                    pickle.dump(i,file)
                    self.phase2()
        except FileExistsError:
            msg=QMessageBox.question(self,"Файл уже существует","Файл с таким именем уже существует.\nПерезаписать?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if msg==QMessageBox.Yes:
                with open("savedgames/"+self.save_name.text()+".wdsave","wb") as file:
                    for i in [self.players,self.player,self.used_words]:
                        pickle.dump(i,file)
                self.phase2()

    def loading(self):
        self.clean_phase()
        
        self.lbl1=QLabel("Введите название сохранения")
        self.widgets.append(self.lbl1)
        self.layout.addWidget(self.lbl1,0,0,1,2)

        self.save_name=QLineEdit()
        self.widgets.append(self.save_name)
        self.layout.addWidget(self.save_name,1,0,1,2)

        self.save_delete=QPushButton("Удалить")
        self.widgets.append(self.save_delete)
        self.layout.addWidget(self.save_delete,2,0)
        self.save_delete.clicked.connect(self.save_delete_clk)
        
        self.save_load=QPushButton("Загрузить")
        self.widgets.append(self.save_load)
        self.layout.addWidget(self.save_load,2,1)
        self.save_load.clicked.connect(self.save_load_clk)

    def save_delete_clk(self):
        if self.save_name.text()+".wdsave" in os.listdir("savedgames"):
            msg=QMessageBox.question(self,"Вы уверены?","Вы точно хотите удалить это сохранение?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if msg==QMessageBox.Yes:
                os.remove("savedgames/"+self.save_name.text()+".wdsave")
        else:
            msg=QMessageBox.information(self,"Ошибка","Данного сохранения не существует.")

    def save_load_clk(self):
        if self.save_name.text()+".wdsave" in os.listdir("savedgames"):
            msg=QMessageBox.question(self,"Вы уверены?","Вы точно хотите загрузить это сохранение?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if msg==QMessageBox.Yes:
                with open("savedgames/"+self.save_name.text()+".wdsave","rb") as file:
                    self.players=pickle.load(file)
                    self.player=pickle.load(file)
                    self.used_words=pickle.load(file)
                    self.lastletter=pickle.load(file)
                self.n=len(self.players)
                self.phase2()
        else:
            msg=QMessageBox.information(self,"Ошибка","Данного сохранения не существует.")

    def settings_phase(self):
        self.clean_phase()

        self.do_wordcheck=QCheckBox("Выполнять проверку существования слова в словаре")
        self.widgets.append(self.do_wordcheck)
        self.layout.addWidget(self.do_wordcheck,0,0,1,2)
        self.do_wordcheck.setChecked(self.par_wordcheck.value)
        self.do_wordcheck.stateChanged.connect(self.par_wordcheck.switch)

        self.do_lastlettercheck=QCheckBox("Следующее слово должно начинаться с буквы,\nна которую оканчивалось предыдущее")
        self.widgets.append(self.do_lastlettercheck)
        self.layout.addWidget(self.do_lastlettercheck,1,0,1,2)
        self.do_lastlettercheck.setChecked(self.par_lastlettercheck.value)
        self.do_lastlettercheck.stateChanged.connect(self.par_lastlettercheck.switch)

        self.back_btn=QPushButton("Готово")
        self.widgets.append(self.back_btn)
        self.layout.addWidget(self.back_btn,2,1)
        self.back_btn.clicked.connect(self.goback)

    def goback(self):
        if self.last_phase=="phase1":
            self.phase1()
        elif self.last_phase=="phase2":
            self.phase2()
    
    def pl_count_inserted(self):
        if self.pl_count.text()=="":
            msg=QMessageBox.warning(self,"Недостаточно данных","Введите число игроков.")
        else:
            try:
                self.n=int(self.pl_count.text())
                if self.n<=0:
                    msg=QMessageBox.warning(self,"Некорректные данные","Вы ввели отрицательное число или ноль.")
                else:
                    self.players=[i+1 for i in range(self.n)]
                    self.player=0
                    self.used_words=[]
                    self.lastletter=""
                    self.phase2()
            except ValueError:
                msg=QMessageBox.warning(self,"Некорректные данные","Вы ввели не целое число, или не число вовсе.")

    def phase2(self):
        self.clean_phase()

        self.savegame.setEnabled(True)

        self.lbl1=QLabel("Ход игрока "+str(self.players[self.player])+":")
        self.widgets.append(self.lbl1)
        self.layout.addWidget(self.lbl1,0,0,1,3)

        self.lbl2=QLabel("Введите слово.")
        self.widgets.append(self.lbl2)
        self.layout.addWidget(self.lbl2,1,1,1,3)

        if self.par_lastlettercheck.value:
            self.lbl3=QLabel("Ваша буква: "+self.lastletter)
            self.widgets.append(self.lbl3)
            self.layout.addWidget(self.lbl3,0,3,1,2)

        self.get_word=QLineEdit()
        self.widgets.append(self.get_word)
        self.layout.addWidget(self.get_word,2,0,1,5)

        self.concede_btn=QPushButton("Сдаться")
        self.widgets.append(self.concede_btn)
        self.layout.addWidget(self.concede_btn,3,0,1,2)
        self.concede_btn.clicked.connect(self.concede_clk)

        self.accept_btn=QPushButton("Ввести")
        self.widgets.append(self.accept_btn)
        self.layout.addWidget(self.accept_btn,3,3,1,2)
        self.accept_btn.clicked.connect(self.accept_clk)

        self.last_phase="phase2"

    def concede_clk(self):
        msg=QMessageBox.question(self,"Сдаться","Вы точно хотите сдаться?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if msg==QMessageBox.Yes:
            self.players.pop(self.player)
            b=[]
            for i in self.players:
                b.append(i)
            self.players=b
            self.n-=1
            self.get_word.setText("")
            if self.n==1:
                msg=QMessageBox.information(self,"Игра окончена","Игра окончена, победил игрок "+str(self.players[0])+"! Поздравляю.")
                self.phase1()
            elif self.player==self.n:
                self.player=0
                self.lbl1.setText("Ход игрока "+str(self.players[self.player])+":")
            else:
                self.lbl1.setText("Ход игрока "+str(self.players[self.player])+":")

    def accept_clk(self):
        log=mt_list(self.par_wordcheck,wordcheck(self.get_word.text()),self.par_lastlettercheck,lastlettercheck(self.get_word.text(),self.lastletter))
        if self.get_word.text()=="":
            msg=QMessageBox.information(self,"Некорректный ввод","Введите слово")
        elif self.get_word.text() in self.used_words:
            msg=QMessageBox.information(self,"Уже было","Данное слово уже было введено")
        elif log.check():
            self.used_words.append(self.get_word.text())
            self.lastletter=lastwordset(self.get_word.text())
            self.player+=1
            if self.player==self.n:
                self.player=0
            self.lbl1.setText("Ход игрока "+str(self.players[self.player])+":")
            if self.par_lastlettercheck.value:
                self.lbl3.setText("Ваша буква: "+self.lastletter)
        else:
            msg=QMessageBox.information(self,"Некорректное слово",log.info())
        self.get_word.setText("")

    def clean_phase(self):
        for widget in self.widgets:
            self.layout.removeWidget(widget)
            delete(widget)
        self.widgets=[]

class parameter():
    def __init__(self,name):
        self.name=str(name)
        with open("usersettings/"+self.name+".wprm","br") as file:
            val=pickle.load(file)
        self.value=val        

    def switch(self):
        self.value=not self.value
        with open("usersettings/"+self.name+".wprm","bw") as file:
            val=self.value
            pickle.dump(val,file)

if __name__=="__main__":
    app=QApplication(sys.argv)
    kek=kekapp()
    sys.exit(app.exec_())