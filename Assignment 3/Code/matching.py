import pandas as pd
import editdistance

def cartesianTables(tableA, tableB):

    tableC = pd.merge(tableA, tableB, how='cross', suffixes=('_ltable', '_rtable'))

    tableC.columns = [column.split('_')[1] + '_' + column.split('_')[0] for column in tableC.columns]

    # tableC['ID'] = range(1, len(tableC) + 1)

    columns = tableC.columns
    ids = []
    attrs = []
    for c in columns:
        if 'ID' in c:
            ids.append(c)
        else:
            attrs.append(c)
    ids.sort()
    tableC = tableC[ids + attrs]

    # print(tableC.head())

    tableC.to_csv('csv/cartesian.csv')
    print('Cartesian Length: {}'.format(len(tableC)))

    tableCId = tableC[[col for col in tableC.columns[:2]]]
    tableCId = tableCId.reset_index(drop=True)

    print(len(tableC))
    tableCId.to_csv('csv/idC.csv')

def jaccard_similarity(set1, set2):

  intersection = len(set1.intersection(set2))
  union = len(set1.union(set2))
  return intersection / union

def editDistance(tableA, tableB):

    for a in tableA['Title']:
        for b in tableB['Title']:
            # print(tableA['Title'][i])
            editDistance = editdistance.eval(a, b)
            if editDistance < len(a) / len(a):
                print('A:', a, 'B:', b)

def jaccard(tableA, tableB):
    for a in tableA['Title']:
        for b in tableB['Title']:
            jaccard = jaccard_similarity(set(a), set(b))
            if jaccard > 0.99:
                print('A:', a, 'B:', b)


def same(tableA, tableB):
    tableC = {}
    for a in range(0, len(tableA)):
        aTitle = tableA['Title'][a]

        row = tableA.iloc[a]
        row_dict = {}
        for column, value in row.items():
            row_dict[column] = value

        tableC[aTitle] = row_dict

    # editDistance(tableA, tableB)
    # jaccard(tableA, tableB)

    onlyMatches = {}

    for b in range(0, len(tableB)):
        bTitle = tableB['Title'][b]

        row = tableB.iloc[b]
        row_dict = {}
        for column, value in row.items():
            row_dict[column] = value

        if bTitle in tableC:
            onlyMatches[bTitle] = row_dict


        tableC[bTitle] = row_dict

    print('A Length: {}'.format(len(tableA)))
    print('B Length: {}'.format(len(tableB)))
    print('C Consolidated Length: {}'.format(len(tableC)))
    print('C Matches Length: {}'.format(len(onlyMatches)))

    columns = ['ID','ltable_ID','rtable_ID','ltable_Title','ltable_Price','ltable_Miles','rtable_Title','rtable_Price','rtable_Miles']
    combined = pd.DataFrame(tableC.values())

    matches = pd.DataFrame(onlyMatches.values())

    # combined.to_csv('csv/consolidated.csv')
    #
    # matches.to_csv('csv/matches.csv')

    print(combined.head())
    print(matches.head())



if __name__ == '__main__':

    tableA = pd.read_csv('csv/cargurusCars.csv')
    tableA = tableA.drop('Market Price', axis=1)
    tableA = tableA.drop('Location', axis=1)
    tableB = pd.read_csv('csv/autotraderCars.csv')

    # cartesianTables(tableA, tableB)
    # editDistance(tableA, tableB)
    # jaccard(tableA, tableB)
    same(tableA, tableB)
