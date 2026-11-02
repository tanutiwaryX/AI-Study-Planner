import re
from textblob import TextBlob

def _prepare_nltk():
    import nltk
    for path, package in [("tokenizers/punkt","punkt"),("corpora/stopwords","stopwords"),
                          ("corpora/wordnet","wordnet"),("corpora/omw-1.4","omw-1.4")]:
        try: nltk.data.find(path)
        except LookupError: nltk.download(package, quiet=True)

def preprocess_text(text):
    try:
        _prepare_nltk()
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer
        from nltk.tokenize import word_tokenize
        tokens=word_tokenize(text.lower()); stops=set(stopwords.words("english"))
        lemma=WordNetLemmatizer()
        return [lemma.lemmatize(t) for t in tokens if re.fullmatch(r"[a-z]+",t) and t not in stops]
    except Exception:
        return [w for w in re.findall(r"[a-z]+",text.lower()) if len(w)>2]

def analyze_text(text):
    polarity=float(TextBlob(text).sentiment.polarity)
    sentiment="Positive" if polarity>0.1 else "Negative" if polarity< -0.1 else "Neutral"
    return {"sentiment":sentiment,"polarity":polarity,"word_count":len(text.split()),"keywords":preprocess_text(text)[:30]}

def extractive_summary(text,max_sentences=3):
    sentences=[s.strip() for s in re.split(r"(?<=[.!?])\\s+",text.strip()) if s.strip()]
    return " ".join(sentences[:max_sentences]) if sentences else "No text was provided."

def summarize_text(text,use_transformer=False):
    if use_transformer:
        try:
            from transformers import pipeline
            summarizer=pipeline("summarization",model="sshleifer/distilbart-cnn-12-6")
            result=summarizer(text[:6000],max_length=130,min_length=30,do_sample=False)
            if result and result[0].get("summary_text"): return result[0]["summary_text"]
        except Exception as exc:
            return f"Transformer summary unavailable ({type(exc).__name__}). Extractive fallback: {extractive_summary(text)}"
    return extractive_summary(text)
