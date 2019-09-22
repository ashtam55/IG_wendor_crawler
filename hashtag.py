from igql import InstagramGraphQL
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import db
import instaloader
import schedule
import time
import paho.mqtt.client as mqtt

broker_address="bot.akriya.co.in"
cred = credentials.Certificate('Social_cafe_ky.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
L = instaloader.Instaloader()
client = mqtt.Client() #create new mqtt instance
client.connect(broker_address)
igql_api = InstagramGraphQL()
media = []



def fetchHashtag():
    
    hashtags = igql_api.get_hashtag('boxwinner')
    for media_batch in hashtags.recent_media():
        media.extend(media_batch)
        print("Total Tags = ",len(media_batch))

        #Push only new hashtags to firebase
        batch = db.batch()
    for i in range( len(media)):
        post_ref = db.collection(u'boxwinner').document(media[i]["node"]["id"])
        toPush = media[i]["node"]
        toPush["owner_id"] = toPush["owner"]["id"]
        ID = media[i]["node"]["owner"]["id"]
        profile = instaloader.Profile.from_id(L.context, ID)
        # print(profile.username)
        toPush["owner_username"] = profile.username
        if (db.collection('boxwinner').document(media[i]["node"]["id"]).get().exists == False):
            print (media[i]["node"]["id"])
            print (media[i]["node"]["taken_at_timestamp"])
            print("pass")
            batch.set(post_ref, toPush)

    batch.commit()
    media.clear()


def on_snapshot(col_snapshot, changes, read_time):
    print(u'Callback received query snapshot.')
    print(u'Current Content:')
    
    for change in changes:
        if change.type.name == 'ADDED':
            client.publish("VMC/1035/VEND_ORDER_ITEM",'{"cmd":"b","oiid":2,"oid":"1"}')#publish
            print(u'New Content: {}'.format(change.document.id))
        elif change.type.name == 'MODIFIED':
            print(u'Modified Content: {}'.format(change.document.id))
        elif change.type.name == 'REMOVED':
            print(u'Removed Content: {}'.format(change.document.id))

col_query = db.collection(u'boxwinner').where(u'fullfilled', u'==', True)
query_watch = col_query.on_snapshot(on_snapshot)


schedule.every(1/10).minutes.do(fetchHashtag)
# schedule.every(1/10).minutes.do(pushTofirebase)

while 1:
    schedule.run_pending()
    time.sleep(1)
