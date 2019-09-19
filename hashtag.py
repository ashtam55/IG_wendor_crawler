from igql import InstagramGraphQL


igql_api = InstagramGraphQL()
media = []

user = igql_api.get_hashtag('boxwinner')
for media in user.recent_media():
    print(media)