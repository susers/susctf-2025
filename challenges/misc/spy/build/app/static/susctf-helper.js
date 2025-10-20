export function caculateProof(answer, token, progressCallback, rateCallback) {
    return new Promise((resolve, reject) => {
        const worker = new Worker("/static/susctf-pow-worker.js", { type: "module" })

        worker.onmessage = function (event) {
            const { type, value } = event.data
            if (type === "progress") {
                progressCallback && progressCallback(value)
            } else if (type === "rate") {
                rateCallback && rateCallback(value)
            } else if (type === "result") {
                progressCallback && progressCallback(-1)
                resolve(value)
                worker.terminate()
            }
        }

        worker.onerror = function (event) {
            progressCallback && progressCallback(-1)
            reject(event)
            worker.terminate()
        }

        worker.postMessage({ answer, token })
        progressCallback && progressCallback(0)
    })
}

export function submitAnswer(answer, proof, token) {
    return fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ answer, proof, token })
    }).then(res => res.json())
}

export function randomUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
        return v.toString(16);
    });
}