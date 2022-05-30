from brownie import accounts, config, network, Contract
from scripts.advanced_canary.mock_scripts import deploy_mocks, contract_to_mock
from pathlib import Path
import requests
import os

LOCAL_ENV = ["development", "ganache-local", "mainnet-fork"]
opensea_url = "https://testnets.opensea.io/assets/{}/{}"


def is_local_env():
    if network.show_active() in LOCAL_ENV:
        return True
    return False


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if is_local_env():
        return accounts[0]
    return accounts.add(config["networks"][network.show_active()]["wallet_private_key"])


def get_contract(contract_name):
    # This function will grab the contract addresses from the brownie config
    # if define, otherwisem it will deploy a new version of that contract , and
    # return that mock contract

    # Args :
    #    contract_name (string)

    # Returns:
    #    brownie.network.contract.ProjectContract: the most recently deployed
    #    version of this contract.
    # """
    print(f"****** Getting contract {contract_name} instance .... ***********")
    contract_type = contract_to_mock[contract_name]

    if is_local_env():
        print(
            f"Environment is local .... a mock contract is required for {contract_name}"
        )
        if len(contract_type) <= 0:
            print("Creating a new mock instance for ", contract_name, " contract...")
            deploy_mocks(get_account(), contract_name)
        else:
            print(
                "An existing mock instance for ",
                contract_name,
                " contract has been identified at address:",
                contract_type[-1].address,
            )
        contract = contract_type[-1]
    else:
        print(
            "Environment is not Local .... getting network ",
            contract_name,
            " contract instance",
        )
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def upload_file_to_ipfs(file_path_binary):
    # This function upload a local image into IPFS and return the decentralized endpoint.

    # we open the file locally
    with Path(file_path_binary).open("rb") as filepath:
        image_binary = filepath.read()
        # upload then into IPFS using CLI command and local node and create a POST request to add our imag to IPFS.
        ipfs_url = "http://127.0.0.1:5001"
        ipfs_add_endpoint = "/api/v0/add"
        response = requests.post(
            url=ipfs_url + ipfs_add_endpoint, files={"file": image_binary}
        )
        ipfs_hash = response.json()["Hash"]
        filename = file_path_binary.split("/")[-1:][0]
        img_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        return img_uri


def upload_file_to_pinata(file_path_binary):
    # This function upload a local image into Pinata Pin service. In case our local node IPFS hasn't propagated and our daemon is down.

    filename = file_path_binary.split("/")[-1:][0]
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }

    # we open the file locally
    with Path(file_path_binary).open("rb") as filepath:
        image_binary = filepath.read()
        # upload then into IPFS using CLI command and local node and create a POST request to add our imag to IPFS.
        pinata_base_url = "https://api.pinata.cloud/"
        endpoint = "pinning/pinFileToIPFS"
        response = requests.post(
            url=pinata_base_url + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        ipfs_hash = response.json()["IpfsHash"]
        img_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        return img_uri
