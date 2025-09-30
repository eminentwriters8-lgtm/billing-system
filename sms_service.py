import africastalking

# Your Africa's Talking credentials
username = "matombiti"  # Your Africa's Talking username
api_key = "atsk_4452aa99cd6609fc76a33e558f46eb59e4056ff7610766f235ab72793adedc87fa2c2e41"  # Your API key

# Initialize Africa's Talking SDK
africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_billing_sms(customer_phone, customer_name, invoice_number, amount, message_type="invoice"):
    """
    Send SMS for billing-related events
    """
    
    # Format phone number to international format
    if customer_phone.startswith('0'):
        customer_phone = '+254' + customer_phone[1:]  # Convert 0712... to +254712...
    
    # Create different message templates
    messages = {
        "invoice": f"Hello {customer_name}, your invoice #{invoice_number} for KES {amount} is ready. Thank you!",
        "reminder": f"Reminder {customer_name}, invoice #{invoice_number} for KES {amount} is due soon. Please pay to avoid interruption.",
        "payment": f"Thank you {customer_name}! Payment of KES {amount} for invoice #{invoice_number} has been received.",
        "overdue": f"URGENT {customer_name}, invoice #{invoice_number} for KES {amount} is OVERDUE. Please pay immediately."
    }
    
    # Get the appropriate message
    message = messages.get(message_type, messages["invoice"])
    
    # Add opt-out message (required by law)
    message += " Reply STOP to opt-out."
    
    try:
        # Send the SMS - ⚠️ REPLACE "YOUR_SENDER_ID" with your actual Sender ID!
        sender_id = "YOUR_SENDER_ID"  # CHANGE THIS to your approved Sender ID from Africa's Talking
        response = sms.send(message, [customer_phone], sender_id)
        
        print(f"✅ SMS sent successfully to {customer_name} ({customer_phone})")
        print(f"📱 Message: {message}")
        return True
        
    except Exception as e:
        print(f"❌ FAILED to send SMS to {customer_name}: {e}")
        return False

# TEST FUNCTION - This will send a real SMS to your phone!
def test_sms_function():
    """Test the SMS function with YOUR phone number"""
    print("🧪 Testing SMS function with your number +254706315742...")
    
    success = send_billing_sms(
        "254706315742",    # YOUR phone number (without +)
        "Mato Mbiti",      # Your name for testing
        "TEST-001",        # Test invoice number
        1500,              # Test amount
        "invoice"          # Message type
    )
    
    if success:
        print("🎉 Test completed successfully! Check your phone for the SMS.")
    else:
        print("💥 Test failed! Check the error message above.")

# RUN THE TEST - Remove the # from the line below to enable testing
test_sms_function()