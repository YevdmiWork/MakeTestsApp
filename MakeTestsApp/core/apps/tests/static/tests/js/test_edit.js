document.addEventListener('DOMContentLoaded', function () {
    const titleInput = document.querySelector('#id_title');
    const contentInput = document.querySelector('#id_content');
    const testEditBlock = document.querySelector('.test-edit');

    if (!titleInput || !contentInput || !testEditBlock) return;

    const testId = testEditBlock.dataset.testId;
    const updateUrl = testEditBlock.dataset.updateUrl;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    function sendUpdate(field, value) {
        if (field === 'title' && !value.trim()) {
            titleInput.style.borderBottom = "3px solid red";
            return;
        }
        if (field === 'content' && !value.trim()) value = "Нет описания";

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
        .then(res => res.json())
        .then(() => {
            const el = field === 'title' ? titleInput : contentInput;
            el.style.borderBottom = "3px solid #4CAF50";
            setTimeout(() => el.style.borderBottom = "", 800);
        })
        .catch(err => console.error("Ошибка сохранения:", err));
    }

    titleInput.addEventListener('blur', () => sendUpdate('title', titleInput.value));
    contentInput.addEventListener('blur', () => sendUpdate('content', contentInput.value));
});

let activeQuestionBlock = null;

function updateAnswer(answerId, data, el, csrfToken) {
    const container = el.closest('.questions-edit__answers-list');
    const updateUrl = container ? container.dataset.updateUrl : null;
    if (!updateUrl) return;

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

function initAddAnswerForms(context = document) {
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfMeta ? csrfMeta.content : document.querySelector('[name=csrfmiddlewaretoken]').value;

    const addAnswerForms = context.querySelectorAll('.questions-edit__add-answer-form');
    addAnswerForms.forEach(form => {
        if (form.dataset.initialized) return;
        form.dataset.initialized = "true";

        form.addEventListener('submit', e => {
            e.preventDefault();

            const formData = new FormData(form);
            const addUrl = form.dataset.addUrl;

            fetch(addUrl, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const questionBlock = form.closest('.questions-edit__question-block');
                    const answersContainer = questionBlock.querySelector('.questions-edit__answers-list');
                    answersContainer.insertAdjacentHTML('beforeend', data.html);
                    form.reset();
                    adjustQuestionHeight(questionBlock);
                } else {
                    alert(data.error || 'Ошибка добавления ответа');
                }
            })
            .catch(() => alert('Ошибка сети при добавлении ответа'));
        });
    });

    const answerLists = context.querySelectorAll('.questions-edit__answers-list');
    answerLists.forEach(container => {
        if (container.dataset.initialized) return;
        container.dataset.initialized = "true";

        container.addEventListener('input', e => {
            if (e.target.classList.contains('questions-edit__answer-input')) {
                const input = e.target;
                const answerId = input.dataset.answerId;
                const text = input.value.trim();
                if (!text) {
                    input.style.borderBottom = '1px solid red';
                    return;
                }
                updateAnswer(answerId, { text }, input, csrfToken);
            }
        });

        container.addEventListener('change', e => {
            if (e.target.classList.contains('questions-edit__answer-flag')) {
                const checkbox = e.target;
                const answerId = checkbox.dataset.answerId;
                updateAnswer(answerId, { flag: checkbox.checked }, checkbox, csrfToken);
            }
        });
    });
}

function initQuestionToggle(context = document) {
    const questionBlocks = context.querySelectorAll(".questions-edit__question-block");

    questionBlocks.forEach(block => {
        if (block.dataset.initialized) return;
        block.dataset.initialized = "true";

        const header = block.querySelector(".questions-edit__question-block-header");
        const details = block.querySelector(".questions-edit__details");
        details.style.maxHeight = "0";
        details.style.overflow = "hidden";
        details.style.transition = "max-height 0.35s ease";

        header.addEventListener("click", e => {
            e.stopPropagation();

            if (activeQuestionBlock === block) {
                closeDetails(block);
                activeQuestionBlock = null;
                return;
            }

            if (activeQuestionBlock) closeDetails(activeQuestionBlock);

            openDetails(block);
            activeQuestionBlock = block;
        });
    });
}

function openDetails(block) {
    const details = block.querySelector(".questions-edit__details");
    details.style.maxHeight = details.scrollHeight + "px";
}

function closeDetails(block) {
    const details = block.querySelector(".questions-edit__details");
    details.style.maxHeight = "0";
}

function adjustQuestionHeight(block) {
    const details = block.querySelector(".questions-edit__details");
    if (block === activeQuestionBlock) {
        details.style.maxHeight = details.scrollHeight + "px";
    }
}


document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.questions-edit__add-question-form');
    const questionsList = document.querySelector('.questions-edit__questions-list-scroll');
    if (!form || !questionsList) return;

    form.addEventListener('submit', async e => {
        e.preventDefault();
        const formData = new FormData(form);
        formData.append('test_id', form.dataset.testId);

        try {
            const response = await fetch(form.dataset.url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: formData
            });

            const data = await response.json();
            if (!data.success) {
                console.warn('Ошибка добавления вопроса:', data.error);
                return;
            }

            form.reset();
            questionsList.insertAdjacentHTML('beforeend', data.question_html);

            questionsList.querySelectorAll('.questions-edit__question-number')
                .forEach((el, i) => el.textContent = (i + 1) + '.');

            const newBlock = questionsList.lastElementChild;

            initAddAnswerForms(newBlock);
            initQuestionToggle(newBlock);

            openDetails(newBlock);
            activeQuestionBlock = newBlock;

        } catch (err) {
            console.error('Ошибка при добавлении вопроса:', err);
        }
    });

    initAddAnswerForms();
    initQuestionToggle();

    const observer = new MutationObserver(() => {
        if (activeQuestionBlock) adjustQuestionHeight(activeQuestionBlock);
    });

    document.querySelectorAll(".questions-edit__details").forEach(details => {
        observer.observe(details, { childList: true, subtree: true });
    });
});