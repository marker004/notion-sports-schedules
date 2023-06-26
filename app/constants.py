from shared import ElligibleSportsEnum, FavoriteCriterion


INDYCAR_CHANNEL_GOODLIST = [
    "NBC",
    "USA Net",
    "Peacock",
]

F1_CHANNEL_GOODLIST = [
    "ESPN",
    "ESPN2",
    "ABC",
    "ESPN/ESPN+",
    "ABC/ESPN+",
    "ESPN2/ESPN+"
]

MLB_BROADCAST_BADLIST = [
    "KOA 850 AM/94.1 FM ",
    "WMMS 100.7",
    "WTAM 1100",
    "Bally Sports Southwest Extra",
    "Bally Sports Kansas City",
    "NESN",
    "KNBR 680",
    "98.7 FM Arizona's Sports Station",
    "SNET",
    "Bally Deportes San Diego",
    "WFAN 660/101.9 FM",
    "Bally Sports Sun",
    "MLB.TV",
    "Bally Sports South",
    "Bally Sports Southwest",
    "97.1 The Ticket",
    "NBCS BA",
    "SportsNet LA",
    "Bally Sports San Diego",
    "A's Cast",
    "Amazon Prime Video",
    "WLW 700",
    "WEEI 850",
    "NBC Sports App",
    "KBME 790 (delay)",
    "Bally Sports Arizona",
    "SNY",
    "WJFK 106.7 The Fan",
    "Bally Sports Great Lakes",
    "WDAE 620 AM/95.3 FM",
    "KWOD 1660",
    "ATT SportsNet-SW",
    "NBCSP+",
    "ATT SportsNet-RM",
    "YES",
    "Marquee Sports Network",
    "MLB.com",
    "WTMJ 620",
    "670 The Score",
    "Bally Sports SoCal",
    "WAQI 710",
    "NESN+",
    "Audacy",
    "WBAL NewsRadio AM/FM/ HD2 97.9 ",
    "Bally Sports Midwest",
    "Dodgers Radio AM570",
    "NBCSP",
    "KTNQ 1020",
    "MLBN (out-of-market only)",
    "KDKA-FM 93.7",
    "WMVP 1000 AM",
    "KLAA 830",
    "The Wolf 102.9 FM",
    "ROOTNW",
    "WEEI 93.7",
    "SN590",
    "Braves Radio Network",
    "KCSP 610",
    "WXYT 1270",
    "WCNN 680/93.7",
    "1510 AM - KSFN",
    "WCBS 880",
    "WSAI-1360",
    "KIRO 710",
    "Bally Sports Florida",
    "Bloomberg 960 AM",
    "KWFN 97.3",
    "Bally Sports Detroit",
    "Bally Sports Ohio",
    "KCOP",
    "The Team 980",
    "Bally Sports Wisconsin",
    "NBCSCA",
    "NESN 360",
    "FOX Sports 940AM (WINZ)",
    "REAL 106.1",
    "Bally Sports Southeast",
    "Cardinals Radio Network",
    "Bally Sports North",
    "ROOTNW+",
    "Bally Sports West",
    "WPIX",
    "KMOX 1120 AM/98.7 FM",
    "TIBN",
    "94 WIP",
    "TVA Sports",
    "ESPN Phoenix 620",
    "105.3 The Fan",
    "WCCO 830",
    "WIFN 1340 AM/103.7FM",
    "KIRO 710 (delay)",
    "Brewers Radio Network",
    "94.5 ESPN Milwaukee",
    "KBME 790 AM/94.5 FM HD-2",
    "100.1 FM/KDKA-AM 1020",
    "ATT SportsNet-PIT",
    "MASN",
    "98 Rock FM/HD2 97.9, WBAL NewsRadio AM/FM",
    "Sportsnet.ca",
    "SNET NOW App",
    "KHOV Univision 105.1",
    "KIQI 1010",
    "Bloomberg 960 AM/103.7 HD2",
    "MLBN",
    "TUDN WRTO 1200",
    "WTTM 1680",
    "TeleXitos",
    "NBC 10",
    "WIJR AM 880 (En Espanol)",
    "WCCM 1490 AM",
    "WAMG 890 AM",
    "twinsbeisbol.com",
    "Bally Sports North Extra",
    "MASN 2",
    "WAMG 890 AM (SP)",
    "WCCM 1490 AM (SP)",
    "Guardians Radio Network",
    "WADO 1280",
    "WEPN 1050",
    "KNRV 1150",
    "Bally Sports Midwest Extra",
    "TUDN 93.3 / KLAT 1010",
    "XEMO 860",
    "ATT SportsNet-PIT2",
    "La Mejor 1600/1460/1130 AM",
    "Bally Sports Arizona Extra",
    "680 AM/93.7 FM The Fan",
    "NBCS BA+",
    "KWKW 1330",
    "WQBN/1300AM",
    "KFLC 1270",
    "SNET-1",
    "94.5 ESPN Radio",
    "KTMZ 1220",
    "Bally Sports Wisconsin Extra",
    "ESPN Deportes 1050",
    "NBC Bay Area",
    "Bally Sports Florida Extra",
]

