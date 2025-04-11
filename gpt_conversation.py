import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class GPTConversationManager:
    def __init__(self):
        """Initialize GPT Conversation Manager"""
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def get_response(self, conversation_history, current_step, user_input):
        """
        Get AI response based on conversation history and current step
        
        Args:
            conversation_history (dict): Previous conversation data
            current_step (str): Current step in conversation flow
            user_input (str): User's latest input
            
        Returns:
            dict: Response containing next step and message
        """
        # Create system message with context and instructions
        system_message = self._create_system_message(current_step)
        
        # Create user message with context from conversation history
        user_message = self._create_user_message(conversation_history, current_step, user_input)
        
        # Call GPT API
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            # Parse response
            ai_message = response.choices[0].message.content.strip()
            
            # Determine next step based on current step and AI response
            next_step = self._determine_next_step(current_step, ai_message, user_input)
            
            return {
                "message": ai_message,
                "next_step": next_step
            }
        except Exception as e:
            print(f"Error in GPT API call: {e}")
            # Fallback responses for each step
            fallback_responses = {
                "greeting": "Thanks for providing your name. What is the best number to call you back on?",
                "phone_number": "What service can we help you with?",
                "service": "What is the address where you need help?",
                "vehicle_info": "What is the address where you need help?",
                "business_name": "What is the address where you need help?",
                "location": "Ok, please stay by your phone, the technician will call you right back."
            }
            
            return {
                "message": fallback_responses.get(current_step, "Can you please repeat that?"),
                "next_step": self._determine_next_step(current_step, "", user_input)
            }
    
    def _create_system_message(self, current_step):
        """Create system message based on current conversation step"""
        base_instructions = (
            "You are Angi, a professional and friendly locksmith assistant. "
            "Your goal is to collect customer information in a natural, conversational way. "
            "Keep responses brief, professional, and friendly. "
            "Do not ask questions beyond the current step. "
            "Do not mention that you are an AI."
        )
        
        step_instructions = {
            "greeting": "Extract the customer's name from their response.",
            "phone_number": "Acknowledge their name and extract their phone number.",
            "service": "Determine what locksmith service they need. Identify if it's for a vehicle or business.",
            "vehicle_info": "Extract the make, model, and year of the vehicle.",
            "business_name": "Extract the name of the business.",
            "location": "Extract the service location or address."
        }
        
        return f"{base_instructions} {step_instructions.get(current_step, '')}"
    
    def _create_user_message(self, conversation_history, current_step, user_input):
        """Create user message with context from conversation history"""
        context = f"Current step: {current_step}\n"
        
        # Add relevant conversation history
        if conversation_history.get('name'):
            context += f"Customer name: {conversation_history['name']}\n"
        
        if conversation_history.get('phone_number'):
            context += f"Phone number: {conversation_history['phone_number']}\n"
        
        if conversation_history.get('service_requested'):
            context += f"Service requested: {conversation_history['service_requested']}\n"
        
        if conversation_history.get('vehicle_info'):
            context += f"Vehicle info: {conversation_history['vehicle_info']}\n"
        
        if conversation_history.get('business_name'):
            context += f"Business name: {conversation_history['business_name']}\n"
        
        # Add user's latest input
        context += f"Customer's response: {user_input}\n"
        
        return context
    
    def _determine_next_step(self, current_step, ai_message, user_input):
        """Determine the next conversation step based on current step and user input"""
        # Default progression of steps
        step_progression = {
            "greeting": "phone_number",
            "phone_number": "service",
            "service": self._determine_service_next_step(user_input),
            "vehicle_info": "location",
            "business_name": "location",
            "location": "completed"
        }
        
        return step_progression.get(current_step, "completed")
    
    def _determine_service_next_step(self, user_input):
        """Determine next step after service question based on user input"""
        user_input_lower = user_input.lower()
        
        # Check if service is for a vehicle
        if any(word in user_input_lower for word in ['car', 'vehicle', 'auto', 'automobile']):
            return "vehicle_info"
        
        # Check if it's a business call
        elif any(word in user_input_lower for word in ['business', 'company', 'office', 'store', 'shop']):
            return "business_name"
        
        # Default to location
        else:
            return "location"
