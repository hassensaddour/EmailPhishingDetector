import pandas as pd


def load_data():
    # Load CSV data
    df = pd.read_csv('CEAS_08.csv')

    # Select necessary columns
    df = df[['sender', 'subject', 'body', 'urls', 'label']]

    # Fill missing values and clean text
    df['sender'] = df['sender'].fillna('').str.lower()
    df['subject'] = df['subject'].fillna('').str.lower()
    df['body'] = df['body'].fillna('').str.lower()
    df['urls'] = df['urls'].fillna(0)

    return df

