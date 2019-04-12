from sip import delete
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QPushButton,QLineEdit,QLabel,QGridLayout

class kekapp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget=QWidget()
        self.setCentralWidget(self.widget)

        self.phase1()
    def phase1(self):
        self.layout=QGridLayout()
        self.widget.setLayout(self.layout)
        self.layout.setSpacing(10)

        self.lbl1=QLabel("Введите количество игроков:")
        self.layout.addWidget(self.lbl1,0,0,1,5)

        self.pl_count=QLineEdit()
        self.layout.addWidget(self.pl_count,1,1,1,3)

        self.play=QPushButton("Играть")
        self.layout.addWidget(self.play,3,3,1,2)
        self.play.clicked.connect(self.pl_count_inserted)
        self.show()

    def phase2(self):
        n=int(self.pl_count.text())
        print("phase2")
        self.layout.removeWidget(self.lbl1)
        self.layout.removeWidget(self.pl_count)
        self.layout.removeWidget(self.play)
        delete(self.lbl1)
        delete(self.pl_count)
        delete(self.play)

if __name__=="__main__":
    app=QApplication(sys.argv)
    kek=kekapp()
    sys.exit(app.exec_())