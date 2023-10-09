from flask import Flask, request
from flask_liquid import Liquid
from flask_liquid import render_template
import threading
import main


app = Flask(__name__)
liquid = Liquid(app)
app.config.update(LIQUID_TEMPLATE_FOLDER="./templates")

base_path = "./templates/"


@app.route("/")
def hello_world():
    return render_template("main.liquid")


@app.route("/getData/<TID>")
def get_thread_info(TID=None):
    if main.threads[int(TID)][1] == "Done":
        main.threads[int(TID)][0].join()
    return render_template("thread.liquid",
                           TID=TID,
                           TSTAT=main.threads[int(TID)][1])


@app.route("/getData")
def get_data():
    import os

    os.system("rm output.db")
    TID = len(main.threads)
    main.threads.append(
        [threading.Thread(target=main.project_2_main,
                          args=[TID]), ""]
        )
    main.threads[-1][0].start()
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


@app.route("/view")
def view_data():
    lSalary = request.args.get('lSalary', '')
    hSalary = request.args.get('hSalary', '100000000')
    isRemote = request.args.get('isRemote')
    sort_by = request.args.get('sort_by')
    # Generate our SQL arguments:
    arg_list = []
    if lSalary != '':
        arg_list.append(f'salary_low > {lSalary}')
    if hSalary != '':
        arg_list.append(f'salary_high < {hSalary}')
    if isRemote == 'true':
        arg_list.append('location NOT LIKE \'%remote%\'')
    args = ' AND '.join(arg_list)

    if sort_by != '':
        match sort_by:
            case 'none':
                pass
            case 'post_name':
                args += ' ORDER BY a.title'
            case 'company_name':
                args += ' ORDER BY b.company'
            case 'location':
                args += ' ORDER BY b.location'
            case 'lsalary':
                args += ' ORDER BY salary_low DESC'
            case 'hsalary':
                args += ' ORDER BY salary_high DESC'

    print(args)
    articles = main.get_from_db(args)
    return render_template("view.liquid", data=articles)


if __name__ == "__main__":
    app.run(debug=True)
