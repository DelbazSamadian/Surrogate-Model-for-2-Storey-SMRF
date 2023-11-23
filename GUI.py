# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 14:25:09 2023

@author: Delbaz Samadian
PhD Student at Teesside University, Email:D.Samadian@tees.ac.uk
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import joblib

# Load the pre-trained ElasticNet model
best_elastic_net_model = joblib.load('best_elastic_net_model.joblib')

# Function to make predictions based on user input
def predict_output():
    try:
        # Get user input for the 10 features
        user_input = {
            'Sa(g)': float(entry_widgets['Sa(g)'].get()),
            'T1': float(entry_widgets['T1'].get()),
            'CAV': float(entry_widgets['CAV'].get()),
            'D95_D5': float(entry_widgets['D95_D5'].get()),
            'IA': float(entry_widgets['IA'].get()),
            'Omega': float(entry_widgets['Omega'].get()),
            'Lbay': float(entry_widgets['Lbay'].get()),
            'Fy': float(entry_widgets['Fy'].get()),
            'Es': float(entry_widgets['Es'].get()),
            'ϴp_Beam2': float(entry_widgets['ϴp_Beam2'].get())
        }

        # Convert the user input into a DataFrame
        user_input_df = pd.DataFrame([user_input])

        # Use the trained ElasticNet model to make predictions
        predicted_output = best_elastic_net_model.predict(user_input_df.values)

        # Display the predicted output
        result_label.config(text=f'Predicted Output: {predicted_output[0]:.6f}')
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for all features.")

# Create the main application window
app = tk.Tk()
app.title("ElasticNet Regression Predictor")

# Create and place input labels and entry widgets
input_labels = ['Sa(g)', 'T1', 'CAV', 'D95_D5', 'IA', 'Omega', 'Lbay', 'Fy', 'Es', 'ϴp_Beam2']

# Declare entry widgets for user input globally
entry_widgets = {}
for i, label in enumerate(input_labels):
    tk.Label(app, text=label + ":").grid(row=i, column=0, padx=10, pady=5, sticky="e")
    entry_widgets[label] = ttk.Entry(app, width=10, justify='center')
    entry_widgets[label].grid(row=i, column=1, padx=10, pady=5, sticky="w")

# Create the Predict button
predict_button = tk.Button(app, text="Predict", command=predict_output)
predict_button.grid(row=len(input_labels), column=0, columnspan=2, pady=10)

# Create a label for displaying the predicted output
result_label = tk.Label(app, text="")
result_label.grid(row=len(input_labels) + 1, column=0, columnspan=2, pady=10)

# Run the application
app.mainloop()



#%%
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import joblib

# Load the pre-trained ElasticNet model
best_elastic_net_model = joblib.load('best_elastic_net_model.joblib')

# Load mean and standard deviation values
mean_std_values = pd.read_csv('mean_std_values.csv', index_col=0)

# Function to make predictions based on user input

def predict_output():
    try:
        # Get user input for the 10 features
        user_input = {
            'Sa(g)': pd.to_numeric(entry_widgets['Sa(g)'].get(), errors='coerce'),
            'T1': pd.to_numeric(entry_widgets['T1'].get(), errors='coerce'),
            'CAV': pd.to_numeric(entry_widgets['CAV'].get(), errors='coerce'),
            'D95_D5': pd.to_numeric(entry_widgets['D95_D5'].get(), errors='coerce'),
            'IA': pd.to_numeric(entry_widgets['IA'].get(), errors='coerce'),
            'Omega': pd.to_numeric(entry_widgets['Omega'].get(), errors='coerce'),
            'Lbay': pd.to_numeric(entry_widgets['Lbay'].get(), errors='coerce'),
            'Fy': pd.to_numeric(entry_widgets['Fy'].get(), errors='coerce'),
            'Es': pd.to_numeric(entry_widgets['Es'].get(), errors='coerce'),
            'ϴp_Beam2': pd.to_numeric(entry_widgets['ϴp_Beam2'].get(), errors='coerce')
        }

        print("User Input (Raw):", user_input)

        # Convert the user input into a DataFrame
        user_input_df = pd.DataFrame([user_input])

        print("User Input (DataFrame):")
        print(user_input_df)

        # Check for NaN values in the DataFrame
        if user_input_df.isna().any().any():
            problematic_features = user_input_df.columns[user_input_df.isna().any()].tolist()
            raise ValueError(f"Input contains non-numeric values in features: {problematic_features}")

        # Standardize the user input using the loaded mean and standard deviation values
        user_input_std = (user_input_df - mean_std_values['mean']) / mean_std_values['std']

        print("User Input (Standardized):")
        print(user_input_std)

        # Use the trained ElasticNet model to make predictions on the standardized input
        predicted_output = best_elastic_net_model.predict(user_input_std.values)

        # Display the predicted output
        result_label.config(text=f'Predicted Output: {predicted_output[0]:.6f}')
    except ValueError as e:
        messagebox.showerror("Error", str(e))


# Create the main application window
app = tk.Tk()
app.title("ElasticNet Regression Predictor")

# Create and place input labels and entry widgets
input_labels = ['Sa(g)', 'T1', 'CAV', 'D95_D5', 'IA', 'Omega', 'Lbay', 'Fy', 'Es', 'ϴp_Beam2']

# Declare entry widgets for user input globally
entry_widgets = {}
for i, label in enumerate(input_labels):
    tk.Label(app, text=label + ":").grid(row=i, column=0, padx=10, pady=5, sticky="e")
    entry_widgets[label] = ttk.Entry(app, width=10, justify='center')
    entry_widgets[label].grid(row=i, column=1, padx=10, pady=5, sticky="w")

# Create the Predict button
predict_button = tk.Button(app, text="Predict", command=predict_output)
predict_button.grid(row=len(input_labels), column=0, columnspan=2, pady=10)

# Create a label for displaying the predicted output
result_label = tk.Label(app, text="")
result_label.grid(row=len(input_labels) + 1, column=0, columnspan=2, pady=10)

# Run the application
app.mainloop()

