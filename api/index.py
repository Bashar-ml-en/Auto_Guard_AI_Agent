"""Vercel Serverless Function entry point for AutoGuard AI."""
import sys
import os

# Add root directory to sys.path for module resolution on Vercel
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.main import app

# Vercel serverless ASGI handler
