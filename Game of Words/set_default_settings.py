import pickle

val=True
with open("usersettings/wordcheck.wprm","bw") as file:
    pickle.dump(val,file)
val=False
with open("usersettings/lastlettercheck.wprm","bw") as file:
    pickle.dump(val,file)

print("done")