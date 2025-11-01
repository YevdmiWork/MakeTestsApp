document.addEventListener('DOMContentLoaded', function () {
    const titleInput = document.querySelector('#id_title');
    const contentInput = document.querySelector('#id_content');
    const testEditBlock = document.querySelector('.test-edit');

    if (!titleInput || !contentInput || !testEditBlock) {
        console.error("Не найдены элементы формы");
        return;
    }

    const testId = testEditBlock.dataset.testId;
    const updateUrl = testEditBlock.dataset.updateUrl;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    function sendUpdate(field, value) {
        if (field === 'title' && !value.trim()) {
            titleInput.style.borderBottom = "3px solid red";
            return;
        } else {
            if (field === 'title') titleInput.style.borderBottom = "";
        }

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

            questionsList.insertAdjacentHTML('beforeend', data.question_html);

            questionsList.querySelectorAll('.questions-edit__question-number').forEach((el, idx) => {
                el.textContent = (idx + 1) + '.';
            });

        } catch (err) {
            console.error('Ошибка при добавлении вопроса:', err);
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    document.querySelectorAll('.questions-edit__add-answer-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(form);
            const addUrl = form.dataset.addUrl;

            fetch(addUrl, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const questionBlock = form.closest('.questions-edit__details');
                    const answersContainer = questionBlock.querySelector('.questions-edit__answers-list');
                    answersContainer.insertAdjacentHTML('beforeend', data.html);
                    form.reset();
                } else {
                    alert(data.error || 'Ошибка добавления ответа');
                }
            })
            .catch(() => alert('Ошибка запроса'));
        });
    });

    document.querySelectorAll('.questions-edit__answers-list').forEach(container => {
        container.addEventListener('input', function(e) {
            if (e.target.classList.contains('questions-edit__answer-input')) {
                const input = e.target;
                const answerId = input.dataset.answerId;
                const text = input.value.trim();
                if (!text) {
                    input.style.borderBottom = '1px solid red';
                    return;
                }
                updateAnswer(answerId, { text }, input);
            }
        });

        container.addEventListener('change', function(e) {
            if (e.target.classList.contains('questions-edit__answer-flag')) {
                const checkbox = e.target;
                const answerId = checkbox.dataset.answerId;
                const flag = checkbox.checked;
                updateAnswer(answerId, { flag }, checkbox);
            }
        });
    });

    function updateAnswer(answerId, data, el) {
        const container = el.closest('.questions-edit__answers-list');
        const updateUrl = container.dataset.updateUrl;

        fetch(updateUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ answer_id: answerId, ...data })
        })
        .then(res => res.json())
        .then(resp => {
            if (resp.success) {
                el.style.borderBottom = '1px solid green';
                setTimeout(() => el.style.borderBottom = '1px solid #bfbfbf', 1000);
            } else {
                el.style.borderBottom = '1px solid red';
            }
        })
        .catch(() => el.style.borderBottom = '1px solid red');
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const questionBlocks = document.querySelectorAll(".questions-edit__question-block");
    let activeBlock = null;

    questionBlocks.forEach(block => {
        const header = block.querySelector(".questions-edit__question-block-header");
        const details = block.querySelector(".questions-edit__details");
        details.style.maxHeight = "0";
        details.style.overflow = "hidden";
        details.style.transition = "max-height 0.35s ease";

        header.addEventListener("click", (event) => {
            event.stopPropagation();

            if (activeBlock === block) {
                closeDetails(block);
                activeBlock = null;
                return;
            }

            if (activeBlock) {
                closeDetails(activeBlock);
            }

            openDetails(block);
            activeBlock = block;
        });
    });

    document.addEventListener("click", (event) => {
        if (
            activeBlock &&
            !activeBlock.contains(event.target)
        ) {
            closeDetails(activeBlock);
            activeBlock = null;
        }
    });

    function openDetails(block) {
        const details = block.querySelector(".questions-edit__details");
        details.style.maxHeight = details.scrollHeight + "px";
    }

    function closeDetails(block) {
        const details = block.querySelector(".questions-edit__details");
        details.style.maxHeight = "0";
    }

    const observer = new MutationObserver(() => {
        if (activeBlock) {
            const details = activeBlock.querySelector(".questions-edit__details");
            details.style.maxHeight = details.scrollHeight + "px";
        }
    });

    document.querySelectorAll(".questions-edit__details").forEach(details => {
        observer.observe(details, { childList: true, subtree: true });
    });
});