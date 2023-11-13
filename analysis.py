import re
import nltk
import os
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import Counter
import pandas as pd
from matplotlib.ticker import MaxNLocator

def word_map(df):
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    stop_words.add("like")
    stop_words.add("game")

    def count_words(text):
        words = re.findall(r'\w+', text.lower())
        words = set(words)
        filtered_words = [word for word in words if word not in stop_words and not word.isdigit()]
        return Counter(filtered_words)

    # Applying the function to each row of the DataFrame
    df['Frequency'] = df['Content'].apply(count_words)

    # Combining frequencies of all rows into a single Counter
    total_frequency = df['Frequency'].sum()
    sum_frequency_less_than_4 = df.loc[df['Rating'] < 4, 'Frequency'].sum()
    sum_frequency_greater_than_equal_4 = df.loc[df['Rating'] >= 4, 'Frequency'].sum()
    wordcloud1 = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(total_frequency)
    wordcloud2 = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(sum_frequency_less_than_4)
    wordcloud3 = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(sum_frequency_greater_than_equal_4)
    wordcloud = [wordcloud1, wordcloud2, wordcloud3]
    return wordcloud

def dates(df):
    df['Date'] = pd.to_datetime(df['Date'])
    # Count frequency of each date
    
    date_count = df['Date'].value_counts().sort_index()
    # Group by month and count frequency
    monthly_count = date_count.resample('M').sum()
    monthly_count = monthly_count.shift(-1, freq='M')

    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create the plot
    ax.plot(monthly_count.index, monthly_count.values, marker='o', color='#3498db', label='Monthly Frequency')

    ax.set_xlabel('Month', fontsize=14)
    ax.set_ylabel('Frequency', fontsize=14)
    ax.tick_params(axis='both', labelsize=12)
    ax.legend(fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Format dates on the x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    # Adjust the number of ticks on the y-axis
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Rotate x-axis labels for better readability
    fig.autofmt_xdate()

    output_folder = "plots"
    # Unir la ruta de la carpeta con el nombre del archivo
    output_path = os.path.join(output_folder, "dates_plot.png")
    fig.savefig(output_path, format='png')
    plt.close()  # Close the figure after saving

    return output_path
