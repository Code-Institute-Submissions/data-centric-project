import os
import pymysql
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

username = os.getenv("C9_USER")

"""
Function to select data from mysql.  
Pass in sql as string and will result the data as a list
"""
def select_data(sql):
    connection = pymysql.connect(host = "localhost",
                            user = username,
                            password = "",
                            db = "recipes")
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

@app.route('/')
def index():
    # prep data for page
    recieps_sql="select course.name as course_name , recipes.ID as recipes_ID, recipes.name as recipes_name from recipes JOIN course on recipes.ID = course.recipes_ID;"
    recipes_data = select_data(recieps_sql)
    
    course_sql ="select count(ID), name as course_name from course group by course_name;"
    course_data = select_data(course_sql)
    
    return render_template("index.html",
                            page_title="Welcome to you're cooking recieps",
                            course_data = course_data,
                            recipes_data = recipes_data)

@app.route("/recieps/<recipe_ID>/")
def recipes(recipe_ID):
    # prep data for page
    recipes_sql = ("SELECT * from recipes where ID =" + recipe_ID)
    recipes_data = select_data(recipes_sql)
    
    directions_sql = ("SELECT * from directions where recipes_ID =" + recipe_ID)
    directions_data = select_data(directions_sql)
    
    ingredients_sql = ("SELECT * from ingredients where recipes_ID =" + recipe_ID)
    ingredients_data = select_data(ingredients_sql)
    
    cuisine_sql = ("SELECT * from cuisine where recipes_ID =" + recipe_ID)
    cuisine_data = select_data(cuisine_sql)
    
    course_sql = ("SELECT * from course where recipes_ID =" + recipe_ID)
    course_data = select_data(course_sql)
    
    allergens_sql = ("SELECT * from allergens where recipes_ID =" + recipe_ID)
    allergens_data = select_data(allergens_sql)
    
    return render_template("recieps.html",
                            page_title="Edit Recipe",
                            recipes_data = recipes_data,
                            directions_data = directions_data,
                            ingredients_data = ingredients_data,
                            cuisine_data = cuisine_data,
                            course_data = course_data,
                            allergens_data = allergens_data)
    
@app.route("/directions/<recipe_ID>/<direction_ID>/")
def directions(recipe_ID, direction_ID):
    # prep data for page
    directions_sql = "SELECT recipes.ID AS recipe_ID, recipes.name AS recipe_name, directions.ID AS direction_ID, directions.name AS direction_name FROM recipes JOIN directions ON recipes.ID = directions.recipes_ID WHERE recipes.ID = " + recipe_ID + " AND directions.ID = " + direction_ID +";"
    directions_data = select_data(directions_sql)
    
    return render_template("directions.html", 
                            page_title="Directions",
                            directions_data = directions_data)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)