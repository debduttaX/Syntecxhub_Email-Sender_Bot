import csv
import os
import time
import logging
import smtplib

from dotenv import load_dotenv
from email.message import EmailMessage



# LOAD ENVIRONMENT VARIABLES


load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")



#  GMAIL SMTP SETTINGS


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
CSV_FILE = "recipients.csv"

ATTACHMENT_FILE = "attachments/report.pdf"


MAX_RETRIES = 3



# 3. LOGGING


logging.basicConfig(
    filename="email_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# 4. CHECK CREDENTIALS


if not EMAIL_ADDRESS or not EMAIL_PASSWORD:

    print("--------------------------------")
    print("       EMAIL SENDER BOT")
    print("--------------------------------")

    print("ERROR: Gmail credentials not found.")
    print("Please check your .env file.")

    exit()



#  SEND EMAIL FUNCTION


def send_email(name, receiver_email):

    subject = "Test Email - Email Sender Bot"

    body = f"""
Hello {name},

I hope you are doing well.

This is an automated email sent using Python.

The email was generated using an Email Sender Bot
built with Python and Gmail SMTP.

Please find the attached report if available.

Regards,
Email Sender Bot
"""


    
    # CREATE EMAIL
    

    message = EmailMessage()

    message["From"] = EMAIL_ADDRESS
    message["To"] = receiver_email
    message["Subject"] = subject

    message.set_content(body)


   
    # ADD ATTACHMENT
   
    if os.path.exists(ATTACHMENT_FILE):

        try:

            with open(ATTACHMENT_FILE, "rb") as file:

                file_data = file.read()

            message.add_attachment(
                file_data,
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(ATTACHMENT_FILE)
            )

            print("Attachment added.")

        except Exception as error:

            print("Warning: Could not attach file.")
            print(error)

            logging.warning(
                f"Attachment error - {error}"
            )

    else:

        print("No attachment found.")
        print("Email will be sent without attachment.")


   
    # RETRY SYSTEM
    

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            print(
                f"\nSending email to {receiver_email}..."
            )

            print(
                f"Attempt {attempt}/{MAX_RETRIES}"
            )


           
            # CONNECT TO GMAIL SMTP
           

            with smtplib.SMTP(
                SMTP_SERVER,
                SMTP_PORT,
                timeout=30
            ) as server:

                # Identify client
                server.ehlo()

                # Secure the connection
                server.starttls()

                # Identify again after TLS
                server.ehlo()

                # Login
                server.login(
                    EMAIL_ADDRESS,
                    EMAIL_PASSWORD
                )

                # Send email
                server.send_message(message)


            
            # SUCCESS
           

            print(
                f"\nSUCCESS: Email sent to {receiver_email}"
            )

            logging.info(
                f"SUCCESS - Email sent to {receiver_email}"
            )

            return 
        
        # ERROR HANDLING
        

        except smtplib.SMTPAuthenticationError:

            print("\nERROR: Gmail authentication failed.")

            print(
                "Check your Gmail address and App Password."
            )

            logging.error(
                f"AUTHENTICATION FAILED - {receiver_email}"
            )

            return False


        except smtplib.SMTPConnectError as error:

            print("\nERROR: Could not connect to Gmail SMTP.")

            print(error)

            logging.error(
                f"CONNECTION FAILED - {receiver_email} - {error}"
            )


        except smtplib.SMTPException as error:

            print("\nSMTP ERROR:")
            print(error)

            logging.error(
                f"SMTP ERROR - {receiver_email} - {error}"
            )


        except Exception as error:

            print("\nERROR:")
            print(error)

            logging.error(
                f"FAILED - {receiver_email} - {error}"
            )

        # RETRY
        

        if attempt < MAX_RETRIES:

            print("\nRetrying in 3 seconds...")

            time.sleep(3)

        else:

            print(
                f"\nFAILED: Could not send email to "
                f"{receiver_email}"
            )

            return False



# READ RECIPIENTS FROM CSV

def main():

    print("\n")
    print("================================")
    print("       EMAIL SENDER BOT")
    print("================================")
    print("\n")



    # CHECK CSV FILE
    

    if not os.path.exists(CSV_FILE):

        print(
            f"ERROR: {CSV_FILE} not found."
        )

        return


    try:

        with open(
            CSV_FILE,
            newline="",
            encoding="utf-8"
        ) as csvfile:

            reader = csv.DictReader(csvfile)


            
            # CHECK CSV COLUMNS
            

            if "name" not in reader.fieldnames:

                print(
                    "ERROR: CSV must contain 'name' column."
                )

                return


            if "email" not in reader.fieldnames:

                print(
                    "ERROR: CSV must contain 'email' column."
                )

                return
            # SEND EMAILS
    

            for row in reader:

                name = row["name"].strip()

                receiver_email = row["email"].strip()


                # Skip empty rows

                if not name or not receiver_email:

                    print(
                        "Skipping empty row..."
                    )

                    continue


                send_email(
                    name,
                    receiver_email
                )


                # Wait before next email

                time.sleep(2)


    except FileNotFoundError:

        print(
            f"ERROR: {CSV_FILE} not found."
        )


    except Exception as error:

        print(
            f"Unexpected error: {error}"
        )

        logging.error(
            f"PROGRAM ERROR - {error}"
        )



if __name__ == "__main__":

    main()