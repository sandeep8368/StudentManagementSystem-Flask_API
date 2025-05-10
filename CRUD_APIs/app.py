from flask import Flask, request, jsonify
from  database import db
from models import StudentModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    db.create_all()


#CREATE API
@app.route('/student', methods = ['POST'])
def create_student():
    data = request.get_json()
    student = StudentModel(name=data['name'], age=data['age'],email=data['email'])
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()),201


#READ ALL API
@app.route('/student/', methods=['GET'])
def get_students():
    students = StudentModel.query.all()
    return jsonify([s.to_dict() for s in students])



#READ ONE API   
@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = StudentModel.query.get(id)
    if student:
        return jsonify(student.to_dict())
    return jsonify({"error" : "student not found"}), 404



#Delete api
@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = StudentModel.query.get(id)
    if not student:
        return jsonify({"error": "student not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message":"student deleted"})



#Update API
@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    student = StudentModel.query.get(id)
    if not student:
        return jsonify({"error": "student not found"}), 404
    data = request.get_json()
    student.name = data['name']
    student.age = data['age']
    student.email = data['email']
    db.session.commit()
    return jsonify(student.to_dict())


app.run(debug=True)