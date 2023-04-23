import openai
import time
from datetime import datetime
from core_def import *
import requests

tokens = "{TISTORY_TOKEN}"
if not tokens:
    tokens = input("Tistory Tokens:")

openai.api_key = "{chatGPT_API_KEY}"
model = "text-davinci-003"


# 1. Select keyword from recent news list.
def targeting():
    """
    :return: ABC,DEF,CGHDJ,DHJSAD
    """
    # option > target_url
    choice_url = generate_target_url(target_url)
    res = openai.Completion.create(
        model=model,
        prompt="only list recent news keywords at %s, %s and keywords format python list. And just show combined in a ONE "
               "list." % (choice_url[0], choice_url[1]),
        max_tokens=2048
    )
    keywords = ""
    for choice in res.choices:
        keywords = choice.text

    newGen_keywords = keywords.replace("\n\n", "") \
        .replace("'", "") \
        .replace('"', "") \
        .strip('][').split(',')
    print(">>> 키워드 추출 완료")
    check_keywords = []
    get_len_keywords = len(newGen_keywords)

    if get_len_keywords < 7:
        max_keywords = get_len_keywords
    else:
        max_keywords = random.choice(range(5, get_len_keywords))
        if max_keywords > 10:
            max_keywords = 10

    while True:
        choice_keyword = random.choice(newGen_keywords)
        # invalid covid keywords
        if choice_keyword not in check_keywords \
                and choice_keyword.lower().replace(" ", "") != "coronavirus" \
                and choice_keyword.lower().replace(" ", "") != "covid-19" \
                and choice_keyword.lower().replace(" ", "") != "virus" \
                and choice_keyword.lower().replace(" ", "") != "vaccines" \
                and choice_keyword.lower().replace(" ", "") != "vaccine" \
                and choice_keyword.lower().replace(" ", "") != "pandemic" \
                and choice_keyword.lower().replace(" ", "") != "covid" \
                and choice_keyword.lower().replace(" ", "") != "Covid-19Vaccines" \
                and choice_keyword.lower().replace(" ", "") != "PCRtesting":
            check_keywords.append(choice_keyword)
            if len(check_keywords) == max_keywords:
                break
        else:
            pass
    suggest_keywords = ','.join(check_keywords)
    print(suggest_keywords)
    return suggest_keywords


#2. Job Action
class Job:
    def __init__(self, blogname, keywords):
        self.name = blogname
        self.keywords = keywords
        self.tokens = ''
        self.en_manuscript = ""
        self.papago = ""
        self.writing_style_text = ''

    # random choice writing style
    def generate_writing_style(self):
        """
        :return: (str) ABC,CDE,DSA
        """
        nonce = random.choices(range(3, len(options["Writing_style"])))
        choice_style = []
        while True:
            styled = random.choices(options["Writing_style"])
            if styled not in choice_style:
                choice_style.append(styled)
                if len(choice_style) == nonce[0]:
                    break
        writing_style_text = ""
        for i in choice_style:
            writing_style_text += i[0]
        self.writing_style_text = writing_style_text
        return writing_style_text

    # Generate article via chatGPT
    def generate_article(self):
        article_subj = "Please write a long blog article based on the following keywords and options.\n"

        writing_style = options["Priority_style"][0] + self.generate_writing_style()
        prompt = article_subj + "Keywords: %s\nNumber of characters: %s\nReaders: %s\nWriting Style: %s\n* Important article " \
                                "format is HTML Code that <h1> tag is title and <h3> tag is sub title and add <br> tag, " \
                                "after sub title " \
                 % (self.keywords, options["characters"]["letters"], random.choices(options["Readers"])[0],
                    writing_style)
        print(">>>>원고 작성중===========")
        res = openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=2048
        )
        manuscript = ""
        for choice in res.choices:
            manuscript = choice.text

        en_manuscript = str(manuscript.replace("\n\n", ""))
        print(">>>>>[EN]원고 완료===========")
        self.en_manuscript = en_manuscript
        return en_manuscript


