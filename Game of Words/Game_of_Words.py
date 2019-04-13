from sip import delete
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QPushButton,QLineEdit,QLabel,QGridLayout,QMessageBox,QAction

class kekapp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget=QWidget()
        self.setCentralWidget(self.widget)
        
        self.re=False

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

        self.savegame.setDisabled(True)

        self.lbl1=QLabel("Введите количество игроков:")
        self.layout.addWidget(self.lbl1,0,0,1,5)

        self.pl_count=QLineEdit()
        self.layout.addWidget(self.pl_count,1,1,1,3)

        self.play=QPushButton("Играть")
        self.layout.addWidget(self.play,3,3,1,2)
        self.play.clicked.connect(self.pl_count_inserted)
        
        if self.re==False:
            self.show()

    def saving(self):
        print("save")

    def loading(self):
        print("load")

    def pl_count_inserted(self):
        self.n=0
        if self.pl_count.text()=="":
            msg=QMessageBox.warning(self,"Недостаточно данных","Введите число игроков.")
        elif self.pl_count.text()=="0" or self.pl_count.text()=="1":
            msg=QMessageBox.warning(self,"Ошибка модуля чувства юмора","Данный прэкол не найден в базе данных \"funny jokes\".")
        else:
            try:
                self.n=int(self.pl_count.text())
            except:
                msg=QMessageBox.warning(self,"Некорректные данные","Вы ввели не число.")
            if self.n!=0:
                self.clean_phase1()

    def clean_phase1(self):
        self.layout.removeWidget(self.lbl1)
        self.layout.removeWidget(self.pl_count)
        self.layout.removeWidget(self.play)
        delete(self.lbl1)
        delete(self.pl_count)
        delete(self.play)

        self.phase2()

    def phase2(self):

        self.players=[i+1 for i in range(self.n)]
        self.player=0
        self.used_words=[]

        self.savegame.setEnabled(True)

        self.lbl1=QLabel("Ход игрока "+str(self.players[self.player])+":")
        self.layout.addWidget(self.lbl1,0,0,1,3)

        self.lbl2=QLabel("Введите слово.")
        self.layout.addWidget(self.lbl2,1,1,1,3)

        self.get_word=QLineEdit()
        self.layout.addWidget(self.get_word,2,0,1,5)

        self.concede_btn=QPushButton("Сдаться")
        self.layout.addWidget(self.concede_btn,3,0,1,2)
        self.concede_btn.clicked.connect(self.concede_clk)

        self.accept_btn=QPushButton("Ввести")
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
            print(self.n)
            self.get_word.setText("")
            if self.n==1:
                msg=QMessageBox.information(self,"Игра окончена","Игра окончена, победил игрок "+str(self.players[0])+"! Поздравляю.")
                self.clean_phase2()
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

    def clean_phase2(self):
        self.layout.removeWidget(self.lbl1)
        self.layout.removeWidget(self.lbl2)
        self.layout.removeWidget(self.get_word)
        self.layout.removeWidget(self.concede_btn)
        self.layout.removeWidget(self.accept_btn)
        delete(self.lbl1)
        delete(self.lbl2)
        delete(self.get_word)
        delete(self.concede_btn)
        delete(self.accept_btn)
        
        self.re=True

        self.phase1()



if __name__=="__main__":
    app=QApplication(sys.argv)
    kek=kekapp()
    sys.exit(app.exec_())