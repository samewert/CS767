import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity (item_1, item_2):
  dot = np.dot(item_1, item_2)
  norm_1 = np.linalg.norm(item_1) # Get norm, or magnitude, of vector
  norm_2 = np.linalg.norm(item_2) # Get norm, or magnitude, of vector
  return dot / (norm_1 * norm_2)



def collaborativeFiltering(trainData, testData):
    # Create a user-item matrix from the training data
    userItemMatrix = trainData.pivot(index='userId', columns='movieId', values='rating').fillna(0)

    # Calculate the similarity between users using cosine similarity
    userSimilarity = cosine_similarity(userItemMatrix)

    # Iterate through the test data and predict ratings for each user and movie
    for _, row in testData.iterrows():
        userId = row['userid']
        movieId = row['movieid']
        userRatings = userItemMatrix[userItemMatrix.index == userId]
        similarUsers = userSimilarity[userItemMatrix.index == userId]

        # Calculate the predicted rating using weighted average of similar users' ratings
        predictedRating = np.sum(similarUsers * userRatings.values) / np.sum(np.abs(similarUsers))

        # Add the predicted rating to the test data
        testData.at[_, 'predictedRating'] = predictedRating

    return testData


if __name__ == "__main__":
    # Load the training and test data
    trainData = pd.read_csv('csv/ratings_small_training.csv')
    testData = pd.read_csv('csv/ratings_small_test.csv')

    maxMovie = trainData['movieId'].max()
    maxUser = trainData['userId'].max()

    itemRatingMatrix = np.full((maxUser+1, maxMovie+1), -1)

    for index, row in trainData.iterrows():
        itemRatingMatrix[int(row['userId']), int(row['movieId'])] = float(row['rating'])

    itemRatingMatrix = np.transpose(itemRatingMatrix)

    itemCount = len(itemRatingMatrix)
    similarityMatrix = np.empty(itemCount, dtype=np.ndarray)

    for i in range(itemCount):
        similar = []
        for j in range(itemCount):
            similar.append((j, compute_similarity(
                itemRatingMatrix[i],
                itemRatingMatrix[j]
            )))

        similar = sorted(similar, key=lambda tup: tup[1], reverse=True)
        similar = list(map(lambda tup: tup[0], similar))
        similarityMatrix[i] = np.array(similar)

    print(similarityMatrix)





    # Apply collaborative filtering to predict ratings for the test data

    predictedRatings = collaborativeFiltering(trainData, testData)

    # Save the updated test data with predicted ratings to a new CSV file
    predictedRatings.to_csv('ratings_small_test_predicted.csv', index=False)
