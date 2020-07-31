from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import auc
from sklearn.metrics import roc_curve

import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
import seaborn as sn
import numpy as np


def accuracy_recall_precision_f1(y_true, y_pred):
    print('accuracy = ', accuracy_score(y_true, y_pred))
    print('recall = ', recall_score(y_true, y_pred))
    print('precision = ', precision_score(y_true, y_pred))
    print('F1 = ', f1_score(y_true, y_pred))


def plot_confusion_matrix(y_true, y_pred):
    data = confusion_matrix(y_true, y_pred)
    df_cm = pd.DataFrame(data, columns=np.unique(y_pred), index=np.unique(y_true))
    df_cm.index.name = 'Actual values'
    df_cm.columns.name = 'Predicted values'

    plt.figure(figsize=(10, 7))

    sn.set(font_scale=1.4)
    akws = {"ha": 'center', "va": 'center'}
    sn.heatmap(df_cm, annot=True, fmt=".0f", cmap="Blues", annot_kws=akws, center=0)

    plt.show()


def plot_roc_curve(y_true, y_pred):
    # ROC curve
    false_positive_rate = dict()
    true_positive_rate = dict()
    roc_auc = dict()
    number_of_classes = 2

    for i in range(number_of_classes):
        false_positive_rate[i], true_positive_rate[i], _ = roc_curve(y_true, y_pred)
        roc_auc[i] = auc(false_positive_rate[i], true_positive_rate[i])

    # Compute roc curve 'micro' and AUC
    false_positive_rate["micro"], true_positive_rate["micro"], _ = roc_curve(y_true.ravel(),
                                                                             y_pred.ravel())
    roc_auc["micro"] = auc(false_positive_rate["micro"], true_positive_rate["micro"])

    plt.figure()
    lw = 2
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])

    plt.plot(false_positive_rate["micro"], true_positive_rate["micro"], color='darkorange', lw=lw,
             label='AUC = %0.2f' % roc_auc["micro"])
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')

    plt.xlabel('Taux de faux positifs')
    plt.ylabel('Taux de vrais positifs')
    plt.title('Courbe ROC')
    plt.legend(loc="lower right")

    plt.show()

def find_the_thresholds_to_have_a_good_recall(predictions_of_the_grades):
    # We are looking for a compromise between the rate of true positives and the rate of false positives
    # The optimal threshold would be when true_positive_rate is high and false_positive_rate is low, ie:
    # true_positive_rate - (1-false-positive-rate) is zero or close to zero

    false_positive_rate, true_positive_rate, thresholds = roc_curve(predictions_of_the_grades['note'],
                                                                    predictions_of_the_grades['score'])

    i = np.arange(len(true_positive_rate))
    roc = pd.DataFrame({'false_positive_rate': pd.Series(false_positive_rate, index=i),
                        'true_positive_rate': pd.Series(true_positive_rate, index=i),
                        '1-false_positive_rate': pd.Series(1 - false_positive_rate, index=i),
                        'true_positive_rate-(1-false_positive_rate)': pd.Series(true_positive_rate - (1 - false_positive_rate), index=i),
                        'thresholds': pd.Series(thresholds, index=i)})

    # Plot true_positive_rate vs 1-false_positive_rate
    fig, ax = pl.subplots()
    pl.plot(roc['true_positive_rate'], color='blue', label='TVP')
    pl.plot(roc['1-false_positive_rate'], color='red', label='1-false_positive_rate')
    pl.xlabel('1-false_positive_rate')
    pl.ylabel('true_positive_rate')
    pl.title('ROC')
    plt.legend(loc="lower right")
    ax.set_xticklabels([])
    plt.show()

    roc = roc.iloc[(roc['true_positive_rate-(1-false_positive_rate)'] - 0).abs().argsort()[:1]]

    return roc
