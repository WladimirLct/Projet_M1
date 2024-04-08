def detect_crop(row):
    if row['M-bin']:
        return 'M'
    elif row['E-bin']:
        return 'E'
    elif row['S-bin']:
        return 'S'
    else:
        return 'C'