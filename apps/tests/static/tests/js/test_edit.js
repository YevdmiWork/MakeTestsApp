async function safeJsonFetch(response) {
    const text = await response.text();

    let data;

    try {
        data = JSON.parse(text);
    } catch (e) {
        console.error("Non-JSON response:", text);
        showGlobalError("Сервер вернул некорректный ответ");
        throw new Error("Invalid JSON");
    }

    if (!response.ok || data.error || data.success === false) {
        throw data;
    }

    return data;
}

function extractErrorMessage(data) {
    const error = data?.error;

    if (!error) return "Ошибка";

    if (error?.details?.errors?.length) {
        return error.details.errors.join("\n");
    }

    return error.message || "Ошибка";
}

function handleRequestError(err) {
    console.error(err);
    showGlobalError(extractErrorMessage(err));
}


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
        .then(safeJsonFetch)
        .then(() => {
            const el = field === 'title' ? titleInput : contentInput;
            el.style.borderBottom = "3px solid #4CAF50";
            setTimeout(() => el.style.borderBottom = "", 800);
        })
        .catch(handleRequestError);
    }

    titleInput.addEventListener('blur', () => sendUpdate('title', titleInput.value));
    contentInput.addEventListener('blur', () => sendUpdate('content', contentInput.value));
});

let activeQuestionBlock = null;


function updateAnswerText(answerId, text, input, csrfToken) {

    const answerBlock = input.closest('.questions-edit__answer-block');
    const url = answerBlock?.dataset.updateTextUrl;
    if (!url) return;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ text })
    })
    .then(safeJsonFetch)
    .then(resp => {
        input.style.borderBottom = '1px solid green';

        if (resp.answer?.html) {
            answerBlock.outerHTML = resp.answer.html;
        }
    })
    .catch(err => {
        input.style.borderBottom = '1px solid red';
        handleRequestError(err);
    });
}

function updateAnswerFlag(answerId, flag, checkbox, csrfToken) {

    const answerBlock = checkbox.closest('.questions-edit__answer-block');
    const url = answerBlock?.dataset.updateFlagUrl;
    if (!url) return;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ flag })
    })
    .then(safeJsonFetch)
    .then(resp => {
        if (resp.answer?.html) {
            answerBlock.outerHTML = resp.answer.html;
        }
    })
    .catch(err => {
        checkbox.checked = !checkbox.checked;
        handleRequestError(err);
    });
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
            .then(safeJsonFetch)
            .then(data => {
            })
            .catch(handleRequestError)
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

                clearTimeout(input._timer);
                input._timer = setTimeout(() => {
                    updateAnswerText(answerId, text, input, csrfToken);
                }, 500);
            }
        });

        container.addEventListener('change', e => {
            if (e.target.classList.contains('questions-edit__answer-flag')) {
                const checkbox = e.target;
                const answerId = checkbox.dataset.answerId;

                updateAnswerFlag(answerId, checkbox.checked, checkbox, csrfToken);
            }
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

        try {
            const response = await fetch(form.dataset.url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: formData
            });

            const data = await safeJsonFetch(response);
            form.reset();
            questionsList.insertAdjacentHTML('beforeend', data.html);

            questionsList.querySelectorAll('.questions-edit__question-number')
                .forEach((el, i) => el.textContent = (i + 1) + '.');

            const newBlock = questionsList.lastElementChild;

            initAddAnswerForms(newBlock);

            openDetails(newBlock);
            activeQuestionBlock = newBlock;

        } catch (err) {
            handleRequestError(err);
        }
    });

    initAddAnswerForms();

});


