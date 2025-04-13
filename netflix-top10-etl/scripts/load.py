from google.cloud import storage
import os

def upload_to_gcs(bucket_name, source_file, destination_blob):
    """
    Uploads a local file to a Google Cloud Storage bucket.
    """
    # Initialize GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Create a new blob and upload file
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_file)

    print(f"✅ Uploaded: {source_file} → gs://{bucket_name}/{destination_blob}")

if __name__ == "__main__":
    bucket_name = "mikey-netflix-pipeline-etl"  # ✅ Replace with your actual bucket name
    source_file = "data/processed/netflix_tudum_top10_cleaned.csv"
    destination_blob = "cleaned/netflix_tudum_top10_cleaned.csv"

    # Make sure the file exists
    if os.path.exists(source_file):
        upload_to_gcs(bucket_name, source_file, destination_blob)
    else:
        print(f"❌ File not found: {source_file}")
