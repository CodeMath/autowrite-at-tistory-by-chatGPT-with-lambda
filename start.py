from main import *

confirm_tokens = '{TISTORY_API_KEY}'
for name in blogList:
    print(">> JOB ", name["id"], name["category"], " <<")
    suggest_keywords = targeting()
    time.sleep(1)
    job = Job(blogname=name["id"], keywords=suggest_keywords)
    while True:
        job.generate_writing_style()
        job.generate_article()
        papago = translator(job.en_manuscript)
        if papago == "Error 5000":
            print("Retry...letter 5000")
            time.sleep(2)
        else:
            file_name = get_blogImage(job.en_manuscript)
            break

    exist_token = confirm_tokens
    confirm_tokens = upload_article_at_blog(
        name["id"],
        name["category"],
        papago,
        file_name,
        exist_token
    )
    print(">> Finish ", name["id"], name["category"], " <<")
    time.sleep(1.5)

print("JOB FINISH")