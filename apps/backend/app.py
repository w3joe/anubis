import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

from anubis.code_generator import CodeGenerator
from anubis.code_evaluator import CodeEvaluator
from anubis.output_formatter import OutputFormatter

app = Flask(__name__)
CORS(app)

# Initialize the Gemini client
client = genai.Client(api_key=os.environ.get('GOOGLE_API_KEY'))

# Initialize Anubis components
code_generator = None
code_evaluator = None

def init_anubis():
    """Initialize Anubis components lazily."""
    global code_generator, code_evaluator
    if code_generator is None:
        code_generator = CodeGenerator()
    if code_evaluator is None:
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        code_evaluator = CodeEvaluator(config_path if os.path.exists(config_path) else None)


@app.route('/')
def hello_world():
    return {'message': 'Hello from Anubis Backend!'}


@app.route('/health')
def health_check():
    return {'status': 'healthy'}


@app.route('/api/gemini/generate', methods=['POST'])
def gemini_generate():
    """
    Generate text using Google Gemini API

    Expected JSON body:
    {
        "prompt": "Your prompt here",
        "model": "gemini-2.0-flash-exp" (optional, defaults to gemini-2.0-flash-exp)
    }
    """
    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt in request body'}), 400

        prompt = data['prompt']
        model = data.get('model', 'gemini-2.0-flash-exp')

        # Generate content using Gemini
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        return jsonify({
            'success': True,
            'response': response.text,
            'model': model
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/gemini/chat', methods=['POST'])
def gemini_chat():
    """
    Chat with Google Gemini API

    Expected JSON body:
    {
        "messages": [
            {"role": "user", "content": "Hello"},
            {"role": "model", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"}
        ],
        "model": "gemini-2.0-flash-exp" (optional)
    }
    """
    try:
        data = request.get_json()

        if not data or 'messages' not in data:
            return jsonify({'error': 'Missing messages in request body'}), 400

        messages = data['messages']
        model = data.get('model', 'gemini-2.0-flash-exp')

        # Convert messages to Gemini format
        contents = []
        for msg in messages:
            contents.append(types.Content(
                role=msg.get('role', 'user'),
                parts=[types.Part(text=msg['content'])]
            ))

        # Generate chat response
        response = client.models.generate_content(
            model=model,
            contents=contents
        )

        return jsonify({
            'success': True,
            'response': response.text,
            'model': model
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/v1/evaluate', methods=['POST'])
def evaluate_code():
    """
    Main Anubis endpoint: Compare and evaluate code generation across multiple AI models.

    Expected JSON body:
    {
        "prompt": "Write a function to find the longest palindromic substring",
        "models": ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash"],
        "metrics": ["readability", "consistency", "time_complexity", "code_documentation", "external_dependencies"] (optional)
    }

    The metrics array defines the priority order for evaluation. Higher-ranked metrics get higher weights.
    If not provided, uses default equal weights.

    Returns evaluation results according to SRS specification.
    """
    try:
        init_anubis()

        data = request.get_json()

        # Validate input (FR-3, FR-4)
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt in request body'}), 400

        if not data.get('prompt', '').strip():
            return jsonify({'error': 'Prompt cannot be empty'}), 400

        if 'models' not in data or not data['models']:
            return jsonify({'error': 'At least one model must be specified'}), 400

        prompt = data['prompt']
        models = data['models']
        metrics_priority = data.get('metrics', None)

        # Step 1: Generate code from all models with weighted metrics instruction (FR-5, FR-6, FR-7, FR-8)
        generation_results = code_generator.generate_code_multi_models(prompt, models, metrics_priority)

        # Step 2: Evaluate generated code with weighted scoring (FR-9 through FR-14)
        evaluations = []
        for gen_result in generation_results:
            if gen_result['success']:
                code = gen_result['generated_code']
                evaluation = code_evaluator.evaluate(code, metrics_priority)
                evaluation['model'] = gen_result['model']
                evaluations.append(evaluation)
            else:
                # Handle failed generation (NFR-4)
                evaluations.append({
                    'model': gen_result['model'],
                    'overall_score': 0,
                    'metrics': {},
                    'error': gen_result['error']
                })

        # Step 3: Format output (FR-15 through FR-19)
        output = OutputFormatter.format_results(prompt, evaluations, generation_results)

        return jsonify(output), 200

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='localhost', port=port)
