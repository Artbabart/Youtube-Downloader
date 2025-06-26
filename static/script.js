function downloadVideo() {
    const url = document.getElementById('url').value.trim();
    const status = document.getElementById('status');

    if (!url) {
        status.innerText = "Kérlek, adj meg egy videó URL-t!";
        return;
    }

    status.innerText = "Letöltés folyamatban...";

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Letöltés sikertelen. Hibakód: ' + response.status);
        }

        const disposition = response.headers.get('Content-Disposition');
        let filename = 'video.mp4';
        if (disposition && disposition.includes('filename=')) {
            filename = disposition
                .split('filename=')[1]
                .replace(/['"]/g, '')
                .trim();
        }

        return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => {
        const blobUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(blobUrl);

        status.innerText = "Sikeres letöltés: " + filename;
    })
    .catch(err => {
        console.error("Letöltési hiba:", err);
        status.innerText = "Hiba: " + err.message;
    });
}
