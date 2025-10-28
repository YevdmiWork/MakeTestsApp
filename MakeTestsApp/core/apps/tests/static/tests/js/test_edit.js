document.addEventListener('DOMContentLoaded', function () {
    const titleInput = document.querySelector('#id_title');
    const contentInput = document.querySelector('#id_content');
    const testEditBlock = document.querySelector('.test-edit');

    if (!titleInput || !contentInput || !testEditBlock) {
        console.error("Не найдены элементы формы. Проверьте селекторы или HTML.");
        return;
    }

    const testId = testEditBlock.dataset.testId;
    const updateUrl = testEditBlock.dataset.updateUrl;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    function sendUpdate(field, value) {
        // Проверка для title: если пустое, подсвечиваем красным и не отправляем
        if (field === 'title' && !value.trim()) {
            titleInput.style.borderBottom = "3px solid red";
            return;
        } else {
            // Сбрасываем красную подсветку, если есть
            if (field === 'title') titleInput.style.borderBottom = "";
        }

        // Для content пустое значение можно заменить на дефолт
        if (field === 'content' && !value.trim()) {
            value = "Нет описания";
        }

        fetch(updateUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                'test_id': testId,
                [field]: value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.warn("Ошибка при сохранении:", data.error);
            }
            showSaveIndicator(field);
        })
        .catch(error => console.error("Ошибка AJAX:", error));
    }

    function showSaveIndicator(field) {
        let el = field === 'title' ? titleInput : contentInput;
        el.style.borderBottom = "3px solid #4CAF50";
        setTimeout(() => el.style.borderBottom = "", 800);
    }

    titleInput.addEventListener('blur', () => sendUpdate('title', titleInput.value));
    contentInput.addEventListener('blur', () => sendUpdate('content', contentInput.value));
});

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.questions-edit__add-question-form');
    const questionsList = document.querySelector('.questions-edit__questions-list-scroll');

    if (!form || !questionsList) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        formData.append('test_id', form.dataset.testId);

        try {
            const response = await fetch('/add-question/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: formData
            });

            if (!response.ok) return;
            const data = await response.json();
            if (!data.success) return;

            form.reset();

            // вставляем готовый HTML в конец списка
            questionsList.insertAdjacentHTML('beforeend', data.question_html);

            // пересчет нумерации на фронтенде (если будут удаления)
            questionsList.querySelectorAll('.questions-edit__question-number').forEach((el, idx) => {
                el.textContent = (idx + 1) + '.';
            });

        } catch (err) {
            console.error('Ошибка при добавлении вопроса:', err);
        }
    });
});

