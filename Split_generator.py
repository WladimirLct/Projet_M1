import os
import pandas as pd
import random
import shutil

# text.py
import sys

seed = None
if len(sys.argv) > 1:
    seed = int(sys.argv[1])
    print(f"Received seed: {seed}")
else:
    seed = random.randint(-1000, 1000)
    print(f"No seed provided.\nSeed is {seed}")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

dataset_folder = "./DataClassification/Dataset_glomeruli/"
files_normal = os.listdir(dataset_folder + "normal")
files_sclerosed = os.listdir(dataset_folder + "sclerosed")

def create_df(files, label):
    df = pd.DataFrame(files, columns=['filename'])
    df['label'] = label
    return df

# Add these file names to a pandas dataframe
df_normal = create_df(files_normal, 'normal')
df_sclerosed = create_df(files_sclerosed, 'sclerosed')

# Concatenate the two dataframes
df = pd.concat([df_normal, df_sclerosed], ignore_index=True)

def get_ID(files):
    IDs = []
    for file in files :
        if file.split('_')[2].isdigit() or 'caso' in file.split('_')[2]:
            numero = file.split('_')[2]
        else:
            numero = file.split('_')[3]
        IDs.append(numero)
    return IDs
    
# Extract the patient ID from the filename
df['patient_id'] = get_ID(df['filename'])

# Group by 'patient_id' and calculate both counts and normalized counts
counts = df.groupby('patient_id')['label'].value_counts().unstack(fill_value=0)
percentages = df.groupby('patient_id')['label'].value_counts(normalize=True).unstack(fill_value=0)

# Rename columns for clarity
counts.columns = [f'count_{label}' for label in counts.columns]
percentages.columns = [f'percentage_{label}' for label in percentages.columns]

# Merge the counts and percentages
grouped = pd.concat([counts, percentages], axis=1)

# Sort columns by patient_id
grouped = grouped.reindex(sorted(grouped.columns), axis=1)

# Total number of images
total_images = len(df)

# Calculate percentages of normal and sclerosed images
grouped['percentage_normal_images'] = (grouped['count_normal'] / total_images) 
grouped['percentage_sclerosed_images'] = (grouped['count_sclerosed'] / total_images) 

# Assuming 'grouped' DataFrame already contains normalized percentages
# Calculate the total percentage of images for each patient
grouped['total_percentage_images'] = grouped['percentage_normal_images'] + grouped['percentage_sclerosed_images']

# Sort the patients by their total percentage of images
grouped = grouped.sort_values('total_percentage_images', ascending=False)

# Obtenez un échantillon aléatoire des indices des lignes du dataframe
current_indices = list(range(len(grouped)))

random.seed(seed)
random.shuffle(current_indices)

# Set the indices to the grouped dataframe
grouped = grouped.iloc[current_indices]

category_1_count = 0
category_2_count = 0
category_3_count = 0
category_1_count_norm = 0
category_1_count_scler = 0
category_2_count_norm = 0
category_2_count_scler = 0
# Create a list of zeros to store the categories
categories = [0] * len(grouped)

def test_category_2(row):
    global category_2_count, category_2_count_norm, category_2_count_scler
    if category_2_count < 0.2 and category_2_count + row['total_percentage_images'] < 0.2:
        if category_2_count_scler + row['percentage_sclerosed_images'] <= 0.1 and category_2_count_norm + row['percentage_normal_images'] <= 0.1:
            categories[idx] = 2
            category_2_count += row['total_percentage_images']
            category_2_count_norm += row['percentage_normal_images']
            category_2_count_scler += row['percentage_sclerosed_images']
            return True
    return False

for idx in current_indices:
    row = grouped.iloc[idx]
    idx = int(idx)  # Convertir l'index en entier

    if category_1_count < 0.6 and category_1_count + row['total_percentage_images'] <= 0.65:
        if category_1_count_scler + row['percentage_sclerosed_images'] <= 0.3 and category_1_count_norm + row['percentage_normal_images'] <= 0.3:
            categories[idx] = 1
            category_1_count += row['total_percentage_images']
            category_1_count_norm += row['percentage_normal_images']
            category_1_count_scler += row['percentage_sclerosed_images']
        else:
            if (not test_category_2(row)):
                categories[idx] = 3
                category_3_count += row['total_percentage_images']
    else:
        if (not test_category_2(row)):
            categories[idx] = 3
            category_3_count += row['total_percentage_images']

