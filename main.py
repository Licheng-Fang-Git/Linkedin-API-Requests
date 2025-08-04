# streamlit_tfidf_similarity.py
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Sidebar option
st.sidebar.title("Analysis Options")
analysis_option = st.sidebar.selectbox("Choose an analysis", ["Overview", "TF-IDF Similarity Clustering"])

# Load data
@st.cache_data
def load_data():
    sheet_id = '1thMQ4ndtgzyEM6qfoA2tfrt3MEzZY2CtxhjpCTNcS0U'  # Example: '1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg'
    content_sheet_name = 'Content'
    content_csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={content_sheet_name}'
    return pd.read_csv(content_csv_url)  # Change this path as needed

df = load_data()

if analysis_option == "Overvie w":
    st.title("LinkedIn Content Overview")
    st.write(df.head())

elif analysis_option == "TF-IDF Similarity Clustering":
    st.title("Detect Similar Posts Using TF-IDF")

    # Ensure 'Content' column exists
    if "Post title" not in df.columns:
        st.error("No 'Post title' column found in dataset.")
    else:
        # Fill NaNs with blanks for text processing
        contents = df['Post title'].fillna("")

        # Compute TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(contents)

        # Compute cosine similarity
        cos_sim = cosine_similarity(tfidf_matrix)

        # Flag similar pairs above threshold
        threshold = 0.9
        similar_pairs = np.argwhere((cos_sim > threshold) & (cos_sim < 1.0))
        similar_df = pd.DataFrame(similar_pairs, columns=['Post A', 'Post B'])

        # Drop duplicates (e.g. (1,2) and (2,1))
        similar_df = similar_df[similar_df['Post A'] < similar_df['Post B']]

        st.subheader(f"Posts with Similarity > {threshold}")
        st.write(similar_df)
        print(df.iloc[68]['Year'])
        # Optionally show the actual text
        for _, row in similar_df.head(5).iterrows():
            idx_a = row['Post A']
            idx_b = row['Post B']
            st.markdown(f"**Pair {idx_a} & {idx_b}:**")
            st.text(f"Post A: {contents.iloc[idx_a][:300]}...")
            st.text(f"Post B: {contents.iloc[idx_b][:300]}...")