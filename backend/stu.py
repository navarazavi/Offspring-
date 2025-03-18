import random
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class StuTheStork:
    def __init__(self):
        self.responses = {
            "greeting": [
                "Hey there! I'm Stu the Stork, here to help with fertility insights.",
                "Hello! How can I support your fertility journey today?",
                "Hi, I'm Stu. Let's talk fertility tracking!"
            ],
            "encouragement": [
                "I know this journey can be hard, but you're doing your best. 💙",
                "You're not broken—fertility is complex, and I'm here to help track what we can.",
                "Small changes can make a big impact. Let’s look at your data together."
            ],
            "cycle_tracking": [
                "Based on your Apple Health data, your predicted fertility window starts soon.",
                "Tracking temperature trends can help pinpoint ovulation. Want to log today’s data?",
                "Have you considered syncing your cycle with your partner’s Apple Health for joint tracking?"
            ],
            "consultation": [
                "I'm here to provide insights, but a fertility specialist can give personalized advice.",
                "I can help track trends, but a doctor can run the right tests to dig deeper.",
                "It might be helpful to consult an expert for more guidance. I can help track symptoms in the meantime."
            ],
            "general_fertility_questions": [
                {"question": "What is fertility?", "answer": "Fertility is the natural ability to conceive a child, involving the functioning of the reproductive system."},
                {"question": "How do I know when I'm most fertile?", "answer": "The most fertile time is typically during ovulation, which occurs around 14 days before your next period."},
                {"question": "How can I improve my fertility?", "answer": "Maintain a healthy lifestyle with a balanced diet, exercise, stress management, and proper medical care."},
                {"question": "What is IVF?", "answer": "In vitro fertilization (IVF) is a procedure where eggs are fertilized outside the body before being implanted in the uterus."},
                # Add more fertility-related questions here...
            ]
        }

        # Load GPT-2 model and tokenizer
        self.model_name = "gpt2"  # You can use larger models like "gpt2-medium" or "gpt2-large"
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)

        # Set pad token to eos_token (important for GPT-2)
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate_response(self, user_input):
        """Generate a response from the GPT-2 model."""
        # Tokenize the user input
        inputs = self.tokenizer(user_input, return_tensors="pt")
        
        # Generate a response from GPT-2
        outputs = self.model.generate(inputs['input_ids'], max_length=100, num_return_sequences=1)
        
        # Decode the output tokens to readable text
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return generated_text

    def match_question(self, user_input):
        """Match user input to a known question and return an appropriate response."""
        user_input_lower = user_input.lower()
        
        # Matching categories based on keywords
        if any(word in user_input_lower for word in ["hi", "hello", "hey"]):
            return random.choice(self.responses["greeting"])
        elif any(word in user_input_lower for word in ["struggling", "broken", "help", "hard"]):
            return random.choice(self.responses["encouragement"])
        elif any(word in user_input_lower for word in ["cycle", "ovulation", "fertile", "window", "period"]):
            return random.choice(self.responses["cycle_tracking"])
        elif any(word in user_input_lower for word in ["doctor", "consult", "specialist"]):
            return random.choice(self.responses["consultation"])
        
        # Check if it matches any specific fertility-related questions
        for response in self.responses["general_fertility_questions"]:
            if user_input_lower in response["question"].lower():
                return response["answer"]

        # If no match found, generate a GPT-2 response
        return self.generate_response(user_input)
