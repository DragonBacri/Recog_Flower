# First, install the necessary libraries:
# pip install google-cloud-storage google-auth

import google.auth
from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError

def main():
    """
    Authenticates with Google Cloud and lists GCS buckets.
    The client library automatically finds and uses Application Default Credentials.
    """
    try:
        # The client library constructor calls google.auth.default() under the hood.
        # This is the recommended and most common way to authenticate.
        storage_client = storage.Client()

        # If you wanted to get the credentials and project ID explicitly, you could:
        # credentials, project_id = google.auth.default()
        # storage_client = storage.Client(credentials=credentials, project=project_id)

        print(f"Successfully authenticated using project: {storage_client.project}")

        print("Listing buckets:")
        buckets = storage_client.list_buckets()
        for bucket in buckets:
            print(f"- {bucket.name}")

    except DefaultCredentialsError:
        print(
            "Authentication failed. Please run 'gcloud auth application-default login' "
            "in your terminal to configure your credentials."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
