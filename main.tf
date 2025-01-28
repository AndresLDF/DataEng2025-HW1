terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.17.0"
    }
  }
}

provider "google" {
  credentials = "../../glossy-grin-413315-24e4af0d311a.json"
  project     = "glossy-grin-413315"
  region      = "us-central1"
  zone        = "us-central1-c"
}

resource "google_storage_bucket" "auto-expire" {
  name          = "glossy-grin-413315-demo-terra-bucked"
  location      = "US"
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

# Create a BigQuery Dataset without specifying the location
resource "google_bigquery_dataset" "example_dataset" {
  dataset_id = "glossy_grin_413315_demo_terra_dataset"  # Your desired dataset ID
}