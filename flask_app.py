"""Initialize Flask app."""
from flask import Flask, render_template, url_for, redirect, current_app
#import dash
#from plotlydash.dashboard import create_dashboard
import sys

#flask_app = Flask(__name__)
#app = create_dashboard(flask_app)

#@flask_app.route('/contact/')
#def contact():
#    return "Success"

#@app.route("/")
#def home():
#    return redirect(url_for('/projects/covid-19-dashboards/'))

#if __name__ == "__main__":
#    flask_app.run_server()

#####previous####
def create_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__)
   # app.config.from_object('config.Config')

    with app.app_context():
        # Import Flask routes
#        from . import routes

        @app.route('/contact/')
        def contact():
            return "Success"

        # Import Dash application
        from FlaskApp.plotlydash.dashboard import create_dashboard
        app = create_dashboard(app)

        @app.route("/")
        def home():
            return redirect(url_for('/projects/covid-19-dashboards/'))

        return app







