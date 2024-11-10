document.getElementById('searchInput').addEventListener('keyup', function () {
    const filter = this.value.toUpperCase();
    const table = document.querySelector('.skyline-table'); // Select the skyline table by class
    const rows = table.getElementsByTagName('tr');

    // Loop through all table rows (skip the header row)
    for (let i = 1; i < rows.length; i++) {
        const nameCell = rows[i].getElementsByTagName('td')[3]; // Adjust index if Name column is not the 4th column
        if (nameCell) {
            const nameText = nameCell.textContent || nameCell.innerText;
            // Show or hide row based on filter match
            rows[i].style.display = nameText.toUpperCase().includes(filter) ? '' : 'none';
        }
    }
});