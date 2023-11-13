from transformers import pipeline

def sentiment_analysis(df):
    #sentiment analysis using a pre trainend model finbert
    classifier = pipeline('sentiment-analysis','ProsusAI/finbert')
    texts = df['Content'].tolist()
    results = classifier(texts)

    df['sentiment'] = [result['label'] for result in results]
    df['confidence'] = [result['score'] for result in results]
    return df