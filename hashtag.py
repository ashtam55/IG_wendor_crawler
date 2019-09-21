from igql import InstagramGraphQL
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import db
import instaloader
import schedule
import time


cred = credentials.Certificate('Social_cafe_ky.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
L = instaloader.Instaloader()

igql_api = InstagramGraphQL()
media = []



def fetchHashtag():
    
    hashtags = igql_api.get_hashtag('boxwinner')
    for media_batch in hashtags.recent_media():
        # print(media)
        media.extend(media_batch)
        print(len(media_batch))
        print("Kartik")
        # ref = db.collection(u'posts').document().set(media)

        # print( len(media) )
        batch = db.batch()
    for i in range( len(media)):
        # print (media[i]["node"]["id"])
        # print (media[i]["node"]["taken_at_timestamp"])
        post_ref = db.collection(u'boxwinner').document(media[i]["node"]["id"])
        toPush = media[i]["node"]
        toPush["owner_id"] = toPush["owner"]["id"]
        ID = media[i]["node"]["owner"]["id"]
        profile = instaloader.Profile.from_id(L.context, ID)
        # print(profile.username)
        toPush["owner_username"] = profile.username
        if (db.collection('boxwinner').document(media[i]["node"]["id"]).get().exists):
            # print("push")
            batch.update(post_ref, toPush)
        # elif(db.collection('boxwinner').document(media[i]["node"]["fullfilled"]).get().exists):
        #     print("here")
        else:
            # print("pass")
            batch.set(post_ref, toPush)
            pass

    batch.commit()
    media.clear()
    # for media_batch in L.get_hashtag_posts('boxwinner'):
    # # post is an instance of instaloader.Post
    #     print(media)
    #     media.extend(media_batch)
    #     print(len(media_batch))
    #     L.download_post(media, target='#boxwinner')



# def pushTofirebase():
#     batch = db.batch()

#     for i in range( len(media)):
#         print (media[i]["node"]["id"])
#         print (media[i]["node"]["taken_at_timestamp"])
#         post_ref = db.collection(u'boxwinner').document(media[i]["node"]["id"])
#         toPush = media[i]["node"]
#         toPush["owner_id"] = toPush["owner"]["id"]
#         ID = media[i]["node"]["owner"]["id"]
#         profile = instaloader.Profile.from_id(L.context, ID)
#         print(profile.username)
#         toPush["owner_username"] = profile.username
#         if (db.collection('boxwinner').document(media[i]["node"]["id"]).get().exists):
#             print("push")
#             batch.update(post_ref, toPush)
#         # elif(db.collection('boxwinner').document(media[i]["node"]["fullfilled"]).get().exists):
#         #     print("here")
#         else:
#             print("pass")
#             batch.set(post_ref, toPush)
#             pass
        
#     batch.commit()
#     media.clear()

# def on_snapshot(col_snapshot, changes, read_time):
#     print(u'Callback received query snapshot.')
#     print(u'Current cities in California:')
#     for doc in col_snapshot:
#         print(u'{}'.format(doc.id))

# col_query = db.collection(u'boxwinner').where(u'fullfilled',u'==',u'true')

# # Watch the collection query
# query_watch = col_query.on_snapshot(on_snapshot)

schedule.every(1/10).minutes.do(fetchHashtag)
# schedule.every(1/10).minutes.do(pushTofirebase)

while 1:
    schedule.run_pending()
    time.sleep(1)