from pytrends.request import TrendReq

def compare_popularity(query1, query2):
    pytrends = TrendReq(hl='ru', tz=360)
    keywords = [query1, query2]
    pytrends.build_payload(keywords, timeframe='today 1-m')
    interest_over_time_df = pytrends.interest_over_time()
    return interest_over_time_df

query1 = "кошки"
query2 = "собаки"
data = compare_popularity(query1, query2)
print(data)

