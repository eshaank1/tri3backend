from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from model.chat import ChatMessage
from __init__ import app, db
import requests
from datetime import datetime

chat_api = Blueprint('chat_api', __name__, url_prefix='/api/chat')
api = Api(chat_api)
CORS(chat_api)

class ChatAPI:
    class _Test(Resource):
        def get(self):
            response = jsonify({"Connection Test": "Successfully connected to backend!"})
            return response

    class _Create(Resource):
        def post(self):
            data = request.json
            message = data.get('message')
            user_id = data.get('user_id', 1)  # Assuming a default user_id
            if message:
                chat_message = ChatMessage(message=message, user_id=user_id)
                db.session.add(chat_message)
                db.session.commit()
                return jsonify({"message": "Data stored successfully!"})
            else:
                return jsonify({"error": "Message is missing"}), 400

    class _Read(Resource):
        def get(self):
            chat_messages = ChatMessage.query.all()
            messages_json = [msg.serialize() for msg in chat_messages]
            return jsonify(messages_json)

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
    class _SortAlphabetically(Resource):
        def get(self):
            chat_messages = ChatMessage.query.order_by(ChatMessage.message).all()
            messages_json = [msg.serialize() for msg in chat_messages]
            return jsonify(messages_json)

api.add_resource(ChatAPI._Create, '/create')
api.add_resource(ChatAPI._Read, '/read')
api.add_resource(ChatAPI._Edit, '/edit')
api.add_resource(ChatAPI._Test, '/test')
api.add_resource(ChatAPI._SortAlphabetically, '/sort/alphabetical')

if __name__ == "__main__":
    app = create_app()  # Create the Flask app
    app.register_blueprint(chat_api)  # Register the chat API Blueprint

    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)  # Run the Flask app