MLB_GOODLIST = [
    "NBCSCH",
    "Apple TV+",
    "Peacock",
    "FOX",
    "ESPN2",
    "TBS",
    "ESPN",
    "FS1",
    "NBC",
]

NHL_BROADCAST_BADLIST = [
    "BSSC",
    "NBCSCH+",
    "BSSW",
    "KCOP-13",
    "ALT",
    "SN360",
    "TSN4",
    "SN1",
    "SNW",
    "BSSUNX",
    "BSNX",
    "RDS",
    "BSWIX",
    "NHLN",
    "BSOH",
    "MSGSN2",
    "KONG",
    "BSSUN",
    "SNOL",
    "SNE",
    "TSN3",
    "CBC",
    "BSSWX",
    "NBCSWA",
    "ATTSN-RM",
    "MSG-B",
    "BSMW",
    "SN",
    "NHLN (JIP)",
    "BSDETX",
    "BSWI",
    "MSGSN",
    "NBCSCA",
    "ATTSN-PT",
    "BSN",
    "MSG 2",
    "BSAZX",
    "BSDET",
    "SNW (JIP)",
    "BSAZ",
    "TSN5",
    "CITY",
    "RDS2",
    "ALT2",
    "BSFLX",
    "SNO",
    "BSMW APP",
    "TVAS",
    "TVAS2",
    "SNP",
    "NBCSWA+",
    "SNF",
    "BSW",
    "MSG",
    "BSFL",
    "KTNV",
    "ROOT-NW",
    "TSN2",
    "RDSI",
    "NESN",
    "NBCSP+",
    "BSSO",
    "NBCSP",
]

NBA_BROADCASTER_BADLIST = ["NBA TV"]

