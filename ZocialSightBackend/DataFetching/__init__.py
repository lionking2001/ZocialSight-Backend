from DataFetching.Facebook import GraphAPI


class init:
    GraphAPI.scrapeFacebookPageFeedPost("TwitterInc",2000)
    GraphAPI.scrapeFacebookPageFeedStatus("TwitterInc",2000)
