import mysql.connector
import math


conn = mysql.connector.Connect(host='192.168.64.3', port='3306', user='root', password='', database='olapdb')
mycursor = conn.cursor()

groups = ['sport', 'agegroup', 'continent', 'gender']
list_of_queries = []
all_columns = {}

str1 = "SELECT distinct sport FROM london12"
mycursor.execute(str1)
column1 = mycursor.fetchall()
all_columns['sport'] = column1

str1 = "SELECT distinct agegroup FROM london12"
mycursor.execute(str1)
column2 = mycursor.fetchall()
all_columns['agegroup'] = column2

str1 = "SELECT distinct continent FROM london12"
mycursor.execute(str1)
column3 = mycursor.fetchall()
all_columns['continent'] = column3

str1 = "SELECT distinct gender FROM london12"
mycursor.execute(str1)
column4 = mycursor.fetchall()
all_columns['gender'] = column4

# producing combination of columns for where clause
combinations2 = []
for i in range(4):
    combinations2.append([groups[i]])
    for j in range(i+1, 4):
        combinations2.append([groups[i], groups[j]])
        for k in range(j+1, 4):
            combinations2.append([groups[i], groups[j], groups[k]])
            for l in range(k+1, 4):
                combinations2.append([groups[i], groups[j], groups[k], groups[l]])

combinations = []
for item in combinations2:
    combinations.append(','.join(item))

for i in combinations2:
    if len(i) == 1:
        for k in all_columns[i[0]]:
            k = ''.join(k)
            k = "'{0}'".format(k)
            query = "SELECT continent,agegroup,sport,gender,gold,silver,bronze from london12 WHERE " + i[0] + " = " + k
            list_of_queries.append(query)
            for x in range(15):
                if i[0] not in combinations[x]:
                     query = "SELECT " + combinations[x] + ",sum(gold),sum(silver),sum(bronze) FROM london12 WHERE " + i[0] + " = " + k + " GROUP BY " + combinations[x]
                     list_of_queries.append(query)
    elif len(i) == 2:
        for k in all_columns[i[0]]:
            k = ''.join(k)
            k = "'{0}'".format(k)
            for l in all_columns[i[1]]:
                l = ''.join(l)
                l = "'{0}'".format(l)
                query = "SELECT continent,agegroup,sport,gender,gold,silver,bronze from london12 WHERE " + i[0] + " = " + k + " and " + i[1] + " = " + l
                list_of_queries.append(query)
                for x in range(15):
                    if i[0] not in combinations[x] and i[1] not in combinations[x]:
                        query = "SELECT "+ combinations[x] + ",sum(gold),sum(silver),sum(bronze) FROM london12 WHERE " +\
                                i[0] + " = " + k + " and " + i[1] + " = " + l + " GROUP BY " + combinations[x]
                        list_of_queries.append(query)

    elif len(i) == 3:
        for k in all_columns[i[0]]:
            k = ''.join(k)
            k = "'{0}'".format(k)
            for l in all_columns[i[1]]:
                l = ''.join(l)
                l = "'{0}'".format(l)
                for j in all_columns[i[2]]:
                    j = ''.join(j)
                    j = "'{0}'".format(j)
                    query = "SELECT continent,agegroup,sport,gender,gold,silver,bronze FROM london12 WHERE " + i[0] + " = " + k +\
                            " and " + i[1] + " = " + l + " and " + i[2] + " = " + j
                    list_of_queries.append(query)
                    for x in range(15):
                        if i[0] not in combinations[x] and i[1] not in combinations[x] and i[2] not in combinations[x]:
                            query = "SELECT " + combinations[x] + ",sum(gold),sum(silver),sum(bronze) FROM london12 WHERE " +\
                                    i[0] + " = " + k + " and " + i[1] + " = " + l + " and " + i[2] + " = " + j + " GROUP BY " + combinations[x]
                            list_of_queries.append(query)

    else:
        for k in all_columns[i[0]]:
            k = ''.join(k)
            k = "'{0}'".format(k)
            for l in all_columns[i[1]]:
                l = ''.join(l)
                l = "'{0}'".format(l)
                for j in all_columns[i[2]]:
                    j = ''.join(j)
                    j = "'{0}'".format(j)
                    for n in all_columns[i[3]]:
                        n = ''.join(n)
                        n = "'{0}'".format(n)
                        query = "SELECT continent,agegroup,sport,gender,gold,silver,bronze FROM london12 WHERE " + i[0] + " = " + k + " and "\
                                + i[1] + " = " + l + " and " + i[2] + " = " + j + " and " + i[3] + " = " + n
                        list_of_queries.append(query)
                        for x in range(15):
                            if i[0] not in combinations[x] and i[1] not in combinations[x] and i[2] not in combinations[x] and i[3] not in combinations[x]:
                                query = "SELECT " + combinations[x] + ",sum(gold),sum(silver),sum(bronze) FROM london12 WHERE " + i[0] + " = " + k +\
                                        " and " + i[1] + " = " + l + " and " + i[2] + " = " + j + " and " + i[3] + " = " + n + " GROUP BY " + combinations[x]
                                list_of_queries.append(query)
