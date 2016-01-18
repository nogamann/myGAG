from buildPickle import *
from dateFuctions import *
from graphBuilder import *
from sys import argv

WORK_DF = './static/data/newNY_min.p'



def userQuery(start_date = 1449496184, end_date = 1452952184):
    start_date = int(start_date)
    end_date = int(end_date)
    # filter Data frame
    df = readPickle(WORK_DF)
    print('removing too early')
    df = removeTooEarly(df, start_date)
    print("removing too late")
    df = removeTooLate(df, end_date + 14*DAY)
    print("clearing none availables")
    df = clearNotAvailables(df)
    print("building graph")
    my_graph = buildGraph(df, start_date, end_date)
    print("running A*")
    result = nx.dijkstra_path(my_graph, source='start', target='end')
    print("returning result")
    df.set_index('id', inplace=1)
    result = returnResultIds(result, my_graph)
    for index, value in enumerate(result):
        row = df.loc[value['name']]
        imurl = row['photos'][0]['large']
        href = row['provider']['url']
        result[index]['imurl']= imurl
        result[index]['href']= href
    return result

if __name__ == '__main__':
    if len(argv) == 3:
        start = int(argv[1])
        end = int(argv[2])
    else:
        start = 1449496184 + DAY
        end = start + 40*DAY
    userQuery(start, end)
