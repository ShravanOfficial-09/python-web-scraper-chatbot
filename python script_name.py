import os
import urllib.request
import json

os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"  # Replace with your OpenAI API Key

url = "https://brainlox.com/courses/category/technical"

def scrape_brainlox_courses(url):
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to retrieve the webpage: {e}")
        return []
    
   
    courses = []
    split_content = html.split('<div class="course-card">') 
    for content in split_content[1:]:
        title_start = content.find('<h3>') + 4
        title_end = content.find('</h3>')
        title = content[title_start:title_end] if title_start > 3 and title_end != -1 else "No title"

        desc_start = content.find('<p>') + 3
        desc_end = content.find('</p>')
        description = content[desc_start:desc_end] if desc_start > 2 and desc_end != -1 else "No description"

        link_start = content.find('href="') + 6
        link_end = content.find('"', link_start)
        link = content[link_start:link_end] if link_start > 5 and link_end != -1 else "No link"

        courses.append({"title": title.strip(), "description": description.strip(), "link": link.strip()})
    
    return courses


def keyword_search(courses, query):
    results = []
    query_lower = query.lower()
    for course in courses:
        if query_lower in course['title'].lower() or query_lower in course['description'].lower():
            results.append(course)
    return results[:3] 


def simulate_chatbot(queries):
    print("Simulating Brainlox Course Chatbot with predefined queries...")

    courses_data = scrape_brainlox_courses(url)

    for user_input in queries:
        print(f"You: {user_input}")
        
        
        results = keyword_search(courses_data, user_input)

        if results:
            print("Here are the top courses I found:")
            for idx, course in enumerate(results, 1):
                print(f"{idx}. {course['title']}: {course['description']} (Link: {course['link']})")
        else:
            print("Sorry, I couldn't find any courses matching your query.")
        print("\n")

if __name__ == '__main__':
    test_queries = [
        "Python",
        "Data Science",
        "Machine Learning",
        "Web Development",
        "exit"
    ]
    simulate_chatbot(test_queries)
