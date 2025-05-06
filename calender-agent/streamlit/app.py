import streamlit as st
from datetime import datetime
import json
from openai import OpenAI
from backend import create_event

# --- Setup ---
st.set_page_config(page_title="Smart Scheduler", layout="centered")
st.title("📅 Smart Meeting Assistant")

# --- OpenAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # or use os.getenv()

# --- Auth Step ---
if "creds" not in st.session_state:
    st.subheader("🔐 Login with Google to continue")
    from google_auth_oauthlib.flow import InstalledAppFlow

    SCOPES = [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/gmail.send",
    ]

    if st.button("Login with Google"):
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        st.session_state["creds"] = creds
        st.success("✅ Logged in!")
        st.rerun()

# --- Initialize Chat State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are an AI meeting assistant that helps schedule meetings using Google Calendar and Gmail.",
        }
    ]

for msg in st.session_state.messages[1:]:  # skip system
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input ---
user_input = st.chat_input("Describe your meeting or request...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construct messages and tools
    today = datetime.now().strftime("%A, %B %d, %Y")
    messages = st.session_state.messages.copy()
    messages.insert(1, {"role": "user", "content": f"Today is {today}."})

    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_event",
                "description": "Creates a new event in Google Calendar with Google Meet and sends confirmation emails.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"},
                        "location": {"type": "string"},
                        "description": {"type": "string"},
                        "start_time": {"type": "string", "format": "date-time"},
                        "end_time": {"type": "string", "format": "date-time"},
                        "attendees": {
                            "type": "array",
                            "items": {"type": "string", "format": "email"},
                        },
                    },
                    "required": ["summary", "start_time", "end_time", "attendees"],
                },
            },
        }
    ]

    try:
        with st.spinner("🧠 Analyzing..."):
            response = client.chat.completions.create(
                model="gpt-4o", messages=messages, tools=tools, tool_choice="auto"
            )

        msg = response.choices[0].message
        tool_calls = msg.tool_calls

        # Append model response to chat if it's just asking for more input
        if not tool_calls:
            content = msg.content or "I'm not sure how to proceed. Could you clarify?"
            with st.chat_message("assistant"):
                st.markdown(content)
            st.session_state.messages.append({"role": "assistant", "content": content})
        else:
            # Parse tool call arguments
            tool_call = tool_calls[0]
            tool_args = json.loads(tool_call.function.arguments)

            # Check for missing fields and ask for them instead of failing
            required_fields = ["summary", "start_time", "end_time", "attendees"]
            missing = [key for key in required_fields if not tool_args.get(key)]

            if missing:
                follow_up = f"I need more information to schedule the meeting. Please provide: {', '.join(missing)}"
                with st.chat_message("assistant"):
                    st.markdown(follow_up)
                st.session_state.messages.append(
                    {"role": "assistant", "content": follow_up}
                )
            else:
                # Proceed to create the event
                with st.spinner("📅 Scheduling your meeting..."):
                    event = create_event(**tool_args, creds=st.session_state["creds"])

                if event:
                    meet_link = event.get("hangoutLink", "#")
                    event_link = event.get("htmlLink", "#")
                    assistant_reply = f"✅ Meeting created!\n\n📅 [Open Event]({event_link})\n📞 [Join Google Meet]({meet_link})"
                else:
                    assistant_reply = (
                        "❌ Failed to create the meeting. Please check your details."
                    )

                with st.chat_message("assistant"):
                    st.markdown(assistant_reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_reply}
                )

    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"An error occurred: {e}")
        st.session_state.messages.append(
            {"role": "assistant", "content": f"Error: {e}"}
        )
