import json

CANARY_BREED_MAPPING = {
    1: "Doctor Canary",
    2: "Golden Canary",
    3: "Knight Canary",
    4: "Love Canary",
    5: "Mushroom Canary",
    6: "Phoenix Canary",
    7: "Punk Canary",
    8: "Rich Canary",
    9: "Techno Canary",
    10: "Witch Canary",
}

CANARY_DESC_MAPPING = {
    1: "Doctor Canary is a healing companion in Canaryland. It cures your illness and prevent from potential diseases.  Although it looks cold and dark, the Canary Doctor is actually warm-hearted and travelling together is good for your health.",
    2: "Golden Canary is a rare specy, most commonly seen with the legendary Chad Canary as it is among the earliest creatures on Canaryland.",
    3: "Knight Canary is a strong specy. With its special armour, the Canary Knight is brave and ready to fight all enemies and monsters to protect Ilona Canary from villain.",
    4: "Love Canary is a sweet specy. Definitely a rare find in Canaryland where everyone is driven by hidden treasures, it is the world, yet it is nothing at all. Isn’t it what love is about? Canary Love is always up for a bang-bang with.",
    5: "Mushroom Canary is definitely not the fast movers among all canaries; yeah it is so slow that mushroom starts growing on it - hmm maybe it’s nutritious? He loves going on adventure with Canary Techno",
    6: "Phoenix Canary is the oldest specy in Canaryland. Apart from the extravagent appearance, He is also the guardian of CanaryLand. Make sure you have one in your pocket when going into the fires.",
    7: "Punk Canary is an alternative specy who grew up with Max La Menace during the CanaryWursteinFur era. This specy goes along well with Canary Techno and Canary Mushroom. Please excuse his look.",
    8: "Rich Canary is rich for a reason. Ask them to guide you to find the treasures in Canaryland. Trading any goodies with them will likely result in loosing value, be carefull...",
    9: "Techno Canary is the way to go, even in Canaryland there is a boogie or two every months ! The Techno Canary loves to experiment new things with his buddy Canary Mushroom and Canary Punk.",
    10: "Witch Canary is a powerful and dark specy. It is hard to control a witch, but would be nice to have a friend that knows some magic?",
}

CANARY_ATR_CUTENESS_MAPPING = {
    1: 5,
    2: 8,
    3: 7,
    4: 10,
    5: 2,
    6: 9,
    7: 4,
    8: 6,
    9: 3,
    10: 1,
}

CANARY_ATR_POWER_MAPPING = {
    1: 60,
    2: 70,
    3: 90,
    4: 20,
    5: 40,
    6: 100,
    7: 30,
    8: 70,
    9: 50,
    10: 80,
}

CANARY_ATR_LOVE_MAPPING = {
    1: 2,
    2: 5,
    3: 6,
    4: 10,
    5: 6,
    6: 4,
    7: 7,
    8: 1,
    9: 8,
    10: 3,
}

CANARY_ATR_SNIFF_MAPPING = {
    1: 7,
    2: 5,
    3: 4,
    4: 10,
    5: 7,
    6: 4,
    7: 6,
    8: 7,
    9: 9,
    10: 2,
}

CANARY_ATR_VISION_MAPPING = {
    1: 80,
    2: 70,
    3: 90,
    4: 100,
    5: 30,
    6: 50,
    7: 60,
    8: 80,
    9: 10,
    10: 60,
}

CANARY_ATR_BOULE_MAPPING = {
    1: 1,
    2: 2,
    3: 3,
    4: 10,
    5: 7,
    6: 5,
    7: 6,
    8: 4,
    9: 8,
    10: 2,
}


def get_canary_breed(breed_number):
    return CANARY_BREED_MAPPING[breed_number]


def get_canary_description(breed_number):
    return CANARY_DESC_MAPPING[breed_number]


def get_canary_attributes(breed_number, attributes_json):
    for attribute in attributes_json:
        if attribute["trait_type"] == "cuteness":
            attribute["value"] = CANARY_ATR_CUTENESS_MAPPING[breed_number]
        if attribute["trait_type"] == "power":
            attribute["value"] = CANARY_ATR_POWER_MAPPING[breed_number]
        if attribute["trait_type"] == "love":
            attribute["value"] = CANARY_ATR_LOVE_MAPPING[breed_number]
        if attribute["trait_type"] == "sniffage":
            attribute["value"] = CANARY_ATR_SNIFF_MAPPING[breed_number]
        if attribute["trait_type"] == "vision":
            attribute["value"] = CANARY_ATR_VISION_MAPPING[breed_number]
        if attribute["trait_type"] == "boules":
            attribute["value"] = CANARY_ATR_BOULE_MAPPING[breed_number]
    return attributes_json
