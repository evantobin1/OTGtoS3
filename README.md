# AWS Greengrass Components

This project provides the necessary directory structure for the AWS Greengrass CDK project defined here: https://github.com/WirelessEco/laser-greengrass-v2

## Setup

1. **Clone the Repository**: Clone this repository to your local machine.

    ```bash
    git clone https://your-repository-url
    cd your-cdk-project-directory
    ```
2. **Create a folder for each component within the `/components` directory**:
3. **Define each recipe file in the following format**:
   ```json
   {
    "RecipeFormatVersion": "2020-01-25",
    "ComponentName": "[INSERT_COMPONENT_NAME_HERE]",
    "ComponentVersion": "1.0.x", // Note, you can customize the version major 
    // and minor numbers, but the patch number is managed by the pipeline.
    "ComponentDescription": "[INSERT_DESCRIPTION_HERE]",
    "ComponentPublisher": "[INSERT_ORG_HERE]",
    "ComponentConfiguration": {},
    "Manifests": [
        {
        "Platform": {
            "os": "linux"
        },
        "Lifecycle": {
            "run": "node {artifacts:decompressedPath}/[INSERT_FILE_PATH_HERE]"
        },
        "Artifacts": [
            {
            "URI": "s3://{bucketName}/[INSERT_COMPONENT_NAME_HERE]/[INSERT_COMPONENT_NAME_HERE].zip",
            "Unarchive": "ZIP"
            }
        ]
        },
        {
        "Platform": {
            "os": "windows"
        },
        "Lifecycle": {
            "run": "node {artifacts:decompressedPath}\\[INSERT_FILE_PATH_HERE]"
        },
        "Artifacts": [
            {
            "URI": "s3://{bucketName}/[INSERT_COMPONENT_NAME_HERE]/[INSERT_COMPONENT_NAME_HERE].zip",
            "Unarchive": "ZIP"
            }
        ]
        }
    ]
    }
   ```