
import os
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-GUI
from .forms import CSVUploadForm
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.conf import settings
import pickle
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Create your views here.


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            csv_file = request.FILES['file']

            # Define the directory to save the file
            data_directory = os.path.join(settings.STATIC_ROOT, 'data')
            os.makedirs(data_directory, exist_ok=True)  # Create the directory if it doesn't exist

            # Define the full path to save the file
            file_path = os.path.join(data_directory, csv_file.name)

            # Save the file
            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            return render(request, 'myapp/upload_success.html')  # Redirect or render success page
    else:
        form = CSVUploadForm()
    return render(request, 'myapp/upload.html', {'form': form})


def dashboard(request):
    return render(request, 'myapp/dashboard.html')




def descriptive_statistics(request):
    # Define the path to the CSV file
    csv_file_path = os.path.join(settings.STATIC_ROOT, 'data', 'merged_output.csv')

    # Check if the file exists
    if os.path.exists(csv_file_path):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)

        # Calculate descriptive statistics
        stats = df.describe(include='all')  # Include all columns, numeric and categorical

        # Convert the DataFrame to HTML for rendering
        stats_html = stats.to_html(classes='table table-striped', border=0)

        return render(request, 'myapp/descriptive_statistics.html', {'stats': stats_html})
    else:
        return render(request, 'myapp/descriptive_statistics.html', {'error': 'CSV file not found.'})



def correlation_heatmap(request):
    # Load the CSV file
    csv_file_path = os.path.join(settings.STATIC_ROOT, 'data', 'merged_output.csv')
    df = pd.read_csv(csv_file_path)

    # Convert 'timestamp_EST' to datetime
    df['timestamp_EST'] = pd.to_datetime(df['timestamp_EST'])

    # Extract features from the datetime column
    df['year'] = df['timestamp_EST'].dt.year
    df['month'] = df['timestamp_EST'].dt.month
    df['day'] = df['timestamp_EST'].dt.day
    df['hour'] = df['timestamp_EST'].dt.hour

    # Calculate the correlation matrix
    correlation_matrix = df.corr()

    # Generate the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
    plt.title('Correlation Heatmap')

    # Save the heatmap to a file
    heatmap_file_path = os.path.join(settings.STATIC_ROOT, 'data', 'images', 'correlation_heatmap.png')
    plt.savefig(heatmap_file_path)
    plt.close()

    return render(request, 'myapp/correlation_heatmap.html', {'heatmap_file': 'data/images/correlation_heatmap.png'})


# Load dataset
df = pd.read_csv('static/data/merged_output.csv')
df['timestamp_EST'] = pd.to_datetime(df['timestamp_EST'])
df['month'] = df['timestamp_EST'].dt.month
df['day'] = df['timestamp_EST'].dt.day
df['hour'] = df['timestamp_EST'].dt.hour

features = ['temp_TX', 'humidity_TX', 'month', 'day', 'hour']
target_columns = [
    'hourly_consumption_education_kwh',
    'hourly_consumption_food_service_kwh',
    'hourly_consumption_healthcare_kwh',
    'hourly_consumption_lodging_kwh',
    'hourly_consumption_mercantile_kwh',
    'hourly_consumption_mobile_home_kwh',
    'hourly_consumption_multi_fam_2_4_kwh',
    'hourly_consumption_multi_fam_5plus_kwh',
    'hourly_consumption_office_kwh',
    'hourly_consumption_single_fam_attached_kwh',
    'hourly_consumption_single_fam_detached_kwh',
    'hourly_consumption_warehouse_and_storage_kwh'
]

def build_model(target):
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return mse, r2

def predictive_model_metrics(request):
    metrics = {}
    for target in target_columns:
        mse, r2 = build_model(target)
        metrics[target] = {'MSE': mse, 'R_squared': r2}
    return render(request, 'myapp/predictive_model_metrics.html', {'metrics': metrics})





def predictive_models(request):
    return render(request, 'myapp/predictive_models.html')


# Define views for each predictive model

def education_energy_prediction(request):
    prediction = None
    if request.method == 'POST':
        temp_TX = float(request.POST['temp_TX'])
        humidity_TX = float(request.POST['humidity_TX'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[temp_TX, humidity_TX, month, day, hour]], columns=features)

        # Load the model and make prediction
        model = RandomForestRegressor()  # You can load a saved model if needed
        model.fit(df[features], df['hourly_consumption_education_kwh'])  # Train on the full dataset for prediction
        prediction = model.predict(input_data)[0]

    return render(request, 'myapp/education_energy_prediction.html', {'prediction': prediction})


def food_services_energy_prediction(request):
    prediction = None
    if request.method == 'POST':
        temp_TX = float(request.POST['temp_TX'])
        humidity_TX = float(request.POST['humidity_TX'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[temp_TX, humidity_TX, month, day, hour]], columns=features)

        # Load the model and make prediction
        model = RandomForestRegressor()  # You can load a saved model if needed
        model.fit(df[features], df['hourly_consumption_food_service_kwh'])  # Train on the full dataset for prediction
        prediction = model.predict(input_data)[0]
    return render(request, 'myapp/food_services_energy_prediction.html', {'prediction': prediction})


def healthcare_energy_prediction(request):
    prediction = None
    if request.method == 'POST':
        temp_TX = float(request.POST['temp_TX'])
        humidity_TX = float(request.POST['humidity_TX'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[temp_TX, humidity_TX, month, day, hour]], columns=features)

        # Load the model and make prediction
        model = RandomForestRegressor()  # You can load a saved model if needed
        model.fit(df[features], df['hourly_consumption_healthcare_kwh'])  # Train on the full dataset for prediction
        prediction = model.predict(input_data)[0]
    return render(request, 'myapp/healthcare_energy_prediction.html',{'prediction': prediction})


