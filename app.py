import streamlit as st
import numpy as np
from PIL import Image

from model import query
from sql import year_range

start_year, end_year = year_range()
years = np.array(range(start_year, end_year + 1))

st.set_page_config(page_title='ARTIST', page_icon='⭐')

logo = Image.open('logo.png')
st.image(logo, width=logo.width//6)

st.title('Arxiv RecommendaTIon SysTem')

query_input = st.text_input("Prompt:",
                              placeholder="Insert your query here!",
                              max_chars=128)

col1, col2, col3 = st.columns([0.7,0.15,0.15])

n_articles = col1.slider("Number of articles:", 1, 20, 5)
box_inital = col2.selectbox('Initial Year', years)
box_final = col3.selectbox('Final Year', years, index=len(years)-1)

if query_input.strip():  # Check if query_input is not blank
    if int(box_final) - int(box_inital) >= 0:
        try:
            results = query(query_input, box_inital, box_final, n_articles)
            for i, result in enumerate(results, start=1):
                article, score = result
                id_, title, abstract, date = article
                
                url = 'http://arxiv.org/abs/' + str(id_)
                title = title.replace('\n', '').capitalize()
                abstract = abstract.replace('\n', '').strip().capitalize()
                
                st.write(f"### {i}) [{title}]({url})")
                st.write(f'Score:  {score:.3f} | Date: {date}')
                st.write(abstract)
        except Exception as e:
            st.error(f"Error occurred: {e}")
    else:
        st.warning("Please enter a valid year range.")  
else:
    st.warning("Please enter some text before submitting.")

st.markdown("---")
st.write("Created with ❤️ by Erick Ghuron, Chi Jiang, Catalina Sáez and Amanda Wasserman")