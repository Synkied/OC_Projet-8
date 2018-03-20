import pandas as pd

csv_file = pd.read_csv(
    'db_file.csv',
    sep=";",
    encoding="utf-8",
    low_memory=False
)

unique_value_list = csv_file['brands'].unique()

brands_list_split = [
    i.split(",") for i in unique_value_list if type(i) is not float
]

brands_set = set()
for brands_list in brands_list_split:
    for brand in brands_list:
        brands_set.add(brand.strip().capitalize())

print(len(brands_set))
