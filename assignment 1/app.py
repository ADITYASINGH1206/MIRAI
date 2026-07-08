import streamlit as st

# Task 1: The UI Shell
st.title("Echo Chamber 9000")
st.write("Welcome to the Echo Chamber. Please provide your name and message below to initiate transmission.")

# Task 2: Multi-Data Collection
user_name = st.text_input("Name")
user_message = st.text_input("Message")

# Task 3: The Action Gate
if st.button("Transmit"):
    # Task 4: Conditional Routing (Edge Cases)
    if not user_name:
        st.error("Please provide your name.")
    elif not user_message:
        st.warning("Please type a message to transmit.")
    else:
        # Task 5: The Formatted Output
        st.success(f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}")

        total_characters = len(user_message)
        token_count = total_characters / 4
        st.info(f"System Check: Your message will consume approximately {token_count} tokens from our context window.")