document.addEventListener("DOMContentLoaded", () => {
    const wrapper = document.querySelector(".test-info-edit__tags-block");
    if (!wrapper) return;

    const tagsContainer = document.getElementById("tagsContainer");
    const addBtn = document.getElementById("addTagBtn");
    const dropdown = document.getElementById("tagDropdown");
    const tagErrors = document.getElementById("tagErrors");
    const maxTags = Number(wrapper.dataset.maxTags);
    const testId = wrapper.dataset.testId;
    const addTagUrl = wrapper.dataset.addTagUrl;
    const removeTagUrl = wrapper.dataset.removeTagUrl;

    const getCSRF = () => {
        const match = document.cookie.match(/csrftoken=([^;]+)/);
        return match ? match[1] : null;
    };

    let errorTimeout;

    const showError = (text) => {
        clearTimeout(errorTimeout);
        tagErrors.textContent = text;
        tagErrors.classList.add("show");

        errorTimeout = setTimeout(() => {
            tagErrors.classList.remove("show");
        }, 3000);
    };

    const clearError = () => {
        clearTimeout(errorTimeout);
        tagErrors.classList.remove("show");
        tagErrors.textContent = "";
    };

    const getTagCount = () =>
        tagsContainer.querySelectorAll(".test-info-edit__tag-block").length;

    const isTagExists = (tagId) =>
        !!tagsContainer.querySelector(`[data-tag-id="${tagId}"]`);

    const updateAddButton = () => {
        if (getTagCount() >= maxTags) {
            addBtn.classList.add("hidden");
            dropdown.classList.remove("active");
        } else {
            addBtn.classList.remove("hidden");
        }
    };

    const hideDropdownTag = (tagId) => {
        const option = dropdown.querySelector(
            `.test-info-edit__tag-option[data-tag-id="${tagId}"]`
        );
        if (option) option.classList.add("hidden");
    };

    const showDropdownTag = (tagId, tagName) => {
        let option = dropdown.querySelector(
            `.test-info-edit__tag-option[data-tag-id="${tagId}"]`
        );

        if (option) {
            option.classList.remove("hidden");
            return;
        }

        option = document.createElement("div");
        option.className = "test-info-edit__tag-option";
        option.dataset.tagId = tagId;
        option.textContent = tagName;

        dropdown.appendChild(option);
        sortDropdown();
    };

    const sortDropdown = () => {
        const options = Array.from(
            dropdown.querySelectorAll(".test-info-edit__tag-option")
        );

        options
            .sort((a, b) =>
                a.textContent.trim().localeCompare(
                    b.textContent.trim(),
                    "ru",
                    { sensitivity: "base" }
                )
            )
            .forEach(option => dropdown.appendChild(option));
    };

    const renderTag = (tag) => {
        const tagBlock = document.createElement("div");
        tagBlock.className = "test-info-edit__tag-block";
        tagBlock.dataset.tagId = tag.id;

        tagBlock.innerHTML = `
            <span class="test-info-edit__tags-text span-text">
                ${tag.name}
            </span>
            <span class="test-info-edit__tag-remove" title="Удалить">×</span>
        `;

        tagsContainer.appendChild(tagBlock);
        updateAddButton();
    };

    const post = async (url, data) => {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRF(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams(data),
        });

        return safeJsonFetch(response);
    };

    addBtn.addEventListener("click", (e) => {
        e.stopPropagation();

        dropdown.style.top =
            addBtn.offsetTop + addBtn.offsetHeight + 6 + "px";

        dropdown.style.left =
            addBtn.offsetLeft + addBtn.offsetWidth + 6 + "px";

        sortDropdown();
        dropdown.classList.toggle("active");
    });

    dropdown.addEventListener("click", async (e) => {
        const option = e.target.closest(".test-info-edit__tag-option");
        if (!option || option.classList.contains("hidden")) return;

        clearError();

        if (getTagCount() >= maxTags) {
            showError(`Максимум ${maxTags} тегов`);
            return;
        }

        const tagId = option.dataset.tagId;

        if (isTagExists(tagId)) {
            showError("Тег повторяется");
            return;
        }

        try {
            const response = await post(addTagUrl, { tag_id: tagId });

            renderTag(response.data);
            hideDropdownTag(tagId);
            dropdown.classList.remove("active");

        } catch (err) {
            handleRequestError(err);
        }
    });

    tagsContainer.addEventListener("click", async (e) => {
        const removeBtn = e.target.closest(".test-info-edit__tag-remove");
        if (!removeBtn) return;

        clearError();

        const tagBlock = removeBtn.closest(".test-info-edit__tag-block");
        const tagId = tagBlock.dataset.tagId;
        const tagName = tagBlock.querySelector(
            ".test-info-edit__tags-text"
        ).textContent.trim();

        try {
            const data = await post(removeTagUrl, {
                test_id: testId,
                tag_id: tagId
            });

            tagBlock.remove();
            showDropdownTag(tagId, tagName);
            updateAddButton();

        } catch (err) {
            btn.disabled = false;
            handleRequestError(err);
        }
    });

    document.addEventListener("click", (e) => {
        if (!wrapper.contains(e.target)) {
            dropdown.classList.remove("active");
        }
    });

    document
        .querySelectorAll(".test-info-edit__tag-block")
        .forEach(tag => hideDropdownTag(tag.dataset.tagId));

    sortDropdown();
    updateAddButton();
});


