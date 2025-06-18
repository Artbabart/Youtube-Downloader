function downloadVideo() {
    const url = document.getElementById('url').value;
    const status = document.getElementById('status');
    status.innerText = "Downloading...";

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url })
    })
    .then(res => res.json())
    .then(data => {
        status.innerText = data.message || data.error;
    })
    .catch(err => {
        status.innerText = "Error: " + err.message;
    });
}
