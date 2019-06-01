def wordcheck(word):
    letter=word[0]
    try:
        with open("dict/"+letter.lower()+".txt","r") as file:
            words=[line.strip() for line in file]
            if word in words:
                return True
            else:
                return False
    except:
        return False

def lastlettercheck(word,letter):
    if word[0]==letter or word[0]==letter.upper() or letter=="":
        return True
    else:
        return False

def lastwordset(word):
    banned=["ь","ъ","й","ы"]
    l=""
    i=-1
    while l=="":
        if word[i] in banned:
            i-=1
        else:
            l=word[i]
    return l


if __name__=="__main__":
    while 1:
        word=input()
        print(wordcheck(word))