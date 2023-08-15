import streamlit as st
from model import query

st.set_page_config(page_title='ARTIST', page_icon='⭐')

st.title('Arxiv RecommendaTIon SysTem')

# Place the text input in the first column
query_input = st.text_input("Prompt:",
                              placeholder="Insert your query here!",
                              max_chars=128)

n_articles = st.slider("Number of articles:", 1, 20, 5)

if query_input:  # Check if query_input is not blank
    try:
        results = query(query_input, n_articles)
        for i, result in enumerate(results, start=1):
            article, score = result
            id_, title, abstract = article
            
            url = 'http://arxiv.org/abs/' + str(id_)
            title = title.replace('\n', '').capitalize()
            abstract = abstract.replace('\n', '').strip().capitalize()
            
            st.write(f"### {i}) [{title}]({url})")
            st.write(f'Score:  {score:.3f}')
            st.write(abstract)
    except Exception as e:
        st.error(f"Error occurred: {e}")  
else:
    st.warning("Please enter some text before submitting.")


