import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)
data_file = "./datas/Book.csv"  # Uisti sa, že cesta k súboru je správna

df = pd.DataFrame()

# Load the CSV file
def load_data():
    return pd.read_csv(data_file, delimiter=";")

# Function that adds new data to the DataFrame
def new_datas(name, who_name, reason, date):
    new_data = pd.DataFrame({'Person': [name], 'Meet with': [who_name], 'Why': [reason], 'Date': [date]})
    return new_data

# Save the updated DataFrame to CSV
def save_data(df):
    df.to_csv(data_file, index=False, sep=";")

if __name__ == "__main__":
    app.run(debug=True)
