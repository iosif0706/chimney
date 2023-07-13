from crypt import methods
import os
import json
import re
from click import password_option
import requests
import importlib
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from sqlalchemy import null
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import valid_email,login_required


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///chimney.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("layout.html")

@app.route("/contact",methods=["GET","POST"] )
@login_required
def contact():
    """ Take input and store in database"""
    if request.method == "POST":
        user_id = session.get("user_id")
        info = db.execute("SELECT * FROM user WHERE id =?",user_id)
        for x in info:
            email = x['email']
            nume = x['name']
        
        
        telefon = request.form.get("telefon")
        if not telefon:
            phone_err = 'insert a phone number'
            return render_template("contact.html",phone_error = phone_err)
        elif not telefon.isdigit():
            phone_err = 'must be numbers'
            return render_template("contact.html",phone_error = phone_err)
        elif (len(telefon) < 10):
            phone_err = 'insert a valid number'
            return render_template("contact.html",phone_error = phone_err)
        
        oras = request.form.get("oras")
        if not oras:
            city_err = 'insert a city'
            return render_template("contact.html",phone_error = city_err)
        
        
        mesaj = request.form.get("mesaj")
        if not mesaj:
            mesaj_err = 'Write a message'
            return render_template("contact.html",msg_error = mesaj_err)
        
        date = datetime.datetime.now()
        db.execute("INSERT INTO contact('email','nume',telefon,'oras','mesaj',persons_id,date) VALUES(?,?,?,?,?,?,?)",email,nume,telefon,oras,mesaj,user_id,date)
        
        flash("message sent succesfuly")
        return redirect("/")
    
    user_id = session.get("user_id")
    info = db.execute("SELECT * FROM detail WHERE id =? ",user_id)
    
    
    return render_template("contact.html",nume = info)
    
@app.route("/product")
def product():
    """Show the products"""
    return render_template("product.html")


