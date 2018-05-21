
import facepy
import urllib3
import json
import datetime
import time


token = "EAACEdEose0cBAMAtCzHkqUGpuNyESRawd3rZC3Qi4UqZB5fsB4Mf1Rl65JOOtXxLviodZBXcvXgs7sYTV3OjO1u8ZCTJWGPdaVXZCNkgwyYZB1tMyMburZACdcwWwwuVsZAWulYPZBaKljJTHLAZAas1JyHi3uZCtvd2gokza8pa2Ei7bI1ubmaD5HnRqewcnuafH8ZD"
graph = facepy.GraphAPI(token, version='2.12')
statueId="20531316728_10157104308481729"
pageId='TwitterInc'
# graph = facebook.GraphAPI(token)


class GraphAPI:
    def __init__(self):
        self.profile = ""

    # access and send order to api
    def getDataFromGraph(self, obj_id, field):
        return graph.get(id=obj_id, fields=field)

    # get feed from api
    def getFeedData(self, obj_id, field):
        return self.getDataFromGraph(obj_id, field)

    # retreive comment of feed
    def getFeedMessage(self, statueId, field):
        self.profile = self.getFeedData(statueId, field)
        for message in self.profile['feed']['data']:
            print(message['message'] + "\n")

    # count reaction of feed
    def getStatueReaction(self,statueId):
        field = "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
                ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
                ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
                ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
                ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
                ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"

        profile = self.getDataFromGraph(statueId, field)
        print("Like: %s" %profile['like']['summary']['total_count'])
        print("Love: %s" % profile['love']['summary']['total_count'])
        print("Wow: %s" % profile['wow']['summary']['total_count'])
        print("Haha: %s" % profile['haha']['summary']['total_count'])
        print("Sad: %s" % profile['sad']['summary']['total_count'])
        print("Angry: %s" % profile['angry']['summary']['total_count'])

    def scrapeFacebookPageFeedPost(self, page_id, limit):
            has_next_page = True
            num_processed = 0  # keep a count on how many we've processed
            scrape_starttime = datetime.datetime.now()
            statuses = graph.get(id=page_id, fields='feed.limit({})'.format(limit))

            while has_next_page:
                for status in statuses['feed']['data']:
                    print(status['message'])
                    num_processed += 1
                    if num_processed % 100 == 0:
                        print("%s Statuses Processed: %s" % (num_processed, datetime.datetime.now()))

                if 'paging' in statuses.keys():
                    statuses = json.loads((statuses['paging']['next']))
                else:
                    has_next_page = False

            print("\nDone!\n%s Statuses Processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime))
            time.sleep(20000)


    # retreive feed from page
    def scrapeFacebookPageFeedStatus(self, page_id, limit):
        has_next_page = True
        num_processed = 0  # keep a count on how many we've processed
        scrape_starttime = datetime.datetime.now()
        statuses = graph.get(id=page_id, fields='feed{comments}')

        while has_next_page:
            for status in statuses['feed']['data']:
                if 'comments' not in status:
                    continue
                for message in status['comments']['data']:
                    print(message['message'])

                num_processed += 1
                if num_processed % 100 == 0:
                    print("%s Statuses Processed: %s" % (num_processed, datetime.datetime.now()))

            if 'paging' in statuses.keys():
                statuses = json.loads((statuses['paging']['next']))
            else:
                has_next_page = False
            time.sleep(3600)

        print("\nDone!\n%s Statuses Processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime))
        print("--------------------------------------------------------------------------------------------------")
c = GraphAPI()
c.scrapeFacebookPageFeedStatus(pageId,1)
c.scrapeFacebookPageFeedPost(pageId,1)
# c.getStatueReaction(1)