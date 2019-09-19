from igql import InstagramGraphQL
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('Social_cafe_ky.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

igql_api = InstagramGraphQL()
media = []

user = igql_api.get_hashtag('boxwinner')
for media in user.recent_media():
    print(media)
    ref = db.collection(u'posts').set(media)




