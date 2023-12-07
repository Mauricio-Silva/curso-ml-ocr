from os import listdir, remove


PATH = "app/static"
CSV_PATH = f"{PATH}/csv"
ORIGINAL_PATH = f"{PATH}/images/original"
PROCESSED_PATH = f"{PATH}/images/processed"


for csv in listdir(CSV_PATH):
    remove(f"{CSV_PATH}/{csv}")


for original in listdir(ORIGINAL_PATH):
    remove(f"{ORIGINAL_PATH}/{original}")


for processed in listdir(PROCESSED_PATH):
    remove(f"{PROCESSED_PATH}/{processed}")


print("\033[31mAll data was Removed!\033[m")
