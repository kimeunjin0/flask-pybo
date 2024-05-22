import os

# Define the directory structure and file contents
project_structure = {
    "my_mbti_pwa/": {
        "app.py": """from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
""",
        "static/": {
            "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="manifest" href="/manifest.json">
    <link rel="stylesheet" href="/styles.css">
    <title>MBTI PWA</title>
</head>
<body>
    <h1>MBTI 유형 선택</h1>
    <select id="mbti-select">
        <option value="">--MBTI 유형 선택--</option>
        <option value="INTJ">INTJ</option>
        <option value="INTP">INTP</option>
        <option value="ENTJ">ENTJ</option>
        <option value="ENTP">ENTP</option>
        <option value="INFJ">INFJ</option>
        <option value="INFP">INFP</option>
        <option value="ENFJ">ENFJ</option>
        <option value="ENFP">ENFP</option>
        <option value="ISTJ">ISTJ</option>
        <option value="ISFJ">ISFJ</option>
        <option value="ESTJ">ESTJ</option>
        <option value="ESFJ">ESFJ</option>
        <option value="ISTP">ISTP</option>
        <option value="ISFP">ISFP</option>
        <option value="ESTP">ESTP</option>
        <option value="ESFP">ESFP</option>
    </select>
    <p id="mbti-description">MBTI 유형을 선택해주세요.</p>
    <img id="mbti-image" src="" alt="" style="display:none; width: 200px; height: 200px;"/>
    <script src="/main.js"></script>
</body>
</html>
""",
            "main.js": """document.addEventListener('DOMContentLoaded', () => {
    const mbtiSelect = document.getElementById('mbti-select');
    const mbtiDescription = document.getElementById('mbti-description');
    const mbtiImage = document.getElementById('mbti-image');

    mbtiSelect.addEventListener('change', async () => {
        const selectedType = mbtiSelect.value;
        if (selectedType) {
            const response = await fetch('/mbti_data.json');
            const data = await response.json();
            mbtiDescription.textContent = data[selectedType].description;
            mbtiImage.src = data[selectedType].image;
            mbtiImage.style.display = 'block';
        } else {
            mbtiDescription.textContent = 'MBTI 유형을 선택해주세요.';
            mbtiImage.style.display = 'none';
        }
    });

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js')
            .then(registration => {
                console.log('Service Worker registered with scope:', registration.scope);
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    }
});
""",
            "service-worker.js": """self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('my-cache').then(cache => {
            return cache.addAll([
                '/',
                '/index.html',
                '/styles.css',
                '/main.js',
                '/mbti_data.json',
                '/manifest.json',
                '/images/INTJ.jpg',
                '/images/INTP.jpg',
                '/images/ENTJ.jpg',
                '/images/ENTP.jpg',
                '/images/INFJ.jpg',
                '/images/INFP.jpg',
                '/images/ENFJ.jpg',
                '/images/ENFP.jpg',
                '/images/ISTJ.jpg',
                '/images/ISFJ.jpg',
                '/images/ESTJ.jpg',
                '/images/ESFJ.jpg',
                '/images/ISTP.jpg',
                '/images/ISFP.jpg',
                '/images/ESTP.jpg',
                '/images/ESFP.jpg'
            ]);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});
""",
            "manifest.json": """{
    "name": "MBTI PWA",
    "short_name": "MBTI",
    "start_url": "/index.html",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#000000",
    "icons": [
        {
            "src": "/icons/icon-192x192.png",
            "type": "image/png",
            "sizes": "192x192"
        },
        {
            "src": "/icons/icon-512x512.png",
            "type": "image/png",
            "sizes": "512x512"
        }
    ]
}
""",
            "styles.css": """body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    margin: 0;
    padding: 20px;
    text-align: center;
}

h1 {
    color: #333;
}

p {
    color: #666;
}

select {
    padding: 10px;
    margin-top: 20px;
    font-size: 16px;
}
""",
            "mbti_data.json": """{
    "INTJ": {
        "description": "INTJ: 전략적 사상가, 독립적이며 창의적인 해결책을 찾습니다.",
        "image": "/images/INTJ.jpg"
    },
    "INTP": {
        "description": "INTP: 논리적 사상가, 분석적이며 독창적인 해결책을 선호합니다.",
        "image": "/images/INTP.jpg"
    },
    "ENTJ": {
        "description": "ENTJ: 천부적인 지도자, 조직적이며 목표 지향적입니다.",
        "image": "/images/ENTJ.jpg"
    },
    "ENTP": {
        "description": "ENTP: 토론자, 혁신적이며 다양한 아이디어를 제시합니다.",
        "image": "/images/ENTP.jpg"
    },
    "INFJ": {
        "description": "INFJ: 옹호자, 이상주의적이며 깊은 통찰력을 가집니다.",
        "image": "/images/INFJ.jpg"
    },
    "INFP": {
        "description": "INFP: 중재자, 이상주의적이며 개인의 가치를 중시합니다.",
        "image": "/images/INFP.jpg"
    },
    "ENFJ": {
        "description": "ENFJ: 집정관, 카리스마 넘치며 사람들에게 영감을 줍니다.",
        "image": "/images/ENFJ.jpg"
    },
    "ENFP": {
        "description": "ENFP: 활동가, 열정적이며 창의적인 문제 해결을 선호합니다.",
        "image": "/images/ENFP.jpg"
    },
    "ISTJ": {
        "description": "ISTJ: 현실주의자, 책임감이 강하며 철저한 계획을 세웁니다.",
        "image": "/images/ISTJ.jpg"
    },
    "ISFJ": {
        "description": "ISFJ: 수호자, 세심하며 헌신적입니다.",
        "image": "/images/ISFJ.jpg"
    },
    "ESTJ": {
        "description": "ESTJ: 경영자, 조직적이며 효율성을 중시합니다.",
        "image": "/images/ESTJ.jpg"
    },
    "ESFJ": {
        "description": "ESFJ: 집정관, 사교적이며 타인의 필요에 민감합니다.",
        "image": "/images/ESFJ.jpg"
    },
    "ISTP": {
        "description": "ISTP: 장인, 실용적이며 문제 해결에 능숙합니다.",
        "image": "/images/ISTP.jpg"
    },
    "ISFP": {
        "description": "ISFP: 모험가, 융통성 있으며 예술적입니다.",
        "image": "/images/ISFP.jpg"
    },
    "ESTP": {
        "description": "ESTP: 기업가, 활동적이며 도전에 강합니다.",
        "image": "/images/ESTP.jpg"
    },
    "ESFP": {
        "description": "ESFP: 연예인, 활기차며 타인을 즐겁게 합니다.",
        "image": "/images/ESFP.jpg"
    }
}
""",
            "images/": {
                "INTJ.jpg": "Sample image content for INTJ",
                "INTP.jpg": "Sample image content for INTP",
                "ENTJ.jpg": "Sample image content for ENTJ",
                "ENTP.jpg": "Sample image content for ENTP",
                "INFJ.jpg": "Sample image content for INFJ",
                "INFP.jpg": "Sample image content for INFP",
                "ENFJ.jpg": "Sample image content for ENFJ",
                "ENFP.jpg": "Sample image content for ENFP",
                "ISTJ.jpg": "Sample image content for ISTJ",
                "ISFJ.jpg": "Sample image content for ISFJ",
                "ESTJ.jpg": "Sample image content for ESTJ",
                "ESFJ.jpg": "Sample image content for ESFJ",
                "ISTP.jpg": "Sample image content for ISTP",
                "ISFP.jpg": "Sample image content for ISFP",
                "ESTP.jpg": "Sample image content for ESTP",
                "ESFP.jpg": "Sample image content for ESFP"
            }
        }
    }
}

# Create project structure and write files
def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_project_structure(path, content)
        else:
            with open(path, 'w') as file:
                file.write(content)

# Create project directory
project_path = '/mnt/data/my_mbti_pwa'
os.makedirs(project_path, exist_ok=True)
create_project_structure(project_path, project_structure)
