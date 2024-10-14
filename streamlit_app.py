import requests
import streamlit as st


TASTY_API_KEY = api_key=st.secrets["tastyapi"]
SPOONACULAR_API_KEY = api_key=st.secrets["spoonacularapi"]

def fetch_spoonacular_recipes(query):
    api_url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "query": query,
        "apiKey": SPOONACULAR_API_KEY,
        "number": 5,  # Number of recipes to fetch
        "addRecipeInformation": True  # Include additional recipe information
    }
    response = requests.get(api_url, params=params)
    return response.json()

def fetch_tasty_recipes(query):
    api_url = "https://tasty.p.rapidapi.com/recipes/list"
    headers = {
        "X-RapidAPI-Key": TASTY_API_KEY,
        "X-RapidAPI-Host": "tasty.p.rapidapi.com"
    }
    params = {"from": 0, "size": 5, "tags": query}  # Use the query directly as tags
    response = requests.get(api_url, headers=headers, params=params)
    return response.json()

# Streamlit UI
st.title("Cooking Bot")

# User input for recipe search
recipe_query = st.text_input("Enter a recipe ingredient or type (e.g., steak):")
recipe_query = recipe_query.lower()

if st.button("Get Recipes"):
    if recipe_query:
        # Fetch recipes from Spoonacular
        spoonacular_recipes = fetch_spoonacular_recipes(recipe_query)
        if spoonacular_recipes.get("results"):
            st.write("### Recipes Found:")
            for recipe in spoonacular_recipes["results"]:
                st.subheader(recipe["title"])
                st.image(recipe["image"])

        

                # Construct the URL for the recipe
                recipe_url = f"https://spoonacular.com/recipes/{'-'.join(recipe['title'].lower().split())}-{recipe['id']}"

                # Format the description with recipe information
                description = f"""
                **Preparation Time**: Approximately **{recipe['readyInMinutes']} minutes**  
                **Servings**: {recipe['servings']}  
                **Cost per Serving**: ${recipe.get('pricePerServing', 'N/A') / 100:.2f}  

                **[View Full Recipe Here]({recipe_url})**
                """
                st.markdown(description)
        else:
            st.write("No Spoonacular recipes found.")

        # Fetch recipes from Tasty
        tasty_recipes = fetch_tasty_recipes(recipe_query)
        if tasty_recipes.get("results"):
            for recipe in tasty_recipes["results"]:
                st.subheader(recipe["name"])
                st.image(recipe["thumbnail_url"])
             
                description = f"""
                **Description**: {recipe.get('description', 'No description available')}  
                **Servings**: {recipe.get('num_servings', 'N/A')} servings  
                **[View Full Recipe Here]({recipe.get('original_video_url', '#')})**
                """
                st.markdown(description)