SOCCER_BROADCAST_BADLIST = [
    "AT&T SportsNet Southwest",
    "AT&T SportsNet Southwest HD",
    "AT&T SportsNet Southwest Plus",
    "Antenna 20 Years",
    "BEINX",
    "Bally Sports Oklahoma",
    "Bally Sports Oklahoma HD",
    "Bally Sports SoCal",
    "Bally Sports SoCal HD",
    "Bally Sports South - Main Feed",
    "Bally Sports South HD(Full Time)",
    "Bally Sports Southwest HD",
    "Bally Sports Southwest (Main Feed)",
    "CL beIN Sports English SD in Spanish",
    "Caracol TV Canal 1",
    "Centroamerica TV",
    "DAZN USA",
    "ESPN 3",
    "ESPN Deportes",
    "ESPN Deportes HD",
    "ESPN3",
    "Fox Deportes",
    "Fox Deportes HD",
    "Fox Soccer Plus",
    "Fox Soccer Plus HD",
    "Fox Sports 2 HD",
    "Globo",
    "GOL TV",
    "In Demand PPVHD (HD Events)",
    "La 7",
    "MLS Season Pass on Apple TV",
    "MSG Zone 1",
    "MSG HD Zone 1",
    "Next Level Sports HD",
    "NBC Sports California SAT",
    "NBC Sports California SAT HD",
    "NBC Sports Washington",
    "NBC Sports Washington HD",
    "NBCSports.com",
    "NWSLsoccer.com",
    "Nuestra Tele Internacional",
    "Premiere 4 HD",
    "Premiere 8 HD",
    "Premiere Clubes HD",
    "REDEGL",
    "RREC",
    "RTPi RadioTV Portuguesa Int'l",
    "SporTV",
    "SporTV HD",
    "SportPlus",
    "TUDN",
    "TV5MONDE Etats Unis",
    "TV5MONDE Etats Unis HD",
    "Telecentro TV",
    "Telemundo Satellite Feed",
    "Telemundo Satellite Feed Pacific",
    "Twitch",
    "TyC Sports HD",
    "TyC Sports Internacional USA",
    "TyC Sports International",
    "UniMas",
    "UniMas Satellite Feed (Pacific)",
    "Univision NOW",
    "Univision Network",
    "VIX+",
    "ViX",
    "ViX Deportes 21",
    "ViX Deportes 22",
    "ViX+ Deportes 1",
    "ViX+ Deportes 10",
    "ViX+ Deportes 11",
    "ViX+ Deportes 12",
    "ViX+ Deportes 13",
    "ViX+ Deportes 14",
    "ViX+ Deportes 15",
    "ViX+ Deportes 16",
    "ViX+ Deportes 17",
    "ViX+ Deportes 18",
    "ViX+ Deportes 19",
    "ViX+ Deportes 2",
    "ViX+ Deportes 20",
    "ViX+ Deportes 3",
    "ViX+ Deportes 4",
    "ViX+ Deportes 5",
    "ViX+ Deportes 6",
    "ViX+ Deportes 7",
    "ViX+ Deportes 8",
    "ViX+ Deportes 9",
    "Vix Premium Deportes 1",
    "Vix Premium Deportes 2",
    "Vix Premium Deportes 3",
    "Vix Premium Deportes 4",
    "Vix Premium Deportes 5",
    "Vix Premium Deportes 6",
    "Vix Premium Deportes 7",
    "Vix Premium Deportes 8",
    "Vix Premium Deportes 9",
    "Vix Premium Deportes 10",
    "Vix Premium Deportes 11",
    "Vix Premium Deportes 12",
    "Vix Premium Deportes 13",
    "Yes Network",
    "Yes Network HD",
    "Zona TUDN",
    "beIN SPORTS 2",
    "beIN SPORTS 2 HD",
    "beIN SPORTS 3",
    "beIN SPORTS 3 HD",
    "beIN SPORTS 4",
    "beIN SPORTS 4 HD",
    "beIN SPORTS 5",
    "beIN SPORTS 5 HD",
    "beIN SPORTS 6",
    "beIN SPORTS 6 HD",
    "beIN SPORTS 7",
    "beIN SPORTS 7 HD",
    "beIN SPORTS 8",
    "beIN SPORTS 8 HD",
    "beIN Sports",
    "beIN Sports En Español",
    "beIN Sports En Español HD",
    "beIN Sports HD",
    "beIN XTRA ESPAñOL",
    "fuboTV",
    "iFollow",
]

SOCCER_GOODLIST = [
    "CBS Sports Network HD",
    "Peacock",
    "TBS HD (Pacific)",
    "FS1 HD",
    "UNIVERSO HD",
    "ESPN+ USA",
    "TBS",
    "CBS",
    "FOX",
    "Telemundo Television Network",
    "CBS Sports Network",
    "FS2",
    "USA Network",
    "TBS HD",
    "UNIVERSO",
    "FS1",
    "USA Network HD",
    "Paramount+",
    "CBS All Access",
    "ESPNU HD",
    "ESPNU",
]


