const tabs = M.Tabs.init(document.querySelector('.tabs'));

//function must be declared async to support the await keyword
async function displayTodos(data) {

  let result = document.querySelector('#result');//access the DOM

  result.innerHTML = '';//clear result area

  let html = '';//make an empty html string 

  if ("error" in data) {//user not logged in 
    html += `
      <li class="card collection-item col s12 m4">
                <div class="card-content">
                  <span class="card-title">
                    Error : Not Logged In
                  </span>
                </div>
        </li>
    `;
  } else {
    for (let todo of data) {
      html += `
        <li class="card collection-item col s12 m4">
                  <div class="card-content">
                    <span class="card-title">${todo.text}
                      <label class="right">
                        <input type="checkbox" data-id="${todo.id}" onclick="toggleDone(event)" ${todo.done ? 'checked' : ''} />
                        <span>Done</span>
                      </label>
                    </span>
                  </div>
                  <div class="card-action">
                    <a href="#" onclick="deleteTodo('${todo.id}')">DELETE</a>
                  </div>
          </li>
      `;//create html for each todo data by interpolating the values in the todo
    }
  }

  //add the dynamic html to the DOM
  result.innerHTML = html;
}

async function loadView() {
  let todos = await sendRequest(`${server}/todos`, 'GET');
  displayTodos(todos);
}

loadView();

async function createTodo(event) {
  event.preventDefault();//stop the form from reloading the page
  let form = event.target.elements;//get the form from the event object

  let data = {
    text: form['addText'].value,//get data from form
    done: false,// newly created todos aren't done by default
  }

  event.target.reset();//reset form

  let result = await sendRequest(`${server}/todos`, 'POST', data);

  if ('error' in result) {
    toast('Error: Not Logged In');
  } else {
    toast('Todo Created!');
  }

  loadView();

}

//attach createTodo() to the submit event of the form
document.forms['addForm'].addEventListener('submit', createTodo);

async function toggleDone(event) {
  let checkbox = event.target;
  let id = checkbox.dataset['id'];//get id from data attribute

  let result = await sendRequest(`${server}/todos/${id}/done`, 'PUT');

  toast(result.message);
}

async function deleteTodo(id) {
  let result = await sendRequest(`${server}/todos/${id}`, 'DELETE');

  toast('Deleted!');

  loadView();
}

function logout() {
  window.localStorage.removeItem('access_token');
  window.location.href = "index.html";
}