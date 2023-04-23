import random
from options import *
import requests
import os
from datetime import datetime

# random choice URL
def generate_target_url(uri):
    """
    :param uri: [list] options.target_url
    :return: [list] len 2
    """
    choice_url = []
    while True:
        chosen = random.choice(uri)
        if chosen not in choice_url:
            choice_url.append(chosen)
            if len(choice_url) == 2:
                break

    print("Target URL: ", choice_url)
    return choice_url


# papago translate
def papago_engine(txt, nonce):
    print("NONCE: ", nonce)
    if nonce == len(certification):
        return "over nonce"
    # data = "source=en&target=ko&text=%s" % txt
    data = {
        "source": "en",
        "target": "ko",
        "text": txt.encode('utf-8')
    }
    res = requests.post(
        "https://openapi.naver.com/v1/papago/n2mt",
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Naver-Client-Id": certification[nonce]["X-Naver-Client-Id"],
            "X-Naver-Client-Secret": certification[nonce]["X-Naver-Client-Secret"]
        },
        data=data
    )

    # 파파고 쿼리 이상 쓸 경우....
    try:
        papago = res.json()["message"]["result"]["translatedText"]
        title = papago[papago.find("<h1>") + 4:papago.find("</h1>")]
        return papago

    except Exception as e:
        if res.json()["errorMessage"]:
            if res.json()["errorMessage"] == "text parameter exceeds max length (text 파라미터가 최대 용량을 초과했습니다.)":
                return "Error 5000"
            else:
                # 쿼리 초과 또는 text 5000 자 초과....
                print(res.json()["errorMessage"])
                return "Error_of_nonce_update"
        else:
            print(str(e))


class Tistory:
    def __init__(self):
        self.code = ""
        self.tokens = ""
        self.tokens_active = "400"
        self.blogname = ""
        self.category = 0

    # get Tokens
    def get_tistory_access_token(self):
        # get code url
        get_code_url = "https://www.tistory.com/oauth/authorize?client_id={client_id}&redirect_uri" \
                       "=https://{redirect_uri}&response_type=code "
        get_code = input("OPEN BROWSER: %s\n And input CODE: " % get_code_url)
        self.code = get_code
        # get Access Tokens
        get_token_url = "https://www.tistory.com/oauth/access_token?client_id={client_id}}&client_secret" \
                        "={client_secret}&redirect_uri=https" \
                        "://{redirect_uri}&code=%s&grant_type=authorization_code" % get_code

        get_code = requests.get(get_token_url).text
        print("Tokens: ", get_code[get_code.find("=")+1:])
        tokens = get_code[get_code.find("=")+1:]
        self.tokens = tokens
        return tokens

    # token check
    def token_active(self):
        if self.tokens:
            self.tokens_active = requests.get("https://www.tistory.com/apis/blog/info?access_token=%s&output=json" %self.tokens).json()["tistory"]["status"]
            if self.tokens_active == "200":
                print("Token 200")
                return self.tokens_active
            else:
                print("Token 400")
                return self.tokens_active
        else:
            print("Token 400")
            self.tokens_active = "400"
            return "400"

    # tistory file uploader
    def tistory_file_uploader(self, filename, new_tokens):
        print(">>>>>", filename, ": main Image uploading =====")
        print("uploade tokens: ", )
        url = "https://www.tistory.com/apis/post/attach"
        files = {'uploadedfile': open(os.getcwd() + '/' + filename, 'rb')}
        params = {
            "access_token": new_tokens,
            "blogName": self.blogname,
            "output": "json",
            'targetUrl': self.blogname
        }
        try:
            res = requests.post(
                url, params=params, files=files
            )
            print(res.json()["tistory"]["replacer"])
            return res.json()["tistory"]["replacer"]
        except Exception as e:
            print("<><><> Error Image Upload: ", str(e), "<><><>")
            return "<br>"

    # tistory write
    def tistory_write(self, res_img_url, title, body, confirm_tokens):
        """
        :param confirm_tokens: exist tokens
        :param res_img_url: (replacer)
        :param title: <h1>title</h1>
        :param body: body
        :return:
        """
        if len(title) > 90:
            title = title[:90] + "..."

        url = "https://www.tistory.com/apis/post/write?"
        form_data = {
            "title": title,
            "content": res_img_url+body,
            "category": self.category,
            "access_token": confirm_tokens,
            "output": "json",
            "blogName": self.blogname,
            "visibility": 2
        }
        print(form_data)
        res = requests.post(
            url,
            data=form_data,
        )

        try:
            result_url = res.json()["tistory"]["url"]
            print(result_url)
            send_msg(datetime.now().strftime("%Y.%m.%d")+"["+self.blogname+"]\n["+title+"]\n\n"+result_url)
            return result_url
        except Exception as e:
            if res.json()["tistory"]["status"] == '406':
                send_msg("**[티스토리 하루 15개 발행 끝]**")
            else:
                print(res.json())
                print(e)
            return "Error:", str(e)


# Telegram API
def send_msg(msg):
    te_bot_api = "{TELEGRAM_BOT_API}"
    chat_id = "{chat_id}"
    base = "https://api.telegram.org/bot" + te_bot_api\
           + "/sendMessage?chat_id=" + chat_id\
           + "&text=" + msg + "&parse_mode=html"

    res = requests.get(base)
    return res.json()

