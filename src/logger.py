import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psutil
import logging

SENDER = 'antoinelecroart@gmail.com'
SENDER_PWD = 'yawhxrkcgisffifs'
RECEIVER = 'antoine.lecroart@neuf.fr'


def send_error_email(traceback_str):
    sender_email = SENDER
    receiver_email = RECEIVER
    password = SENDER_PWD

    message = MIMEMultipart()
    message["Subject"] = "Error in Flask Application"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"An error occurred in your Flask application:\n\n{traceback_str}"

    message.attach(MIMEText(text, "plain"))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_metrics_alert(metric, value, threshold):
    sender_email = SENDER
    receiver_email = RECEIVER
    password = SENDER_PWD

    message = MIMEMultipart()
    message["Subject"] = "Metrics Alert in Flask Application"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"The {metric} has exceeded the threshold:\n\nCurrent Value: {value}\nThreshold: {threshold}"
    part = MIMEText(text, "plain")

    message.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent

    cpu_threshold = 0.1  # Seuil pour l'utilisation du CPU en pourcentage
    memory_threshold = 80  # Seuil pour l'utilisation de la RAM en pourcentage

    if cpu_usage > cpu_threshold:
        alert_message = f"CPU Usage has exceeded the threshold: Current Value: {cpu_usage}, Threshold: {cpu_threshold}"
        logging.warning(alert_message)
        send_metrics_alert("CPU Usage", cpu_usage, cpu_threshold)

    if memory_usage > memory_threshold:
        alert_message = f"Memory Usage has exceeded the threshold: Current Value: {memory_usage}, Threshold: {memory_threshold}"
        logging.warning(alert_message)
        send_metrics_alert("Memory Usage", memory_usage, memory_threshold)

