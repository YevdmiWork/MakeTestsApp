document.addEventListener("DOMContentLoaded", function () {
    const select = document.querySelector(".panel__custom-select");
    const selectDefault = select.querySelector(".panel__custom-default-select");
    const selectItems = select.querySelector(".panel__select-items");
    const selectText = select.querySelector(".tests-panel__custom-select-text");
    const hiddenSortValue = document.getElementById("sort-value");
    const sortForm = document.getElementById("sort-form");

    selectDefault.addEventListener("click", function (e) {
        e.stopPropagation();
        selectItems.classList.toggle("tests-panel__select-hide");
    });

    selectItems.querySelectorAll(".panel__custom-select-item").forEach(item => {
        item.addEventListener("click", function () {
            const value = this.getAttribute("data-value");
            const text = this.innerText.trim();
            selectText.textContent = text;
            hiddenSortValue.value = value;
            selectItems.classList.add("tests-panel__select-hide");
            sortForm.submit();
        });
    });

    document.addEventListener("click", function (e) {
        if (!select.contains(e.target)) {
            selectItems.classList.add("tests-panel__select-hide");
        }
    });
});