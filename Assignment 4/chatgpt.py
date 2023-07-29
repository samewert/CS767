import pandas as pd
import numpy as np

def collaborative_filtering(train_data, test_data):
    # Create a user-item matrix from the training data
    user_item_matrix = train_data.pivot(index='userId', columns='movieId', values='rating').fillna(0)

    # Calculate the similarity between users using cosine similarity
    user_similarity = cosine_similarity(user_item_matrix)

    # Iterate through the test data and predict ratings for each user and movie
    predicted_ratings = []
    for _, row in test_data.iterrows():
        user_id = row['userId']
        movie_id = row['movieId']
        user_ratings = user_item_matrix[user_item_matrix.index == user_id]
        similar_users = user_similarity[user_item_matrix.index == user_id]

        # Calculate the predicted rating using weighted average of similar users' ratings
        predicted_rating = np.sum(similar_users * user_ratings.values) / np.sum(np.abs(similar_users))

        # Add the predicted rating to the test data
        predicted_ratings.append(predicted_rating)

    return predicted_ratings

if __name__ == "__main__":
    # Load the training and test data
    train_data = pd.read_csv('ratings_small_training.csv')
    test_data = pd.read_csv('ratings_small_test.csv')

    # Import the cosine similarity function from scikit-learn
    from sklearn.metrics.pairwise import cosine_similarity

    # Apply collaborative filtering to predict ratings for the test data
    predicted_ratings = collaborative_filtering(train_data, test_data)

    # Add the predicted ratings to the test data as the third column
    test_data['predictedRating'] = predicted_ratings

    # Save the updated test data with predicted ratings to a new CSV file
    test_data.to_csv('ratings_small_test_predicted.csv', index=False)