for i in combinations:
    query = "SELECT " + i + ",sum(gold),sum(silver),sum(bronze) FROM london12 GROUP BY " + i
    list_of_queries.append(query)
query = "SELECT continent,agegroup,sport,gender,gold,silver,bronze FROM london12"
list_of_queries.append(query)


print("number of queries: ", len(list_of_queries))

rsd = {}
medals_in_records = {}
developing_sub_cube = {}
developed_sub_cube = {}

for i in range(len(list_of_queries)):
    mycursor.execute(list_of_queries[i])
    result = mycursor.fetchall()
    all_medals = 0
    bronze_silver = 0
    gold_medals = 0
    mean = []
    for r in result:
        all_medals += float(r[-3] + r[-2] + r[-1])
        bronze_silver += float(r[-2] + r[-1])
        gold_medals += float(r[-3])
        mean.append(r[-3] + r[-2] + r[-1])

    # part A
    if all_medals > 19 and len(result) > 99:
        avg = 0
        for m in mean:
            avg += m
        avg = avg / len(mean)
        sigma = 0
        for m in mean:
            sigma += (m - avg) ** 2

        rsd[i] = math.sqrt(sigma / (len(mean) - 1))

    # part B
    if len(result) > 9:
        medals_in_records[i] = all_medals/len(result)

    # part C
    if all_medals != 0 and (bronze_silver * 100.0 / all_medals) >= 90:
        developing_sub_cube[i] = all_medals

    # part D
    if all_medals != 0 and (gold_medals * 100.0 / all_medals) >= 50:
        developed_sub_cube[i] = all_medals

# part A
holds = []
itemMaxValue = max(rsd.items(), key=lambda x: x[1])
for key, value in rsd.items():
    if value == itemMaxValue[1]:
        holds.append(list_of_queries[key])

for item in holds:
    print("a) query: ", item)

# part B
holds = []
itemMaxValue = max(medals_in_records.items(), key=lambda x: x[1])
for key, value in medals_in_records.items():
    if value == itemMaxValue[1]:
        holds.append(list_of_queries[key])

for item in holds:
    print("b) query: ", item)

# part C
holds = []
itemMaxValue = max(developing_sub_cube.items(), key=lambda x: x[1])
for key, value in developing_sub_cube.items():
    if value == itemMaxValue[1]:
        holds.append(list_of_queries[key])

for item in holds:
    print("c) query: ", item)

# part D
holds = []
itemMaxValue = max(developed_sub_cube.items(), key=lambda x: x[1])
for key, value in developed_sub_cube.items():
    if value == itemMaxValue[1]:
        holds.append(list_of_queries[key])

for item in holds:
    print("d) query: ", item)
