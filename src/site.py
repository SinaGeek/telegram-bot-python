#!/usr/bin/env python3
"""
Web server for Google OAuth authentication
"""

import os
import json
import logging
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from config import *

# Configure logging
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# OAuth configuration
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRETS_FILE = 'client_secrets.json'
REDIRECT_URI = 'http://localhost:8080/callback'

# Store user credentials (in production, use a database)
user_credentials = {}


def get_flow():
    """Get OAuth flow configuration"""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    return flow


@app.route('/')
def index():
    """Main page"""
    return render_template('Index.html')


@app.route('/login')
def login():
    """Initiate Google OAuth login"""
    try:
        flow = get_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        session['state'] = state
        return redirect(authorization_url)
    except Exception as e:
        logger.error(f"Login error: {e}")
        return render_template('notfound.html', error=str(e))


@app.route('/callback')
def callback():
    """Handle OAuth callback"""
    try:
        flow = get_flow()
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials
        user_id = request.args.get('user_id', 'default')

        # Store credentials
        user_credentials[user_id] = credentials

        # Save to file for persistence
        token_file = f"token_{user_id}.json"
        with open(token_file, 'w') as f:
            f.write(credentials.to_json())

        return render_template('googlesignIn.html',
                               success=True,
                               user_id=user_id)
    except Exception as e:
        logger.error(f"Callback error: {e}")
        return render_template('googlesignIn.html',
                               success=False,
                               error=str(e))


@app.route('/auth/<user_id>')
def auth_user(user_id):
    """Get auth URL for specific user"""
    try:
        flow = get_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=user_id
        )
        session['state'] = state
        return jsonify({
            'success': True,
            'auth_url': authorization_url
        })
    except Exception as e:
        logger.error(f"Auth URL error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/credentials/<user_id>')
def get_credentials(user_id):
    """Get user credentials"""
    if user_id in user_credentials:
        return jsonify({
            'success': True,
            'credentials': user_credentials[user_id].to_json()
        })
    else:
        # Try to load from file
        token_file = f"token_{user_id}.json"
        if os.path.exists(token_file):
            try:
                with open(token_file, 'r') as f:
                    creds_data = json.load(f)
                credentials = Credentials.from_authorized_user_info(creds_data)

                # Refresh if needed
                if credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                    user_credentials[user_id] = credentials
                    with open(token_file, 'w') as f:
                        f.write(credentials.to_json())

                return jsonify({
                    'success': True,
                    'credentials': credentials.to_json()
                })
            except Exception as e:
                logger.error(f"Error loading credentials: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        else:
            return jsonify({
                'success': False,
                'error': 'No credentials found'
            })


@app.route('/revoke/<user_id>')
def revoke_credentials(user_id):
    """Revoke user credentials"""
    try:
        if user_id in user_credentials:
            credentials = user_credentials[user_id]
            credentials.revoke(Request())
            del user_credentials[user_id]

        # Remove token file
        token_file = f"token_{user_id}.json"
        if os.path.exists(token_file):
            os.remove(token_file)

        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Revoke error: {e}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/policy')
def policy():
    """Privacy policy page"""
    return render_template('policy.html')


@app.route('/terms')
def terms():
    """Terms of service page"""
    return render_template('terms.html')


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('notfound.html'), 404


def start_web_server():
    """Start the web server"""
    app.run(host='0.0.0.0', port=8080, debug=False)
