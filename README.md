# Data Analysis Application

## Overview

The Data Analysis Application is a web-based tool for uploading, analyzing, and visualizing CSV data files. Developed with Django, it provides functionalities to handle missing values, generate plots, and display various statistics about the data.

## Features

- **Upload CSV Files**: Allows users to upload CSV files for analysis. Only CSV files are supported. Otherwise a warning is shown
- **Data Analysis**: Displays the head and summary statistics of the uploaded data.
- **Handle Missing Values**: Options to remove or fill missing values in the dataset.  
- **Visualization**: Generates histograms and combined histograms of numerical columns in the data.

## Installation

To set up and run the project locally, follow these steps:

1. **Ensure you have installed Python and VSCode(optional)**:
2.  **Clone the Repository using the web url**:
   https://github.com/cks844/Data_Analysis_Webapplication.git
3. **Navigate to the project folder by using the command in terminal**:
   cd project
4. **Install the required libraries by using the command in terminal**:
   pip install -r requirements.txt
5. **For Migration**:
   python manage.py migrate
6. **For running the application**:
   python manage.py runserver
7. **To access the application**:
   http://127.0.0.1:8000/ 
   
