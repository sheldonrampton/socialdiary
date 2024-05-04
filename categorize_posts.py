import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora, models
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import re


# nltk.download('stopwords')
# nltk.download('wordnet')


def preprocess_text(texts):
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    preprocessed_texts = []
    for text in texts:
        tokens = tokenizer.tokenize(text.lower())
        stopped_tokens = [i for i in tokens if not i in stop_words]
        lemmatized_tokens = [lemmatizer.lemmatize(i) for i in stopped_tokens]
        preprocessed_texts.append(lemmatized_tokens)
    return preprocessed_texts


def remove_urls(text):
    # Define the regular expression pattern for URLs
    url_pattern = r'https?://\S+|www\.\S+'
    # Substitute found URLs with an empty string
    no_urls = re.sub(url_pattern, '', text)
    return no_urls


posts_file = "posts.csv"
texts = []
publications = [
   "- YouTube",
   "<<<<<<< Local Changes",
   ">>>>>>> External Changes",
   "ABC News",
   "ABC7 Los Angeles",
   "About",
   "ActBlue",
   "al.com",
   "Amazon.com",
   "Apple",
   "Atlas Obscura",
   "auction details",
   "BBC News",
   "bellingcat",
   "Big Think",
   "billymeinke.com",
   "Blogger",
   "Bloomberg",
   "BlueHost.com",
   "Boing Boing",
   "by Steve Stewart-Williams",
   "Capitol Weekly",
   "Clarity",
   "CounterPunch.org",
   "Google Accounts",
   "Imgur",
   "Los Angeles Times",
   "Macleans.ca",
   "National Memo",
   "Opinion",
   "POLITICO",
   "POLITICO Magazine",
   "PolitiFact",
   "Poynter",
   "Quora",
   "Raw Story",
   "snpy.tv",
   "The Washington Post",
   "The White House",
   "TheaterMania.com",
   "TPM – Talking Points Memo",
   "Vox",
   "Wikipedia",
   "YouTube"
]

with open(posts_file, "r") as infile:
    posts = csv.reader(infile)
    next(posts, None)  # skip the headers
    for post in posts:
        timestamp = post[0]
        date = post[1]
        url = post[2]
        url_title = remove_urls(post[3])
        url_title = url_title.split('|')[0].strip()
        url_error = post[4]
        post_text = remove_urls(post[5])
        if url_title != '':
            pieces = url_title.split(' - ')
            if len(pieces) > 1:
                pieces.pop()
                url_title = ' - '.join(pieces)
                print(url_title)
                # print(url_title.split(' - ').pop())
            texts.append(url_title)
        if post_text != '':
            texts.append(post_text)
        # print("URL Title:", url_title)
        # print("Post:", post_text)

processed_posts = preprocess_text(texts)
print(len(processed_posts))
# dictionary = corpora.Dictionary(processed_posts)
# corpus = [dictionary.doc2bow(text) for text in processed_posts]

# ldamodel = models.ldamodel.LdaModel(corpus, num_topics=100, id2word=dictionary, passes=25)
# topics = ldamodel.print_topics(num_words=8)
# for topic in topics:
#     print(topic)

vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
X = vectorizer.fit_transform([' '.join(text) for text in processed_posts])

nmf_model = NMF(n_components=20, random_state=1)
nmf_model.fit(X)
feature_names = vectorizer.get_feature_names_out()

for topic_idx, topic in enumerate(nmf_model.components_):
    print(f"Topic {topic_idx}: ", " ".join([feature_names[i] for i in topic.argsort()[:-4 - 1:-1]]))

