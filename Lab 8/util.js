// replace with your fork of the completed lab 3 repl https://replit.com/@Snickdx/INFO-2602-Lab-3-Completed
const server = "https://9d12af7b-a3db-40f8-874b-72cc4ceba9dc-00-1mhomfu4s2k6l.riker.replit.dev";

function toast(message){
  M.toast({html: message});
}

async function sendRequest(url, method, data){
  try{
    //retrieve token from localStorage
    let token = window.localStorage.getItem('access_token');

    let options = {//options passed to fetch function
        method: method,
        headers: { 
          'Content-Type' : 'application/json',
          'Authorization' : `Bearer ${token}`//send token in request
        }
    };

    if(data)//data will be given for PUT & POST requests
      options.body = JSON.stringify(data);//convert data to JSON string

    let response = await fetch(url, options);
      
    let result = await response.json();//Get json data from response
    return result;//return the result

  }catch(error){
    return {error: error};//catch and log any errors
  }
}