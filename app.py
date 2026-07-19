from flask import Flask, Response, redirect
import sqlite3

app = Flask(__name__)

DB = "reaction.db"

# 你的 AO3 作品地址
RETURN_URL = "https://archiveofourown.org/works/88826811"


def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reactions (
        id INTEGER PRIMARY KEY,
        count INTEGER
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO reactions (id, count)
    VALUES (1, 0)
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "AO3 Reaction Server Running"


# 点击 reaction
@app.route("/vote")
def vote():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE reactions
    SET count = count + 1
    WHERE id = 1
    """)

    conn.commit()
    conn.close()

    return redirect(RETURN_URL)


# 生成图片
@app.route("/count.svg")
def count_svg():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT count FROM reactions WHERE id=1
    """)

    count = cursor.fetchone()[0]

    conn.close()


    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="120"
         height="40">

        <rect width="120"
              height="40"
              rx="8"
              fill="#f5f5f5"/>

        <text x="15"
              y="26"
              font-size="18"
              fill="#8A6CCF">
            ❤️ {count}
        </text>

    </svg>
    """

    return Response(svg, mimetype="image/svg+xml")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)