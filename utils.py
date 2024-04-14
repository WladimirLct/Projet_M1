import pandas as pd

def detect_crop(row):
    if row['M-bin']:
        return 'M'
    elif row['E-bin']:
        return 'E'
    elif row['S-bin']:
        return 'S'
    else:
        return 'C'
    
def get_history():
    base_path = "./Data/Export/"
    try:
        df = pd.read_csv(base_path + 'Report/Oxford.csv', sep=';')
        history = []
        
        for _, row in df.iterrows():
            name = row[0]  # First column
            score = ''.join(map(str, row[1:5]))  # Concatenate values from second to fourth column
            history.append({'name': name, 'score': score, 'date': row[9], 'filesize': int(row[10]/1_000_000)})
        return history
    
    except FileNotFoundError:
        return False




  