import numpy as np
import pandas as pd

def main():
    symptoms = pd.read_csv("symptom.csv", delimiter=";")
    patient_symptoms = np.random.randint(0, 2, symptoms.shape[0])
    diseases = pd.read_csv("disease.csv", delimiter=";")
    prob_diseases = []
    for i in range(diseases.shape[0] - 1):
        prob_diseases.append(diseases.iloc[i][-1] / diseases.iloc[-1][-1])
    prob_max = 0
    index_max = -1
    for i in range(len(prob_diseases)):
        prob = 1
        for j in range(len(patient_symptoms)):
            if patient_symptoms[j] == 1:
                prob *= symptoms.iloc[j][i + 1]
        prob *= prob_diseases[i]
        if prob > prob_max:
            prob_max = prob
            index_max = i
    print(diseases.iloc[index_max][0])


if __name__ == '__main__':
    main()
