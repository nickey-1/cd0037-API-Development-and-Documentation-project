# Full Stack Trivia API Project
This project is a game where users can test their knowledge answering trivia questions. The task for the project was to create an API and test suite for implementing the following functionality:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started

#### Installing Dependencies

Developers using this project should already have Python3, pip, node, and npm installed.

##### Frontend Dependencies
This project uses NPM to manage software dependencies. NPM Relies on the `package.json` file located in the `/frontend`  directory of this repository. After cloning, open your terminal and run:

```bash, cmd
npm install
```

##### Backend Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash, cmd
pip install -r requirements.txt
```

## Running the Frontend in Dev Mode
The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.

```bash, cmd
npm start
```

## Running the Server
From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Testing
To run the tests, run

```bash, cmd
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
Omit the dropdb command the first time you run tests.

## API Reference

### Getting Started

- Base URL: Currently this application is only hosted locally. The backend is hosted at `http://127.0.0.1:5000/`
- Authentication: This version does not require authentication or API keys.

### Error Handling
Errors are returned as JSON in the following format:

```
{
   "success": False,
   "error": 404,
   "message": "resource not found"
}
```
The API will return three types of errors:

- 400 – bad request
- 404 – resource not found
- 405 - method not allowed
- 422 – unprocessable
- 500 - server error(rare)

### Endpoints

#### GET /api/categories

- General: Returns list of categories.
- Sample:`curl http://127.0.0.1:5000/api/categories`

    ```
    {
      "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
      }, 
      "success": true
    }
    ```
    
#### GET /api/questions

- General:

    - Returns list of questions.
    - Results are paginated in groups of 10.
    - Also returns list of categories, total number of questions per page, and total number of questions.
    - Questions are ordered by difficulty
- Sample:`curl http://127.0.0.1:5000/api/questions`

  ```
  {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Jupiter",
            "category": 1,
            "difficulty": 1,
            "id": 28,
            "question": " Which planet has the most gravity?"
        },
        {
            "answer": "K",
            "category": 1,
            "difficulty": 1,
            "id": 32,
            "question": "What is the symbol for potassium?"
        },
        {
            "answer": "Short",
            "category": 1,
            "difficulty": 1,
            "id": 39,
            "question": "What is the opposite of tall?"
        },
        {
            "answer": "Alaska",
            "category": 3,
            "difficulty": 1,
            "id": 29,
            "question": "Which American state is the largest (by area)?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "The weather",
            "category": 1,
            "difficulty": 2,
            "id": 27,
            "question": "What is meteorology the study of?"
        },
        {
            "answer": "The Sahara Desert (although Antarctica which is larger might qualify as a desert too)",
            "category": 3,
            "difficulty": 2,
            "id": 30,
            "question": "Which desert is the largest in the world?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
                "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "1877",
            "category": 6,
            "difficulty": 3,
            "id": 24,
            "question": "In what year was the first ever Wimbledon Championship held?"
        }
    ],
    "questions_per_page": 10,
    "success": true,
    "total_questions": 19
  }  
  ```

#### DELETE /api/questions/<<int:question_id>>

- General:

    - Deletes a question by id using url parameters.
    - Returns id of deleted question upon success.
    - Returns updated questions paginated in groups of 10.
    - Also total number of questions per page, and total number of questions.
- Sample:`curl http://127.0.0.1:5000/api/questions/24 -X DELETE`
  ```
  {   
    "deleted": 24,
    "questions": [
        {
            "answer": "Jupiter",
            "category": 1,
            "difficulty": 1,
            "id": 28,
            "question": " Which planet has the most gravity?"
        },
        {
            "answer": "K",
            "category": 1,
            "difficulty": 1,
            "id": 32,
            "question": "What is the symbol for potassium?"
        },
        {
            "answer": "Short",
            "category": 1,
            "difficulty": 1,
            "id": 39,
            "question": "What is the opposite of tall?"
        },
        {
            "answer": "Alaska",
            "category": 3,
            "difficulty": 1,
            "id": 29,
            "question": "Which American state is the largest (by area)?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "The weather",
            "category": 1,
            "difficulty": 2,
            "id": 27,
            "question": "What is meteorology the study of?"
        },
        {
            "answer": "The Sahara Desert (although Antarctica which is larger might qualify as a desert too)",
            "category": 3,
            "difficulty": 2,
            "id": 30,
            "question": "Which desert is the largest in the world?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        }
    ],
    "questions_per_page": 10,
    "success": true,
    "total_questions": 18
  }  
  ```

