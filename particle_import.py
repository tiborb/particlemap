import csv
import hashlib
from elasticsearch import Elasticsearch
es = Elasticsearch()

FILE = 'rawdata/particledata.csv'
LIMIT = 1000000
INDEX = 'particles-test-index'
DOC = 'measure'

def getCoords(id):
    return {
        '0': [9.182932, 48.775846], # charlottenplatz
        '1': [9.202080, 48.795440], # neckertor
        '2': [9.231777, 48.806068], # canstatt
        '3': [9.163113, 48.768349], # karlshoehe
        '4': [9.131784, 48.765238] # birenkopf
    }.get(id, [9.138565, 48.753469]) # heslach


def createIndex():
     # create empty index
    es.indices.create(
        index=INDEX,
        body={
          'settings': {
            # just one shard, no replicas for testing
            'number_of_shards': 1,
            'number_of_replicas': 0,
          }
        },
        # ignore already existing index
        ignore=400
    )
    es.indices.put_mapping(
        index=INDEX,
        doc_type=DOC,
        body={
          DOC: {
            'properties': {
                #'time': {'type': 'date'},
                'coords': {'type': 'geo_point'},
                #'P10': {'type': 'float'},
                #'P25': {'type': 'float'},
                #'durP10': {'type': 'integer'},
                #'durP25': {'type': 'integer'},
                #'ratioP10': {'type': 'float'},
                #'ratioP25': {'type': 'float'}
            }
          }
        }
    )



def publish(data):
    m = hashlib.md5()
    m.update(data['time'] + data['type'])
    id = m.hexdigest()
    res = es.index(index=INDEX, doc_type=DOC, id=id, body=data)
    print(res['created'])


def walkData():
    with open(FILE, 'rb') as f:
        reader = csv.reader(f)
        cnt = 0
        for row in reader:
            data = {
                'time': row[0],
                'type': row[1],
                'indoor': row[2],
                'location_id': row[3],
                'sampling_rate': row[4],
                'P1': row[5],
                'P2': row[6],
                'durP1': row[7],
                'durP2': row[8],
                'ratioP1': row[9],
                'ratioP2': row[10],
                'temperature': row[11],
                'humidity': row[12],
                'pressure': row[13],
                'altitude': row[14],
                'pressure_sealevel': row[15],
                'brightness': row[16],
                'dust_density': row[17],
                'vo_raw': row[18],
                'voltage': row[19],
                'P10': row[20],
                'P25': row[21],
                'durP10': row[22],
                'durP25': row[23],
                'ratioP10': row[24],
                'ratioP25': row[25]
            }

            data['coords'] = getCoords(data['location_id'])

            #print data, "\n"
            publish(data)

            cnt += 1
            if (cnt >= LIMIT):
                break

## run
createIndex()
walkData()