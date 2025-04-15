
function initSlider() {
    const slider = document.querySelector('.slider');
    if (!slider) return; // Если слайдера нет на странице, выходим из функции
  
    const slides = document.querySelectorAll('.slide');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    const textContents = document.querySelectorAll('.text-content');
  
    // Проверка на существование кнопок и элементов слайдера (важно!)
    if (!slides || !prevButton || !nextButton || !textContents) {
      console.warn('Slider elements not found on this page.');
      return;
    }
  
    let counter = 0;
    const slideWidth = document.querySelector('.slider-container').clientWidth;
  
    function updateTextContent() {
      textContents.forEach((content, index) => {
        content.classList.toggle('active', index === counter);
      });
    }
  
    function slide() {
      const translateX = -slideWidth * counter;
      slider.style.transform = `translateX(${translateX}px)`;
    }
  
    nextButton.addEventListener('click', () => {
      counter = (counter + 1) % slides.length;
      slide();
      updateTextContent();
    });
  
    prevButton.addEventListener('click', () => {
      counter = (counter - 1 + slides.length) % slides.length;
      slide();
      updateTextContent();
    });
  
    updateTextContent(); // Инициализируем текст
  }
  
  // Функция для инициализации формы добавления кота
  function initCatForm() {
    const catForm = document.getElementById('catForm');
    if (!catForm) return; // Если формы нет на странице, выходим из функции
  
    $('#catForm').submit(function(event) {
      event.preventDefault();
  
      var name = $('#name').val();
      var age = $('#age').val();
      var description = $('#description').val();
      var imageFile = $('#image')[0].files[0];
  
      var formData = new FormData();
      formData.append('name', name);
      formData.append('age', age);
      formData.append('description', description);
      formData.append('image', imageFile);
  
      $.ajax({
        url: '/api/cats',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
          $('#message').text('Котик успешно добавлен!');
          $('#catForm')[0].reset();
          $(".custom-file-label").removeClass("selected").html("Выберите файл");
        },
        error: function(jqXHR, textStatus, errorThrown) {
          $('#message').text('Ошибка при добавлении котика: ' + textStatus + ' - ' + errorThrown);
        }
      });
    });
  }
  
  function initNewsForm() {
    const newsForm = document.getElementById('newsForm');
    if (!newsForm) return; // Если формы нет на странице, выходим из функции
  
    $('#newsForm').submit(function(event) {
      event.preventDefault();
  
      var title = $('#title').val();
      var date = $('#date').val();
      var content = $('#content').val();
      var imageFile = $('#image')[0].files[0];
  
      var formData = new FormData();
      formData.append('title', title);
      formData.append('date', date);
      formData.append('content', content);
      formData.append('image', imageFile);
  
      $.ajax({
        url: '/api/news',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
          $('#message').text('Новость успешно добавлена!');
          $('#newsForm')[0].reset();
          $(".custom-file-label").removeClass("selected").html("Выберите файл");
        },
        error: function(jqXHR, textStatus, errorThrown) {
          $('#message').text('Ошибка при добавлении новости: ' + textStatus + ' - ' + errorThrown);
        }
      });
    });
  }
  
  
  window.addEventListener('load', () => {
    initSlider();
    initCatForm();
    initNewsForm();
  });