document.addEventListener('change', function (e) {
    if (e.target.classList.contains('questions-edit__type-selector')) {
        const select = e.target;
        const questionId = select.dataset.questionId;
        const updateUrl = select.dataset.updateUrl;
        const newType = select.value;

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const formData = new FormData();
        formData.append('type', newType);

        fetch(updateUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData
        })
        .then(safeJsonFetch)
        .catch(handleRequestError);
    }
});


document.addEventListener('input', function (e) {

    if (!e.target.classList.contains('questions-edit__title-textarea')) return;

    const textarea = e.target;
    const questionId = textarea.dataset.questionId;
    const updateUrl = textarea.dataset.updateUrl;

    const displayInput = document.querySelector(
        `.questions-edit__title-input[data-question-id="${questionId}"]`
    );

    if (displayInput) {
        displayInput.value = textarea.value;
    }

    const value = textarea.value.trim();

    if (value === '') {
        textarea.classList.add('error-border');
        return;
    }

    textarea.classList.remove('error-border');

    clearTimeout(textarea._saveTimer);

    textarea._saveTimer = setTimeout(() => {

        fetch(updateUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]')?.value
            },
            body: new URLSearchParams({
                text: value
            })
        })
        .then(safeJsonFetch)
        .then(() => {
            textarea.classList.add('success-border');
            setTimeout(() => {
                textarea.classList.remove('success-border');
            }, 2000);
        })
        .catch(err => {
            textarea.classList.add('error-border');
            handleRequestError(err);
        });

    }, 1500);

});


document.addEventListener("click", function (e) {
    if (!e.target.classList.contains("questions-edit__add-image-btn")) return;

    const questionBlock = e.target.closest(".questions-edit__question-block");
    const fileInput = questionBlock.querySelector(".image-input");
    fileInput.click();
});


document.addEventListener("change", function (e) {
    if (!e.target.classList.contains("image-input")) return;

    const input = e.target;
    const questionBlock = input.closest(".questions-edit__question-block");
    const container = questionBlock.querySelector(".questions-edit__question-image-container");

    const questionId = input.dataset.questionId;
    const file = input.files[0];
    if (!file) return;

    const uploadUrl = container.dataset.uploadUrl;
    const deleteUrl = container.dataset.deleteUrl;

    const formData = new FormData();
    formData.append("image", file);

    fetch(uploadUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
        },
        body: formData
    })
    .then(safeJsonFetch)
    .then(data => {
        const imageUrl = data.data.image_url;

        container.innerHTML = `
            <button class="questions-edit__delete-image-btn span-answer-input"
                    type="button"
                    data-question-id="${questionId}"
                    data-delete-url="${deleteUrl}">
                Удалить картинку
            </button>
            <img src="${imageUrl}"
                 class="questions-edit__question-image">
        `;
    })
    .catch(handleRequestError);
});


