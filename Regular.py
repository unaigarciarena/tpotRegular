from tpot import TPOTClassifier
from sklearn.cross_validation import train_test_split
import random
import argparse
import numpy as np
from sklearn import preprocessing
import copy
from sklearn.metrics import accuracy_score

dbs = ["adult.csv", "agaricus-lepiota.csv", "allbp.csv", "allhyper.csv", "allhypo.csv", "allrep.csv", "analcatdata_aids.csv",
       "analcatdata_asbestos.csv", "analcatdata_authorship.csv", "analcatdata_bankruptcy.csv", "analcatdata_boxing1.csv", "analcatdata_boxing2.csv", "analcatdata_creditscore.csv", "analcatdata_cyyoung8092.csv", "analcatdata_cyyoung9302.csv", "analcatdata_dmft.csv", "analcatdata_fraud.csv",
       "analcatdata_germangss.csv", "analcatdata_happiness.csv", "analcatdata_japansolvent.csv", "analcatdata_lawsuit.csv", "ann-thyroid.csv", "australian.csv", "auto.csv"]
classes = [-1]*len(dbs)
def insertMAR(data):
    x = data.shape[0]
    y = data.shape[1]
    obs = []
    nVar = 3
    percent = 30
    y1 = random.sample(range(0, y), nVar+1)  # First element in y1 will be the "causative" variable, remaining three will lose values

    # Auxiliary causative variable, to select the observations losing values, without modifying the causative.
    auxy = copy.copy(data[:, y1[0]])
    while len(obs) < int((percent*x*y/100)/nVar):
        obs.append(np.argmin(auxy))
        auxy[obs[len(obs)-1]] = 999999

    for i in range(0, len(obs)):
        for j in range(1, len(y1)):
            data[obs[i], y1[j]] = "NaN"  # "NaN" assigning

    return data

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def main(seed, psize, ngen, db):
    random.seed(seed)
    x = np.genfromtxt("DB/" + dbs[db], delimiter="\t", dtype=str, skip_header=True)
    le = preprocessing.LabelEncoder()
    # labels = []
    for i in range(0, x.shape[1]):
        #print(x[:, i])
        if not is_number(x[0, i]):
            le.fit(x[:, i])
            x[:, i] = (le.transform(x[:, i]))
    x = x.astype("float32")
    y = x[:,classes[db]]
    x = np.delete(x, classes[db], 1)
    #x = insertMAR(x)

    X_train, X_test, y_train, y_test = train_test_split(x, y, train_size=0.75, test_size=0.25, random_state=seed)

    tpot = TPOTClassifier(generations=ngen, population_size=psize, verbosity=0, n_jobs=1, disable_update_check=True, random_state=seed, db=db)
    tpot.fit(X_train, y_train, X_test, y_test)
    print(tpot.score(X_test, y_test))
    print("Pareto")
    for pipe in tpot.pareto_front_fitted_pipelines_:
        print(pipe)
        print(accuracy_score(tpot.pareto_front_fitted_pipelines_[pipe].predict(X_test), y_test))



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("a", nargs='+')
    args = parser.parse_args().__dict__["a"]
    seed = int(args[0])  # Seed: Used to set different outcomes of the stochastic program
    psize = int(args[1])  # Population size
    ngen = int(args[2])  # Number of generations
    db = int(args[3])
    main(seed, psize, ngen, db)

