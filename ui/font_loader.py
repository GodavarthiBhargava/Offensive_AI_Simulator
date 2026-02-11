import os

class FontLoader:
    """Utility class to load and manage custom fonts"""
    
    @staticmethod
    def get_font(size=12, weight="normal"):
        """Get Consolas font"""
        return ("Consolas", size, weight)
    
    @staticmethod
    def get_font_tuple(size=12, weight="normal"):
        """Returns font as tuple for tkinter widgets"""
        return FontLoader.get_font(size, weight)
