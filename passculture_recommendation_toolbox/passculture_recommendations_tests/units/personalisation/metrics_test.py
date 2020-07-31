from passculture_recommendations.personalisation.metrics import accuracy_recall_precision_f1

def test_accuracy_recall_precision_f1_should_print_the_metrics():
    # Given
    y_true = [1,0,0]
    y_pred = [0,0,0]

    # When
    x = accuracy_recall_precision_f1(y_true, y_pred)

    # Then
    assert x == None
