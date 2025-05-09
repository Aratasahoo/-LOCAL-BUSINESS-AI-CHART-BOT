from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure OpenAI API
openai.api_key=("")

# Enhanced predefined responses with more emojis
PREDEFINED_QA = {
    "what are your hours of operation": "⏰ **Our Hours** ⏰\n\n• Mon-Fri: 8:00 AM - 9:00 PM\n• Sat-Sun: 9:00 AM - 10:00 PM\n\nWe can't wait to serve you! 😊",
    "where are you located": "📍 **Our Location** 📍\n\n123 Main Street\nDowntown District\nAnytown, AT 12345\n\nCome visit us today! 🏡✨",
    "do you offer delivery": "🚚 **Delivery Options** 🚚\n\n• Free delivery (orders >$25)\n• Partner apps: DoorDash, UberEats\n• 5-mile radius\n\nYour food arrives fresh! 🌯🔥",
    "what's on the menu": "🍽️ **Menu Highlights** 🍽️\n\n• 🍔 Gourmet Burgers\n• 🍕 Artisan Pizzas\n• 🥗 Fresh Salads\n• 🍝 Pasta Specialties\n• 🍰 Decadent Desserts\n\nWant our full menu PDF? 📥",
    "hours": "⏰ Open Daily:\n\nWeekdays: 8AM-9PM\nWeekends: 9AM-10PM\n\nLate night cravings? We got you! 🌙",
    "location": "🗺️ Find Us At:\n\n123 Main St (Between 5th & 6th)\nPlenty of parking! 🚗💨",
    "delivery": "🛵 Fast Delivery!\n\n• 30-min guarantee\n• Track your driver\n• Contactless option\n\nWhere should we deliver? 🏠",
    "menu": "📋 **Today's Specials** 📋\n\n1. Truffle Burger 🍔+🍟\n2. Margherita Pizza 🍕\n3. Caesar Salad 🥗\n\nDietary requests? Just ask! 💬"
}

def get_predefined_answer(question):
    """Check if question matches any predefined questions"""
    lower_question = question.lower().strip("?.!,")
    for q, a in PREDEFINED_QA.items():
        if q in lower_question or any(word in lower_question.split() for word in q.split()):
            return a
    return None

def get_ai_response(prompt):
    """Get response from OpenAI API for non-predefined questions"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a friendly assistant for 'Urban Eats' restaurant. Respond concisely (max 2 sentences) with helpful info and tasteful emojis. Be warm and professional."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return "🔌 Connection issue - please try again soon! For immediate help, call (123) 456-7890 📞"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    # First check if this is a predefined question
    predefined_answer = get_predefined_answer(user_message)
    if predefined_answer:
        return jsonify({'response': predefined_answer})
    
    # If not, use AI
    ai_response = get_ai_response(user_message)
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
