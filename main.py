from db.models import User
from sqlalchemy.orm import Session
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from forms.users_form import UserForm
import os
from dotenv import load_dotenv
from db.session import init_db, get_db

# --------------------------------------------------------------- #
# ----------------------- LOAD PROPERTIES ----------------------- #
# --------------------------------------------------------------- #
load_dotenv(dotenv_path="./resources/application.properties")


# --------------------------------------------------------------- #
# -------------------- FLASK DECLARATION APP -------------------- #
# --------------------------------------------------------------- #
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ACCESS_KEY=os.getenv('access_key')
bootstrap = Bootstrap5(app)

init_db()

def update_payment(order_id, payed_import):
    db: Session = next(get_db())
    user_data = db.query(User).filter(User.id == order_id).first()
    user_data.topay = user_data.total - user_data.payd
    db.commit()

def update_total(order_id, box_number):
    db: Session = next(get_db())
    user_data = db.query(User).filter(User.id == order_id).first()
    if box_number < 10:
        box_cost = float(os.getenv('costo_box'))
    else:
        box_cost = float(os.getenv('costo_box_scontato'))
    total_cost = box_number * box_cost
    user_data.total = total_cost
    user_data.topay = user_data.total - user_data.payd
    db.commit()




# --------------------------------------------------------------- #
# ------------------------- CONTROLLERS ------------------------- #
# --------------------------------------------------------------- #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/deposit", methods=['GET', 'POST'])
def deposit():
    user_id = request.args.get("user_id", type=int)
    db: Session = next(get_db())
    user_data = db.query(User).filter(User.id == user_id).first()

    if request.method == "POST":
        user_id = request.form.get("user_id", type=int)
        db: Session = next(get_db())
        user_data = db.query(User).filter(User.id == user_id).first()
        deposit_payed = request.form.get("importo", type=float)

        if deposit_payed > user_data.total:
            flash("Importo non valido: supera il totale dovuto.", "danger")
            return redirect(url_for("pay", user_id=user_id))

        user_data.payd = deposit_payed
        db.commit()
        update_payment(user_id, user_data.payd)
        flash("Pagamento registrato correttamente.", "success")
        return redirect(url_for("deposit", user_id=user_id))

    return render_template("deposit.html", user_id=user_id, user_data=user_data)


''' Controller che gestisce il pagamento'''
@app.route("/pay", methods=['GET', 'POST'])
def pay():
    user_id = request.args.get("user_id", type=int)
    db: Session = next(get_db())
    user_data = db.query(User).filter(User.id == user_id).first()

    if request.method == "POST":
        user_id = request.form.get("user_id", type=int)
        user_data = db.query(User).filter(User.id == user_id).first()
        importo_pagato = request.form.get("importo", type=float)

        if user_data.payd + importo_pagato > user_data.total:
            flash("Importo non valido: supera il totale dovuto.", "danger")
            return redirect(url_for("pay", user_id=user_id))

        user_data.payd += importo_pagato
        user_data.topay = user_data.total - user_data.payd
        db.commit()
        flash("Pagamento registrato correttamente.", "success")
        return redirect(url_for("pay", user_id=user_id))

    return render_template("pay.html", user_id=user_id, user_data=user_data)


@app.route("/boxrecap", methods=['GET'])
def box_recap():
    if request.method == "GET":
        db: Session = next(get_db())
        users = db.query(User).all()

        return render_template("boxrecap.html", users=users)
    else:
        return "Method not allowed"

@app.route("/adduser", methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            anticipo = form.deposit.data
            if form.box_number.data < 10:
               totale = float(os.getenv('costo_box')) * form.box_number.data
            else:
                totale = float(os.getenv('costo_box_scontato')) * form.box_number.data
            da_pagare = totale - anticipo

            db: Session = next(get_db())
            new_user = User(
                name=form.name.data, box=form.box_number.data, payd=anticipo, topay=da_pagare,total=totale)
            db.add(new_user)
            db.commit()

            return redirect(url_for("add_user", success=1))

    success = request.args.get("success")
    return render_template("adduser.html", form=form, success=success)

@app.route("/delete", methods=['GET'])
def delete_user():
    user_id = request.args.get("user_id", type=int)
    db: Session = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        flash("Utente non trovato", "danger")
        return redirect(url_for("box_recap"))
    db.delete(user)
    db.commit()
    return redirect(url_for("box_recap"))

@app.route("/addbox", methods=['GET', 'POST'])
def add_box():
    user_id = request.args.get("user_id", type=int)
    db: Session = next(get_db())
    user_data = db.query(User).filter(User.id == user_id).first()

    if request.method == "POST":
         user_id = request.form.get("user_id", type=int)
         box_number = request.form.get("boxnr", type=int)
         user_data = db.query(User).filter(User.id == user_id).first()
         user_data.box += box_number
         db.commit()
         update_total(user_id, user_data.box)
         flash("Pagamento registrato correttamente.", "success")
         return redirect(url_for("add_box", user_id=user_id))

    return render_template("add_box.html", user_id=user_id, user_data=user_data)

# --------------------------------------------------------------- #
# ---------------------------MAIN-------------------------------- #
# --------------------------------------------------------------- #
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)