python
import africastalking

# Use sandbox credentials (FREE)
username = "sandbox"  # ← CHANGE to sandbox
api_key = "YOUR_SANDBOX_API_KEY"  # Get from Africa's Talking sandbox

africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_free_sms(customer_phone, customer_name, invoice_number, amount):
    # Format phone number
    if customer_phone.startswith('0'):
        customer_phone = '+254' + customer_phone[1:]
    
    message = f"Hello {customer_name}, invoice #{invoice_number} for KES {amount} is ready. Thank you!"
    
    try:
        # Use FREE shortcode
        response = sms.send(message, [customer_phone], "22550")
        print(f"✅ FREE SMS sent to {customer_name}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

# Test with your number
send_free_sms("254706315742", "Mato Test", "INV-001", 1500)