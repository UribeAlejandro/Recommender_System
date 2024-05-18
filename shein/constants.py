import os

# Setup
DOMAIN = "shein.com"  # For checking if the URL is from the same domain
DEBUG = True  # Set to True to limit to 1 page
USE_DB = False  # True = MongoDB, False = JSON
URLS = "shein-categories.txt"

# Database
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
DATABASE_URL = f"mongodb://{MONGO_HOST}:27017/"


# Text processing
BLACKLISTED_WORDS = [
    "javascript:",
    "mailto:",
    "tel:",
    "facebook.com",
    "twitter.com",
    "instagram.com",
    "youtube.com",
    "pinterest.com",
    "tiktok.com",
    "Copyright",
    "copyright",
    "Privacy",
    "privacy",
    "Terms",
    "terms",
    "Imprint",
    "imprint",
    "bonus",
    "campaign",
    "campaigns",
    "sale",
    "refund",
    "track",
    "How-to",
    "how-to",
    "shein.com/women",
    "shein.com/other",
    "shein.com/Return-Policy",
    "shein.com/men",
    "shein.com/plussize",
    "shein.com/curve-plus-size",
    "promotion",
    "shein.com/home",
    "shein.com/cart",
    "contact",
    "About",
    "SUPPLY-CHAIN-TRANSPARENCY",
    "prime",
    "shein.com/kids",
    "shein.com/beauty",
    "shein.com/flashsale",
    "Shipping-Info",
    "coupon-a",
    "/user/auth/login",
    "daily-new",
    "New-in-Trends",
    "shein.com/style",
    "New-in-Trends",
    "shein.com/member-image-list",
    "weekly-picks",
]


CATEGORIES = [
    {"name": "Pet Clothing", "url": "https://us.shein.com/Pet-Supplies-c-2400.html?child_cat_id=2875"},
    {"name": "Pet Accessories", "headers": "child_cat_id=2892"},
    {"name": "Pet Toys", "headers": "child_cat_id=2893"},
    {"name": "Pet Furniture", "headers": "child_cat_id=4056"},
    {"name": "Pet Bedding", "headers": "child_cat_id=2894"},
    {"name": "Pet Bowls & Feeders", "headers": "child_cat_id=2896"},
    {"name": "Pet Cleaning", "headers": "child_cat_id=2946"},
    {"name": "Pet Outdoor Gear", "headers": "child_cat_id=2947"},
    {"name": "Pet Collars, Leashes & Harnesses", "headers": "child_cat_id=2949"},
    {"name": "Pet Grooming", "headers": "child_cat_id=2951"},
    {"name": "Pet Health Care", "headers": "child_cat_id=2955"},
    {"name": "Pet Appliances", "headers": "child_cat_id=3880"},
    {"name": "Bird Supplies", "headers": "child_cat_id=4028"},
    {"name": "Fish & Aquarium Supplies", "headers": "child_cat_id=4035"},
    {"name": "Small Animal Supplies", "headers": "child_cat_id=4040"},
    {"name": "Reptile & Amphibian Supplies", "headers": "child_cat_id=4043"},
    {"name": "Farm Animal Supplies", "headers": "child_cat_id=4047"},
    {"name": "Pet Memorial", "headers": "child_cat_id=4053"},
    {"name": "Horses", "headers": "child_cat_id=6327"},
    {"name": "Pet Treats", "headers": "child_cat_id=9682"},
    {"name": "Custom Pet Supplies", "headers": "child_cat_id=9815"},
]
