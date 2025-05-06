import os
import base64
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText



def build_services(creds):
    calendar_service = build("calendar", "v3", credentials=creds)
    gmail_service = build("gmail", "v1", credentials=creds)
    return calendar_service, gmail_service


def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}


def send_confirmation_email(gmail_service, to_list, subject, message_text):
    for recipient in to_list:
        try:
            message = create_message(recipient, subject, message_text)
            sent_message = (
                gmail_service.users()
                .messages()
                .send(userId="me", body=message)
                .execute()
            )
            print(
                f"✅ Confirmation email sent to {recipient} (ID: {sent_message['id']})"
            )
        except Exception as e:
            print(f"❌ Failed to send email to {recipient}: {e}")


def create_event(
    summary,
    start_time,
    end_time,
    attendees,
    creds,
    location=None,
    description=None,
):
    calendar_service, gmail_service = build_services(creds)

    event = {
        "summary": summary,
        "location": location,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": "Asia/Karachi",
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "Asia/Karachi",
        },
        "attendees": [{"email": email} for email in attendees],
        "conferenceData": {
            "createRequest": {
                "requestId": f"meet-{int(datetime.utcnow().timestamp())}",
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
            }
        },
    }

    try:
        created_event = (
            calendar_service.events()
            .insert(calendarId="primary", body=event, conferenceDataVersion=1)
            .execute()
        )

        meet_link = created_event.get("hangoutLink", "No Google Meet link available.")
        subject = f"Meeting Confirmation: {summary}"
        body = (
            f"You are invited to the meeting:\n\n"
            f"📍 Location: {location or 'Online'}\n"
            f"🗓 Start: {start_time}\n"
            f"🕒 End: {end_time}\n"
            f"📄 Description: {description}\n"
            f"🔗 Event: {created_event['htmlLink']}\n"
            f"📞 Google Meet: {meet_link}"
        )

        send_confirmation_email(gmail_service, attendees, subject, body)

        return created_event
    except HttpError as error:
        print(f"❌ Calendar API error: {error}")
        return None
