import requests
import streamlit as st
import spacy

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# API Keys from secrets.toml
TASTY_API_KEY = st.secrets["tastyapi"]
SPOONACULAR_API_KEY = st.secrets["spoonacularapi"]

# Function to fetch recipes from Spoonacular
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

# Function to fetch recipes from Tasty
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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Please enter the dish you want to make"):
    prompt.lower()

    doc = nlp(prompt)
    ingredients = [token.text for token in doc if not token.is_stop and not token.is_punct]

    # Join ingredients for the query
    ingredient_query = ', '.join(ingredients)

    st.chat_message("user").markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    chatlog = ""

    with st.chat_message("assistant"):
        

        spoonacular_recipes = fetch_spoonacular_recipes(ingredient_query)
        if spoonacular_recipes.get("results"):
            spoonacularresponse = ""
            for recipe in spoonacular_recipes["results"]:
                

                # Construct the URL for the recipe
                recipe_url = f"https://spoonacular.com/recipes/{'-'.join(recipe['title'].lower().split())}-{recipe['id']}"

                # Format the description with recipe information
                description = f"""
                ## {recipe['title']}
                **Preparation Time**: Approximately **{recipe['readyInMinutes']} minutes**  
                **Servings**: {recipe['servings']}  
                **Cost per Serving**: ${recipe.get('pricePerServing', 'N/A') / 100:.2f}  

                **[View Full Recipe Here]({recipe_url})**
                """
                st.markdown(description)
                spoonacularresponse += description
            chatlog += spoonacularresponse

        # Fetch recipes from Tasty
        tasty_recipes = fetch_tasty_recipes(ingredient_query)
        if tasty_recipes.get("results"):
            tastyresponse = ""
            for recipe in tasty_recipes["results"]:
                

                description = f"""
                ## {recipe['name']}
                **Description**: {recipe.get('description', 'No description available')}  
                **Servings**: {recipe.get('num_servings', 'N/A')} servings  
                **[View Full Recipe Here]({recipe.get('original_video_url', '#')})**
                """
                st.markdown(description)
                tastyresponse += description
            chatlog += tastyresponse
        
        

    st.session_state.messages.append({"role": "assistant", "content": chatlog})
            

                
        
        
 
    