@app.route("/login",methods=["GET","POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method =="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # Ensure username was submitted
        if not email:
            email_error = 'must provide email adress'
            return render_template('login.html',error = email_error)
    
        elif not password:
            password_error = 'must put a password'
            return render_template("login.html",pass_err = password_error)
        # Ensure username exists and password is correct
        check = db.execute("SELECT * FROM user WHERE email = ?",email)
        if len(check) != 1 or not check_password_hash(check[0]["hash"],password):
            error_message = 'invalid email or password'
            return render_template("login.html", msg = error_message)
        
        # Remember which user has logged in
        session["user_id"] = check[0]["id"]
      
       
        
        flash("wellcome back ")
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    
    # Redirect user to login form
    return redirect("/")


      
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method =="POST":
        #Ensure email is corect
        email = request.form.get("email")
        if not email:
            not_email = 'insert a mail adress'
            return render_template("signup.html",email = not_email)
        elif not valid_email(email):
            
            email_error = 'invalid email'
            return render_template("signup.html",email = email_error)
        check = db.execute("SELECT email FROM user")
        check_mail = []
        for x in check:
            check_mail.append(x['email'])    
        if email in check_mail:
            email_error = 'email alredy exist'
            return render_template("signup.html",email = email_error) 
        #Ensure password have 8 caracters long,a uper & lower letter and a number
        password = request.form.get("password")
        if (len(password) <=7):
            password_error = 'must have 8 caracter'
            return render_template("signup.html", error =password_error )
        elif not re.search("[a-z]",password):
            password_error = 'missing alphabetical letter'
            return render_template("signup.html", error =password_error )
        elif not re.search("[A-Z]",password):
            password_error = 'missing uper letter'
            return render_template("signup.html", error =password_error )
        elif not re.search("[0-9]",password):
            password_error = 'must have a number'
            return render_template("signup.html", error =password_error )
        #Ensure ist the same password
        confpass = request.form.get("cpass")
        if confpass != password:
            confpass_error = 'password not mach'
            return render_template("signup.html",confpass = confpass_error)
                   
        fname = request.form.get("fname")
        if not fname:
            fname_error = 'insert a valid name'
            return render_template("signup.html",fname_error = fname_error)
        
        lname = request.form.get("lname")
        if not fname:
            lname_error = 'insert a valid last name'
            return render_template("signup.html",lname_error = lname_error)
        
        adress = request.form.get("adress")
        if len(adress) <= 3:
            adress_error = 'must put a street'
            return render_template("signup.html",adress_error = adress_error)
        elif not re.search('[0-9]',adress):
            adress_error = 'must put a number street'
            return render_template("signup.html",adress_error = adress_error)
        
        
        postcode = request.form.get("postcode") 
        if len(postcode) <= 3:
            postcode_error = 'insert a postcode'
            return render_template("signup.html",postcode_error = postcode_error)
        elif not re.search("[0-9]",postcode):
            postcode_error = 'inseart a valid adress'
            return render_template("signup.html",postcode_error=postcode_error)
        
        birthday = request.form.get("birthday")  
        if not birthday :
            bth_error = 'put a date'
            return render_template("signup.html",birthday_error=bth_error)
        
        elif not re.search("[0-9]",birthday):
            brithday_error = 'invalide date'
            return render_template("signup.html",birthday_error=brithday_error)
        
        user_id = session.get("user_id")
        hash = generate_password_hash(password)
        #Insert in database all user input
        lname = lname.capitalize()
        fname = fname.capitalize()
        db.execute("INSERT INTO user('name','email',hash) VALUES (?,?,?)",fname,email,hash)
        db.execute("INSERT INTO detail('nume','prenume','adresa',zip,birthday) VALUES (?,?,?,?,?)",fname,lname,adress,postcode,birthday)
        
        flash('you are registred')
        return redirect ("/login")
    
    
    else:
        return render_template("/signup.html")
@app.route("/aboutus",methods=["GET"])
def aboutus():
    return render_template("/aboutus.html")

@app.route("/news",methods=["GET"])
def news():
    return render_template("/news.html")

@app.route("/mesaje")
@login_required
def mesaje():
    #Show all massages from all user to admin
    check = db.execute("SELECT * FROM contact ORDER BY date DESC  LIMIT 20")
    return render_template("/mesaje.html",check = check)

@app.route("/profil")
@login_required
def profil():
    #Show messages to user
    user_id = session.get("user_id")
    profil = db.execute("SELECT * FROM detail WHERE id = ? ",user_id)
    mesaj = db.execute("SELECT * FROM contact WHERE  persons_id = ? ORDER BY date DESC LIMIT 5",user_id)
    
    
    return render_template("profil.html",profil=profil,mesaj=mesaj)



@app.route("/changepass",methods=["POST"])
@login_required
def change_pass():
        #Change password
        user_id = session.get("user_id")
        profil = db.execute("SELECT * FROM user WHERE id = ? ",user_id)
        
        
        change_pass = request.form.get("curent_pass")
        if not check_password_hash(profil[0]["hash"],change_pass):
            invalid_pass='Invalid Password'
            return render_template("profil.html",error = invalid_pass)
        
        
        confirm_pass= request.form.get("confirm_pass") 
        if (len(confirm_pass) <=7):
            password_error = 'must have 8 caracter'
            return render_template("profil.html", error =password_error )
        elif not re.search("[a-z]",confirm_pass):
            password_error = 'missing alphabetical letter'
            return render_template("profil.html", error =password_error )
        elif not re.search("[A-Z]",confirm_pass):
            password_error = 'missing uper letter'
            return render_template("profil.html", error =password_error )
        elif not re.search("[0-9]",confirm_pass):
            password_error = 'must have a number'
            return render_template("profil.html", error =password_error )
        
        
        reconfirm_pass=request.form.get("reconfirm_pass")
        if confirm_pass != reconfirm_pass:
            password_error = 'password not mach'
            return render_template("profil.html",error=password_error)
        
        
        hash = generate_password_hash(confirm_pass)
        db.execute("UPDATE user SET hash = ? WHERE id =?",hash,user_id)
        
        flash('password changed succesfuly')
        return redirect("/")
    
    
@app.route("/changename",methods=["POST"])
@login_required
def change_name():
        #Change name
        user_id = session.get("user_id")
        
        
        first_name = request.form.get("first_name")
        first_name=first_name.capitalize()
        if not change_name:
            invalid_name='must put a name'
            return render_template("profil.html",error = invalid_name)
        
        
        last_name = request.form.get("last_name")
        last_name= last_name.capitalize()
        if not last_name:
            invalid_name ='must put a name'
            return render_template("profil.html",error = invalid_name)
        
        db.execute("UPDATE detail SET nume = ?,prenume = ? WHERE id =?",first_name,last_name,user_id)
        
        flash('name changed succesfuly')
        return redirect("/")
    
    



    