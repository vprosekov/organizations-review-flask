from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///organizations-review-flask.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

# CREATE TABLE `organizations` (
#   `id` INTEGER NOT NULL AUTO_INCREMENT,
#   `name` INTEGER(100) NOT NULL,
#   `email` VARCHAR(120) NOT NULL,
#   `cachedpassword` VARCHAR(100) NOT NULL,
#   `org_type` INTEGER NOT NULL,
#   `photo` MEDIUMTEXT NOT NULL,
#   `description` MEDIUMTEXT NULL DEFAULT NULL,
#   PRIMARY KEY (`id`)
# );
class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    cachedpassword = db.Column(db.String(100), nullable=False)
    org_type = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Organization %r>' % self.name

# CREATE TABLE `feedbacks` (
#   `id` INTEGER NOT NULL AUTO_INCREMENT,
#   `organization_id` INTEGER NOT NULL,
#   `info_avaliability` INTEGER NOT NULL,
#   `comfort` INTEGER NOT NULL,
#   `queue_time` INTEGER NOT NULL,
#   `service_time` INTEGER NOT NULL,
#   `workers_politeness` INTEGER NOT NULL,
#   `notes_text` MEDIUMTEXT NOT NULL,
#   PRIMARY KEY (`id`)
# );
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, nullable=False)
    info_avaliability = db.Column(db.Integer, nullable=False)
    comfort = db.Column(db.Integer, nullable=False)
    queue_time = db.Column(db.Integer, nullable=False)
    service_time = db.Column(db.Integer, nullable=False)
    workers_politeness = db.Column(db.Integer, nullable=False)
    notes_text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Feedback %r>' % self.id


# CREATE TABLE `org_types` (
#   `org_type_id` INTEGER NOT NULL AUTO_INCREMENT,
#   `org_type_name` VARCHAR(100) NOT NULL,
#   PRIMARY KEY (`org_type_id`)
# );
class OrgType(db.Model):
    org_type_id = db.Column(db.Integer, primary_key=True)
    org_type_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<OrgType %r>' % self.org_type_name

# CREATE TABLE `service_types` (
#   `service_type_id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
#   `service_type_name` VARCHAR(100) NOT NULL,
#   PRIMARY KEY (`service_type_id`)
# );
class ServiceType(db.Model):
    service_type_id = db.Column(db.Integer, primary_key=True)
    service_type_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<ServiceType %r>' % self.service_type_name

# CREATE TABLE `org_services_list` (
#   `orgId` INTEGER NOT NULL,
#   `serviceId` INTEGER NOT NULL,
#   PRIMARY KEY (`orgId`)
# );
class OrgServicesList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orgId = db.Column(db.Integer, primary_key=False)
    serviceId = db.Column(db.Integer, primary_key=False)

    def __repr__(self):
        return '<OrgServicesList %r>' % self.orgId

# CREATE TABLE `feedback_files_list` (
#   `feedbackId` INTEGER NOT NULL,
#   `fileUrl` MEDIUMTEXT NOT NULL,
#   PRIMARY KEY (`feedbackId`)
# );
class FeedbackFilesList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedbackId = db.Column(db.Integer, primary_key=False)
    fileUrl = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<FeedbackFilesList %r>' % self.feedbackId


# ! delete
class Article(db.Model):
    articleId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Article %r>" % self.articleId

@app.route('/makefeedback')
def makefeedback():
    return redirect('/')

@app.route('/makefeedback/<int:orgId>')
def makefeedbackOrg(orgId):
    return render_template('makefeedback.html', orgId=orgId, orgTitle="Шаурма “У Ахмеда”", orgDescription = "Шаурма “У Ахмеда” в г. Киев, ул. Ахмеда, д. 1, офис 1", orgPhoto = "https://www.yarosonline.ru/wp-content/uploads/2019/08/blobid1564592210029.jpg") 

@app.route('/sendfeedback', methods=['POST'])
def sendfeedback():
    return json.dumps(request.form)
    

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date).all()
    return render_template('posts.html', articles=articles)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page: {} {}".format(name, id)
    
# make route create-article
@app.route('/create-article', methods=['GET', 'POST'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)  

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except: 
            return "There was an issue adding your article"

    else:
        return render_template('create-article.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True, threaded=True)