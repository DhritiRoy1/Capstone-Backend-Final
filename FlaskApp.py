import imp, os
from flask import Flask,request,jsonify
from flask_restful import Api,Resource, marshal_with_field,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Nullable
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
data = None
goals = None
page_title = None
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
api = Api(app)
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("Url",type=str,help="You need to enter the video name")
video_put_args.add_argument("Time",type=float,help="You need to enter the number of likes")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'database.db')
db = SQLAlchemy(app)
resource_fields = {
    'id' : fields.Integer,
    'Url' : fields.String,
    'Time': fields.Float
}

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Url = db.Column(db.String(100),nullable=False)
    Time = db.Column(db.Float,nullable=False)
with app.app_context():
        db.create_all()
Videos = {}
def abort_program(id):
    if id not in Videos:
        abort(404,message="Video not found")
def abort_if_video_exists(id):
    if id in Videos:
        abort(409,message="Video already exists")
class Video(Resource):
    @marshal_with(resource_fields)
    def get(self,id):
        result = VideoModel.query.get(id)
        return result
    def put(self,id):
        args = video_put_args.parse_args()
        video = VideoModel(id =id,url=args['Url'],Time=args['Time'])
        db.session.add(video)
        db.session.commit()
    def delete(self,id):
        abort_program(id)
        del Videos[id]
        return "", 204
api.add_resource(Video,'/<int:id>')
@app.route("/page-title",methods=["POST"])
def get_page_title():
    global page_title
    page_title = request.get_json(silent=True)
    print(page_title)
    return jsonify({"status": "success"}), 200
@app.route("/",methods=["POST"])
def get_goal():
    global goals
    goals = request.get_json(silent=True)
    return jsonify({"status": "success", "received": goals}), 200
@app.route("/page-title",methods=["GET"])
def show_page_title():
    return jsonify(page_title),200


@app.route("/", methods = ["GET"])
def show_goal():
    #print(calculate_scores_for_titles(goals,data))
    return jsonify(calculate_scores_for_titles(goals,data),goals),400
@app.route("/api/recieve", methods=["POST"])
def recieve():
    global data
    data = request.get_json(silent=True)

    return jsonify({"status": "success", "received": data}), 200

@app.route("/api/recieve", methods=["GET"])
def get_status():
    return jsonify(data), 400

@app.route("/api/recieve/productivity-scores", methods=["GET"])
def send_scores():
    new_dictionary = {}
    count = 0
    for i in data.keys():
        new_dictionary[i] = calculate_scores_for_titles(goals,data)[count]
        count+=1
    return jsonify(new_dictionary),200
def calculate_scores_for_titles(goals_array, titles_array):
    """
    Calculates the Cosine Similarity score for a list of page titles 
    against a combined user goal.
    
    Args:
        goals_array (list): List of user's goals (e.g., ["study python", "apply for jobs"]).
        titles_array (list): List of page titles to score (e.g., ["Python Tutorial 1", "Funny Cat Video"]).
        
    Returns:
        list: An array of similarity scores (floats) corresponding to the input titles.
    """
    if not goals_array or not titles_array:
        if not goals_array:
            return "none"
        else:
            return "titles_array"

    # 1. Create the 'super-goal' document
    #print(goals_array["goals_array"])
    user_goal_document = " ".join(goals_array["goals_array"])
    #print(user_goal_document)
    # 2. Define the Corpus
    # The corpus must contain the goal document PLUS all the titles to be compared.
    # [Goal, Title1, Title2, Title3, ...]
    corpus = [user_goal_document] + list(titles_array.keys())
    #print(corpus)

    
    # 3. Vectorize the Corpus
    # The vectorizer fits on ALL text, determining word importance across the entire set.
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    #print(tfidf_matrix)
    
    # 4. Calculate Cosine Similarity
    # We compare the Goal vector (index 0) against ALL other vectors (index 1 onwards).
    # Since the matrix includes the goal itself, we take the entire first row.
    cosine_score_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)    
    #print(cosine_score_matrix)
    # 5. Extract and Return Scores
    # The result is the first row of the matrix. We discard index [0][0] (Goal vs. Goal) 
    # and return the rest, which are the scores for Title1, Title2, etc.
    
    # [0] selects the first row of the matrix (the row showing scores against the Goal)
    # [1:] selects all scores starting from the second element (Title 1's score).
    similarity_scores = cosine_score_matrix[0][1:].tolist() 
    productivity_list = []
    for i in similarity_scores:
        if i>0.1:
            productivity_list.append("productive");
        else:
            productivity_list.append("unproductive");

    
    return productivity_list


    # Do something with `data` here
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)