def lodging_energy_prediction(request):
    prediction = None
    if request.method == 'POST':
        temp_TX = float(request.POST['temp_TX'])
        humidity_TX = float(request.POST['humidity_TX'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[temp_TX, humidity_TX, month, day, hour]], columns=features)

        # Load the model and make prediction
        model = RandomForestRegressor()  # You can load a saved model if needed
        model.fit(df[features], df['hourly_consumption_lodging_kwh'])  # Train on the full dataset for prediction
        prediction = model.predict(input_data)[0]
    return render(request, 'myapp/lodging_energy_prediction.html', {'prediction': prediction})

def mercantile_energy_prediction(request):
    prediction = None
    if request.method == 'POST':
        temp_TX = float(request.POST['temp_TX'])
        humidity_TX = float(request.POST['humidity_TX'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[temp_TX, humidity_TX, month, day, hour]], columns=features)

        # Load the model and make prediction
        model = RandomForestRegressor()  # You can load a saved model if needed
        model.fit(df[features], df['hourly_consumption_mercantile_kwh'])  # Train on the full dataset for prediction
        prediction = model.predict(input_data)[0]
    return render(request, 'myapp/mercantile_energy_prediction.html', {'prediction': prediction})

def mobile_home_energy_prediction(request):
    prediction = None
    if request.method == 'POST':
        temp_TX = float(request.POST['temp_TX'])
        humidity_TX = float(request.POST['humidity_TX'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[temp_TX, humidity_TX, month, day, hour]], columns=features)

        # Load the model and make prediction
        model = RandomForestRegressor()  # You can load a saved model if needed
        model.fit(df[features], df['hourly_consumption_mobile_home_kwh'])  # Train on the full dataset for prediction
        prediction = model.predict(input_data)[0]
    return render(request, 'myapp/mobile_home_energy_prediction.html', {'prediction': prediction})

def multifamily_2_4_energy_prediction(request):
    prediction = None
    if request.method == 'POST':
        temp_TX = float(request.POST['temp_TX'])
        humidity_TX = float(request.POST['humidity_TX'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[temp_TX, humidity_TX, month, day, hour]], columns=features)

        # Load the model and make prediction
        model = RandomForestRegressor()  # You can load a saved model if needed
        model.fit(df[features], df['hourly_consumption_multi_fam_2_4_kwh'])  # Train on the full dataset for prediction
        prediction = model.predict(input_data)[0]
    return render(request, 'myapp/multifamily_2_4_energy_prediction.html', {'prediction': prediction})


def multifamily_5plus_energy_prediction(request):
    prediction = None
    if request.method == 'POST':
        temp_TX = float(request.POST['temp_TX'])
        humidity_TX = float(request.POST['humidity_TX'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[temp_TX, humidity_TX, month, day, hour]], columns=features)

        # Load the model and make prediction
        model = RandomForestRegressor()  # You can load a saved model if needed
        model.fit(df[features], df['hourly_consumption_multi_fam_5plus_kwh'])  # Train on the full dataset for prediction
        prediction = model.predict(input_data)[0]
    return render(request, 'myapp/multifamily_5plus_energy_prediction.html', {'prediction': prediction})

def office_energy_prediction(request):
    prediction = None
    if request.method == 'POST':
        temp_TX = float(request.POST['temp_TX'])
        humidity_TX = float(request.POST['humidity_TX'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[temp_TX, humidity_TX, month, day, hour]], columns=features)

        # Load the model and make prediction
        model = RandomForestRegressor()  # You can load a saved model if needed
        model.fit(df[features], df['hourly_consumption_office_kwh'])  # Train on the full dataset for prediction
        prediction = model.predict(input_data)[0]
    return render(request, 'myapp/office_energy_prediction.html', {'prediction': prediction})

def single_family_attached_energy_prediction(request):
    prediction = None
    if request.method == 'POST':
        temp_TX = float(request.POST['temp_TX'])
        humidity_TX = float(request.POST['humidity_TX'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[temp_TX, humidity_TX, month, day, hour]], columns=features)

        # Load the model and make prediction
        model = RandomForestRegressor()  # You can load a saved model if needed
        model.fit(df[features], df['hourly_consumption_single_fam_attached_kwh'])  # Train on the full dataset for prediction
        prediction = model.predict(input_data)[0]
    return render(request, 'myapp/single_family_attached_energy_prediction.html', {'prediction': prediction})

def single_family_detached_energy_prediction(request):
    prediction = None
    if request.method == 'POST':
        temp_TX = float(request.POST['temp_TX'])
        humidity_TX = float(request.POST['humidity_TX'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[temp_TX, humidity_TX, month, day, hour]], columns=features)

        # Load the model and make prediction
        model = RandomForestRegressor()  # You can load a saved model if needed
        model.fit(df[features], df['hourly_consumption_single_fam_detached_kwh'])  # Train on the full dataset for prediction
        prediction = model.predict(input_data)[0]
    return render(request, 'myapp/single_family_detached_energy_prediction.html', {'prediction': prediction})

def warehouse_energy_prediction(request):
    prediction = None
    if request.method == 'POST':
        temp_TX = float(request.POST['temp_TX'])
        humidity_TX = float(request.POST['humidity_TX'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[temp_TX, humidity_TX, month, day, hour]], columns=features)

        # Load the model and make prediction
        model = RandomForestRegressor()  # You can load a saved model if needed
        model.fit(df[features], df['hourly_consumption_warehouse_and_storage_kwh'])  # Train on the full dataset for prediction
        prediction = model.predict(input_data)[0]
    return render(request, 'myapp/warehouse_energy_prediction.html', {'prediction': prediction})
