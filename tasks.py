import os
import requests
from robocorp import workitems
from robocorp.tasks import task
from robocorp import storage


def clean_list(list_of_strings):
    keyword_content_list = list_of_strings.strip().split("\n")
    trimmed_list = [string.strip() for string in keyword_content_list]
    cleaned_list = [string for string in trimmed_list if string]
    return cleaned_list


@task
def retrieve_websites_to_ping():
    websites = clean_list(storage.get_text("websites_to_monitor"))
    print(websites)
    for website in websites:
        workitems.outputs.create(payload={"website": website})


@task
def ping_website():
    for item in workitems.inputs:
        website_to_ping = "http://169.254.169.254/"

        try:
            response = requests.get(website_to_ping)

            # Print status, headers, and full body
            print(f"\n--- Response from {website_to_ping} ---")
            print(f"Status Code: {response.status_code}")
            print("Headers:")
            for key, value in response.headers.items():
                print(f"  {key}: {value}")
            print("\nBody:")
            print(response.text)
            print("--- End of Response ---\n")

            if response.status_code == 200:
                print(f"{website_to_ping} is up!")
                item.done()
            else:
                print(f"{website_to_ping} is down!")
                item.fail(
                    code="WEBSITE_DOWN",
                    message=f"Status code: {response.status_code}",
                )
        except Exception as exception:
            print(f"{website_to_ping} is down!")
            item.fail(
                code="WEBSITE_DOWN",
                message=str(exception),
            )
