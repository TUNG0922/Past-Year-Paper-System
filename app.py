from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from bson import ObjectId  # Import ObjectId for handling MongoDB IDs

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection string
client = MongoClient('mongodb+srv://tungjinyou:dumvn9MCrfFzGZLC@pastyearpapersystem.vf6cs.mongodb.net/?retryWrites=true&w=majority&appName=PastYearPaperSystem')

# Access the database
db = client['PastYearPaperSystem']  
users_collection = db['users']
papers_collection = db['papers']  # Create a separate collection for papers

# Set the upload folder for file storage
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the uploads directory if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({'message': 'All fields are required!'}), 400

    hashed_password = generate_password_hash(password)

    user = {
        'username': username,
        'password': hashed_password,
        'role': role
    }

    try:
        if users_collection.find_one({'username': username}):
            return jsonify({'message': 'Username already exists!'}), 409
        
        users_collection.insert_one(user)
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')  # Get role from request

    user = users_collection.find_one({'username': username})

    if user and check_password_hash(user['password'], password):
        if user['role'] == role:  # Check if the role matches
            return jsonify({'message': 'Login successful!', 'role': user['role']}), 200
        else:
            return jsonify({'message': 'Role does not match!'}), 403  # Forbidden if role doesn't match
    else:
        return jsonify({'message': 'Invalid username or password!'}), 401

@app.route('/api/papers', methods=['POST'])
def create_paper():
    title = request.form.get('title')  # Get the title from the form data
    type_ = request.form.get('type')    # Get the type from the form data

    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Secure the filename and save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)  # Save the file to the specified upload folder

    # Save paper info to MongoDB
    paper_id = papers_collection.insert_one({
        'title': title,
        'file_path': file_path,  # Save the file path
        'type': type_,
    }).inserted_id

    return jsonify({'message': 'Paper created successfully!', 'id': str(paper_id)}), 201

@app.route('/api/papers', methods=['GET'])
def get_papers():
    papers = list(papers_collection.find())  # Get all papers
    for paper in papers:
        paper['_id'] = str(paper['_id'])  # Convert ObjectId to string for easy use
    return jsonify(papers)

@app.route('/api/papers/<paper_id>', methods=['GET'])
def get_paper(paper_id):
    try:
        paper = papers_collection.find_one({'_id': ObjectId(paper_id)})
        if paper:
            # Return just the filename for constructing the URL
            filename = os.path.basename(paper['file_path'])  
            return jsonify({'file_path': filename}), 200
        return jsonify({'message': 'Paper not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/api/papers/<paper_id>', methods=['PUT'])
def update_paper(paper_id):
    try:
        paper = papers_collection.find_one({'_id': ObjectId(paper_id)})
        if not paper:
            return jsonify({'message': 'Paper not found'}), 404

        title = request.form.get('title')
        type_ = request.form.get('type')
        
        # Update fields if provided
        update_fields = {}
        if title:
            update_fields['title'] = title
        if type_:
            update_fields['type'] = type_

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # Secure the filename and save the file
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)  # Save the new file to the specified upload folder
                update_fields['file_path'] = file_path  # Update file path

        # Update the paper in MongoDB
        papers_collection.update_one({'_id': ObjectId(paper_id)}, {'$set': update_fields})

        return jsonify({'message': 'Paper updated successfully!'}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Serve files from the upload folder
@app.route('/uploads/<filename>', methods=['GET'])
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/papers/<paper_id>', methods=['DELETE'])
def delete_paper(paper_id):
    # Logic to delete the paper
    return jsonify({"message": "Paper deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
