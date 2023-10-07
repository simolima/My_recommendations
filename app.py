import streamlit as st
import pickle
import numpy as np
import requests
import sqlite3
import re

# Imposta il layout su "wide" per utilizzare tutto lo spazio disponibile
st.set_page_config(layout="wide")


movies = pickle.load(open("df_movie_remaining.pkl",'rb'))
similarity= pickle.load(open("similarities_movies.pkl",'rb'))
movies_nodes_list = pickle.load(open("list_movies_for_simililarity.pkl",'rb'))


movies_list=movies['title'].values

def extract_release_year(title):
    # Cerca un anno tra parentesi tonde nel titolo del film
    match = re.search(r'\((\d{4})\)', title)
    if match:
        return int(match.group(1))
    else:
        return 0 
movies_list_sorted = sorted(movies_list, key=extract_release_year)

# Visualizza il titolo con la classe CSS personalizzata e l'animazione
st.markdown(
    """
    <h1 class="custom-title title-animation" style="color: #FF0000; text-align: center;">
        Netflix ma povero
    </h1>
    """,
    unsafe_allow_html=True,
)
# Personalizza l'aspetto della tua applicazione
#st.title(" Netflix ma povero ")  # Utilizza un titolo più accattivante con emoji


# Aggiungi una classe CSS personalizzata per l'animazione
st.markdown(
    """
    <style>
        .title-animation {
            animation: slide-in 2s cubic-bezier(0.25, 1, 0.5, 1) 1s both;
        }

        @keyframes slide-in {
            0% {
                transform: translateX(-100%);
            }
            30% {
                transform: translateX(20%); /* Supera leggermente il centro */
            }
            100% {
                transform: translateX(0);
            }
        }

        .custom-title {
            font-size: 75px;
            font-style: italic;
            font-weight: bold; 
            letter-spacing: -1px; /* Vicine tra loro */
            text-align: center;
            color: #FF0000;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

#Bottone per selezione
selectvalue = st.selectbox("Seleziona un film figo e goditene 5 simili", movies_list_sorted) 

def get_movie_poster_by_title(api_key, movie_title_with_year):
    base_url = 'https://api.themoviedb.org/3'
    
    # Estrai il titolo e l'anno dal titolo completo
    movie_title = movie_title_with_year.split('(')[0].strip()
    
    # Effettua una ricerca del film per titolo
    search_url = f'{base_url}/search/movie'
    params = {'api_key': api_key, 'query': movie_title}
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            movie_id = data['results'][0]['id']
            
            # Ottieni informazioni dettagliate sul film
            movie_url = f'{base_url}/movie/{movie_id}'
            response = requests.get(movie_url, params={'api_key': api_key})
            
            if response.status_code == 200:
                movie_data = response.json()
                if movie_data.get('poster_path'):
                    poster_url = f'https://image.tmdb.org/t/p/w500{movie_data["poster_path"]}'
                    return poster_url
    return None

def recommend_movies(movie_title, similarity_matrix, movie_nodes, df, top_n=5):
    # Trova il movieId corrispondente al titolo del film
    film_corrispondente = movies[movies['title'] == movie_title]
    movieId_corrispondente = film_corrispondente['movieId'].values[0]

    # Trova l'indice corrispondente a questo movieId nella matrice di similarità
    film_index = movie_nodes.index(movieId_corrispondente)

    # Estrai le similarità del film corrente con tutti gli altri film
    similarities = similarity_matrix[film_index]

    # Ordina gli indici delle similarità in ordine decrescente
    sorted_indices = np.argsort(similarities)[::-1]

    # Filtra i primi top_n film più simili, escludendo il film di riferimento
    recommended_indices = [i for i in sorted_indices if i != film_index][:top_n]

    # Ottieni i titoli dei film raccomandati
    recommended_movies = [movies[movies['movieId'] == movie_nodes[i]]['title'].values[0] for i in recommended_indices]

    # Ottieni i poster dei film raccomandati
    api_key = '2477d59760a8e9747995a0b0ddd2402c'
    recommended_posters = [get_movie_poster_by_title(api_key, movie) for movie in recommended_movies]
    
    return recommended_movies, recommended_posters

 # Restituisci 0 se l'anno non è presente nel titolo

# Ordina i film raccomandati in base all'anno di uscita
recommended_movies, recommended_posters = recommend_movies(selectvalue, similarity, movies_nodes_list, movies)
recommended_movies_sorted = sorted(recommended_movies, key=extract_release_year)



# Definisci la larghezza e l'altezza delle immagini dei poster
poster_width = 200
poster_height = 300





# Aggiorna il layout per i film raccomandati
# Funzione per visualizzare il titolo dei film e le immagini dei poster
def display_movie_info(movie_name, movie_poster, col):
    with col:
        st.image(movie_poster, width=poster_width)
        st.write(f'<div style="text-align: center; font-size: 16px; font-weight: bold;">{movie_name}</div>', unsafe_allow_html=True)

# Imposta uno spazio tra le colonne
st.write(" ")  # Aggiungi una riga vuota tra le colonne
st.write(" ")  # Aggiungi un'altra riga vuota per migliorare la separazione



# Visualizza i risultati dei film raccomandati
movie_name, movie_poster = recommend_movies(selectvalue, similarity, movies_nodes_list, movies)
col1, col2, col3, col4, col5 = st.columns(5)


for i in range(min(5, len(movie_name))):  # Visualizza al massimo 5 film raccomandati
    display_movie_info(movie_name[i], movie_poster[i], col1 if i % 5 == 0 else col2 if i % 5 == 1 else
    col3 if i % 5 == 2 else col4 if i % 5 == 3 else col5)







   







