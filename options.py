"""
blogList = [
    {
        "id" : "{blogname}",
        "category": 0000000
    }
]
"""
blogList = [
    {"id": "dummy", "category": 0000000},
]

certification = [
    #HE
    {
        "X-Naver-Client-Id": "{id}",
        "X-Naver-Client-Secret": "{secret}"
    },

]

target_url = [
    "https://www.sciencenews.org",
    "https://www.economist.com",
    "https://www.bbc.com",
    "https://www.huffpost.com",
    "https://forbes.com",
    "https://finance.yahoo.com/",
    "https://www.nytimes.com/",
    "https://www.washingtonpost.com/",
    "https://www.cnbc.com/",
    "https://www.wsj.com/",
    "https://www.thetimes.co.uk/",
    "https://www.yomiuri.co.jp/"
]

options = {
    "keywords": [],
    "characters": {
        "letters": "around 2000 letters not over 2500 letters",
        "a4": 3
    },
    "Readers": [
        "Young people in their 20s and 30s",
        "Youth",
        "children",
        "old man",
        "Ma'am",
        "Bride-to-be",
        "university student",
        "Examine",
        "retired person",
        "investor",
        "high-ranking official",
        "government employee",
        "audience"
    ],
    "Content_goal": [
        "for meta-analysis.",
        "for personal analysis",
        "Bold the parts you think are important",
        "first person to experience",
    ],
    "Priority_style": [
        "First show article title format HTML Code <h1> tag. Add a comment with a sub-head and detail description.",
    ],
    "Writing_style": [
        "include expert opinions\n",
        "Add the summarize news articles that related this article manuscript.\n",
        "Add positive view sight.\n",
        "Add negative view sight.\n",
        "Add Comparative analysis of differences.\n",
        "Grammatical description style.\n",
        "Poetic permission.\n",
        "Editorial style.\n",
        "compare and analyze.\n",
        "suggest planning for the future.\n",
        "add recent news and SNS comment.\n",
    ],
}

