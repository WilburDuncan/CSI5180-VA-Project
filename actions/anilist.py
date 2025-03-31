import requests
import re
from bs4 import BeautifulSoup

def getDescription(name: str):
    query = '''
    query ($search: String) {
    Media(search: $search, type: ANIME) {
        id
        title {
        romaji
        english
        }
        description
        episodes
        averageScore
        genres
        characters(perPage: 5) {
        nodes {
            name {
            full
            }
        }
        }
    }
    }
    '''
    variables = {"search": name}
    response = requests.post("https://graphql.anilist.co",    json={"query": query, "variables": variables})
    data = response.json()
    media = data["data"]["Media"]
    text_message = BeautifulSoup(media['description'], 'html.parser').get_text()
    
    return text_message

def getRcmdAni(genre):
    num = 5
    query = '''
    query ($perPage: Int, $genre: String) {  # 统一使用单数$genre
        Page(perPage: $perPage) {
            media(type: ANIME, sort: [SCORE_DESC], status: FINISHED, genre: $genre) {
                title {
                    romaji
                    english
                }
                averageScore
            }
        }
    }
    '''
    
    formatted_genre = genre.capitalize() if genre else None
    variables = {"perPage": num, "genre": formatted_genre}
    
    try:
        response = requests.post(
            "https://graphql.anilist.co",
            json={"query": query, "variables": variables}
        )
        response.raise_for_status()
        data = response.json()
        
        if not data["data"]["Page"]["media"]:
            return f"No anime found for genre: {formatted_genre}"
        
        media_list = data["data"]["Page"]["media"]
        
        text_message = ""
        for idx, anime in enumerate(media_list, 1):
            title = anime["title"].get("english") or anime["title"].get("romaji") or "Untitled"
            score = anime.get("averageScore", 0) / 10 if anime.get("averageScore") else 0
            
            entry = f"{idx}. {title} (Score: {score:.1f}/10)\n"
            text_message += entry
            
        return text_message.strip()
    
    except Exception as e:
        error_msg = f"Error fetching recommendations: {str(e)}"
        print(error_msg)
        return error_msg
    
def getMainCharacter(name):
    query = '''
    query ($search: String) {
        Media(search: $search, type: ANIME) {
            title {
                romaji
                english
            }
            characters(perPage: 3, sort: ROLE, role: MAIN) {
                nodes {
                    name {
                        full
                    }
                    
                    image {
                        large
                    }
                }
            }
        }
    }
    '''
    
    variables = {"search": name}

    try:
        response = requests.post(
            "https://graphql.anilist.co",
            json={"query": query, "variables": variables},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        media_data = data["data"]["Media"]
        if not media_data or not media_data.get("characters"):
            return f"No main characters found for '{name}'"
        
        characters = media_data["characters"]["nodes"]
        text_message = ""
        
        for idx, character in enumerate(characters, 1):
            char_name = character["name"]["full"]
            image_url = character["image"]["large"] if character.get("image") else None

            entry = f"""{idx}. {char_name}
Image: {image_url}
"""      
            text_message += entry + "\n"

        return text_message.strip()
    
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        print(error_msg)
        return error_msg
    except KeyError as e:
        error_msg = f"Data parsing error: {str(e)}"
        print(error_msg)
        return f"Could not process data for '{name}'"
    
def getCharacterDescription(name):
    query = '''
    query ($search: String) {
        Character(search: $search) {
            name{
                full
                }
            description(asHtml: true)
            gender
            dateOfBirth{
                        month
                        day
                    }
            age
        }
    }
    '''
    
    variables = {"search": name}

    try:
        response = requests.post(
            "https://graphql.anilist.co",
            json={"query": query, "variables": variables},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        character=data["data"]["Character"]
        gender=character["gender"]
        age=character["age"]
        dob = character.get("dateOfBirth", {})
        dob_str = f"{dob.get('month', '?')}-{dob.get('day', '?')}" if dob else "Unknown"
        description=character['description']
        text_message=f"""
Gender: {gender}
Birthday: {dob_str}
Age: {age}
{description}
"""
        text_message = BeautifulSoup(text_message, 'html.parser').get_text()
 
        return text_message.strip()
    
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        print(error_msg)
        return error_msg
    except KeyError as e:
        error_msg = f"Data parsing error: {str(e)}"
        print(error_msg)
        return f"Could not process data for '{name}'"