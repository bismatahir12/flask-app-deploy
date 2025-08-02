
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Keyword Extractor</title>
    <link rel="icon" type="image/png" href="{{ url_for('static', filename='favicon.png') }}">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 40px;
            background-color: #f4f4f4;
            color: #333;
        }

        .container {
            max-width: 800px;
            margin: auto;
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #2c3e50;
            text-align: center;
        }

        textarea {
            width: 100%;
            height: 150px;
            padding: 12px;
            font-size: 16px;
            margin-top: 20px;
            border: 1px solid #ccc;
            border-radius: 6px;
            resize: vertical;
        }

        button {
            margin-top: 20px;
            padding: 12px 24px;
            font-size: 16px;
            background-color: #2c3e50;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }

        button:hover {
            background-color: #34495e;
        }

        #result {
            margin-top: 30px;
            background: #fdfdfd;
            padding: 20px;
            border-left: 5px solid #2c3e50;
            border-radius: 4px;
        }

        .error {
            color: red;
            font-weight: bold;
        }

        .keywords {
            margin-top: 10px;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Keyword Extractor</h1>
        <form id="keywordForm">
            <label for="textInput">Enter your text below:</label>
            <textarea id="textInput" placeholder="e.g., Social media platforms like Twitter and Instagram..."></textarea>
            <button type="submit">Extract Keywords</button>
        </form>
        <div id="result"></div>
    </div>

    <script>
        const form = document.getElementById('keywordForm');
        const resultDiv = document.getElementById('result');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            resultDiv.innerHTML = '';  // Clear previous result

            const text = document.getElementById('textInput').value.trim();

            if (!text) {
                resultDiv.innerHTML = `<p class="error">Please enter some text to extract keywords.</p>`;
                return;
            }

            try {
                const response = await fetch('/api/v1/keywords', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text })
                });

                const data = await response.json();

                if (response.ok) {
                    resultDiv.innerHTML = `
                        <strong>Extracted Keywords:</strong>
                        <div class="keywords">${data.keywords.join(', ')}</div>
                    `;
                } else {
                    resultDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
                }
            } catch (err) {
                resultDiv.innerHTML = `<p class="error">Unexpected error occurred. Please try again later.</p>`;
                console.error(err);
            }
        });
    </script>
</body>
</html>