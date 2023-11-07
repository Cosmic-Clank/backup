from django.shortcuts import render
from django.http import HttpResponse
import os

from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
# Create your views here.

def handle_uploaded_file(f, filename):
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def index(request):
    if request.method == 'POST':
        # Check if a crypto address has been entered
        address = request.POST.get('address', '').strip()
        if address:
            # Process the entered crypto address
            pass  # replace with your processing logic
        
        # Check if a file has been uploaded
        file = request.FILES.get('file')
        if file:
            # Process the uploaded file
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            filename = os.path.join(BASE_DIR, 'uploads', file.name)
            handle_uploaded_file(file, filename)
            # Now you can open and process the file

            testing_data = pd.read_csv(f"{BASE_DIR}/uploads/{file.name}")
            testing_data_original = testing_data.copy()
            testing_data['bytecode_split'] = testing_data['bytecode'].apply(lambda x: ' '.join(x[i:i+2] for i in range(0, len(x), 2)))
            svm_model = load(f'{BASE_DIR}/svm_model.joblib')
            
            vectorizer = load(f'{BASE_DIR}/svm_vectorizer.joblib')
            vectorized_testing_data = vectorizer.transform(testing_data['bytecode_split'])
            
            test_predictions = svm_model.predict(vectorized_testing_data)
            
            testing_data['actual_is_vulnerable'] = testing_data['is_vulnerable']
            
            testing_data['is_vulnerable'] = test_predictions

            testing_data['ai_prediction'] = testing_data.apply(lambda row: 'CORRECT' if row['is_vulnerable'] == row['actual_is_vulnerable'] else 'INCORRECT', axis=1)
            
            
            testing_data['bytecode'] = testing_data['bytecode'].str[:50] + '...'
            # testing_data_original['bytecode'] = testing_data_original['bytecode'].str[:100] + '...'
            testing_data['is_vulnerable'] = testing_data['is_vulnerable'].map({0: "NO", 1: "YES"})
            # testing_data_original['is_vulnerable'] = testing_data_original['is_vulnerable'].map({0: "NO", 1: "YES"})
            testing_data['actual_is_vulnerable'] = testing_data['actual_is_vulnerable'].map({0: "NO", 1: "YES"})


            accuracy = accuracy_score(testing_data_original['is_vulnerable'].values, test_predictions)
            report = classification_report(testing_data_original['is_vulnerable'].values, test_predictions, output_dict=True)
        # After processing, you can redirect or send a response
        return render(request, "smartcontract/metrics.html", {"dataframe": testing_data, "metrics_dataframe": testing_data, "percentages": [("Accuracy", accuracy*100), ("Precision", report["1"]["precision"]*100), ("Recall", report["1"]["recall"]*100), ("f1-score", report["1"]["f1-score"]*100)]})
    
    # If not a POST request, just render the template
    return render(request, 'smartcontract/index.html')