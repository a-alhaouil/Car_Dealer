from django.shortcuts import render
from django.http import JsonResponse
from .forms import PredictionForm
import joblib
import numpy as np
import pandas as pd
# from tensorflow.keras.models import load_model

# Load the models
scaler = joblib.load(r'C:\Users\abdes\Desktop\MIAAD\S3\Data_Mining\Car_Dealer\car_dealer\predictor\models\8_cl_scaler.pkl')
decision_tree = joblib.load(r'C:\Users\abdes\Desktop\MIAAD\S3\Data_Mining\Car_Dealer\car_dealer\predictor\models\8_cl_decision_tree_model.pkl')
random_forest = joblib.load(r'C:\Users\abdes\Desktop\MIAAD\S3\Data_Mining\Car_Dealer\car_dealer\predictor\models\8_cl_random_forest_model.pkl')
svm = joblib.load(r'C:\Users\abdes\Desktop\MIAAD\S3\Data_Mining\Car_Dealer\car_dealer\predictor\models\8_cl_svm_model.pkl')
naive_bayes = joblib.load(r'C:\Users\abdes\Desktop\MIAAD\S3\Data_Mining\Car_Dealer\car_dealer\predictor\models\8_cl_naive_bayes_model.pkl')
# tf_model = load_model(r'C:\Users\abdes\Desktop\MIAAD\S3\Data_Mining\Car_Dealer\car_dealer\predictor\models\8_cl_my_neural_network_model.h5')
# Home page view

# Load the catalogue data
catalogue_file = r'C:\Users\abdes\Desktop\MIAAD\S3\Data_Mining\Car_Dealer\car_dealer\predictor\data\Catalogue_8Clusters.xlsx'  # Update with actual file path
catalogue_data = pd.read_excel(catalogue_file)

def index(request):
    form = PredictionForm()
    return render(request, r'C:\Users\abdes\Desktop\MIAAD\S3\Data_Mining\Car_Dealer\car_dealer\predictor\templates\index.html', {'form': form})

# Prediction view
def predict(request):
    if request.method == 'POST':
        new_category_mapping = {
            2: "Mini",
            6: "Economy",
            4: "Small Compact",
            7: "Large Compact",
            0: "standard",
            5: "Luxury v1.0",
            3: "Luxury",
            1: "Sports Car",

        }
        form = PredictionForm(request.POST)
        if form.is_valid():

            # Extract data from form
            age = form.cleaned_data['age']
            sexe = bool(int(form.cleaned_data['sexe']))
            taux = form.cleaned_data['taux']
            situationFamiliale = bool(int(form.cleaned_data['situationFamiliale']))
            nbEnfantsAcharge = form.cleaned_data['nbEnfantsAcharge']
            deuxieme_voiture = bool(int(form.cleaned_data['deuxieme_voiture']))

            # Combine inputs into a single array
            input_data = np.array([[age, sexe, taux, situationFamiliale, nbEnfantsAcharge, deuxieme_voiture]])

            # Scale the data
            scaled_data = scaler.transform(input_data)


            # Make predictions with each model
            predicted_category = random_forest.predict(scaled_data)[0]
            # prediction_dt = decision_tree.predict(scaled_data)[0]
            # prediction_svm = svm.predict(scaled_data)[0]
            # prediction_nb = naive_bayes.predict(scaled_data)[0]
            # TensorFlow prediction
            # y_pred_tf = tf_model.predict(scaled_data)
            # prediction_tf = y_pred_tf.argmax(axis=1)[0]


            predicted_category = new_category_mapping[predicted_category]

            filtered_cars = catalogue_data[catalogue_data['category'] == predicted_category]



            # Return predictions as JSON response
            return render(request, r'C:\Users\abdes\Desktop\MIAAD\S3\Data_Mining\Car_Dealer\car_dealer\predictor\templates\car_list.html', {
                'category': predicted_category,
                'cars': filtered_cars.to_dict(orient='records'),
            })

    return JsonResponse({'error': 'Invalid form submission'})


def category_cars(request):
    # Load the catalogue data
    catalogue_file = 'predictor/data/Catalogue_8Clusters.xlsx'  # Update with the actual path
    catalogue_data = pd.read_excel(catalogue_file)

    # Get the unique categories
    categories = catalogue_data['category'].unique()

    # Check if a category is selected
    selected_category = request.GET.get('category', None)

    # Filter cars by the selected category
    if selected_category:
        filtered_cars = catalogue_data[catalogue_data['category'] == selected_category]
        cars = filtered_cars.to_dict(orient='records')
    else:
        cars = []

    # Pass the data to the template
    return render(request, r'C:\Users\abdes\Desktop\MIAAD\S3\Data_Mining\Car_Dealer\car_dealer\predictor\templates\category_cars.html', {
        'categories': categories,
        'selected_category': selected_category,
        'cars': cars,
    })
def car_list(request):


    # Group cars by category
    grouped_cars = catalogue_data.groupby('category')

    # Convert grouped data to a dictionary
    car_dict = {category: group.to_dict(orient='records') for category, group in grouped_cars}

    # Pass the grouped data to the template
    return render(request, r'C:\Users\abdes\Desktop\MIAAD\S3\Data_Mining\Car_Dealer\car_dealer\predictor\templates\car_details.html', {'car_dict': car_dict})
