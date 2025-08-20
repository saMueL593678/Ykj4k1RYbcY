# 代码生成时间: 2025-08-21 06:58:54
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Theme Switcher Service using Falcon framework
"""

from falcon import API, Request, Response
from falcon import HTTP_200, HTTP_400, HTTP_404, HTTP_500
from falcon.media.validators import json_validator
import json

class ThemeManager:
    """
    Class responsible for managing the theme of the application.
    It stores the current theme and provides methods to switch themes.
    """
    def __init__(self):
        self.current_theme = 'light'  # Default theme

    def switch_theme(self, new_theme):
        """
        Switches the theme to the new theme provided.
        
        Args:
        new_theme (str): The new theme to switch to.
        
        Returns:
        bool: True if the theme was switched successfully, False otherwise.
        """
        if new_theme in ['light', 'dark']:
            self.current_theme = new_theme
            return True
        return False

    def get_current_theme(self):
        """
        Returns the current theme.
        
        Returns:
        str: The current theme.
        """
        return self.current_theme

class ThemeResource:
    """
    Resource class for handling theme switching requests.
    """
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager

    def on_get(self, req, resp):
        """
        Handles GET requests to retrieve the current theme.
        """
        try:
            current_theme = self.theme_manager.get_current_theme()
            resp.media = {'theme': current_theme}
            resp.status = HTTP_200
        except Exception as e:
            resp.media = {'error': str(e)}
            resp.status = HTTP_500

    def on_post(self, req, resp):
        """
        Handles POST requests to switch the theme.
        """
        try:
            if not json_validator.validate(req.media):
                raise ValueError('Invalid JSON')
            new_theme = req.media.get('theme')
            if new_theme is None:
                raise ValueError('No theme provided')
            if not self.theme_manager.switch_theme(new_theme):
                raise ValueError('Invalid theme provided')
            resp.media = {'theme': self.theme_manager.get_current_theme()}
            resp.status = HTTP_200
        except ValueError as ve:
            resp.media = {'error': str(ve)}
            resp.status = HTTP_400
        except Exception as e:
            resp.media = {'error': str(e)}
            resp.status = HTTP_500

# Create an instance of the ThemeManager
theme_manager = ThemeManager()

# Create the Falcon API app
app = API()

# Add the ThemeResource to the app
theme_resource = ThemeResource(theme_manager)
app.add_route('/theme', theme_resource, suffix='re')
