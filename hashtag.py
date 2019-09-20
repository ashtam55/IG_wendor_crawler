from igql import InstagramGraphQL
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import db
import instaloader



cred = credentials.Certificate('Social_cafe_ky.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
L = instaloader.Instaloader()

igql_api = InstagramGraphQL()
media = []

hashtags = igql_api.get_hashtag('boxwinner')
for media_batch in hashtags.recent_media():
    # print(media)
    media.extend(media_batch)
    print(len(media_batch))
    print("Kartik")
    # ref = db.collection(u'posts').document().set(media)

print( len(media) )
batch = db.batch()

for i in range( len(media)):
    print (media[i]["node"]["id"])
    print (media[i]["node"]["taken_at_timestamp"])
    post_ref = db.collection(u'boxwinner').document(media[i]["node"]["id"])
    toPush = media[i]["node"]
    toPush["owner_id"] = toPush["owner"]["id"]
    ID = media[i]["node"]["owner"]["id"]
    profile = instaloader.Profile.from_id(L.context, ID)
    print(profile.username)
    toPush["owner_username"] = profile.username
    batch.update(post_ref, toPush)
batch.commit()