#### POST /api/questions
This endpoint either creates a new question or returns search results.
1) If no search term is included in request:
 - General:
      
      - Creates a new question using JSON request parameters.
      - Returns JSON object with newly created question, as well as paginated questions.
      - Also returns the name and the id of the question
 - Sample:`curl http://127.0.0.1:5000/api/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Which US state contains an area known as the Upper Penninsula?", "answer": "Michigan", "difficulty": 3, "category": "3" }'`
     ```
     {
       "created": 40,
       "question_created": "Which US state contains an area known as the Upper Penninsula?",
       "questions": [
           {
               "answer": "K",
               "category": 1,
               "difficulty": 1,
               "id": 32,
               "question": "What is the symbol for potassium?"
           },
           {
               "answer": "Short",
               "category": 1,
               "difficulty": 1,
               "id": 39,
               "question": "What is the opposite of tall?"
           },
           {
               "answer": "Alaska",
               "category": 3,
               "difficulty": 1,
               "id": 29,
               "question": "Which American state is the largest (by area)?"
           },
           {
               "answer": "Jupiter",
               "category": 1,
               "difficulty": 1,
               "id": 28,
               "question": " Which planet has the most gravity?"
           },
           {
               "answer": "The weather",
               "category": 1,
               "difficulty": 2,
               "id": 27,
               "question": "What is meteorology the study of?"
           },
           {
               "answer": "The Sahara Desert (although Antarctica which is larger might qualify as a desert too)",
               "category": 3,
               "difficulty": 2,
               "id": 30,
               "question": "Which desert is the largest in the world?"
           },
           {
               "answer": "Lake Victoria",
               "category": 3,
               "difficulty": 2,
               "id": 13,
               "question": "What is the largest lake in Africa?"
           },
           {
               "answer": "Agra",
               "category": 3,
               "difficulty": 2,
               "id": 15,
               "question": "The Taj Mahal is located in which Indian city?"
           },
           {
               "answer": "George Washington Carver",
               "category": 4,
               "difficulty": 2,
               "id": 12,
               "question": "Who invented Peanut Butter?"
           },
           {
               "answer": "Michigan",
               "category": 3,
               "difficulty": 3,
               "id": 40,
               "question": "Which US state contains an area known as the Upper Penninsula?"
           }
       ],
       "questions_per_page": 10,
       "success": true,
       "total_questions": 19
     }
     ```

 2.. If search term is included in request:
- General:

    - Searches for questions using search term in JSON request parameters.
    - Returns JSON object with paginated matching questions.
- Sample:`curl http://127.0.0.1:5000/api/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "dec"}'`
  ```
  {
    "questions": [
        {
            "answer": "Hammer throw",
            "category": 6,
            "difficulty": 4,
            "id": 26,
            "question": " Which of these events is NOT part of a decathlon?"
        }
    ],
    "success": true,
    "total_questions": 1
  }
  ```
 
#### GET /api/categories/<<int:category_id>>/questions

- General:

    - Gets questions by category id using url parameters.
    - Returns JSON object with paginated matching questions.
    - Also returns the current category name and total number of questions
- Sample:`curl http://127.0.0.1:5000/api/categories/4/questions`
   
  ````
  {
    "current_category": "History",
    "questions": [
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        }
    ],
    "questions_per_page": 2,
    "success": true,
    "total_questions": 19
  }
  ````    
   
#### POST /api/quizzes
- General:

    - Allows users to play the quiz game.
    - Uses JSON request parameters of category and previous questions.
    - Returns JSON object with random question not among previous questions.
- Sample: `curl http://127.0.0.1:5000/api/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21], "quiz_category": {"type": "Science", "id": "1"}}'`
  ```
  {
    "question": {
            "answer": "Jupiter",
            "category": 1,
            "difficulty": 1,
            "id": 28,
            "question": " Which planet has the most gravity?"
    },
    "success": true
  }  
  ```
  
## Authors
Adebayo Precious authored the API (__init__.py), test suite (test_flaskr.py), and this README.
All other project files, including the models and frontend, were created by Udacity as a project template for the Full Stack Web Developer Nanodegree.