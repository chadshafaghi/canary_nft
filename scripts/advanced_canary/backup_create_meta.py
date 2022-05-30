from scripts.advanced_canary.canary_helpful_script import (
    get_canary_breed,
    get_canary_description,
    get_canary_attributes,
)
from brownie import AdvancedCanaryCollectible, network
from scripts.helpful_scripts import (
    upload_file_to_pinata,
)
from metadata.sample_metadata import metadata_template
from pathlib import Path
import json


def main():
    canary_contract = AdvancedCanaryCollectible[-1]
    number_token = canary_contract.tokenCounter()
    print(f"The last contract created has {number_token} token minted")

    for token_id in range(number_token):
        canary_breed_number = canary_contract.canaryRandomBreedByTokenID(token_id + 1)
        canary_breed = get_canary_breed(canary_breed_number)

        print(
            f"Canary Token #{token_id} is breed of {canary_breed} which was random Breed # {canary_breed_number}"
        )
        # Preparing the Metadata file for each token
        token_metadata = metadata_template
        img_cleaned_name = canary_breed.replace(" ", "_")
        metadata_json_filepath = (
            f"./metadata/{network.show_active()}/{token_id}-{img_cleaned_name}.json"
        )
        if Path(metadata_json_filepath).exists():
            print(
                f"The Metadata file for {canary_breed} already exists. Please delete it if you want to regenerate a new one."
            )
        else:
            print(
                f"The Metadata file for breed {canary_breed} doesn't exist. Creating now..."
            )
            # Loading all Metadata attributes to this token #
            canary_description = get_canary_description(canary_breed_number)
            canary_attributes = get_canary_attributes(
                canary_breed_number, token_metadata["attributes"]
            )
            image_path = f"./img/CanaryNFT_{canary_breed.split()[0].capitalize()}.png"
            # canary_img_uri = upload_image_uri_to_ipfs(image_path)
            canary_img_uri = upload_file_to_pinata(image_path)

            token_metadata["name"] = canary_breed
            token_metadata["description"] = canary_description
            token_metadata["attributes"] = canary_attributes
            token_metadata["image"] = canary_img_uri

            # We now write the Metadata attributes into the URI JSON file

            with open(metadata_json_filepath, "w") as file:
                json.dump(token_metadata, file)

            file_uri = upload_file_to_pinata(metadata_json_filepath)
            print(f"This Json file has been successfully added to Pinata : {file_uri}")