NATIONAL_FLAGS = {
    "Ascension Island": "🇦🇨",
    "Andorra": "🇦🇩",
    "United Arab Emirates": "🇦🇪",
    "Afghanistan": "🇦🇫",
    "Antigua & Barbuda": "🇦🇬",
    "Anguilla": "🇦🇮",
    "Albania": "🇦🇱",
    "Armenia": "🇦🇲",
    "Angola": "🇦🇴",
    "Antarctica": "🇦🇶",
    "Argentina": "🇦🇷",
    "American Samoa": "🇦🇸",
    "Austria": "🇦🇹",
    "Australia": "🇦🇺",
    "Aruba": "🇦🇼",
    "Åland Islands": "🇦🇽",
    "Azerbaijan": "🇦🇿",
    "Bosnia & Herzegovina": "🇧🇦",
    "Barbados": "🇧🇧",
    "Bangladesh": "🇧🇩",
    "Belgium": "🇧🇪",
    "Burkina Faso": "🇧🇫",
    "Bulgaria": "🇧🇬",
    "Bahrain": "🇧🇭",
    "Burundi": "🇧🇮",
    "Benin": "🇧🇯",
    "St. Barthélemy": "🇧🇱",
    "Bermuda": "🇧🇲",
    "Brunei": "🇧🇳",
    "Bolivia": "🇧🇴",
    "Caribbean Netherlands": "🇧🇶",
    "Brazil": "🇧🇷",
    "Bahamas": "🇧🇸",
    "Bhutan": "🇧🇹",
    "Bouvet Island": "🇧🇻",
    "Botswana": "🇧🇼",
    "Belarus": "🇧🇾",
    "Belize": "🇧🇿",
    "Canada": "🇨🇦",
    "Cocos (Keeling) Islands": "🇨🇨",
    "Congo - Kinshasa": "🇨🇩",
    "Central African Republic": "🇨🇫",
    "Congo - Brazzaville": "🇨🇬",
    "Switzerland": "🇨🇭",
    "Côte d’Ivoire": "🇨🇮",
    "Cook Islands": "🇨🇰",
    "Chile": "🇨🇱",
    "Cameroon": "🇨🇲",
    "China": "🇨🇳",
    "Colombia": "🇨🇴",
    "Clipperton Island": "🇨🇵",
    "Costa Rica": "🇨🇷",
    "Cuba": "🇨🇺",
    "Cape Verde": "🇨🇻",
    "Curaçao": "🇨🇼",
    "Christmas Island": "🇨🇽",
    "Cyprus": "🇨🇾",
    "Czechia": "🇨🇿",
    "Germany": "🇩🇪",
    "Diego Garcia": "🇩🇬",
    "Djibouti": "🇩🇯",
    "Denmark": "🇩🇰",
    "Dominica": "🇩🇲",
    "Dominican Republic": "🇩🇴",
    "Algeria": "🇩🇿",
    "Ceuta & Melilla": "🇪🇦",
    "Ecuador": "🇪🇨",
    "Estonia": "🇪🇪",
    "Egypt": "🇪🇬",
    "Western Sahara": "🇪🇭",
    "Eritrea": "🇪🇷",
    "Spain": "🇪🇸",
    "Ethiopia": "🇪🇹",
    "European Union": "🇪🇺",
    "Finland": "🇫🇮",
    "Fiji": "🇫🇯",
    "Falkland Islands": "🇫🇰",
    "Micronesia": "🇫🇲",
    "Faroe Islands": "🇫🇴",
    "France": "🇫🇷",
    "Gabon": "🇬🇦",
    "United Kingdom": "🇬🇧",
    "Grenada": "🇬🇩",
    "Georgia": "🇬🇪",
    "French Guiana": "🇬🇫",
    "Guernsey": "🇬🇬",
    "Ghana": "🇬🇭",
    "Gibraltar": "🇬🇮",
    "Greenland": "🇬🇱",
    "Gambia": "🇬🇲",
    "Guinea": "🇬🇳",
    "Guadeloupe": "🇬🇵",
    "Equatorial Guinea": "🇬🇶",
    "Greece": "🇬🇷",
    "South Georgia & South Sandwich Islands": "🇬🇸",
    "Guatemala": "🇬🇹",
    "Guam": "🇬🇺",
    "Guinea-Bissau": "🇬🇼",
    "Guyana": "🇬🇾",
    "Hong Kong SAR China": "🇭🇰",
    "Heard & McDonald Islands": "🇭🇲",
    "Honduras": "🇭🇳",
    "Croatia": "🇭🇷",
    "Haiti": "🇭🇹",
    "Hungary": "🇭🇺",
    "Canary Islands": "🇮🇨",
    "Indonesia": "🇮🇩",
    "Ireland": "🇮🇪",
    "Israel": "🇮🇱",
    "Isle of Man": "🇮🇲",
    "India": "🇮🇳",
    "British Indian Ocean Territory": "🇮🇴",
    "Iraq": "🇮🇶",
    "Iran": "🇮🇷",
    "Iceland": "🇮🇸",
    "Italy": "🇮🇹",
    "Jersey": "🇯🇪",
    "Jamaica": "🇯🇲",
    "Jordan": "🇯🇴",
    "Japan": "🇯🇵",
    "Kenya": "🇰🇪",
    "Kyrgyzstan": "🇰🇬",
    "Cambodia": "🇰🇭",
    "Kiribati": "🇰🇮",
    "Comoros": "🇰🇲",
    "St. Kitts & Nevis": "🇰🇳",
    "North Korea": "🇰🇵",
    "South Korea": "🇰🇷",
    "Kuwait": "🇰🇼",
    "Cayman Islands": "🇰🇾",
    "Kazakhstan": "🇰🇿",
    "Laos": "🇱🇦",
    "Lebanon": "🇱🇧",
    "St. Lucia": "🇱🇨",
    "Liechtenstein": "🇱🇮",
    "Sri Lanka": "🇱🇰",
    "Liberia": "🇱🇷",
    "Lesotho": "🇱🇸",
    "Lithuania": "🇱🇹",
    "Luxembourg": "🇱🇺",
    "Latvia": "🇱🇻",
    "Libya": "🇱🇾",
    "Morocco": "🇲🇦",
    "Monaco": "🇲🇨",
    "Moldova": "🇲🇩",
    "Montenegro": "🇲🇪",
    "St. Martin": "🇲🇫",
    "Madagascar": "🇲🇬",
    "Marshall Islands": "🇲🇭",
    "North Macedonia": "🇲🇰",
    "Mali": "🇲🇱",
    "Myanmar (Burma)": "🇲🇲",
    "Mongolia": "🇲🇳",
    "Macao Sar China": "🇲🇴",
    "Northern Mariana Islands": "🇲🇵",
    "Martinique": "🇲🇶",
    "Mauritania": "🇲🇷",
    "Montserrat": "🇲🇸",
    "Malta": "🇲🇹",
    "Mauritius": "🇲🇺",
    "Maldives": "🇲🇻",
    "Malawi": "🇲🇼",
    "Mexico": "🇲🇽",
    "Malaysia": "🇲🇾",
    "Mozambique": "🇲🇿",
    "Namibia": "🇳🇦",
    "New Caledonia": "🇳🇨",
    "Niger": "🇳🇪",
    "Norfolk Island": "🇳🇫",
    "Nigeria": "🇳🇬",
    "Nicaragua": "🇳🇮",
    "Netherlands": "🇳🇱",
    "Norway": "🇳🇴",
    "Nepal": "🇳🇵",
    "Nauru": "🇳🇷",
    "Niue": "🇳🇺",
    "New Zealand": "🇳🇿",
    "Oman": "🇴🇲",
    "Panama": "🇵🇦",
    "Peru": "🇵🇪",
    "French Polynesia": "🇵🇫",
    "Papua New Guinea": "🇵🇬",
    "Philippines": "🇵🇭",
    "Pakistan": "🇵🇰",
    "Poland": "🇵🇱",
    "St. Pierre & Miquelon": "🇵🇲",
    "Pitcairn Islands": "🇵🇳",
    "Puerto Rico": "🇵🇷",
    "Palestinian Territories": "🇵🇸",
    "Portugal": "🇵🇹",
    "Palau": "🇵🇼",
    "Paraguay": "🇵🇾",
    "Qatar": "🇶🇦",
    "Réunion": "🇷🇪",
    "Romania": "🇷🇴",
    "Serbia": "🇷🇸",
    "Russia": "🇷🇺",
    "Rwanda": "🇷🇼",
    "Saudi Arabia": "🇸🇦",
    "Solomon Islands": "🇸🇧",
    "Seychelles": "🇸🇨",
    "Sudan": "🇸🇩",
    "Sweden": "🇸🇪",
    "Singapore": "🇸🇬",
    "St. Helena": "🇸🇭",
    "Slovenia": "🇸🇮",
    "Svalbard & Jan Mayen": "🇸🇯",
    "Slovakia": "🇸🇰",
    "Sierra Leone": "🇸🇱",
    "San Marino": "🇸🇲",
    "Senegal": "🇸🇳",
    "Somalia": "🇸🇴",
    "Suriname": "🇸🇷",
    "South Sudan": "🇸🇸",
    "São Tomé & Príncipe": "🇸🇹",
    "El Salvador": "🇸🇻",
    "Sint Maarten": "🇸🇽",
    "Syria": "🇸🇾",
    "Eswatini": "🇸🇿",
    "Tristan Da Cunha": "🇹🇦",
    "Turks & Caicos Islands": "🇹🇨",
    "Chad": "🇹🇩",
    "French Southern Territories": "🇹🇫",
    "Togo": "🇹🇬",
    "Thailand": "🇹🇭",
    "Tajikistan": "🇹🇯",
    "Tokelau": "🇹🇰",
    "Timor-Leste": "🇹🇱",
    "Turkmenistan": "🇹🇲",
    "Tunisia": "🇹🇳",
    "Tonga": "🇹🇴",
    "Turkey": "🇹🇷",
    "Trinidad & Tobago": "🇹🇹",
    "Tuvalu": "🇹🇻",
    "Taiwan": "🇹🇼",
    "Tanzania": "🇹🇿",
    "Ukraine": "🇺🇦",
    "Uganda": "🇺🇬",
    "U.S. Outlying Islands": "🇺🇲",
    "United Nations": "🇺🇳",
    "United States": "🇺🇸",
    "Uruguay": "🇺🇾",
    "Uzbekistan": "🇺🇿",
    "Vatican City": "🇻🇦",
    "St. Vincent & Grenadines": "🇻🇨",
    "Venezuela": "🇻🇪",
    "British Virgin Islands": "🇻🇬",
    "U.S. Virgin Islands": "🇻🇮",
    "Vietnam": "🇻🇳",
    "Vanuatu": "🇻🇺",
    "Wallis & Futuna": "🇼🇫",
    "Samoa": "🇼🇸",
    "Kosovo": "🇽🇰",
    "Yemen": "🇾🇪",
    "Mayotte": "🇾🇹",
    "South Africa": "🇿🇦",
    "Zambia": "🇿🇲",
    "Zimbabwe": "🇿🇼",
    "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Wales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿",
}

