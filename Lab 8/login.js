async function login(event) {
  // Prevent default action ie page direction
  event.preventDefault();

  // Get form data
  const form = event.target;

  let fields = form.elements;

  let data = {
    username: fields['username'].value,
    password: fields['password'].value,
  }

  form.reset();

  let result = await sendRequest(`${server}/login`, 'POST', data);
 
  
  if ("error" in result) {
    toast("Login Failed: ");
  } else {
    toast("Logged Successful");
    
    window.localStorage.setItem('access_token', result.access_token);
    window.location.href = 'app.html';
  }

}

document.forms['loginForm'].addEventListener('submit', login);
// document.querySelector('#loginForm').onSubmit(login);