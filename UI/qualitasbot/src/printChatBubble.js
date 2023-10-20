function printChatBubble(message) {
    // Create a new row
    let row = document.createElement('div');
    row.className = 'row justify-content-end';

    // Create a column
    let col = document.createElement('div');
    col.className = 'col-6 text-right';

    // Create a chat bubble
    let bubble = document.createElement('div');
    bubble.className = 'p-3 mb-2 bg-secondary text-white rounded';
    bubble.textContent = message;

    // Append the bubble to the column, and the column to the row
    col.appendChild(bubble);
    row.appendChild(col);

    // Append the row to the container
    let container = document.querySelector('.container');
    container.appendChild(row);
}