document.addEventListener("click", function (e) {
    if (!e.target.classList.contains("questions-edit__delete-image-btn")) return;

    const btn = e.target;
    const questionBlock = btn.closest(".questions-edit__question-block");
    const container = questionBlock.querySelector(".questions-edit__question-image-container");

    const questionId = btn.dataset.questionId;
    const deleteUrl = container.dataset.deleteUrl;

    const formData = new FormData();

    fetch(deleteUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
        },
        body: formData
    })
    .then(safeJsonFetch)
    .then(() => {

        container.innerHTML = `
            <input type="file"
                   class="image-input"
                   data-question-id="${questionId}"
                   style="display:none;">
            <button class="questions-edit__add-image-btn span-answer-input"
                    type="button">
                Добавить картинку
            </button>
        `;
    })
    .catch(handleRequestError);
});


document.addEventListener("click", function (e) {

    const header = e.target.closest(".questions-edit__question-block-header");
    if (!header) return;

    const block = header.closest(".questions-edit__question-block");

    if (activeQuestionBlock === block) {
        closeDetails(block);
        activeQuestionBlock = null;
        return;
    }

    if (activeQuestionBlock) {
        closeDetails(activeQuestionBlock);
    }

    openDetails(block);
    activeQuestionBlock = block;
});


document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('publishForm');
    const publishBtn = document.getElementById('publishBtn');
    const statusText = document.querySelector('.test-info-edit__status-txt');
    const errorContainer = document.querySelector('.test-info-edit__status-errors');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const testEditBlock = document.querySelector('.test-edit');

    if (!form || !publishBtn || !testEditBlock) return;

    const publishUrl = form.dataset.publishUrl;
    const unpublishUrl = form.dataset.unpublishUrl;

    const modal = document.getElementById('unpublishModal');
    const confirmBtn = document.getElementById('confirmUnpublish');
    const cancelBtn = document.getElementById('cancelUnpublish');

    let pendingSubmit = null;

    function showErrors(errors) {
        if (!errorContainer) return;

        errorContainer.innerHTML = '';

        errors.forEach(err => {
            const p = document.createElement('p');
            p.textContent = err;
            p.style.color = 'red';
            errorContainer.appendChild(p);
        });
    }

    function clearErrors() {
        if (!errorContainer) return;
        errorContainer.innerHTML = '';
    }

    function toggleInputs(enable) {

        testEditBlock.querySelectorAll('textarea').forEach(el => {
            el.readOnly = !enable;
        });

        testEditBlock.querySelectorAll('input').forEach(el => {

            if (el === publishBtn) return;

            if (el.type === 'checkbox') {
                el.disabled = !enable;
            } else {
                el.readOnly = !enable;
            }

        });

        testEditBlock.querySelectorAll('select').forEach(el => {
            el.disabled = !enable;
        });

        testEditBlock.querySelectorAll('button').forEach(el => {
            if (el === publishBtn) return;
            el.disabled = !enable;
        });

    }

    toggleInputs(testEditBlock.dataset.status !== 'published');

    publishBtn.textContent =
        testEditBlock.dataset.status === 'published'
        ? 'Редактировать'
        : 'Опубликовать';

    async function handlePublish() {

        const isPublished = testEditBlock.dataset.status === 'published';
        const url = isPublished ? unpublishUrl : publishUrl;

        try {

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await safeJsonFetch(response);
            testEditBlock.dataset.status =
                isPublished ? 'unpublished' : 'published';

            statusText.textContent = 'Статус: ' + data.data.status;

            publishBtn.textContent =
                isPublished ? 'Опубликовать' : 'Редактировать';

            toggleInputs(isPublished);

        } catch (err) {
            handleRequestError(err);
        }

    }

    form.addEventListener('submit', async function(e) {

        e.preventDefault();
        clearErrors();

        const isPublished = testEditBlock.dataset.status === 'published';

        if (isPublished) {

            modal.classList.add('active');

            pendingSubmit = async () => {
                modal.classList.remove('active');
                await handlePublish();
            };

            return;

        }

        await handlePublish();

    });

    if (confirmBtn) {
        confirmBtn.addEventListener('click', () => {
            if (pendingSubmit) pendingSubmit();
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
            modal.classList.remove('active');
        });
    }

});


