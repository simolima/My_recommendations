# My personal movies recommendation system with deployement on Heroku
Implementation of an Item-Item based recommendation system using Pearson similarity.

## Programming Language and libraries
Python 3.11.5 


numpy,
pandas,
networkx,
streamlit,
matplotlib,
scipy.


## Dataset
The datasets used are available at https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset/data
in particular i used the entire datasets ratings.csv and movies.csv
The dataset consists of 26 million ratings from 270,000 users on all the 45,000 movies.

## Preprocessing 
I wanted to have my dataset in nodal form so i created a bipartite nodal network where movies and users are the nodes and arcs between the are weighted with the ratings given by a user to that film.

## Goals
The goal was implements two different types of reccomendation system, one that i could deploy on Heroku based on Item-Item similarity were my Item are the movies and one based on User-User similarity.
Item-Item similarity works in the following way , for every film i create a similarity matrix (i decided for Pearson similarity) where every pair film-film has a similarity score.
User-User similarity works in the following way , for every user i create a similarity matrix (i decided for Pearson similarity) where every pair user-user has a similarity score.

## Pearson similarity
$r = \frac{\sum((x - \bar{x})(y - \bar{y}))}{\sqrt{\sum(x - \bar{x})^2} \sqrt{\sum(y - \bar{y})^2}}$


- r è il coefficiente di correlazione di Pearson.
- x rappresenta i valori della prima variabile.
- y rappresenta i valori della seconda variabile.
- $\bar{x}$ è la media dei valori di x.
- $\bar{y}$ è la media dei valori di y.





## Item-Item similarity Recommendation System
I associate every film to a vector of ratings given by the users to that particular film.Then calculated the Pearson similarity on the common users,the higher is this similarity the more "similar" are considered the movies.
I selected only the 769 movies withi more valutations in order to have a computational time of 2 hours for the construction of the similarity matrix.
The big advantages of this model is that you can access the results even offline and that you have a smaller similarity matrix at the beginning (movies are less than users) and that you can even reduce the dimensionality of this matrix as i have done choosing only the movies with the higher number of valutation discarding a large number of films that only a small number of users has seen.
Then i create a funtion that has as input the title of a movie and returns the top-5 movies more similar.
Then i developed a web app e deployed it on the cloud service heroku.
You can visit my app at the following link https://recbysimone-7a1c5f52cc56.herokuapp.com/


## User-User similarity Recommendation System
I associate every user to a vector of ratings given by that particular user to all films.Then calculated the Pearson similarity,the higher is this similarity the more "similar" are considered the users.
The goal in this case is predict what ratings a user could give to a particular film and suggests the ones with higher ratings.
So on this case for every user i splitted the datase in 80 train 20 test and trained the following model :


$r˜uα = r¯u + κ \sum_{v∈Uˆu} suv(rvα − r¯v)$
Dove:.

- `Uˆu` rappresenta l'insieme di utenti più simili all'utente `u`.
- `suv` è la similarità tra l'utente `u` e l'utente `v`.
- `κ` è un fattore di normalizzazione calcolato come:
- $κ = \sum_{v} \frac{1}{|suv|}$
- `r¯u` è la media delle valutazioni dell'utente `u`.

  
The MSE results were good but the computational cost was really high and i couldn't evaluate every user but only a small percentage.
The big disadvantage of this model is that you cannot reduce the dimension of the similarity matrix because you have to give a prediction for every user in the real applications,and another disadvantage is that users without ratings can't have suggestions.
The advantage is that in this way you can have a really personalized suggestions.

## Conclusion
I think that in my situation the only way to deploy a product was using the item-item method and i think that it has a large number of advantages if compared with user-user similarity.On the other hand i understand that in situations in which an user search highly specific recommendations the user-user method can be the better one.





