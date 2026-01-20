from fastapi import FastAPI
import json

app = FastAPI()

global data

with open('./data.json') as f:
    data = json.load(f)


@app.get('/')
def hello_world():
    return 'Hello, World!'

@app.get('/students/{id}')
async def get_student(id):
  for student in data: 
    if student['id'] == id:
      return student

@app.get('/stats')
def get_stats():
    
    student_pref = {}
    student_programme = {}
    
    for item in data:
        if item.get('pref') in student_pref:
            student_pref[item.get('pref')] += 1
        else:
            student_pref[item.get('pref')] = 1
            
        if item.get('programme') in student_programme:
            student_programme[item.get('programme')] += 1
        else:
            student_programme[item.get('programme')] = 1
        
    return {
        'preference_counts': student_pref,
        'programme_counts': student_programme
    }
    
@app.get('/add/{num1}/{num2}')
def add_numbers(num1: int, num2: int):
    return {'result': num1 + num2}

@app.get('/multiply/{num1}/{num2}')
def multiply_numbers(num1: int, num2: int):
    return {'result': num1 * num2}

@app.get('/subtract/{num1}/{num2}')
def subtract_numbers(num1: int, num2: int):
    return {'result': num1 - num2}

@app.get('/divide/{num1}/{num2}')
def divide_numbers(num1: int, num2: int):
    if num2 == 0:
        return {'error': 'Division by zero is not allowed.'}
    return {'result': num1 / num2}

@app.get('/prime-sum/{prime_sum}')
def sum_prime(prime_sum: int):
    
    def is_prime(n):
        if n <= 1:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5)+1, 2):
            if n % i == 0:
                return False
        return True

    total = 0
    p_Count = 0
    num = 2
    while p_Count < int(prime_sum):
        if is_prime(num):
            total += num
            p_Count += 1
        num += 1
        
    return {'prime_sum': total}