# 3. en_manuscript
def translator(en_manuscripts):
    print("번역 작성중===========")
    papago_nonce = 0
    while True:
        papago = papago_engine(en_manuscripts, papago_nonce)
        if papago == "Error_of_nonce_update":
            papago_nonce += 1
            print("[Error] >>>>> papapgo nonce update")
        elif papago == "Error 5000":
            break
        elif papago == "over nonce":
            send_msg("[Over Nonce]\nhttps://developers.naver.com/apps/#/list")
            breakpoint(">>>>>>>>>> over nonce")

        else:
            break
        time.sleep(1)
    return papago


# 3. en_manuscript 필요
def get_blogImage(en_manuscript):
    print("Load Image URL...")
    en_title = en_manuscript[en_manuscript.find("<h1>") + 4:en_manuscript.find("</h1>")]
    res_img = openai.Completion.create(
        model=model,
        prompt='[INFO: Use the Unsplash API (https://source.unsplash.com/1600x900/?<PUT YOUR QUERY HERE>). the query is just some tags that describes the image. Write the final Image URL.] ## DO NOT RESPOND TO INFO BLOCK ## Give me a blog cover image url fit to this subject: %s"' \
               % en_title,
        max_tokens=50
    )
    get_url_img = ""
    for choice in res_img.choices:
        get_url_img = choice.text.replace("\n\n", "")

    headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Connection": "keep-alive", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"}

    r = requests.get(get_url_img, headers=headers, stream=True)
    file_name = datetime.now().strftime("%y%m%d%H%s") + ".jpeg"

    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            for chunk in r:
                f.write(chunk)
            f.close()
    time.sleep(1.5)
    print(">>>>> main image download=====")
    return file_name


# 4. blog job
def upload_article_at_blog(blogname, category, papago, file_name, exist_tokens='',):
    # 더미 Tistory 객체
    checker = Tistory()
    if exist_tokens:
        checker.tokens = exist_tokens
        checker.token_active()
        if checker.tokens_active == "200":
            confirm_tokens = exist_tokens
        else:
            confirm_tokens = checker.get_tistory_access_token()
    else:
        confirm_tokens = checker.get_tistory_access_token()
        checker.token_active()
        if checker.tokens_active == "200":
            pass

    print("CHECKER CONFIRM TOKENS: ", checker.tokens)
    # Tistory 클래스 생성
    tis = Tistory()
    tis.tokes = confirm_tokens.replace(" ", "")
    tis.tokens_active = "200"
    tis.blogname = blogname
    tis.category = category

    res_img_url = '<p data-ke-size="size18">' + tis.tistory_file_uploader(file_name, confirm_tokens) + '</p><br>'
    # 타이틀 # 내용
    ptag = '<p data-ke-size="size18">'
    body = ''
    ct = 0
    if "</h1>" in papago:
        if "<h1>" in papago:
            title = papago[papago.find("<h1>") + 4:papago.find("</h1>")]
        else:
            title = papago[:papago.find("</h1>")]

        for i in papago[papago.find("</h1>") + 5:].split("."):
            if body[-4:] == "</p>":
                body += ptag + i + ". "
            else:
                body += i + ". "
            ct += 1
            if ct == 5:
                body += '</p>'
                ct = 0
    else:
        if "<h1>" not in papago:
            title = papago[:30] + "..."
            # 내용
            for i in papago.split("."):
                if body[-4:] == "</p>":
                    body += ptag + i + ". "
                else:
                    body += i + ". "
                ct += 1
                if ct == 5:
                    body += '</p>'
                    ct = 0
        else:
            title = papago[:papago.find("<h1>")]
            # 내용
            for i in papago[papago.find("<h1>") + 4:].split("."):
                if body[-4:] == "</p>":
                    body += ptag + i + ". "
                else:
                    body += i + ". "
                ct += 1
                if ct == 5:
                    body += '</p>'
                    ct = 0


    """
    tokens, res_img_url, title, body
    """
    tis.tistory_write(res_img_url, title, body, confirm_tokens)

    print("Finish")
    return confirm_tokens