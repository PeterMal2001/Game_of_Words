import pickle

val=True
with open("usersettings/wordcheck.wprm","bw") as file:
    pickle.dump(val,file)