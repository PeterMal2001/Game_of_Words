from sip import delete
import sys
import pickle
import os
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QPushButton,QLineEdit,QLabel,QGridLayout,QMessageBox,QAction,QScrollArea

class kekapp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget=QWidget()
        self.setCentralWidget(self.widget)
        
        self.re=False
        self.widgets=[]

        self.phase1()

    def phase1(self):
        if self.re==False:
            self.layout=QGridLayout()
            self.widget.setLayout(self.layout)
            self.layout.setSpacing(10)

            self.loadgame=QAction("Загрузить игру")
            self.loadgame.triggered.connect(self.loading)

            self.savegame=QAction("Сохранить игру")
            self.savegame.triggered.connect(self.saving)

            kekbar=self.menuBar()
            the_game=kekbar.addMenu("Игра")
            the_game.addAction(self.savegame)
            the_game.addAction(self.loadgame)

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
                for i in [self.players,self.player,self.used_words]:
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
        lbl1=QLabel("Выберите сохранение")
        self.widgets.append(self.lbl1)
        self.layout.addWidget(self.lbl1,0,0,1,2)

        self.saved_games=os.listdir("savedgames")

    def pl_count_inserted(self):
        self.n=0
        if self.pl_count.text()=="":
            msg=QMessageBox.warning(self,"Недостаточно данных","Введите число игроков.")
        else:
            try:
                self.n=int(self.pl_count.text())
            except:
                msg=QMessageBox.warning(self,"Некорректные данные","Вы ввели не число.")
            if self.n<0:
                msg=QMessageBox.warning(self,"Некорректные данные","Вы ввели отрицательное число.")
            elif self.n!=0:
                self.players=[i+1 for i in range(self.n)]
                self.player=0
                self.used_words=[]
                self.phase2()

    def phase2(self):
        self.clean_phase()

        self.savegame.setEnabled(True)

        self.lbl1=QLabel("Ход игрока "+str(self.players[self.player])+":")
        self.widgets.append(self.lbl1)
        self.layout.addWidget(self.lbl1,0,0,1,3)

        self.lbl2=QLabel("Введите слово.")
        self.widgets.append(self.lbl2)
        self.layout.addWidget(self.lbl2,1,1,1,3)

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
                self.re=True
                self.phase1()
            elif self.player==self.n:
                self.player=0
                self.lbl1.setText("Ход игрока "+str(self.players[self.player])+":")
            else:
                self.lbl1.setText("Ход игрока "+str(self.players[self.player])+":")

    def accept_clk(self):
        if self.get_word.text()=="":
            msg=QMessageBox.information(self,"Некорректный ввод","Введите слово")
        if self.get_word.text() in self.used_words:
            msg=QMessageBox.information(self,"Уже было","Данное слово уже было введено")
        else:
            self.used_words.append(self.get_word.text())
            self.player+=1
            if self.player==self.n:
                self.player=0
            self.lbl1.setText("Ход игрока "+str(self.players[self.player])+":")
        self.get_word.setText("")

    def clean_phase(self):
        for widget in self.widgets:
            self.layout.removeWidget(widget)
            delete(widget)
        self.widgets=[]

if __name__=="__main__":
    app=QApplication(sys.argv)
    kek=kekapp()
    sys.exit(app.exec_())