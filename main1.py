from fastapi import FastAPI, HTTPException

app = FastAPI()

all_todos = [
    {'todo_id' : 1, 'todo_name' : 'Sports', 'todo_description' : 'Go to the gym'}, 
    {'todo_id' : 2, 'todo_name' : 'Read', 'todo_description' : 'Complete DISC course'}, 
    {'todo_id' : 3, 'todo_name' : 'Shop', 'todo_description' : 'Buy clothes'}, 
    {'todo_id' : 4, 'todo_name' : 'Code', 'todo_description' : 'Learn FastAPI'}
]

@app.get('/')
def index():
    return {"message" : "Hello World"}

@app.get('/todos/{todo_id}')
def get_todo(todo_id : int):
    for todo in all_todos: 
        if todo['todo_id'] == todo_id: 
            return {'result' : todo}
    raise HTTPException(status_code=404, detail="Todo not found")
        
@app.get('/todos')
def get_all_todos():
    return all_todos

@app.post('/todos')
def create_todo(todo : dict):
    new_todo_id = max(item['todo_id'] for item in all_todos) + 1

    new_todo = {
        'todo_id' : new_todo_id, 
        'todo_name' : todo['todo_name'], 
        'todo_description' : todo['todo_description']
    }

    all_todos.append(new_todo)

    return new_todo