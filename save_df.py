from datetime import datetime
import pandas as pd
from pdf_generator import clean_filename

def save_df(df,values):
    date = datetime.now().date()
    pdf_filename = "{}.xlsx".format(clean_filename("{} {} {} {}".format(values['name'], values['device'], values['type'], date)))
    final_path = "excel_files/{}".format(pdf_filename)  # Change this path to desired location
    df.to_excel(final_path, index=False) 
    pdf_filename = "{}.csv".format(clean_filename("{} {} {} {}".format(values['name'], values['device'], values['type'], date)))
    final_path = "csv_files/{}".format(pdf_filename)
    df.to_csv(final_path, index=False) 