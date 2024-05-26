import pickle
import pprint

class test:
    obj = pickle.load(open("code/NonCodeFiles/q_table.pkl", "rb"))

    with open("out.txt", "a") as f:
         pprint.pprint(obj, stream=f)