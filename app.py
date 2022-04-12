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
    serviceId = db.Column(db.Integer, nullable=False)
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

orgTypes = [
    {'org_type_id': 1, 'org_type_name': 'Частная организация'},
    {'org_type_id': 2, 'org_type_name': 'Государственная организация'},
    {'org_type_id': 3, 'org_type_name': 'Муниципальная организация'},
    {'org_type_id': 4, 'org_type_name': 'Общественная организация'}
];
serviceTypes = [
    {'service_type_id': 0, 'service_type_name': 'Общественное питание'},
    {'service_type_id': 1, 'service_type_name': 'Жилищно-коммунальные услуги'},
    {'service_type_id': 2, 'service_type_name': 'Строительные услуги'},
    {'service_type_id': 3, 'service_type_name': 'Техническая поддержка'},
    {'service_type_id': 4, 'service_type_name': 'Электроснабжение'},
    {'service_type_id': 5, 'service_type_name': 'Газоснабжение'},
    {'service_type_id': 6, 'service_type_name': 'Теплоснабжение'},
    {'service_type_id': 7, 'service_type_name': 'Водоснабжение и канализация'},
    {'service_type_id': 8, 'service_type_name': 'Транспортные услуги'},
    {'service_type_id': 9, 'service_type_name': 'Услуги связи и телекоммуникации'},
    {'service_type_id': 10, 'service_type_name': 'Торговые услуги'},
    {'service_type_id': 11, 'service_type_name': 'Услуги общественного питания'},
    {'service_type_id': 12, 'service_type_name': 'Бытовые услуги'},
    {'service_type_id': 13, 'service_type_name': 'Услуги аренды'},
    {'service_type_id': 14, 'service_type_name': 'Медицинские услуги'},
    {'service_type_id': 15, 'service_type_name': 'Образовательные услуги'},
    {'service_type_id': 16, 'service_type_name': 'Юридические услуги'},
    {'service_type_id': 17, 'service_type_name': 'Услуги переводчиков'},
    {'service_type_id': 18, 'service_type_name': 'Услуги по обслуживанию и поддержке предприятий'},
    {'service_type_id': 19, 'service_type_name': 'Финансовые услуги'},
    {'service_type_id': 20, 'service_type_name': 'Охранные услуги'},
    {'service_type_id': 21, 'service_type_name': 'Туристские услуги'},
    {'service_type_id': 22, 'service_type_name': 'Развлечения'},
];

# function to get all serviceTypes by orgId
def getServiceTypesByOrgId(orgId):
    ids = []
    sids = db.session.query(OrgServicesList).filter(OrgServicesList.orgId == orgId).all()
    for serviceType in sids:
        ids.append(serviceType.serviceId)
        # print(serviceType.serviceId)
    names = []
    for i in ids:
        for j in serviceTypes:
            if i == j['service_type_id']:
                names.append(j['service_type_name'])
    # return ids and names lists
    return ids, names


# function to get info by orgId
def getOrgInfoByOrgId(orgId):
    return db.session.query(Organization).filter(Organization.id == orgId).first()

# function to get all Feedbacks
def getFeedbacks():
    return db.session.query(Feedback).all()

# function to gel all Feedbacks by orgId
def getFeedbacksByOrgId(orgId):
    return db.session.query(Feedback).filter(Feedback.organization_id == orgId).all()

# function to get number of feedbacks of every serviceTypeId by orgId
def getServiceFeedbacksByOrgId(orgId):
    ids = []
    sids = db.session.query(OrgServicesList).filter(OrgServicesList.orgId == orgId).all()
    for serviceType in sids:
        ids.append(serviceType.serviceId)
        # print(serviceType.serviceId)
    names = []
    for i in ids:
        for j in serviceTypes:
            if i == j['service_type_id']:
                names.append(j['service_type_name'])
    # return ids and names lists
    fbs = getFeedbacksByOrgId(orgId)
    fbs_by_service = {}
    for i in ids:
        print("i = ", i)
        for j in fbs:
            print("j = ", j.serviceId)
            if i == j.serviceId:
                if i in fbs_by_service:
                    fbs_by_service[i]["count"] += 1
                    
                    avrg = 0;
                    avrg += j.info_avaliability
                    avrg += j.comfort
                    avrg += j.queue_time
                    avrg += j.service_time
                    avrg += j.workers_politeness
                    avrg /= 5
                    fbs_by_service[i]["average"] = (fbs_by_service[i]["average"] + avrg) / fbs_by_service[i]["count"]

                else:
                    fbs_by_service[i]={"count":1, "average":0}

                    avrg = 0;
                    avrg += j.info_avaliability
                    avrg += j.comfort
                    avrg += j.queue_time
                    avrg += j.service_time
                    avrg += j.workers_politeness
                    avrg /= 5
                    fbs_by_service[i]["average"] = avrg
    print(fbs_by_service)
    return fbs_by_service

# function to get number of scores by orgId
def getScoresByOrgId(orgId):
    fbs = getFeedbacksByOrgId(orgId)
    scores = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
    for i in fbs:

        scores[i.info_avaliability] += 1
        scores[i.comfort] += 1
        scores[i.queue_time] += 1
        scores[i.service_time] += 1
        scores[i.workers_politeness] += 1

    return scores