# Add the 'category' column to the DataFrame
grouped['category'] = categories

# Fusionner les dataframes en utilisant les colonnes "filename" et "patient_id"
merged_df = pd.merge(df, grouped, left_on='patient_id', right_index=True)

# Créer les dataframes à partir des listes de noms de fichiers et de labels
categories = [[], [], []]
# Itérer sur les lignes du dataframe fusionné
for index, row in merged_df.iterrows():
    filename = row['filename']
    category = row['category']
    label = row['label']  # Ajouter la colonne "label"

    # According to the category, add the filename and label to the corresponding dataframe
    if category == 1:
        categories[0].append({'filename': filename, 'label': label})
    elif category == 2:
        categories[1].append({'filename': filename, 'label': label})
    elif category == 3:
        categories[2].append({'filename': filename, 'label': label})

# Turn the lists into dataframes
categories = [pd.DataFrame(category) for category in categories]

# Chemin des dossiers "normal" et "sclerosed"
normal_folder_path = r'./DataClassification/Dataset_glomeruli/normal'
sclerosed_folder_path = r'./DataClassification/Dataset_glomeruli/sclerosed'

# Dossiers de destination pour les copies
destinations = [
    r'./DataClassification/Split_dataset/Train',
    r'./DataClassification/Split_dataset/Valid',
    r'./DataClassification/Split_dataset/Test'
]

# Create the folders if they don't exist
for destination_folder in destinations:
    for categ in ['normal', 'sclerosed']:
        if not os.path.exists(os.path.join(destination_folder, categ)):
            os.makedirs(os.path.join(destination_folder, categ))
        if os.path.exists(os.path.join(destination_folder, categ)):
            for file in os.listdir(os.path.join(destination_folder, categ)):
                os.remove(os.path.join(os.path.join(destination_folder, categ), file))

# Copy the files to the corresponding folders
for idx in range(len(categories)):
    for index, row in categories[idx].iterrows():
        filename = row['filename']
        label = row['label']

        if label == 'normal':
            shutil.copyfile(os.path.join(normal_folder_path, filename), os.path.join(destinations[idx], "normal", filename))
        elif label == 'sclerosed':
            shutil.copyfile(os.path.join(sclerosed_folder_path, filename), os.path.join(destinations[idx], "sclerosed", filename))

# Show by normal and sclerosed and a total by category
for idx in range(len(categories)):
    print(f"{destinations[idx]} :")
    for categ in ['normal', 'sclerosed']:
        print(f"\t{categ} : {len(os.listdir(os.path.join(destinations[idx], categ)))}")
    print(f"\tTotal : {len(os.listdir(os.path.join(destinations[idx], 'normal'))) + len(os.listdir(os.path.join(destinations[idx], 'sclerosed')))}")

# Show the total number of images
print(f"\nTotal : {len(os.listdir(os.path.join(destinations[0], 'normal'))) + len(os.listdir(os.path.join(destinations[0], 'sclerosed')))} + {len(os.listdir(os.path.join(destinations[1], 'normal'))) + len(os.listdir(os.path.join(destinations[1], 'sclerosed')))} + {len(os.listdir(os.path.join(destinations[2], 'normal'))) + len(os.listdir(os.path.join(destinations[2], 'sclerosed')))} = {len(os.listdir(os.path.join(destinations[0], 'normal'))) + len(os.listdir(os.path.join(destinations[0], 'sclerosed'))) + len(os.listdir(os.path.join(destinations[1], 'normal'))) + len(os.listdir(os.path.join(destinations[1], 'sclerosed'))) + len(os.listdir(os.path.join(destinations[2], 'normal'))) + len(os.listdir(os.path.join(destinations[2], 'sclerosed')))}")