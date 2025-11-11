document.addEventListener('DOMContentLoaded', function () {
  const table = document.querySelector('.profile__table');
  const headers = Array.from(table.querySelectorAll('th[data-sort]'));
  let currentSort = { column: null, order: 'asc' };

  headers.forEach((header, headerIndex) => {
    header.addEventListener('click', function () {
      const column = header.getAttribute('data-sort');
      const rows = Array.from(table.querySelectorAll('tbody tr'));
      const newOrder = currentSort.column === column && currentSort.order === 'asc' ? 'desc' : 'asc';
      currentSort = { column, order: newOrder };

      const statusOrder = [
        'unpublished', 'published',
        'не опубликовано', 'опубликовано'
      ];

      rows.sort((a, b) => {
        const aCell = a.querySelector(`td:nth-child(${headerIndex + 1})`);
        const bCell = b.querySelector(`td:nth-child(${headerIndex + 1})`);
        const aText = aCell ? aCell.textContent.trim() : '';
        const bText = bCell ? bCell.textContent.trim() : '';

        const aVal = (aCell && (aCell.dataset.status || aCell.dataset.value)) || aText;
        const bVal = (bCell && (bCell.dataset.status || bCell.dataset.value)) || bText;

        let comparison = 0;

        if (column === 'time_create') {
          const aDate = parseDate(aText);
          const bDate = parseDate(bText);
          comparison = aDate - bDate;
        } else if (column === 'rating' || column === 'completion') {
          const aNum = parseInt(aVal.replace(/\D/g, '') || '0', 10);
          const bNum = parseInt(bVal.replace(/\D/g, '') || '0', 10);
          comparison = aNum - bNum;
        } else if (column === 'status') {
          const aKey = String(aVal).toLowerCase();
          const bKey = String(bVal).toLowerCase();
          const ia = statusOrder.indexOf(aKey);
          const ib = statusOrder.indexOf(bKey);
          if (ia !== -1 && ib !== -1) {
            comparison = ia - ib;
          } else if (ia !== -1) {
            comparison = -1;
          } else if (ib !== -1) {
            comparison = 1;
          } else {
            comparison = aKey.localeCompare(bKey);
          }
        } else {
          comparison = String(aVal).localeCompare(String(bVal), undefined, { numeric: true, sensitivity: 'base' });
        }

        return newOrder === 'asc' ? comparison : -comparison;
      });

      const tbody = table.querySelector('tbody');
      rows.forEach(row => tbody.appendChild(row));
      updateSortIndicators();
    });
  });

  function parseDate(dateString) {
    if (!dateString) return 0;
    const [day, month, year] = dateString.split('.').map(num => parseInt(num, 10));
    return new Date(year, month - 1, day).getTime();
  }

  function updateSortIndicators() {
    headers.forEach(header => {
      header.classList.remove('asc', 'desc');
      const column = header.getAttribute('data-sort');
      if (currentSort.column === column) {
        header.classList.add(currentSort.order);
      }
    });
  }
});