function validateQuestionBlock(questionBlock) {
    const textarea = questionBlock.querySelector('.questions-edit__title-textarea');
    const typeSelect = questionBlock.querySelector('.questions-edit__type-selector');
    const answers = questionBlock.querySelectorAll('.questions-edit__answer-block');
    const correctAnswers = questionBlock.querySelectorAll(
        '.questions-edit__answer-flag:checked'
    );

    const text = textarea ? textarea.value.trim() : '';
    const type = typeSelect ? typeSelect.value : null;

    const totalAnswers = answers.length;
    const correctCount = correctAnswers.length;

    let isValid = true;

    if (!text) isValid = false;

    if (type === 'TF') {
        if (totalAnswers < 1) isValid = false;
    } else {
        if (totalAnswers < 2) isValid = false;
    }
    if (type === 'SC') {
        if (correctCount !== 1) isValid = false;
    }

    if (type === 'MC' || type === 'TF') {
        if (correctCount === 0) isValid = false;
    }

    questionBlock.classList.toggle(
        'questions-edit__question-block--invalid',
        !isValid
    );

    const panelText = questionBlock.querySelector('.questions-edit__panel-text');
    if (panelText) {
        if (!isValid) {
            panelText.style.color = 'orange';
            panelText.textContent = '!';
        } else {
            panelText.style.color = '';
            panelText.textContent = '';
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document
        .querySelectorAll('.questions-edit__question-block')
        .forEach(block => validateQuestionBlock(block));
});

document.addEventListener('input', function (e) {
    const block = e.target.closest('.questions-edit__question-block');
    if (block) validateQuestionBlock(block);
});

document.addEventListener('change', function (e) {
    const block = e.target.closest('.questions-edit__question-block');
    if (block) validateQuestionBlock(block);
});


document.addEventListener('click', async function (e) {

    if (!e.target.classList.contains('questions-edit__answer-delete')) return;

    const btn = e.target;
    const answerBlock = btn.closest('.questions-edit__answer-block');
    const container = btn.closest('.questions-edit__answers-list');

    const deleteUrl = answerBlock.dataset.deleteUrl;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    if (!deleteUrl) return;

    try {
        const response = await fetch(deleteUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams()
        });

        await safeJsonFetch(response);

        answerBlock.remove();

        container.querySelectorAll('.questions-edit__answer-number')
            .forEach((el, index) => {
                el.textContent = (index + 1) + '.';
            });

        const questionBlock = container.closest('.questions-edit__question-block');
        if (questionBlock) validateQuestionBlock(questionBlock);

        } catch (err) {
            handleRequestError(err);
        }
});


document.addEventListener('click', async function (e) {

    if (!e.target.classList.contains('questions-edit__delete-question-btn')) return;

    const btn = e.target;
    const questionId = btn.dataset.questionId;
    const deleteUrl = btn.dataset.deleteUrl;

    const questionBlock = btn.closest('.questions-edit__question-block');
    const questionsList = questionBlock.parentElement;

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    if (!deleteUrl || !questionId) return;

    btn.disabled = true;

    try {
        const response = await fetch(deleteUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams({
                question_id: questionId
            })
        });

        await safeJsonFetch(response);
        const height = questionBlock.offsetHeight + 'px';
        questionBlock.style.height = height;
        questionBlock.offsetHeight;

        questionBlock.style.transition = 'all 0.25s cubic-bezier(.4,0,.2,1)';
        questionBlock.style.opacity = '0';
        questionBlock.style.transform = 'translateX(-10px)';
        questionBlock.style.height = '0';
        questionBlock.style.margin = '0';
        questionBlock.style.padding = '0';

        requestAnimationFrame(() => {
            setTimeout(() => {
                questionBlock.remove();
                questionsList.querySelectorAll('.questions-edit__question-number')
                    .forEach((el, index) => {
                        el.textContent = (index + 1) + '.';
                    });
            }, 250);
        });

    } catch (err) {
        btn.disabled = false;
        handleRequestError(err);
    }

});