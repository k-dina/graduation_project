//const saveButton = document.getElementById('save-button');

//saveButton.addEventListener('click', () => {
//  axios.get(`/users/save_simulation_view/${simulation_id}/`);
//  console.log('simulation saved');
//});

//const saveButton = document.getElementById('save-button');
//
//saveButton.addEventListener('click', () => {
//  axios.post(`/users/save_simulation_view/${simulation_id}/`)
//    .then(response => {
//      // Проверка, выполнилось ли перенаправление
//      if (response.headers['content-type'] === 'text/html; charset=utf-8') {
//        // Если это HTML-страница (перенаправление), перезагрузите страницу
//        window.location.href = response.request.responseURL;
//      } else {
//        console.log('simulation saved');
//      }
//    })
//    .catch(error => {
//      console.error('Произошла ошибка:', error);
//    });
//});
