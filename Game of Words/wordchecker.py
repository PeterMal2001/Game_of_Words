def wordcheck(word):
    with open("russian.txt","r") as file:
        words=[line.strip() for line in file]
        if word in words:
            return True
        else:
            return False

if __name__=="__main__":
    while 1:
        word=input()
        print(wordcheck(word))