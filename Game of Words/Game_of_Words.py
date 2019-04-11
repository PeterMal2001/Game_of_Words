used_words=[]
print("Введите число игроков...")
n=int(input())
players=[i+1 for i in range(n)]
win=False
new=False

while win==False:
    for player in players:
        print("Ход игрока "+str(player)+".")
        new=False
        if len(players)==1:
            win=True
            break
        while new==False:
            print("Введите слово...")
            word=input()
            if word=="fin":
                print("Игрок "+str(player)+" сдаётся и выбывает из игры.")
                players.remove(player)
                new=True
            elif not (word in used_words):
                print("Слово принято.")
                used_words.append(word)
                new=True
                winner=player
            else:
                print("Данное слово уже было введено.")
            
print("Игра окончена, побеждает игрок "+str(winner)+"!")