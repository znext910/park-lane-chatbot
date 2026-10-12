
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import re

app = Flask(__name__)

BUSINESS_NAME = "Park Lane Motors"
BUSINESS_PHONE = "+971 52 934 1194"
WHATSAPP_NUMBER = "971529341194"

FAQS = [
    {
        "keywords": ["hello", "hi", "hey", "good morning", "good afternoon"],
        "answer": (
            "Hello! Welcome to Park Lane Motors, Dubai. "
            "How can I help you today?"
        )
    },
    {
        "keywords": ["buy", "buying", "purchase", "available cars", "inventory", "stock"],
        "answer": (
            "We can help you explore our premium used cars. "
            "Visit our Buy Car section to browse available vehicles. "
            "Is there a particular make or model you're looking for?"
        )
    },
    {
        "keywords": ["sell", "selling", "my car", "sell my vehicle"],
        "answer": (
            "Interested in selling your car? Please share the make, "
            "model, year, and mileage of your vehicle. Our team can "
            "help you with the next steps."
        )
    },
    {
        "keywords": ["finance", "loan", "monthly payment", "installment", "instalment"],
        "answer": (
            "For vehicle finance enquiries, our team can explain "
            "the available options and eligibility requirements. "
            "Please contact the dealership for current terms."
        )
    },
    {
        "keywords": ["location", "address", "where are you", "directions"],
        "answer": (
            "Park Lane Motors is located in Dubai Investments Park, Dubai, UAE. "
            "Please contact our team for directions to the showroom."
        )
    },
    {
        "keywords": ["opening hours", "business hours", "timings", "open", "close"],
        "answer": (
            "For our current showroom opening hours, please contact "
            "our team directly so we can provide accurate information."
        )
    },
    {
        "keywords": ["contact", "phone", "call", "number", "telephone"],
        "answer": (
            f"You can call Park Lane Motors at {BUSINESS_PHONE}. "
            "You can also message us on WhatsApp."
        )
    },
    {
        "keywords": ["whatsapp", "message you", "chat with team"],
        "answer": (
            "You can contact our team directly on WhatsApp using "
            "the WhatsApp button in this chat."
        )
    },
    {
        "keywords": ["event", "events", "exhibition"],
        "answer": (
            "For information about upcoming events, please contact "
            "our team or visit the Events section of our website."
        )
    },
    {
        "keywords": ["warranty", "guarantee", "service history", "inspection"],
        "answer": (
            "Vehicle warranty, inspection, and service-history details "
            "can vary by car. Tell us which vehicle interests you, "
            "and our team can help confirm the details."
        )
    },
    {
        "keywords": ["thank", "thanks"],
        "answer": "You're welcome! Is there anything else I can help you with?"
    },
    {
        "keywords": ["bye", "goodbye"],
        "answer": (
            "Thank you for contacting Park Lane Motors. "
            "Have a great day!"
        )
    }
]


def find_answer(message):
    """Find the best matching predefined FAQ answer."""
    text = message.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    if not text:
        return "Please type a question so I can help you."

    best_answer = None
    best_score = 0

    for faq in FAQS:
        score = 0

        for keyword in faq["keywords"]:
            keyword = keyword.lower()

            if " " in keyword:
                if keyword in text:
                    score += 2
            elif keyword in text.split():
                score += 1

        if score > best_score:
            best_score = score
            best_answer = faq["answer"]

    if best_answer:
        return best_answer

    return (
        "I don't have a confirmed answer for that question yet. "
        "Please contact our team on WhatsApp, or tell me whether "
        "your enquiry is about buying a car, selling a car, or finance."
    )


@app.route("/")
def home():
    return render_template(
        "index.html",
        business_name=BUSINESS_NAME,
        whatsapp_number=WHATSAPP_NUMBER
    )


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({
            "success": False,
            "reply": "Please enter a message."
        }), 400

    if len(message) > 1000:
        return jsonify({
            "success": False,
            "reply": "Please keep your message under 1000 characters."
        }), 400

    return jsonify({
        "success": True,
        "reply": find_answer(message),
        "business": BUSINESS_NAME,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
