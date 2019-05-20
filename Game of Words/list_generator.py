class mt_list():
    def __init__(self,wordcheck,res_wordcheck,lastlettercheck,res_lastlettercheck):
        self.wordcheck=wordcheck
        self.res_wordcheck=res_wordcheck
        self.lastlettercheck=lastlettercheck
        self.res_lastlettercheck=res_lastlettercheck
    
    def check(self):
        if self.wordcheck and not self.res_wordcheck:
            self.i1=False
        else:
            self.i1=True
        if self.lastlettercheck and not self.res_lastlettercheck:
            self.i2=False
        else:
            self.i2=True
        return self.i1 and self.i2
    
    def info(self):
        text="Ваше слово не соответствует данным правилам:"
        if not self.i1:
            text+="\n>Этого слова нет в нашем словаре."
        if not self.i2:
            text+="\n>Это слово начинается не с той буквы, на которую оканчивалось прошлое."
        return text