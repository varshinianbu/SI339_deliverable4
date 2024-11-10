document.getElementById('searchInput').addEventListener('keyup', function () {
    const filter = this.value.toUpperCase();
    const table = document.getElementById('athlete-table');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {  // Start from 1 to skip the header row
        const nameCell = rows[i].getElementsByTagName('td')[2];  // Adjust to the 'Name' column index
        if (nameCell) {
            const nameText = nameCell.textContent || nameCell.innerText;
            rows[i].style.display = nameText.toUpperCase().includes(filter) ? '' : 'none';
        }
    }
});