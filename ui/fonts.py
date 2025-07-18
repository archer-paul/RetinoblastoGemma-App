"""
Configuration des polices modernes pour RetinoblastoGemma v6
Support des polices Google et fallbacks système
VERSION CORRIGÉE - Imports et méthodes fixés
"""
import tkinter.font as tkFont
import platform
import os
import random  # Import ajouté pour éviter les erreurs
from pathlib import Path

class FontManager:
    """Gestionnaire de polices avec fallbacks intelligents"""
    
    def __init__(self):
        self.system = platform.system()
        self.available_fonts = list(tkFont.families())
        self.google_fonts_available = False
        
        # Detect Google Fonts availability
        self._detect_google_fonts()
        
        # Configure font sets
        self.modern_fonts = self._configure_modern_fonts()
        
    def _detect_google_fonts(self):
        """Détecte si les polices Google sont disponibles"""
        google_fonts = ['Google Sans', 'Roboto', 'Inter', 'Poppins']
        
        for font in google_fonts:
            if font in self.available_fonts:
                self.google_fonts_available = True
                break
    
    def _configure_modern_fonts(self):
        """Configure les polices modernes avec fallbacks"""
        if self.google_fonts_available:
            return self._get_google_fonts()
        else:
            return self._get_system_fonts()
    
    def _get_google_fonts(self):
        """Configuration avec polices Google"""
        base_fonts = {
            'primary': 'Google Sans',
            'secondary': 'Roboto', 
            'mono': 'Roboto Mono',
            'display': 'Google Sans Display'
        }
        
        # Fallbacks si Google Sans n'est pas disponible
        if 'Google Sans' not in self.available_fonts:
            if 'Inter' in self.available_fonts:
                base_fonts['primary'] = 'Inter'
            elif 'Poppins' in self.available_fonts:
                base_fonts['primary'] = 'Poppins'
            else:
                base_fonts['primary'] = self._get_best_system_font()
        
        return {
            # Titres et headers
            'display_large': (base_fonts['display'], 48, 'bold'),
            'display': (base_fonts['display'], 36, 'normal'),
            'headline_large': (base_fonts['primary'], 32, 'bold'),
            'headline': (base_fonts['primary'], 28, 'bold'),
            'title_large': (base_fonts['primary'], 22, 'bold'),
            'title': (base_fonts['primary'], 18, 'normal'),
            
            # Corps de texte
            'label_large': (base_fonts['primary'], 16, 'normal'),
            'label': (base_fonts['primary'], 14, 'normal'),
            'body_large': (base_fonts['secondary'], 16, 'normal'),
            'body': (base_fonts['secondary'], 14, 'normal'),
            'caption': (base_fonts['secondary'], 12, 'normal'),
            'overline': (base_fonts['secondary'], 10, 'normal'),
            
            # Spécialisées
            'mono': (base_fonts['mono'], 12, 'normal'),
            'mono_small': (base_fonts['mono'], 10, 'normal'),
            'button': (base_fonts['primary'], 14, 'bold'),
            'badge': (base_fonts['primary'], 10, 'bold')
        }
    
    def _get_system_fonts(self):
        """Configuration avec polices système"""
        primary_font = self._get_best_system_font()
        mono_font = self._get_best_mono_font()
        
        return {
            # Titres et headers
            'display_large': (primary_font, 48, 'bold'),
            'display': (primary_font, 36, 'normal'),
            'headline_large': (primary_font, 32, 'bold'),
            'headline': (primary_font, 28, 'bold'),
            'title_large': (primary_font, 22, 'bold'),
            'title': (primary_font, 18, 'normal'),
            
            # Corps de texte
            'label_large': (primary_font, 16, 'normal'),
            'label': (primary_font, 14, 'normal'),
            'body_large': (primary_font, 16, 'normal'),
            'body': (primary_font, 14, 'normal'),
            'caption': (primary_font, 12, 'normal'),
            'overline': (primary_font, 10, 'normal'),
            
            # Spécialisées
            'mono': (mono_font, 12, 'normal'),
            'mono_small': (mono_font, 10, 'normal'),
            'button': (primary_font, 14, 'bold'),
            'badge': (primary_font, 10, 'bold')
        }
    
    def _get_best_system_font(self):
        """Trouve la meilleure police système disponible"""
        if self.system == "Windows":
            preferred_fonts = [
                'Segoe UI Variable Display',
                'Segoe UI Variable Text', 
                'Segoe UI',
                'Calibri',
                'Arial'
            ]
        elif self.system == "Darwin":  # macOS
            preferred_fonts = [
                'SF Pro Display',
                'SF Pro Text',
                'Helvetica Neue',
                'Helvetica',
                'Arial'
            ]
        else:  # Linux
            preferred_fonts = [
                'Ubuntu',
                'Noto Sans',
                'DejaVu Sans',
                'Liberation Sans',
                'Arial'
            ]
        
        for font in preferred_fonts:
            if font in self.available_fonts:
                return font
        
        return 'Arial'  # Fallback ultime
    
    def _get_best_mono_font(self):
        """Trouve la meilleure police monospace"""
        if self.system == "Windows":
            preferred_fonts = [
                'Cascadia Code',
                'JetBrains Mono',
                'Fira Code',
                'Consolas',
                'Courier New'
            ]
        elif self.system == "Darwin":  # macOS
            preferred_fonts = [
                'SF Mono',
                'JetBrains Mono',
                'Fira Code',
                'Menlo',
                'Monaco'
            ]
        else:  # Linux
            preferred_fonts = [
                'JetBrains Mono',
                'Fira Code',
                'Ubuntu Mono',
                'DejaVu Sans Mono',
                'Liberation Mono'
            ]
        
        for font in preferred_fonts:
            if font in self.available_fonts:
                return font
        
        return 'Courier New'  # Fallback ultime
    
    def get_fonts(self):
        """Retourne la configuration de polices"""
        return self.modern_fonts
    
    def get_font_info(self):
        """Retourne des informations sur les polices utilisées"""
        return {
            'system': self.system,
            'google_fonts_available': self.google_fonts_available,
            'primary_font': self.modern_fonts['body'][0],
            'mono_font': self.modern_fonts['mono'][0],
            'total_available': len(self.available_fonts)
        }
    
    def test_font_rendering(self, font_name, size=12):
        """Teste le rendu d'une police"""
        try:
            test_font = tkFont.Font(family=font_name, size=size)
            return test_font.measure("Test") > 0
        except:
            return False

