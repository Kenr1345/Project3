from flask import Flask, render_template, request, url_for
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, DecimalField

app = Flask(__name__)

app.config["SECRET_KEY"]="cop4813"
app.config["MONGO_URI"]="mongodb+srv://cop4813:5770425@learningmongodb.1xbgs.mongodb.net/db?retryWrites=true&w=majority"

mongo = PyMongo(app)

class Expenses(FlaskForm):
    #stringfield for description
    #selectfield for category
    #decimalfield for cost
    #datefield for date
    string_input = StringField('Description')
    select_input = SelectField(
        choices=[('harddrives', 'Hard Drives'), ('gpus', 'GPUs'), ('cpus', 'CPUs'), ('monitors', 'Monitors'),
                 ('headsets', 'Headsets'), ('keyboards', 'Keyboards'), ('mice', 'Mice'), ('psus', 'PSUs')])
    decimal_input = DecimalField()
    date_input = DateField(format='%Y-%m-%d')


def get_total_expenses(category):
    #access the database adding the cost of all documents
    # of the category passed as input parameter
    #write the appropriate query to retrieve the cost
    total_category_expenses = 0
    query = {"category": category}
    for x in mongo.db.expenses.find(query):
        total_category_expenses += float(x['cost'])
    return total_category_expenses

@app.route('/')
def index():
    my_expenses = mongo.db.expenses.find()
    total_cost = 0
    for i in my_expenses:
        total_cost += float(i['cost'])
    expensesByCategory = [('Hard Drives', get_total_expenses("harddrives")), ('GPUs', get_total_expenses("gpus")),
                          ('CPUs', get_total_expenses("cpus")), ('Monitors', get_total_expenses("monitors")),
                          ('Headsets', get_total_expenses("headsets")), ('Keyboards', get_total_expenses("keyboards")),
                          ('Mice', get_total_expenses("mice")), ('PSUs', get_total_expenses("psus"))]
    return render_template("index.html",expenses=total_cost,expensesByCategory=expensesByCategory)

@app.route('/addExpenses',methods=["GET","POST"])
def addExpenses():
    expensesForm = Expenses(request.form) #include the form based on class expenses
    if request.method == "POST":
        #insert one document to the database
        #containing the data logged by the user
        #remeber that it should be a python dictionary
        stringinput = request.form['string_input']
        selectinput = request.form['select_input']
        decimalinput = request.form['decimal_input']
        dateinput = request.form['date_input']

        expenseEntry = {'description': stringinput,
                        'category': selectinput,
                        'cost': decimalinput,
                        'date': dateinput}
        mongo.db.expenses.insert_one(expenseEntry)

        return render_template("expenseAdded.html")
    return render_template("addExpenses.html", form=expensesForm)

app.run()

