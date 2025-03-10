from textblob import TextBlob
from langdetect import detect

def analyze_sentiment(text):
    original_blob = TextBlob(text)
    words = original_blob.words
    word_count = len(words)
    sentences = original_blob.sentences
    sentence_count = len(sentences)
    avg_word_length = sum(len(word) for word in text.split()) / word_count if word_count > 0 else 0
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    noun_phrases = list(original_blob.noun_phrases)

    try:
        language = detect(text)
    except Exception as e:
        print("Language detection error:", e)
        language = 'en'

    blob = original_blob
    if language != 'en':
        if hasattr(original_blob, "translate"):
            try:
                blob = original_blob.translate(to='en')
            except Exception as e:
                print("Translation error:", e)
                blob = original_blob
        else:
            print("Translation not supported, using original text")
            blob = original_blob

    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    sentiment = "neutral"
    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"

    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "sentiment": sentiment,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
        "avg_sentence_length": avg_sentence_length,
        "noun_phrases": noun_phrases
    }
