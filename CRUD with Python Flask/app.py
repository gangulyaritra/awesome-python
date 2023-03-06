from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "123"

conn = sqlite3.connect("database.db")
conn.execute(
    "CREATE TABLE IF NOT EXISTS data(pid INTEGER PRIMARY KEY, name TEXT, address TEXT, contact INTEGER, email TEXT)"
)
conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_record")
def add_record():
    return render_template("add_record.html")


@app.route("/addData", methods=["POST", "GET"])
def addData():
    if request.method != "POST":
        return
    try:
        name = request.form["name"]
        address = request.form["address"]
        contact = request.form["contact"]
        email = request.form["email"]
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO data(name, address, contact, email) values(?,?,?,?)",
            (name, address, contact, email),
        )
        conn.commit()
        flash("Record Added Successfully", "Success")

    except Exception:
        flash("Error in Insert Operation", "Failed")

    finally:
        return redirect(url_for("home"))


@app.route("/view_record")
def view_record():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM data")
    data = cur.fetchall()
    conn.close()
    return render_template("view_record.html", data=data)


@app.route("/update_record/<string:id>", methods=["POST", "GET"])
def update_record(id):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM data where pid=?", (id))
    data = cur.fetchone()
    conn.close()

    if request.method == "POST":
        try:
            name = request.form["name"]
            address = request.form["address"]
            contact = request.form["contact"]
            email = request.form["email"]
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute(
                "UPDATE data SET name=?, address=?, contact=?, email=? where pid=?",
                (name, address, contact, email, id),
            )
            con.commit()
            flash("Update Successful", "Success")

        except Exception:
            flash("Error in Update Operation", "Failed")

        finally:
            return redirect(url_for("home"))
            con.close()

    return render_template("update_record.html", data=data)


@app.route("/delete_record/<string:id>")
def delete_record(id):
    try:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM data where pid=?", (id))
        con.commit()
        flash("Record Deleted Successfully", "Success")

    except Exception:
        flash("Error in Delete Operation", "Failed")

    finally:
        return redirect(url_for("home"))
        con.close()


if __name__ == "__main__":
    app.run(debug=True)
