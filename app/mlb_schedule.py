from urllib import parse

BOOKENDS = ["03-30-2023", "10-01-2023"]

base_url = "https://bdfed.stitch.mlbinfra.com/bdfed/transform-mlb-schedule?"

# example for April
params = (
    ("stitch_env", "prod"),
    ("sortTemplate", 5),
    ("sportId", 1),
    ("sportId", 51),
    ("startDate", "2023-04-01"),
    ("endDate", "2023-04-30"),
    # ('gameType', 'S'),
    ("gameType", "R"),
    # ('gameType', 'F'),
    # ('gameType', 'D'),
    # ('gameType', 'L'),
    # ('gameType', 'W'),
    # ('gameType', 'A'),
    ("language", "en"),
    ("leagueId", 104),
    # ('leagueId', 160),
    ("contextTeamId", ""),
)

assembled_url = base_url + parse.urlencode(params)

print(assembled_url)

# this appears to work to fetch all games (probably need to request by month and loop)
# url="https://bdfed.stitch.mlbinfra.com/bdfed/transform-mlb-schedule?stitch_env=prod&sortTemplate=5&sportId=1&&sportId=51&startDate=2023-03-30&endDate=2023-10-01&gameType=E&&gameType=S&&gameType=R&&gameType=F&&gameType=D&&gameType=L&&gameType=W&&gameType=A&language=en&leagueId=104&&leagueId=103&&leagueId=160&contextTeamId="

# import pdb; pdb.set_trace()
