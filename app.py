from flask import Flask, request
from flask_liquid import Liquid
from flask_liquid import render_template
import threading
import main
from datetime import datetime


app = Flask(__name__)
liquid = Liquid(app)
app.config.update(LIQUID_TEMPLATE_FOLDER="./templates")

base_path = "./templates/"


@app.route("/")
def hello_world():
    return render_template("main.liquid")


@app.route("/getData/<TID>")
def get_thread_info(TID=None):
    if main.thread_strs[int(TID)] == "Done":
        main.threads[int(TID)].join()
    return render_template("thread.liquid",
                           TID=TID,
                           TSTAT=main.thread_strs[int(TID)])


@app.route("/getData")
def get_data():
    import os
    try:
        os.system("rm output.db")
    except FileNotFoundError:
        pass
    TID = len(main.threads)
    main.threads.append(
        threading.Thread(target=main.project_2_main,
                         args=[TID])
        )
    main.thread_strs.append("")
    main.threads[-1].start()
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="refresh" content="5; url=/getData/{
        len(main.threads) - 1
        }">
    <title>Thread Started, Redirecting...</title>
    </head>
    <body>
    <h1>Thread Started, Redirecting...</h1>
    <h2>Thread ID: {len(main.threads) - 1}</h2>
    </body>
    </html>
    """


@app.route("/expand/<CID>")
def view_one(CID=None):
    query = f"SELECT * FROM comments where ID = {CID}"
    results = main.get_from_db("output.db", query)[0]
    return render_template("expand.liquid", id=CID, data=results)


@app.route("/view")
def view_all():
    salary_low = request.args.get("lSalary", '')
    salary_high = request.args.get("hSalary", '')
    show_remote = request.args.get("isRemote") != "true"
    post_after = request.args.get("post_by", '')
    keywords = request.args.get("keywords", '')
    post_before = request.args.get("post_before", '')
    query = "SELECT company, location, created_at, id FROM comments"
    args = []
    if salary_low != "":
        args.append(f" salary_low > {salary_low} ")
    if salary_high != "":
        args.append(f" salary_high < {salary_high} ")
    if not show_remote:
        args.append(" location not like '%remote%' ")
    if post_after != "":
        args.append(f" created_at > {post_after} ")
    if post_before != "":
        args.append(f" created_at < {post_before} ")
    if keywords != "":
        for keyword in keywords.split(","):
            args.append(f" raw_comment like '%{keyword}%' ")
    if len(args) != 0:
        query += ' where ' + 'and'.join(args)
    print(query)
    results = main.get_from_db("output.db", query)

    updated_results = [[row[0],
                        row[1],
                        get_year_fmt(int(row[2])),
                        row[3]]
                       for row in results]
    return render_template("view_all.liquid", data=updated_results)


def get_year_fmt(timestamp: int):
    dt_obj = datetime.fromtimestamp(timestamp)
    date = f"{dt_obj.month}/{dt_obj.day}/{dt_obj.year}"
    return date


if __name__ == "__main__":
    app.run(debug=True)
