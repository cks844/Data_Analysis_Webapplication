from django.shortcuts import render, redirect
from .forms import UploadFileForm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import urllib, base64

# To save the uploaded file to the server
def handle_uploaded_file(file):
    file_path = os.path.join('media', file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path

# To generate plots
def generate_plot(df):
    numerical_columns = df.select_dtypes(include=['float', 'int']).drop(columns=['ID'], errors='ignore')
    if not numerical_columns.empty:
        num_cols = len(numerical_columns.columns)
        fig, axes = plt.subplots(num_cols + 1, 1, figsize=(10, 6 * (num_cols + 1)))

        if num_cols == 1:
            axes = [axes]  

        # Histogram for all numerical columns
        for ax, column in zip(axes[:-1], numerical_columns.columns):
            sns.histplot(numerical_columns[column], ax=ax)
            ax.set_title(f'Histogram of {column}')

        # Combined histogram 
        combined_data = pd.concat([numerical_columns[col].dropna() for col in numerical_columns.columns])
        sns.histplot(combined_data, ax=axes[-1], kde=True)
        axes[-1].set_title('Combined Histogram of All Numerical Columns')

        buf = io.BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        return uri
    else:
        return None

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = handle_uploaded_file(request.FILES['file'])
            df = pd.read_csv(file_path, low_memory=False) # To read the file using pandas

            head = df.head() # For showing the head of uploaded data
            summary = df.describe() # For showing the summary of the data
            missing_values = df.isnull().sum() # For finding the number of null values in each columns
            numerical_missing_values = df.select_dtypes(include=['float', 'int']).drop(columns=['ID'], errors='ignore').isnull().sum()
            numerical_missing_values = numerical_missing_values[numerical_missing_values > 0]

            plot_uri = generate_plot(df)

            context = {
                'file_path': file_path,
                'head': head.to_html(),
                'summary': summary.to_html(),
                'missing_values': missing_values.to_dict(),
                'plot_uri': plot_uri,
                'numerical_missing_values': numerical_missing_values.to_dict(),
                'new_head': None  
            }

            request.session['df_path'] = file_path
            request.session['df'] = df.to_json()

            return render(request, 'csv_analysis_app/results.html', context)
    else:
        form = UploadFileForm()
    return render(request, 'csv_analysis_app/landing.html', {'form': form})

# Function for removing the null values 
def remove_missing_values(request):
    file_path = request.session.get('df_path')
    if not file_path:
        return redirect('upload_file')

    df = pd.read_json(request.session.get('df'))

    numerical_columns = df.select_dtypes(include=['float', 'int']).drop(columns=['ID'], errors='ignore')
    df_cleaned = numerical_columns.dropna(axis=0, how='any') # dropping rows with null values

    cleaned_summary = df_cleaned.describe().to_html()

    context = {
        'head': df.head().to_html(),  
        'new_head': df_cleaned.head().to_html(),  
        'summary': df_cleaned.describe().to_html(),
        'missing_values': df_cleaned.isnull().sum().to_dict(),
        'plot_uri': generate_plot(df_cleaned),
        'cleaned_summary': cleaned_summary,
        'numerical_missing_values': df_cleaned.select_dtypes(include=['float', 'int']).isnull().sum().to_dict(),
    }

    request.session['df'] = df_cleaned.to_json()

    return render(request, 'csv_analysis_app/results.html', context)

# Function for filling the columns with values
def fill_missing_values(request):
    file_path = request.session.get('df_path')
    if not file_path:
        return redirect('upload_file')

    df = pd.read_json(request.session.get('df'))

    numerical_columns = df.select_dtypes(include=['float', 'int']).drop(columns=['ID'], errors='ignore')
    if not numerical_columns.empty:
        df[numerical_columns.columns] = numerical_columns.fillna(numerical_columns.mean()) # filling missing values with mean value

    filled_summary = df.describe().to_html()

    context = {
        'head': df.head().to_html(),  
        'new_head': df.head().to_html(),  
        'summary': df.describe().to_html(),
        'missing_values': df.isnull().sum().to_dict(),
        'plot_uri': generate_plot(df),
        'cleaned_summary': filled_summary,
        'numerical_missing_values': df.select_dtypes(include=['float', 'int']).isnull().sum().to_dict(),
    }

    request.session['df'] = df.to_json()

    return render(request, 'csv_analysis_app/results.html', context)