class ThemeManager:
    """Gestionnaire de thèmes visuels"""
    
    def __init__(self):
        self.themes = {
            'light_medical': self._light_medical_theme(),
            'dark_medical': self._dark_medical_theme(),
            'google_gemini': self._google_gemini_theme(),
            'high_contrast': self._high_contrast_theme()
        }
        
        self.current_theme = 'google_gemini'
    
    def _light_medical_theme(self):
        """Thème médical clair"""
        return {
            'primary': '#1976d2',
            'secondary': '#2196f3', 
            'accent': '#4caf50',
            'background': '#fafafa',
            'surface': '#ffffff',
            'error': '#f44336',
            'warning': '#ff9800',
            'success': '#4caf50',
            'text_primary': '#212121',
            'text_secondary': '#757575'
        }
    
    def _dark_medical_theme(self):
        """Thème médical sombre"""
        return {
            'primary': '#2196f3',
            'secondary': '#03dac6',
            'accent': '#bb86fc',
            'background': '#121212',
            'surface': '#1e1e1e',
            'error': '#cf6679',
            'warning': '#ffb74d',
            'success': '#81c784',
            'text_primary': '#ffffff',
            'text_secondary': '#b3b3b3'
        }
    
    def _google_gemini_theme(self):
        """Thème Google Gemini"""
        return {
            'primary': '#1a73e8',
            'secondary': '#4285f4',
            'accent': '#9c27b0',
            'background': '#fafbff',
            'surface': '#ffffff',
            'error': '#ea4335',
            'warning': '#fbbc04',
            'success': '#34a853',
            'text_primary': '#202124',
            'text_secondary': '#5f6368',
            
            # Couleurs spéciales Gemini
            'gemini_blue': '#4285f4',
            'gemini_purple': '#9c27b0',
            'gemini_cyan': '#00bcd4',
            'gemini_green': '#34a853',
            
            # Glassmorphism (couleurs solides pour Tkinter)
            'glass_white': '#fefefe',
            'glass_blue': '#e3f2fd',
            
            # Gradients (représentés par la première couleur)
            'gradient_primary': '#667eea',
            'gradient_medical': '#4285f4',
            'gradient_gemini': '#9c27b0'
        }
    
    def _high_contrast_theme(self):
        """Thème haute accessibilité"""
        return {
            'primary': '#000000',
            'secondary': '#333333',
            'accent': '#0066cc',
            'background': '#ffffff',
            'surface': '#f5f5f5',
            'error': '#cc0000',
            'warning': '#ff6600',
            'success': '#006600',
            'text_primary': '#000000',
            'text_secondary': '#333333'
        }
    
    def get_theme(self, theme_name=None):
        """Retourne un thème"""
        if theme_name is None:
            theme_name = self.current_theme
        
        return self.themes.get(theme_name, self.themes['google_gemini'])
    
    def set_theme(self, theme_name):
        """Change le thème actuel"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False

def setup_fonts_and_theme():
    """Configuration complète des polices et thèmes"""
    font_manager = FontManager()
    theme_manager = ThemeManager()
    
    return {
        'fonts': font_manager.get_fonts(),
        'font_info': font_manager.get_font_info(),
        'theme': theme_manager.get_theme(),
        'theme_manager': theme_manager
    }

def get_medical_ui_config():
    """Configuration spécialisée pour interface médicale"""
    config = setup_fonts_and_theme()
    
    # Ajustements spécifiques pour interface médicale
    medical_adjustments = {
        'fonts': {
            **config['fonts'],
            # Tailles légèrement plus grandes pour lisibilité médicale
            'medical_title': (config['fonts']['title_large'][0], 24, 'bold'),
            'medical_body': (config['fonts']['body'][0], 15, 'normal'),
            'medical_caption': (config['fonts']['caption'][0], 13, 'normal'),
            'medical_mono': (config['fonts']['mono'][0], 13, 'normal')
        },
        'spacing': {
            'card_padding': 20,
            'section_spacing': 15,
            'element_spacing': 10,
            'tight_spacing': 5
        },
        'sizes': {
            'card_corner_radius': 12,
            'button_height': 44,
            'input_height': 40,
            'icon_size': 24
        }
    }
    
    return {**config, **medical_adjustments}

# Test de compatibilité
if __name__ == "__main__":
    print("🔤 Testing Font Configuration...")
    
    font_manager = FontManager()
    print(f"System: {font_manager.system}")
    print(f"Google Fonts Available: {font_manager.google_fonts_available}")
    
    fonts = font_manager.get_fonts()
    print(f"Primary Font: {fonts['body'][0]}")
    print(f"Mono Font: {fonts['mono'][0]}")
    
    # Test des polices
    print("\n📝 Font Availability Test:")
    test_fonts = ['Google Sans', 'Segoe UI', 'Arial', 'Consolas']
    
    for font in test_fonts:
        available = font in font_manager.available_fonts
        status = "✅" if available else "❌"
        print(f"{status} {font}")
    
    print(f"\nTotal fonts available: {len(font_manager.available_fonts)}")
    
    # Test du thème
    theme_manager = ThemeManager()
    gemini_theme = theme_manager.get_theme('google_gemini')
    print(f"\n🎨 Using theme: {theme_manager.current_theme}")
    print(f"Primary color: {gemini_theme['primary']}")
