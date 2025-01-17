// Функция обновления информации о системе
function updateSystemInfo(cpu, ram, disk) {
    document.getElementById('cpu').innerText = cpu;  // Обновляем отображение использования CPU
    document.getElementById('ram').innerText = ram;  // Обновляем отображение использования RAM
    document.getElementById('disk').innerText = disk;  // Обновляем отображение использования диска

    // Обновляем ширину полос для визуализации использования
    document.getElementById('cpu-bar').style.width = cpu + '%';
    document.getElementById('ram-bar').style.width = ram + '%';
    document.getElementById('disk-bar').style.width = disk + '%';
}

let recording = false;  // Флаг записи
let seconds = 0;  // Секунды
let minutes = 0;  // Минуты
let hours = 0;  // Часы
let intervalId;  // ID интервала для таймера

// Функция для начала и остановки записи
function toggleRecording() {
    recording = !recording;  // Переключаем флаг записи
    if (recording) {
        document.getElementById("recordButton").innerText = "Stop Recording";  // Изменяем текст кнопки
        document.getElementById("recordButton").classList.remove("btn-success");  // Убираем зеленый цвет
        document.getElementById("recordButton").classList.add("btn-danger");  // Добавляем красный цвет
        startTimer();  // Запускаем таймер
        // Вызов функции Python для начала записи
        window.pywebview.api.toggle_recording();
    } else {
        document.getElementById("recordButton").innerText = "Start Recording";  // Изменяем текст кнопки
        document.getElementById("recordButton").classList.remove("btn-danger");  // Убираем красный цвет
        document.getElementById("recordButton").classList.add("btn-success");  // Добавляем зеленый цвет
        stopTimer();  // Останавливаем таймер
        // Вызов функции Python для остановки записи
        window.pywebview.api.toggle_recording();
    }
}

// Функция для начала таймера
function startTimer() {
    intervalId = setInterval(function() {
        seconds++;  // Увеличиваем секунды
        
        // Преобразуем секунды в минуты
        if (seconds === 60) {
            seconds = 0;
            minutes++;
        }
        
        // Преобразуем минуты в часы
        if (minutes === 60) {
            minutes = 0;
            hours++;
        }

        // Обновляем таймер в формате часы:минуты:секунды
        document.getElementById("timer").innerText = formatTime(hours, minutes, seconds);
    }, 1000);
}

// Функция для остановки таймера
function stopTimer() {
    clearInterval(intervalId);  // Останавливаем интервал
}

// Функция для форматирования времени
function formatTime(hours, minutes, seconds) {
    return `${padZero(hours)}:${padZero(minutes)}:${padZero(seconds)}`;  // Форматируем время в формат 00:00:00
}

// Функция для добавления ведущего нуля к числам меньше 10
function padZero(number) {
    return number < 10 ? `0${number}` : number;  // Если число меньше 10, добавляем ноль в начале
}

// Функция для получения истории данных из базы
function get_history() {
    document.getElementById('system_info').style.display = 'none';  // Скрываем текущую информацию о системе
    document.getElementById('history_info').style.display = 'block';  // Показываем историю

    window.pywebview.api.get_history().then(data => {
        let historyContent = "<table class='table'><thead><tr><th>ID</th><th>CPU Usage (%)</th><th>RAM (%)</th><th>Disk (%)</th><th>Timestamp</th></tr></thead><tbody>";
        data.forEach(row => {
            historyContent += `<tr><td>${row.id}</td><td>${row.cpu_usage}</td><td>${row.ram}</td><td>${row.disk}</td><td>${row.timestamp}</td></tr>`;
        });
        historyContent += "</tbody></table>";
        document.getElementById("historyTable").innerHTML = historyContent;  // Отображаем таблицу с историей
    });
}

// Функция для возврата на главную страницу
function back_home() {
    document.getElementById('system_info').style.display = 'block';  // Показываем текущую информацию о системе
    document.getElementById('history_info').style.display = 'none';  // Скрываем историю
}

// Функция для очистки истории
function clear_history() {
    window.pywebview.api.clear_history();  // Очищаем историю через API
    document.getElementById("historyTable").innerHTML = "";  // Очищаем таблицу на странице
}