MLB_FAVORITE_CRITERIA: list[FavoriteCriterion] = [
    {"property": "matchup", "comparison": "contains", "value": "Red Sox"},
]

NBA_FAVORITE_CRITERIA: list[FavoriteCriterion] = [
    {
        "property": "sport",
        "comparison": "equals",
        "value": ElligibleSportsEnum.NBA.value,
    },
]

NCAA_TOURNAMENT_FAVORITE_CRITERIA: list[FavoriteCriterion] = [
    {
        "property": "sport",
        "comparison": "equals",
        "value": ElligibleSportsEnum.BASKETBALL.value,
    },
]

NHL_FAVORITE_CRITERIA: list[FavoriteCriterion] = [
    {"property": "matchup", "comparison": "contains", "value": "Bruins"},
]


SOCCER_FAVORITE_CRITERIA: list[FavoriteCriterion] = [
    {"property": "league", "comparison": "equals", "value": "Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
    {"property": "league", "comparison": "equals", "value": "MLS 🇺🇸"},
    {"property": "league", "comparison": "equals", "value": "Champions League"},
    {"property": "league", "comparison": "equals", "value": "EURO"},
    {"property": "matchup", "comparison": "contains", "value": "Indy Eleven"},
    {"property": "matchup", "comparison": "contains", "value": "USA"},
]
