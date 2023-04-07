import os

project_path = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':
    os.environ["FLASK_APP"] = 'mainapp.py'
    os.environ["FLASK_ENV"] = 'development'
    os.environ["FLASK_DEBUG"] = 'true'
    from mainapp import app

    os.environ["APP_CONFIG_FILE"] = os.path.join(project_path, 'config', 'api_config.py')
    os.environ["APPLICATION_ROOT"] = project_path
    app.run(host='0.0.0.0', debug=True, use_debugger=False, use_reloader=True, passthrough_errors=True)
