import pandas as pd
import numpy as np
import scipy.stats
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity

def predictRating(pickedUserId, movieId):

    train_data = pd.read_csv('../csv/ratings_small_training.csv')

    # print(train_data.head())


    # matrix = train_data.pivot_table(index='userId', columns='movieId', values='rating')
    matrix = train_data.pivot_table(index='movieId', columns='userId', values='rating')

    # print(matrix.head())



    matrixNorm = matrix.subtract(matrix.mean(axis=1), axis = 'rows')

    userSimilarity = matrixNorm.T.corr() # Pearson Correlation


    # userSimilarityCosine = cosine_similarity(matrixNorm.fillna(0))


    pickedUserId = pickedUserId

    userSimilarity.drop(index=pickedUserId, inplace=True)

    # print(userSimilarity.head())


    n = 200

    userSimilarityThreshold = 0.55

    similarUsers = userSimilarity[userSimilarity[pickedUserId] > userSimilarityThreshold][pickedUserId].sort_values(ascending=False)[:n]

    # print(f'The similar users for user {pickedUserId} are', similarUsers)

    pickedUserIdWatched = matrixNorm[matrixNorm.index == pickedUserId].dropna(axis=1, how='all')

    similarUserMovies = matrixNorm[matrixNorm.index.isin(similarUsers.index)].dropna(axis=1, how='all')

    similarUserMovies.drop(pickedUserIdWatched.columns,axis=1,inplace=True, errors='ignore')

    itemScore = {}

    for i in similarUserMovies.columns:
        movieRating = similarUserMovies[i]
        total = 0
        count = 0
        for u in similarUsers.index:
            if pd.isna(movieRating[u]) == False:
                score = similarUsers[u] * movieRating[u]
                total += score
                count += 1
        itemScore[i] = total/count

    itemScore = pd.DataFrame(itemScore.items(), columns=['movieId', 'movieScore'])

    rankedItemScore = itemScore.sort_values(by='movieScore', ascending=False)

    m = 10
    # print(rankedItemScore.head(m))



    avgRating = matrix[matrix.index == pickedUserId].T.mean()[pickedUserId]

    # print(f'The average movie rating for user {pickedUserId} is {avgRating:.2f}')

    rankedItemScore['predictedRating'] = rankedItemScore['movieScore'] + avgRating

    for index, row in rankedItemScore.iterrows():
        if row['movieId'] == movieId:
            return row['predictedRating']
    return None

    # row = rankedItemScore[rankedItemScore['movieId']==movieId]
    #
    # return row['predictedRating']

    # print(rankedItemScore.head(m))


test_data = pd.read_csv('../csv/ratings_small_test.csv')

predictedRatings = []

for index, row in test_data.iterrows():
    rating = predictRating(row['userid'], row['movieid'])
    predictedRatings.append(rating)

print(predictedRatings)

test_data['predictedRatings'] = predictedRatings

test_data.to_csv('../csv/predictedRatings.csv')

#
#
#
# def collaborative_filtering(train_data, test_data):
#     # Create a user-item matrix from the training data
#     user_item_matrix = train_data.pivot(index='userId', columns='movieId', values='rating').fillna(0)
#
#     # Calculate the similarity between users using cosine similarity
#     user_similarity = cosine_similarity(user_item_matrix)
#
#     # Iterate through the test data and predict ratings for each user and movie
#     predicted_ratings = []
#     for _, row in test_data.iterrows():
#         user_id = row['userId']
#         movie_id = row['movieId']
#         user_ratings = user_item_matrix[user_item_matrix.index == user_id]
#         similar_users = user_similarity[user_item_matrix.index == user_id]
#
#         # Calculate the predicted rating using weighted average of similar users' ratings
#         predicted_rating = np.sum(similar_users * user_ratings.values) / np.sum(np.abs(similar_users))
#
#         # Add the predicted rating to the test data
#         predicted_ratings.append(predicted_rating)
#
#     return predicted_ratings
#
# if __name__ == "__main__":
#     # Load the training and test data
#     train_data = pd.read_csv('ratings_small_training.csv')
#     test_data = pd.read_csv('ratings_small_test.csv')
#
#     # Import the cosine similarity function from scikit-learn
#     from sklearn.metrics.pairwise import cosine_similarity
#
#     # Apply collaborative filtering to predict ratings for the test data
#     predicted_ratings = collaborative_filtering(train_data, test_data)
#
#     # Add the predicted ratings to the test data as the third column
#     test_data['predictedRating'] = predicted_ratings
#
#     # Save the updated test data with predicted ratings to a new CSV file
#     test_data.to_csv('ratings_small_test_predicted.csv', index=False)
