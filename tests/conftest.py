import sys
import os

# Add the project root directory to sys.path
# This allows tests to import modules from 'src' as 'from src.connectors...'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
