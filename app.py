from flask import Flask, Response, redirect
import sqlite3

app = Flask(__name__)

DB = "reaction.db"

# 改成你的 AO3 作品地址，不要加 #page1
RETURN_URL = "https://archiveofourown.org/works/90597281"

# 三个选项
# option1 / option2 / option3 是服务器内部使用的名字
# page1 / page2 / page3 是点击后跳转的页面
REACTIONS = {
    "option1": {
        "icon": "❤️",
        "page": "page1"
    },
    "option2": {
        "icon": "❤️",
        "page": "page2"
    },
    "option3": {
        "icon": "❤️",
        "page": "page3"
    }
}


def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reactions (
        reaction TEXT PRIMARY KEY,
        count INTEGER
    )
    """)

    for reaction in REACTIONS:
        cursor.execute("""
        INSERT OR IGNORE INTO reactions (reaction, count)
        VALUES (?, 0)
        """, (reaction,))

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "AO3 Reaction Server Running"


# 点击 reaction
@app.route("/vote/<reaction>")
def vote(reaction):

    if reaction not in REACTIONS:
        return "Unknown reaction", 404

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE reactions
    SET count = count + 1
    WHERE reaction = ?
    """, (reaction,))

    conn.commit()
    conn.close()

    page = REACTIONS[reaction]["page"]

    return redirect(RETURN_URL + "#" + page)


# 生成 SVG 图片
@app.route("/count/<reaction>.svg")
def count_svg(reaction):

    if reaction not in REACTIONS:
        return "Unknown reaction", 404

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT count
    FROM reactions
    WHERE reaction = ?
    """, (reaction,))

    result = cursor.fetchone()

    count = result[0] if result else 0

    conn.close()

    icon = REACTIONS[reaction]["icon"]

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="120"
         height="40">

        <rect width="120"
              height="40"
              rx="8"
              fill="#f5f5f5"/>

        <text x="15"
              y="27"
              font-family="Arial"
              font-size="18"
              fill="#8A6CCF">
            {icon} {count}
        </text>

    </svg>
    """

    return Response(
        svg,
        mimetype="image/svg+xml",
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
