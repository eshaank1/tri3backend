# Import necessary modules from Flask and other libraries
from flask import Blueprint, request, jsonify  
from flask_restful import Api, Resource 
from flask_cors import CORS
from model.chat import ChatMessage  # Import the ChatMessage model
from __init__ import app, db
import requests 

# Create a Blueprint for the chat API with a URL prefix
chat_api = Blueprint('chat_api', __name__, url_prefix='/api/chat')
# Create an instance of Flask-RESTful API
api = Api(chat_api)
# Enable CORS for the chat API
CORS(chat_api)  
# Define API endpoints using Resource classes
class ChatAPI:
    # Endpoint for testing the connection
    class _Test(Resource):
        def get(self):
            response = jsonify({"Connection Test": "Successfully connected to backend!"})
            return response
        
    # Endpoint for creating a chat message
    class _Create(Resource):
        def get(self):
            var = jsonify({"message": "This is the GET request for _Create"})
            return var
        def post(self):
            data = request.json
            message = data.get('message')
            if message:
                chat_message = ChatMessage(message=message)
                db.session.add(chat_message)
                db.session.commit()
                return jsonify({"message": "Data stored successfully!"})
            else:
                return jsonify({"error": "Message is missing"}), 400

    # Endpoint for reading all chat messages
    class _Read(Resource):
        def get(self):
            chat_messages = ChatMessage.query.all()
            messages_json = [msg.serialize() for msg in chat_messages]
            var = jsonify(messages_json)
            return var

    # Endpoint for editing a chat message
    class _Edit(Resource):
        def put(self):
            data = request.json
            message_id = data.get('message_id')
            new_message = data.get('message')
            if not message_id or not new_message:
                return jsonify({"error": "Missing message ID or new message content"}), 400

            message = ChatMessage.query.get(message_id)
            if message:
                message.message = new_message
                db.session.commit()
                return jsonify({"message": "Message updated successfully!"})
            else:
                return jsonify({"error": "Message not found"}), 404

# Add endpoints to the API
api.add_resource(ChatAPI._Create, '/create')
api.add_resource(ChatAPI._Read, '/read')
api.add_resource(ChatAPI._Edit, '/edit')
api.add_resource(ChatAPI._Test, '/test')

# Run the Flask app
if __name__ == "__main__":
    from app import create_app
    app = create_app()
    app.register_blueprint(chat_api)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
