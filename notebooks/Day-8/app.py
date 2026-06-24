from flask import Flask, request, render_template_string

app = Flask(__name__)

template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multiply Numbers App</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        body {
            background: linear-gradient(135deg, #667eea, #764ba2);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            width: 100%;
            max-width: 500px;
            padding: 35px;
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 10px;
        }

        p {
            color: #666;
            margin-bottom: 20px;
            font-size: 15px;
        }

        .input-box {
            width: 100%;
            padding: 14px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            margin-bottom: 15px;
            outline: none;
            transition: 0.3s;
        }

        .input-box:focus {
            border-color: #667eea;
            box-shadow: 0 0 8px rgba(102, 126, 234, 0.3);
        }

        .btn {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.3s;
        }

        .btn:hover {
            transform: translateY(-2px);
            opacity: 0.95;
        }

        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 12px;
            background: #f3f4f6;
            color: #222;
            font-size: 18px;
            font-weight: bold;
        }

        .error {
            margin-top: 20px;
            padding: 15px;
            border-radius: 12px;
            background: #ffe5e5;
            color: #d90429;
            font-size: 16px;
            font-weight: bold;
        }

        .example {
            margin-top: 15px;
            color: #777;
            font-size: 14px;
        }

        .footer {
            margin-top: 20px;
            font-size: 13px;
            color: #999;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Multiply Any Numbers</h1>
        <p>Enter numbers separated by commas to multiply them together.</p>

        <form method="POST">
            <input
                type="text"
                name="numbers"
                class="input-box"
                placeholder="Example: 2, 3, 4, 5"
                value="{{ numbers }}"
                required
            >
            <button type="submit" class="btn">Multiply</button>
        </form>

        {% if result is not none %}
            <div class="result">
                Result = {{ result }}
            </div>
        {% endif %}

        {% if error %}
            <div class="error">
                {{ error }}
            </div>
        {% endif %}

        <div class="example">
            Example input: <b>2, 3, 4</b> → Output: <b>24</b>
        </div>

        <div class="footer">
            Flask Multiplication App
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    numbers = ""

    if request.method == "POST":
        numbers = request.form.get("numbers", "").strip()

        try:
            num_list = [float(num.strip()) for num in numbers.split(",") if num.strip()]

            if not num_list:
                error = "Please enter at least one number."
            else:
                result = 1
                for num in num_list:
                    result *= num

                # If result is a whole number, show it as int
                if result.is_integer():
                    result = int(result)

        except ValueError:
            error = "Invalid input! Please enter numbers only, separated by commas."

    return render_template_string(
        template,
        result=result,
        error=error,
        numbers=numbers
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)