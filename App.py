# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrapeinfo

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    marsdata = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", marsdata = marsdata)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

   marsdata = scrapeinfo.scrape()

   mongo.db.marsdata.update({},marsdata,upsert=True)
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
