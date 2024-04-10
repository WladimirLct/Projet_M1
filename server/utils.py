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
    base_path = "./Data/Export/cascade_R_50_FPN_3x/"
    try:
        df = pd.read_csv(base_path + '/Report/M-efficientnetv2-m_E-efficientnetv2-m_S-densenet161_C-mobilenetv2/Oxford.csv', sep=';')
        history = []
        
        for _, row in df.iterrows():
            name = row[0]  # First column
            score = ''.join(map(str, row[1:5]))  # Concatenate values from second to fourth column
            history.append({'name': name, 'score': score})
        return history
    except FileNotFoundError:
        return False




  