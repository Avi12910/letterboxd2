import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.connect import get_all_unseen
from backend.movielist import MovieList


def recommend(user_list: MovieList):
    user_movies = []
    for movie_id, movie_data in user_list.films.items():
        film_info = movie_data['film_info']
        user_movies.append({
            'movie_id': movie_id,
            'title': film_info['full_name'],
            'genres': ' '.join(film_info['genres']) if 'genres' in film_info else '',
            'themes': ' '.join(
                theme.replace(' ', '') for theme in film_info['themes']) if 'themes' in film_info else '',
            # 'length': film_info['length'],
            # 'release_year': film_info['year'],
            'user_rating': movie_data['rating']
        })
    user_movies_df = pd.DataFrame(user_movies)

    all_movies = []

    for movie_id, movie_data in get_all_unseen(user_list).items():
        all_movies.append({
            'movie_id': movie_id,
            'title': movie_data['title'],
            'genres': ' '.join(movie_data['genres']),
            'themes': ' '.join(theme for theme in movie_data['themes']),
            # 'length': movie_data['length'],
            # 'release_year': movie_data['release_year']
        })

    all_movies_df = pd.DataFrame(all_movies)

    user_movies_df['combined_features'] = user_movies_df['genres'] + ' ' + user_movies_df['themes']

    user_movies_df.replace({'n/a': np.nan, '': np.nan}, inplace=True)
    user_movies_df['combined_features'].fillna('unknown', inplace=True)
    user_movies_df['user_rating'].fillna(0, inplace=True)

    vectorizer = TfidfVectorizer(stop_words='english')
    vectorized_features = vectorizer.fit_transform(user_movies_df['combined_features'])

    weighted_features = vectorized_features.toarray() * user_movies_df['user_rating'].values.reshape(-1, 1)

    user_profile = np.mean(weighted_features, axis=0)  # You can also use np.sum() if summing is preferred
    user_profile = user_profile.reshape(1, -1)

    # profile_weights = pd.Series(user_profile.flatten(), index=vectorizer.get_feature_names_out())
    # print("User Profile Weights:\n", profile_weights['horror'])

    all_movies_df['combined_features'] = all_movies_df['genres'] + ' ' + all_movies_df['themes']

    all_movies_df.replace({'n/a': np.nan, '': np.nan}, inplace=True)
    all_movies_df['combined_features'].fillna('unknown', inplace=True)

    all_vectorized_features = vectorizer.transform(all_movies_df['combined_features'])

    similarity_scores = cosine_similarity(user_profile, all_vectorized_features)

    all_movies_df['similarity'] = similarity_scores.flatten()
    recommended_movies = all_movies_df.sort_values(by='similarity', ascending=False)

    output = recommended_movies.where(pd.notnull(recommended_movies), None).head(100).to_dict(orient='records')

    return output
