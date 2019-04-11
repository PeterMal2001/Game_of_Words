used_words=[]
n=int(input())
players=[i+1 for i in range(n)]
win=False
new=False

while win==False:
    for player in players:
        new=False
        if len(players)==1:
            win=True
            break
        while new==False:
            word=input()
            if word=="fin":
                players.remove(player)
                new=True
            elif not (word in used_words):
                used_words.append(word)
                new=True
                winner=player
            
print(winner)