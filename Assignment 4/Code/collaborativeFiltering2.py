import pandas as pd

def predictRating(pickedUserId, movieId):

    train_data = pd.read_csv('../csv/ratings_small_training.csv')

    # rows/index are movieId's, columns are userId, values are ratings
    matrix = train_data.pivot_table(index='movieId', columns='userId', values='rating')
    # matrix = train_data.pivot_table(index='userId', columns='movieId', values='rating')

    # 0 is rows/index, 1 is columns
    # x = matrix.mean(axis=1)
    # y = matrix.mean(axis=0)

    # rows/index are movieId's, columns are userId, values are ratings
    matrixNorm = matrix.subtract(matrix.mean(axis=0), axis='columns')


    # Pearson Correlation
    userSimilarity = matrixNorm.corr(method='pearson')
    # userSimilarity = matrix.corr(method='pearson')

    # Given userId to predict the movie for
    pickedUserId = pickedUserId

    # ensure the picked user is not included when picking similar neighbors
    userSimilarity.drop(index=pickedUserId, inplace=True)

    # Hien used 50
    n = 50

    bottom = 0

    userSimilarityThreshold = 0.7

    # loop the prediction calculation until there are users who have rated the movie
    while bottom == 0:

        # Hien used 0.7 or 0.8


        # Take the column of the picked user. Get the top n userIds (index/rows) with a value larger than similarity threshold
        similarUsers = userSimilarity[pickedUserId][userSimilarity[pickedUserId] > userSimilarityThreshold].sort_values(
            ascending=False)[:n]

        # movie to predict the rating for
        movieId = movieId

        # top and bottom match rating prediction formula from slides
        # SUM ( w_a,u * (r_u,i - -r_u) )
        top = 0
        # SUM (w_a,u)
        # bottom = 0

        for userId, similarity in similarUsers.items():
            w = similarity

            # matrixNorm already has (ratings - average rating)
            normRating = matrixNorm[userId][movieId]

            # If the user didn't rate the movie, don't include the rating
            if pd.isna(normRating):
                # normRating = 0
                continue

            top += w * normRating
            bottom += w

        # Incrementally change parameters until we get users who have rated the given movie
        userSimilarityThreshold -= 0.05
        if len(similarUsers) == n:
            # Only increase group size if the similar user group is already full
            n += 50

    # Given user's average rating
    rAverage = matrix[pickedUserId].mean()


    # print(pickedUserId)
    # print(top)
    # print(bottom)

    # Final calculation for predicted rating
    p = (rAverage + (top / bottom))

    return p


test_data = pd.read_csv('../csv/ratings_small_test.csv')

predictedRatings = []

for index, row in test_data.iterrows():
    rating = predictRating(row['userid'], row['movieid'])
    predictedRatings.append(rating)

print(predictedRatings)

test_data['predictedRatings'] = predictedRatings

test_data.to_csv('../csv/newPredictedRatings.csv')