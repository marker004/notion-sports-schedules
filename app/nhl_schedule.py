from urllib import parse

BOOKENDS = ["2022-10-07", "2023-14-13"]

base_url = "https://statsapi.web.nhl.com/api/v1/schedule?"

params = (
    ("startDate", "2023-02-14"),
    ("endDate", "2023-02-19"),
    ("hydrate", "broadcasts(all)"),
    ("site", "en_nhl"),
    ("teamId", ""),
    ("gameType", ""),
    ("timecode", ""),
)

assembled_url = base_url + parse.urlencode(params, safe=",()")

url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate=2023-02-14&endDate=2023-02-19&hydrate=team,linescore,broadcasts(all),tickets,game(content(media(epg)),seriesSummary),radioBroadcasts,metadata,seriesSummary(series)&site=en_nhl&teamId=&gameType=&timecode="

print(assembled_url)
print(url)

assert assembled_url == url
