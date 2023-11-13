from analysis import dates, word_map
from pdf_generator import create_pdf
from save_df import save_df
from scrape import scrape_url
from tranformer_analysis import sentiment_analysis
import sys


if len(sys.argv) != 6:  # El número de argumentos debe ser 3 (python nombre_script.py argumento1 argumento2 argumento3)
    url = 'https://play.google.com/store/apps/details?id=com.brotato.shooting.survivors.games.paid.android&hl=en_419&gl=US'
    device = "phone"
    type = "relevant"
    sentiment= False
    iteration = 30
else:
    url = sys.argv[1]
    device = sys.argv[2]
    type = sys.argv[3]
    sentiment = sys.argv[4]
    iteration = sys.argv[5]

df, values = scrape_url(url, device, type,iteration)
if sentiment:
    df= sentiment_analysis(df)
save_df(df, values)
fig = dates(df)
map = word_map(df)
create_pdf(values, map, fig)