# function to get average scores by months
def getMonthAverageScoresByOrgId(orgId):
    fbs = db.session.query(Feedback).filter(Feedback.organization_id == orgId).all()
    months_score = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
    months_count = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
    for i in fbs:
        months_count[int(i.date_created.month)] += 1
        months_score[int(i.date_created.month)] += i.info_avaliability
        months_score[int(i.date_created.month)] += i.comfort
        months_score[int(i.date_created.month)] += i.queue_time
        months_score[int(i.date_created.month)] += i.service_time
        months_score[int(i.date_created.month)]+= i.workers_politeness
        months_score[int(i.date_created.month)] /= 5
    for i in months_score:
        if months_count[i] != 0:
            months_score[i] /= months_count[i]

    

    return months_score

# function to get all notes_text by orgId
def getNotesTextByOrgId(orgId):
    fbs = db.session.query(Feedback).filter(Feedback.organization_id == orgId).all()
    ret = []
    for i in fbs:
        ret.append(i.notes_text)
    return ret


@app.route('/makefeedback')
def makefeedback():
    return redirect('/')

@app.route('/makefeedback/<int:orgId>')
def makefeedbackOrg(orgId):
    # if Organization with orgId exists
    organ = db.session.query(Organization).filter(Organization.id == orgId).first()
    if organ:
        servicetps = []
        serIds, serNames = getServiceTypesByOrgId(orgId)
        for i in range(len(serIds)):
            servicetps.append({'service_type_id': serIds[i], 'service_type_name': serNames[i]})
            # print(servicetps)
            
        return render_template('makefeedback.html', orgId=organ.id, 
            orgTitle= organ.name, 
            orgDescription=  organ.description, 
            orgPhoto= organ.photo,
            serviceTypes= servicetps)
    else:
        # return error bad request
        return "400"


@app.route('/lk/<int:orgId>')
def lk(orgId):
    organ = db.session.query(Organization).filter(Organization.id == orgId).first()
    if organ:
        servicetps = []
        serIds, serNames = getServiceTypesByOrgId(orgId)
        for i in range(len(serIds)):
            servicetps.append({'service_type_id': serIds[i], 'service_type_name': serNames[i]})
            # print(servicetps)
            orgType = ""
            for j in orgTypes:
                if organ.org_type == j['org_type_id']:
                    orgType = j['org_type_name']
            
        return render_template('lk.html', org = organ,
            serviceTypes= servicetps, orgType = orgType, numberOfFeedbacks = len(getFeedbacksByOrgId(orgId)),
            serviceFeedbacks = json.dumps(getServiceFeedbacksByOrgId(orgId)),
            scoresTotal = json.dumps(getScoresByOrgId(orgId)),
            months_score= getMonthAverageScoresByOrgId(orgId),
            notes = getNotesTextByOrgId(orgId))
    else:
        # return error bad request
        return "400"

@app.route('/sendfeedback', methods=['POST'])
def sendfeedback():
    return json.dumps(request.form)
    fb = Feedback()
    fb.organization_id = int(request.form['orgId'])
    fb.serviceId = int(request.form['serviceId'])
    fb.info_avaliability = int(request.form['avaliability'])
    fb.comfort = int(request.form['comfort'])
    fb.queue_time = int(request.form['queue_time'])
    fb.service_time = int(request.form['service_time'])
    fb.workers_politeness = int(request.form['workers_politeness'])
    fb.notes_text = request.form['notes_text']

    db.session.add(fb)
    db.session.commit()

    return redirect('https://google.com')
    
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        org = Organization()
        org.name = request.form['orgName']
        org.email = request.form['orgEmail']
        org.cachedpassword = request.form['orgPassword']
        org.org_type = request.form['orgType']
        org.photo = request.form['orgPhoto']
        org.description = request.form['orgDescription']

        db.session.add(org)
        db.session.commit()

        orgId = Organization.query.filter_by(email=request.form['orgEmail']).first().id
        gotServiceTypes = request.form.getlist('serviceTypes')
        for ser_type in gotServiceTypes:
            orgServices = OrgServicesList()
            orgServices.orgId = int(orgId)
            orgServices.serviceId = int(ser_type)
            # print("{} {}".format(orgServices.orgId, orgServices.serviceId))
            db.session.add(orgServices)
        db.session.commit()


        return redirect('/')
    else:
        return render_template('register.html', orgTypes=orgTypes, serviceTypes=serviceTypes)

@app.route('/test')
def test():
    print(getServiceTypesByOrgId(2))
    # display all organizations
    data = Organization.query.all()
    data2 = OrgServicesList.query.all()
    return render_template('test.html', data=data, data2=data2, data3 = getFeedbacksByOrgId(orgId=1), data4 = getServiceFeedbacksByOrgId(1), data5=getScoresByOrgId(1), data6= getMonthAverageScoresByOrgId(1), data7 = getNotesTextByOrgId(1))
    

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