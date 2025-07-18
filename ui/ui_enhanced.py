"""
Interface Ultra-Moderne avec Effet "Wahou" pour RetinoblastoGemma v6
Inspirée des tendances 2024-2025 : Spatial Design, Glassmorphism, Micro-animations
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
import math
import time
import threading
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EnhancedModernUI:
    """Interface ultra-moderne avec effets visuels avancés"""
    
    def __init__(self, parent_app):
        self.app = parent_app
        self.root = parent_app.root
        
        # Configuration des couleurs - Palette Google moderne avec glassmorphism
        self.colors = {
            # Couleurs primaires Google/Gemini
            'primary_blue': '#1a73e8',
            'light_blue': '#4285f4', 
            'darker_blue': '#1557b0',
            'google_blue': '#4285f4',
            'gemini_purple': '#9c27b0',
            'gemini_cyan': '#00bcd4',
            
            # Glassmorphism et modernité
            'glass_white': 'rgba(255, 255, 255, 0.95)',
            'glass_blue': 'rgba(66, 133, 244, 0.1)',
            'glass_purple': 'rgba(156, 39, 176, 0.1)',
            'backdrop_blur': 'rgba(248, 249, 250, 0.8)',
            
            # Base colors
            'white': '#ffffff',
            'pure_white': '#fafbff',
            'light_gray': '#f8f9fa',
            'medium_gray': '#e8eaed',
            'dark_gray': '#5f6368',
            
            # Status colors avec variations
            'success': '#34a853',
            'success_light': '#e8f5e8',
            'warning': '#fbbc04',
            'warning_light': '#fff3cd',
            'error': '#ea4335',
            'error_light': '#ffebee',
            'info': '#1a73e8',
            'info_light': '#e8f0fe',
            
            # Gradients modernes
            'gradient_primary': ['#667eea', '#764ba2'],
            'gradient_medical': ['#4285f4', '#34a853'],
            'gradient_gemini': ['#9c27b0', '#4285f4', '#00bcd4'],
            'gradient_ai': ['#1a73e8', '#9c27b0'],
            
            # Text colors
            'text_primary': '#202124',
            'text_secondary': '#5f6368',
            'text_tertiary': '#9aa0a6',
            'text_accent': '#1a73e8'
        }
        
        # Configuration des polices modernes
        self.fonts = {
            'display_large': ('Segoe UI Variable Display', 48, 'bold'),
            'display': ('Segoe UI Variable Display', 36, 'normal'),
            'headline_large': ('Segoe UI Variable Text', 32, 'bold'),
            'headline': ('Segoe UI Variable Text', 28, 'bold'),
            'title_large': ('Segoe UI Variable Text', 22, 'bold'),
            'title': ('Segoe UI Variable Text', 18, 'normal'),
            'label_large': ('Segoe UI Variable Text', 16, 'normal'),
            'label': ('Segoe UI Variable Text', 14, 'normal'),
            'body_large': ('Segoe UI Variable Text', 16, 'normal'),
            'body': ('Segoe UI Variable Text', 14, 'normal'),
            'caption': ('Segoe UI Variable Text', 12, 'normal'),
            'overline': ('Segoe UI Variable Text', 10, 'normal'),
            'mono': ('JetBrains Mono', 12, 'normal')
        }
        
        # Animation et timing
        self.animation_speed = 200  # ms
        self.animation_easing = 'ease-out'
        self.micro_interactions = True
        
        # État de l'interface
        self.ui_state = {
            'theme': 'light',
            'accent_color': 'blue',
            'animations_enabled': True,
            'glassmorphism': True,
            'current_card_hover': None
        }
        
        # Composants animés
        self.animated_elements = {}
        self.animation_queue = []
        
        self.setup_modern_styles()
        
    def setup_modern_styles(self):
        """Configure les styles ultra-modernes avec glassmorphism"""
        self.style = ttk.Style()
        
        # Style principal avec glassmorphism
        self.style.configure('Glass.TFrame',
                           background=self.colors['glass_white'],
                           relief='flat',
                           borderwidth=0)
        
        # Boutons avec effet de profondeur
        self.style.configure('Primary.TButton',
                           background=self.colors['primary_blue'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           relief='flat',
                           padding=(24, 16),
                           font=self.fonts['label_large'])
        
        self.style.map('Primary.TButton',
                      background=[('active', self.colors['light_blue']),
                                ('pressed', self.colors['darker_blue'])],
                      relief=[('pressed', 'flat'),
                             ('!pressed', 'flat')])
        
        # Style pour les cartes avec ombre
        self.style.configure('Card.TFrame',
                           background=self.colors['white'],
                           relief='flat',
                           borderwidth=0)
        
        # Progressbar moderne
        self.style.configure('Modern.Horizontal.TProgressbar',
                           background=self.colors['light_gray'],
                           troughcolor=self.colors['light_gray'],
                           borderwidth=0,
                           lightcolor=self.colors['primary_blue'],
                           darkcolor=self.colors['primary_blue'])
        
    def create_enhanced_interface(self):
        """Crée l'interface ultra-moderne avec effets wahou"""
        # Configuration de la fenêtre
        self.root.configure(bg=self.colors['pure_white'])
        self.root.title("RetinoblastoGemma v6 - Google Gemma Hackathon")
        
        # Container principal avec glassmorphism
        self.main_container = tk.Frame(self.root, bg=self.colors['pure_white'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header ultra-moderne avec effets
        self.create_futuristic_header()
        
        # Floating navigation (optionnel)
        self.create_floating_nav()
        
        # Corps principal avec layout moderne
        self.create_main_layout()
        
        # Footer intelligent
        self.create_smart_footer()
        
        # Démarrer les animations
        self.start_ambient_animations()
        
    def create_futuristic_header(self):
        """Crée un header futuriste avec animations"""
        # Container header avec hauteur dynamique
        header_height = 160
        self.header_frame = tk.Frame(self.main_container, bg=self.colors['pure_white'], 
                                   height=header_height)
        self.header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        self.header_frame.pack_propagate(False)
        
        # Canvas pour les effets visuels
        self.header_canvas = tk.Canvas(self.header_frame, height=header_height,
                                     bg=self.colors['pure_white'], highlightthickness=0)
        self.header_canvas.pack(fill=tk.BOTH)
        
        # Gradient animé en arrière-plan
        self.create_animated_gradient()
        
        # Container du contenu header
        content_frame = tk.Frame(self.header_canvas, bg=self.colors['pure_white'])
        content_frame.place(relx=0.03, rely=0.15, relwidth=0.94, relheight=0.7)
        
        # Section gauche - Logo et titre
        left_section = tk.Frame(content_frame, bg=self.colors['pure_white'])
        left_section.pack(side=tk.LEFT, fill=tk.Y)
        
        # Logo animé (sera un widget personnalisé)
        self.create_animated_logo(left_section)
        
        # Titre principal avec effet moderne
        title_frame = tk.Frame(left_section, bg=self.colors['pure_white'])
        title_frame.pack(side=tk.LEFT, padx=(20, 0), fill=tk.Y)
        
        main_title = tk.Label(title_frame, text="RetinoblastoGemma", 
                             font=self.fonts['display'],
                             bg=self.colors['pure_white'], fg=self.colors['text_primary'])
        main_title.pack(anchor=tk.W)
        
        version_subtitle = tk.Label(title_frame, text="v6 • Powered by Gemma 3n", 
                                  font=self.fonts['title'],
                                  bg=self.colors['pure_white'], fg=self.colors['text_secondary'])
        version_subtitle.pack(anchor=tk.W, pady=(5, 0))
        
        # Badges modernes
        badges_frame = tk.Frame(title_frame, bg=self.colors['pure_white'])
        badges_frame.pack(anchor=tk.W, pady=(10, 0))
        
        self.create_modern_badges(badges_frame)
        
        # Section droite - Status intelligent
        right_section = tk.Frame(content_frame, bg=self.colors['pure_white'])
        right_section.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.create_intelligent_status(right_section)
        
    def create_animated_logo(self, parent):
        """Crée un logo animé moderne"""
        logo_frame = tk.Frame(parent, bg=self.colors['pure_white'], width=80, height=80)
        logo_frame.pack(side=tk.LEFT, pady=10)
        logo_frame.pack_propagate(False)
        
        # Canvas pour le logo animé
        logo_canvas = tk.Canvas(logo_frame, width=80, height=80, 
                              bg=self.colors['pure_white'], highlightthickness=0)
        logo_canvas.pack()
        
        # Dessiner le logo avec animations
        self.draw_animated_logo(logo_canvas)
        
    def draw_animated_logo(self, canvas):
        """Dessine le logo avec animations"""
        center_x, center_y = 40, 40
        
        # Cercle extérieur avec gradient
        self.create_circle_gradient(canvas, center_x, center_y, 35, 
                                  self.colors['primary_blue'], self.colors['gemini_purple'])
        
        # Cercle intérieur
        canvas.create_oval(center_x-25, center_y-25, center_x+25, center_y+25,
                          fill=self.colors['white'], outline='', width=0)
        
        # Icône médicale moderne
        canvas.create_text(center_x, center_y, text="🧬", font=('Arial', 24), fill=self.colors['primary_blue'])
        
        # Animation de rotation (simulée avec timer)
        self.animate_logo_rotation(canvas)
        
    def create_modern_badges(self, parent):
        """Crée des badges modernes avec effets"""
        badges = [
            ("🏆 Google Gemma", self.colors['gradient_gemini']),
            ("🔒 100% Local", self.colors['gradient_medical']),
            ("🤖 AI Powered", self.colors['gradient_ai'])
        ]
        
        for i, (text, gradient) in enumerate(badges):
            badge = self.create_gradient_badge(parent, text, gradient)
            badge.pack(side=tk.LEFT, padx=(0, 8))
            
    def create_gradient_badge(self, parent, text, gradient_colors):
        """Crée un badge avec gradient"""
        badge_frame = tk.Frame(parent, bg=gradient_colors[0] if gradient_colors else self.colors['primary_blue'],
                             relief='flat', bd=0)
        
        badge_label = tk.Label(badge_frame, text=text, 
                             font=self.fonts['caption'],
                             bg=gradient_colors[0] if gradient_colors else self.colors['primary_blue'], 
                             fg='white',
                             padx=12, pady=6)
        badge_label.pack()
        
        return badge_frame
        
    def create_intelligent_status(self, parent):
        """Crée un status intelligent avec métriques en temps réel"""
        status_container = tk.Frame(parent, bg=self.colors['pure_white'])
        status_container.pack(fill=tk.BOTH, expand=True)
        
        # Status principal avec animation
        self.main_status = tk.Label(status_container, text="🔄 INITIALIZING SYSTEMS", 
                                  font=self.fonts['label_large'],
                                  bg=self.colors['pure_white'], fg=self.colors['warning'])
        self.main_status.pack(anchor=tk.E, pady=(10, 5))
        
        # Métriques en temps réel
        metrics_frame = tk.Frame(status_container, bg=self.colors['pure_white'])
        metrics_frame.pack(anchor=tk.E, pady=(5, 0))
        
        self.create_live_metrics(metrics_frame)
        
    def create_live_metrics(self, parent):
        """Crée des métriques en temps réel"""
        self.metrics_display = {}
        
        metrics = [
            ("GPU", "GTX 1650", "success"),
            ("RAM", "8GB", "info"),
            ("Model", "Gemma 3n", "warning")
        ]
        
        for i, (label, value, status) in enumerate(metrics):
            metric_frame = tk.Frame(parent, bg=self.colors['pure_white'])
            metric_frame.pack(anchor=tk.E, pady=1)
            
            # Indicateur coloré
            indicator = tk.Label(metric_frame, text="●", font=('Arial', 8),
                               bg=self.colors['pure_white'], fg=self.colors[status])
            indicator.pack(side=tk.RIGHT, padx=(5, 0))
            
            # Texte métrique
            metric_text = tk.Label(metric_frame, text=f"{label}: {value}",
                                 font=self.fonts['caption'],
                                 bg=self.colors['pure_white'], fg=self.colors['text_secondary'])
            metric_text.pack(side=tk.RIGHT)
            
            self.metrics_display[label.lower()] = (indicator, metric_text)
    
    def create_floating_nav(self):
        """Crée une navigation flottante moderne (optionnel)"""
        nav_height = 60
        self.floating_nav = tk.Frame(self.main_container, bg=self.colors['white'],
                                   height=nav_height, relief='flat')
        self.floating_nav.pack(fill=tk.X, padx=40, pady=(15, 0))
        self.floating_nav.pack_propagate(False)
        
        # Ombre simulée avec gradient
        self.add_shadow_effect(self.floating_nav)
        
        # Navigation items
        nav_items = ["Analysis", "Results", "History", "Settings"]
        
        for i, item in enumerate(nav_items):
            nav_btn = tk.Button(self.floating_nav, text=item,
                              font=self.fonts['label'],
                              bg=self.colors['white'], fg=self.colors['text_secondary'],
                              borderwidth=0, relief='flat', cursor='hand2',
                              padx=20, pady=15)
            nav_btn.pack(side=tk.LEFT, padx=10)
            
            # Hover effects
            self.add_hover_effect(nav_btn)
    
    def create_main_layout(self):
        """Crée le layout principal avec cartes modernes"""
        # Container principal avec espacement moderne
        body_container = tk.Frame(self.main_container, bg=self.colors['pure_white'])
        body_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Grid layout moderne
        body_container.columnconfigure(0, weight=1, minsize=380)  # Panel gauche
        body_container.columnconfigure(1, weight=2, minsize=650)  # Panel principal
        body_container.rowconfigure(0, weight=1)
        
        # Panel de contrôle ultra-moderne
        self.create_control_panel_enhanced(body_container)
        
        # Zone principale avec glassmorphism
        self.create_display_area_enhanced(body_container)
        
    def create_control_panel_enhanced(self, parent):
        """Panel de contrôle avec effets glassmorphism"""
        # Container principal avec glassmorphism
        self.control_container = tk.Frame(parent, bg=self.colors['pure_white'])
        self.control_container.grid(row=0, column=0, sticky='nsew', padx=(0, 15))

        # Créer les cartes modernes directement sans scroll pour l'instant
        self.create_enhanced_cards_direct()

    def create_enhanced_cards_direct(self):
        """Crée les cartes modernes directement dans le container"""
        # Hackathon Info Card avec gradient
        hackathon_card = self.create_glass_card("🏆 Hackathon Challenge", 
                             "Google Gemma Worldwide\n🥇 Medical AI Innovation Track\n🔒 Privacy-First Solution\n🚀 100% Local Processing",
                             self.colors['gradient_gemini'], 'large')

        # Image Loading Card moderne - CORRIGÉE
        self.create_interactive_image_card_fixed()

        # AI Analysis Card avec animations - CORRIGÉE
        self.create_ai_analysis_card_fixed()

        # System Status Card intelligente - CORRIGÉE
        self.create_smart_system_card_fixed()

        # Settings Card moderne - CORRIGÉE
        self.create_modern_settings_card_fixed()

        # Progress Card avec visualisations - CORRIGÉE
        self.create_enhanced_progress_card_fixed()

        # Actions Card avec micro-interactions - CORRIGÉE
        self.create_micro_interactions_card_fixed()
        
    def create_scrollable_cards(self):
        """Crée un container scrollable pour les cartes"""
        # Canvas pour scroll
        self.cards_canvas = tk.Canvas(self.control_container, bg=self.colors['pure_white'],
                                    highlightthickness=0)
        self.cards_scrollbar = ttk.Scrollbar(self.control_container, orient="vertical",
                                           command=self.cards_canvas.yview)
        self.cards_scrollable_frame = tk.Frame(self.cards_canvas, bg=self.colors['pure_white'])
        
        self.cards_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all"))
        )
        
        self.cards_canvas.create_window((0, 0), window=self.cards_scrollable_frame, anchor="nw")
        self.cards_canvas.configure(yscrollcommand=self.cards_scrollbar.set)
        
        self.cards_canvas.pack(side="left", fill="both", expand=True)
        self.cards_scrollbar.pack(side="right", fill="y")
        
        # Créer les cartes modernes
        self.create_enhanced_cards()
        
    def create_enhanced_cards(self):
        """Crée les cartes avec effets modernes"""
        # Hackathon Info Card avec gradient
        self.create_glass_card("🏆 Hackathon Challenge", 
                             "Google Gemma Worldwide\n🥇 Medical AI Innovation Track\n🔒 Privacy-First Solution\n🚀 100% Local Processing",
                             self.colors['gradient_gemini'], 'large')
        
        # Image Loading Card moderne
        self.create_interactive_image_card()
        
        # AI Analysis Card avec animations
        self.create_ai_analysis_card()
        
        # System Status Card intelligente
        self.create_smart_system_card()
        
        # Settings Card moderne
        self.create_modern_settings_card()
        
        # Progress Card avec visualisations
        self.create_enhanced_progress_card()
        
        # Actions Card avec micro-interactions
        self.create_micro_interactions_card()
        
    def create_glass_card(self, title, content, gradient=None, size='medium'):
        """Crée une carte avec effet glassmorphism"""
        # Dimensions selon la taille
        heights = {'small': 100, 'medium': 150, 'large': 180}
        card_height = heights.get(size, 150)

        # Container avec ombre - UTILISER LE CONTAINER PRINCIPAL
        shadow_container = tk.Frame(self.control_container, bg=self.colors['medium_gray'])
        shadow_container.pack(fill=tk.X, pady=(0, 15), padx=3)

        # Carte principale avec glassmorphism
        card_frame = tk.Frame(shadow_container, bg=self.colors['white'], height=card_height)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        card_frame.pack_propagate(False)

        # Header avec gradient si spécifié
        if gradient:
            header_canvas = tk.Canvas(card_frame, height=50, bg=gradient[0], highlightthickness=0)
            header_canvas.pack(fill=tk.X)

            # Gradient effect simulé
            self.create_canvas_gradient(header_canvas, gradient)

            # Titre sur le gradient
            header_canvas.create_text(15, 25, text=title, anchor='w',
                                    font=self.fonts['title_large'], fill='white')
        else:
            # Header simple
            header_frame = tk.Frame(card_frame, bg=self.colors['primary_blue'], height=50)
            header_frame.pack(fill=tk.X)
            header_frame.pack_propagate(False)

            title_label = tk.Label(header_frame, text=title, font=self.fonts['title_large'],
                                 bg=self.colors['primary_blue'], fg='white')
            title_label.pack(expand=True, pady=12)

        # Contenu
        content_frame = tk.Frame(card_frame, bg=self.colors['white'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        content_label = tk.Label(content_frame, text=content, font=self.fonts['body'],
                               bg=self.colors['white'], fg=self.colors['text_secondary'],
                               justify=tk.LEFT, anchor='nw')
        content_label.pack(fill=tk.BOTH, expand=True)

        # Effets hover
        self.add_card_hover_effects(card_frame)

        return card_frame
        
    def create_interactive_image_card(self):
        """Carte de chargement d'image avec interactions avancées"""
        card_frame = self.create_glass_card("📸 Medical Image Upload", "", 
                                          self.colors['gradient_medical'], 'medium')
        
        # Remplacer le contenu par des éléments interactifs
        for widget in card_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == self.colors['white']:
                # C'est le content_frame
                for child in widget.winfo_children():
                    child.destroy()
                
                # Zone de drop avec style moderne
                drop_zone = tk.Frame(widget, bg=self.colors['light_gray'], relief='flat',
                                   bd=2, height=80)
                drop_zone.pack(fill=tk.X, pady=(0, 10))
                drop_zone.pack_propagate(False)
                
                # Texte de la drop zone
                drop_text = tk.Label(drop_zone, text="📁 Drop image here or click to browse",
                                   font=self.fonts['body'], bg=self.colors['light_gray'],
                                   fg=self.colors['text_secondary'])
                drop_text.pack(expand=True)
                
                # Bouton moderne
                modern_btn = tk.Button(widget, text="🔍 Select Medical Image",
                                     font=self.fonts['label'],
                                     bg=self.colors['primary_blue'], fg='white',
                                     borderwidth=0, relief='flat', cursor='hand2',
                                     command=self.app.load_image, pady=12)
                modern_btn.pack(fill=tk.X, pady=(0, 10))
                
                # Info label modernisé
                self.app.image_info_label = tk.Label(widget, text="No image loaded",
                                                   font=self.fonts['caption'],
                                                   bg=self.colors['white'], 
                                                   fg=self.colors['text_tertiary'])
                self.app.image_info_label.pack(anchor=tk.W)
                
                # Effets hover sur le bouton
                self.add_button_animations(modern_btn)
                break
    
    def create_ai_analysis_card(self):
        """Carte d'analyse AI avec animations"""
        card_frame = self.create_glass_card("🤖 Gemma 3n Analysis", "", 
                                          self.colors['gradient_ai'], 'medium')
        
        # Personnaliser le contenu
        for widget in card_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == self.colors['white']:
                for child in widget.winfo_children():
                    child.destroy()
                
                # Status de Gemma avec animation
                gemma_status = tk.Label(widget, text="🧠 Gemma 3n: Loading...",
                                      font=self.fonts['body'], bg=self.colors['white'],
                                      fg=self.colors['warning'])
                gemma_status.pack(anchor=tk.W, pady=(0, 10))
                
                # Bouton d'analyse ultra-moderne
                self.app.analyze_button = tk.Button(widget, text="🔬 Start AI Analysis",
                                                  font=self.fonts['label_large'],
                                                  bg=self.colors['success'], fg='white',
                                                  borderwidth=0, relief='flat', cursor='hand2',
                                                  command=self.analyze_with_confirmation,
                                                  state='disabled', pady=16)
                self.app.analyze_button.pack(fill=tk.X, pady=(0, 10))
                
                # Progress mini
                mini_progress = ttk.Progressbar(widget, mode='indeterminate', length=200)
                mini_progress.pack(fill=tk.X, pady=(0, 5))
                
                # Métrique temps réel
                time_label = tk.Label(widget, text="Ready for analysis",
                                    font=self.fonts['caption'], bg=self.colors['white'],
                                    fg=self.colors['text_tertiary'])
                time_label.pack(anchor=tk.W)
                
                self.add_button_animations(self.app.analyze_button)
                break
    
    def create_smart_system_card(self):
        """Carte système intelligente avec métriques live"""
        card_frame = self.create_glass_card("⚡ System Intelligence", "", 
                                          self.colors['gradient_primary'], 'large')
        
        # Contenu intelligent
        for widget in card_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == self.colors['white']:
                for child in widget.winfo_children():
                    child.destroy()
                
                # Grid pour les modules
                modules_grid = tk.Frame(widget, bg=self.colors['white'])
                modules_grid.pack(fill=tk.BOTH, expand=True)
                
                # Créer les status modules modernes
                self.create_modern_module_status(modules_grid)
                break
    
    def create_modern_module_status(self, parent):
        """Status des modules avec design moderne"""
        self.app.module_status = {}
        
        modules = [
            ('gemma', '🧠 Gemma 3n', 'Initializing...'),
            ('eye_detector', '👁️ Eye Detection', 'Waiting...'),
            ('face_handler', '👤 Face Tracking', 'Waiting...'),
            ('visualizer', '🎨 Visualization', 'Waiting...')
        ]
        
        for i, (key, name, status) in enumerate(modules):
            # Container pour chaque module
            module_container = tk.Frame(parent, bg=self.colors['light_gray'], relief='flat')
            module_container.pack(fill=tk.X, pady=3, padx=5)
            
            # Status dot avec animation
            status_frame = tk.Frame(module_container, bg=self.colors['light_gray'])
            status_frame.pack(side=tk.LEFT, padx=10, pady=8)
            
            status_dot = tk.Label(status_frame, text="●", font=('Arial', 12),
                                bg=self.colors['light_gray'], fg=self.colors['warning'])
            status_dot.pack()
            
            # Texte du module
            text_frame = tk.Frame(module_container, bg=self.colors['light_gray'])
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=8)
            
            module_name = tk.Label(text_frame, text=name, font=self.fonts['label'],
                                 bg=self.colors['light_gray'], fg=self.colors['text_primary'])
            module_name.pack(anchor=tk.W)
            
            module_status = tk.Label(text_frame, text=status, font=self.fonts['caption'],
                                   bg=self.colors['light_gray'], fg=self.colors['text_secondary'])
            module_status.pack(anchor=tk.W)
            
            # Stocker pour updates
            self.app.module_status[key] = {
                'dot': status_dot,
                'name': module_name,
                'status': module_status,
                'container': module_container
            }
            
            # Animation de pulse pour les dots
            self.animate_status_dot(status_dot)
    
    def create_enhanced_progress_card(self):
        """Carte de progression avec visualisations avancées"""
        card_frame = self.create_glass_card("📊 Analysis Progress", "", 
                                          self.colors['gradient_medical'], 'medium')
        
        # Trouver le content frame
        content_frame = None
        for widget in card_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == self.colors['white']:
                content_frame = widget
                break
        
        if content_frame:
            # Nettoyer le contenu existant
            for child in content_frame.winfo_children():
                child.destroy()
            
            # Barre de progression moderne
            self.app.progress = ttk.Progressbar(content_frame, mode='determinate', 
                                               style='Modern.Horizontal.TProgressbar')
            self.app.progress.pack(fill=tk.X, pady=(0, 10))
            
            # Label de progression
            self.app.progress_label = tk.Label(content_frame, text="Ready for analysis",
                                              font=self.fonts['caption'],
                                              bg=self.colors['white'],
                                              fg=self.colors['text_secondary'])
            self.app.progress_label.pack(anchor=tk.W)

    def create_micro_interactions_card(self):
        """Carte avec micro-interactions pour les actions"""
        card_frame = self.create_glass_card("💾 Smart Actions", "", 
                                          self.colors['gradient_primary'], 'large')
        
        for widget in card_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == self.colors['white']:
                for child in widget.winfo_children():
                    child.destroy()
                
                # Boutons d'action avec effets
                actions = [
                    ("📊 Export Results", self.app.export_results),
                    ("🏥 Medical Report", self.app.generate_medical_report),
                    ("🧠 AI Recommendations", self.app.generate_recommendations),
                    ("👤 Patient Summary", self.app.show_face_tracking_summary),
                    ("⚙️ System Info", self.app.show_system_info)
                ]
                
                for text, command in actions:
                    btn = tk.Button(widget, text=text, command=command,
                                  font=self.fonts['label'], bg=self.colors['primary_blue'],
                                  fg='white', borderwidth=0, relief='flat',
                                  cursor='hand2', pady=8)
                    btn.pack(fill=tk.X, pady=2)
                    self.add_button_animations(btn)
                
                break

    def create_display_area_enhanced(self, parent):
        """Zone d'affichage principale avec glassmorphism"""
        # Container principal avec glassmorphism
        self.display_container = tk.Frame(parent, bg=self.colors['pure_white'])
        self.display_container.grid(row=0, column=1, sticky='nsew', padx=(15, 0))
        
        # Utiliser le système d'onglets existant de l'app
        if hasattr(self.app, 'setup_display_area'):
            # Créer un conteneur temporaire pour l'ancien système
            temp_parent = tk.Frame(self.display_container)
            temp_parent.pack(fill=tk.BOTH, expand=True)
            
            # Appeler la méthode existante
            try:
                self.app.setup_display_area(temp_parent)
            except Exception as e:
                logger.error(f"Error setting up display area: {e}")
                # Fallback : créer une zone simple
                fallback_label = tk.Label(self.display_container, 
                                        text="Display area loading...",
                                        font=self.fonts['title'])
                fallback_label.pack(expand=True)

    def create_modern_settings_card(self):
        """Carte de paramètres moderne"""
        card_frame = self.create_glass_card("⚙️ Analysis Settings", "", 
                                          self.colors['gradient_ai'], 'large')
        
        for widget in card_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == self.colors['white']:
                for child in widget.winfo_children():
                    child.destroy()
                
                # Seuil de confiance
                conf_frame = tk.Frame(widget, bg=self.colors['white'])
                conf_frame.pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(conf_frame, text="Confidence Threshold:",
                        font=self.fonts['label'], bg=self.colors['white'],
                        fg=self.colors['text_primary']).pack(anchor=tk.W)
                
                self.app.confidence_var = tk.DoubleVar(value=0.5)
                confidence_scale = ttk.Scale(conf_frame, from_=0.1, to=0.9,
                                           variable=self.app.confidence_var,
                                           orient=tk.HORIZONTAL)
                confidence_scale.pack(fill=tk.X, pady=2)
                
                # Options avec checkboxes modernes
                self.app.face_tracking_var = tk.BooleanVar(value=True)
                face_cb = tk.Checkbutton(widget, text="🔍 Enable Face Tracking",
                                       variable=self.app.face_tracking_var,
                                       font=self.fonts['body'], bg=self.colors['white'],
                                       fg=self.colors['text_primary'])
                face_cb.pack(anchor=tk.W, pady=2)
                
                self.app.enhanced_detection_var = tk.BooleanVar(value=True)
                enhanced_cb = tk.Checkbutton(widget, text="🚀 Enhanced Detection",
                                           variable=self.app.enhanced_detection_var,
                                           font=self.fonts['body'], bg=self.colors['white'],
                                           fg=self.colors['text_primary'])
                enhanced_cb.pack(anchor=tk.W, pady=2)
                
                # Métriques de session
                self.app.metrics_label = tk.Label(widget, text="No analysis yet",
                                                 font=self.fonts['caption'],
                                                 bg=self.colors['white'],
                                                 fg=self.colors['text_tertiary'])
                self.app.metrics_label.pack(anchor=tk.W, pady=(10, 0))
                
                break

    def create_animated_gradient(self):
        """Crée un gradient animé en arrière-plan du header"""
        try:
            # Créer un gradient simple avec des rectangles de couleurs
            canvas_width = self.header_canvas.winfo_reqwidth()
            canvas_height = self.header_canvas.winfo_reqheight()
            
            # Gradient de bleu à violet
            colors = ['#4285f4', '#5a67d8', '#667eea', '#764ba2', '#9c27b0']
            
            if canvas_width > 0 and canvas_height > 0:
                section_width = max(1, canvas_width // len(colors))
                
                for i, color in enumerate(colors):
                    x1 = i * section_width
                    x2 = min((i + 1) * section_width, canvas_width)
                    self.header_canvas.create_rectangle(
                        x1, 0, x2, canvas_height, 
                        fill=color, outline=color
                    )
        except Exception as e:
            logger.error(f"Error creating animated gradient: {e}")
    
    def animate_logo_rotation(self, canvas):
        """Anime la rotation du logo (simulation)"""
        try:
            # Animation simple avec changement de couleur
            def rotate_logo():
                try:
                    # Changer la couleur de l'icône périodiquement
                    colors = ['#4285f4', '#9c27b0', '#00bcd4', '#34a853']
                    current_color = colors[int(time.time()) % len(colors)]
                    canvas.delete("logo_icon")
                    canvas.create_text(40, 40, text="🧬", font=('Arial', 24), 
                                     fill=current_color, tags="logo_icon")
                    self.root.after(2000, rotate_logo)  # Répéter toutes les 2 secondes
                except:
                    pass
            
            # Démarrer l'animation
            self.root.after(1000, rotate_logo)
        except Exception as e:
            logger.error(f"Error animating logo: {e}")
    
    def create_circle_gradient(self, canvas, x, y, radius, color1, color2):
        """Crée un cercle avec effet de gradient"""
        try:
            # Créer plusieurs cercles concentriques pour simuler un gradient
            steps = 5
            for i in range(steps):
                r = radius * (1 - i / steps)
                # Interpoler entre les couleurs (simplifié)
                canvas.create_oval(
                    x - r, y - r, x + r, y + r,
                    fill=color1, outline=color1, width=0
                )
        except Exception as e:
            logger.error(f"Error creating circle gradient: {e}")
    
    def add_shadow_effect(self, widget):
        """Ajoute un effet d'ombre à un widget (simulation)"""
        try:
            # Simuler une ombre en changeant la couleur de fond
            widget.configure(relief='solid', bd=1)
        except Exception as e:
            logger.error(f"Error adding shadow effect: {e}")
    
    def add_hover_effect(self, widget):
        """Ajoute des effets de survol à un widget"""
        try:
            original_bg = widget.cget('bg')
            original_fg = widget.cget('fg')
            
            def on_enter(event):
                widget.configure(bg=self.colors['light_blue'], fg='white')
            
            def on_leave(event):
                widget.configure(bg=original_bg, fg=original_fg)
            
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        except Exception as e:
            logger.error(f"Error adding hover effect: {e}")
    
    def add_card_hover_effects(self, card_frame):
        """Ajoute des effets de survol aux cartes"""
        try:
            def on_enter(event):
                card_frame.configure(relief='raised', bd=2)
            
            def on_leave(event):
                card_frame.configure(relief='flat', bd=0)
            
            card_frame.bind("<Enter>", on_enter)
            card_frame.bind("<Leave>", on_leave)
        except Exception as e:
            logger.error(f"Error adding card hover effects: {e}")
    
    def create_canvas_gradient(self, canvas, gradient_colors):
        """Crée un gradient sur un canvas"""
        try:
            width = canvas.winfo_reqwidth()
            height = canvas.winfo_reqheight()
            
            if width > 0 and height > 0:
                # Gradient horizontal simple
                section_width = max(1, width // len(gradient_colors))
                
                for i, color in enumerate(gradient_colors):
                    x1 = i * section_width
                    x2 = min((i + 1) * section_width, width)
                    canvas.create_rectangle(
                        x1, 0, x2, height,
                        fill=color, outline=color
                    )
        except Exception as e:
            logger.error(f"Error creating canvas gradient: {e}")
    
    def add_button_animations(self, button):
        """Ajoute des animations aux boutons"""
        try:
            original_bg = button.cget('bg')
            
            def on_click(event):
                button.configure(bg=self.colors['darker_blue'])
                self.root.after(100, lambda: button.configure(bg=original_bg))
            
            def on_enter(event):
                button.configure(bg=self.colors['light_blue'])
            
            def on_leave(event):
                button.configure(bg=original_bg)
            
            button.bind("<Button-1>", on_click)
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
        except Exception as e:
            logger.error(f"Error adding button animations: {e}")
    
    def animate_status_dot(self, dot_widget):
        """Anime les points de statut"""
        try:
            def pulse_dot():
                try:
                    current_color = dot_widget.cget('fg')
                    if current_color == self.colors['warning']:
                        dot_widget.configure(fg=self.colors['light_blue'])
                    else:
                        dot_widget.configure(fg=self.colors['warning'])
                    self.root.after(1500, pulse_dot)
                except:
                    pass
            
            # Démarrer l'animation
            self.root.after(500, pulse_dot)
        except Exception as e:
            logger.error(f"Error animating status dot: {e}")
    
    def start_ambient_animations(self):
        """Démarre les animations d'ambiance"""
        try:
            # Démarrer les animations après un délai
            self.root.after(2000, self._start_background_animations)
        except Exception as e:
            logger.error(f"Error starting ambient animations: {e}")
    
    def _start_background_animations(self):
        """Animations de fond continues"""
        try:
            # Animation subtile en arrière-plan
            def subtle_animation():
                try:
                    # Changer légèrement les couleurs de l'header
                    if hasattr(self, 'header_canvas'):
                        # Animation très subtile
                        pass
                    self.root.after(5000, subtle_animation)
                except:
                    pass
            
            subtle_animation()
        except Exception as e:
            logger.error(f"Error in background animations: {e}")

    def analyze_with_confirmation(self):
        """Méthode de confirmation d'analyse"""
        try:
            if hasattr(self.app, 'analyze_image'):
                self.app.analyze_image()
        except Exception as e:
            logger.error(f"Error in analyze confirmation: {e}")

    def update_module_status_enhanced(self, module_key, text, color):
        """Met à jour le statut d'un module avec interface moderne"""
        try:
            # Mise à jour pour l'interface classique (compatibilité)
            if hasattr(self.app, 'module_status') and module_key in self.app.module_status:
                self.app.module_status[module_key].config(text=text, foreground=color)
            
            # Mise à jour pour l'interface moderne
            if hasattr(self.app, 'module_status_enhanced') and module_key in self.app.module_status_enhanced:
                status_info = self.app.module_status_enhanced[module_key]
                
                # Mettre à jour le point de statut
                if 'dot' in status_info:
                    color_map = {
                        'green': self.colors['success'],
                        'red': self.colors['error'], 
                        'blue': self.colors['info'],
                        'orange': self.colors['warning']
                    }
                    dot_color = color_map.get(color, self.colors['warning'])
                    status_info['dot'].configure(fg=dot_color)
                
                # Mettre à jour le texte de statut
                if 'status' in status_info:
                    status_info['status'].configure(text=text)
                    
        except Exception as e:
            logger.error(f"Error updating module status: {e}")

    def update_main_status_badge(self, text, status_type):
        """Met à jour le badge de statut principal"""
        try:
            if hasattr(self, 'main_status'):
                color_map = {
                    'loading': self.colors['warning'],
                    'success': self.colors['success'],
                    'error': self.colors['error'],
                    'info': self.colors['info']
                }
                color = color_map.get(status_type, self.colors['text_primary'])
                self.main_status.configure(text=text, fg=color)
        except Exception as e:
            logger.error(f"Error updating main status badge: {e}")

    def show_error_notification(self, title, message):
        """Affiche une notification d'erreur"""
        try:
            messagebox.showerror(title, message)
        except Exception as e:
            logger.error(f"Error showing error notification: {e}")

    def show_success_notification(self, title, message):
        """Affiche une notification de succès"""
        try:
            messagebox.showinfo(title, message)
        except Exception as e:
            logger.error(f"Error showing success notification: {e}")

    def show_loading_overlay(self, message):
        """Affiche un overlay de chargement"""
        try:
            # Pour l'instant, juste mettre à jour le statut
            self.update_main_status_badge(message, "loading")
        except Exception as e:
            logger.error(f"Error showing loading overlay: {e}")

    def hide_loading_overlay(self):
        """Cache l'overlay de chargement"""
        try:
            # Pour l'instant, juste mettre à jour le statut
            self.update_main_status_badge("✅ READY", "success")
        except Exception as e:
            logger.error(f"Error hiding loading overlay: {e}")

    def success_celebration_animation(self, root):
        """Animation de célébration de succès"""
        try:
            # Animation simple de succès
            if hasattr(self, 'main_status'):
                original_text = self.main_status.cget('text')
                self.main_status.configure(text="🎉 SUCCESS! 🎉")
                root.after(2000, lambda: self.main_status.configure(text=original_text))
        except Exception as e:
            logger.error(f"Error in success celebration: {e}")

    def show_analysis_confirmation_modern(self):
        """Affiche une confirmation moderne pour l'analyse"""
        try:
            # Pour l'instant, utiliser la confirmation standard
            if hasattr(self.app, '_start_analysis_process'):
                self.app._start_analysis_process()
        except Exception as e:
            logger.error(f"Error showing analysis confirmation: {e}")

    def create_smart_footer(self):
        """Crée un footer intelligent"""
        try:
            # Footer simple en bas de la fenêtre
            footer_frame = tk.Frame(self.main_container, bg=self.colors['medium_gray'], height=40)
            footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
            footer_frame.pack_propagate(False)
            
            # Status et informations
            footer_content = tk.Frame(footer_frame, bg=self.colors['medium_gray'])
            footer_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)
            
            # Status à gauche
            self.app.status_label = tk.Label(footer_content, 
                text="RetinoblastoGemma v6 Ready - Hackathon Google Gemma",
                bg=self.colors['medium_gray'], fg=self.colors['text_secondary'],
                font=self.fonts['caption'])
            self.app.status_label.pack(side=tk.LEFT)
            
            # Informations à droite
            time_label = tk.Label(footer_content, text="🕒 Ready",
                                bg=self.colors['medium_gray'], fg=self.colors['text_tertiary'],
                                font=self.fonts['caption'])
            time_label.pack(side=tk.RIGHT)
            
        except Exception as e:
            logger.error(f"Error creating smart footer: {e}")

    def create_main_layout(self):
        """Crée le layout principal avec cartes modernes"""
        try:
            # Container principal avec espacement moderne
            body_container = tk.Frame(self.main_container, bg=self.colors['pure_white'])
            body_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Grid layout moderne
            body_container.columnconfigure(0, weight=1, minsize=380)  # Panel gauche
            body_container.columnconfigure(1, weight=2, minsize=650)  # Panel principal
            body_container.rowconfigure(0, weight=1)
            
            # Panel de contrôle ultra-moderne
            self.create_control_panel_enhanced(body_container)
            
            # Zone principale avec glassmorphism
            self.create_display_area_enhanced(body_container)
            
        except Exception as e:
            logger.error(f"Error creating main layout: {e}")

    def create_floating_nav(self):
        """Crée une navigation flottante moderne (optionnel)"""
        try:
            nav_height = 60
            self.floating_nav = tk.Frame(self.main_container, bg=self.colors['white'],
                                       height=nav_height, relief='flat')
            self.floating_nav.pack(fill=tk.X, padx=40, pady=(15, 0))
            self.floating_nav.pack_propagate(False)
            
            # Ombre simulée avec gradient
            self.add_shadow_effect(self.floating_nav)
            
            # Navigation items
            nav_items = ["Analysis", "Results", "History", "Settings"]
            
            for i, item in enumerate(nav_items):
                nav_btn = tk.Button(self.floating_nav, text=item,
                                  font=self.fonts['label'],
                                  bg=self.colors['white'], fg=self.colors['text_secondary'],
                                  borderwidth=0, relief='flat', cursor='hand2',
                                  padx=20, pady=15)
                nav_btn.pack(side=tk.LEFT, padx=10)
                
                # Hover effects
                self.add_hover_effect(nav_btn)
        except Exception as e:
            logger.error(f"Error creating floating nav: {e}")

    def create_display_area_enhanced(self, parent):
        """Zone d'affichage principale avec glassmorphism"""
        try:
            # Container principal avec glassmorphism
            self.display_container = tk.Frame(parent, bg=self.colors['pure_white'])
            self.display_container.grid(row=0, column=1, sticky='nsew', padx=(15, 0))
            
            # Créer un conteneur pour le système d'onglets
            display_frame = tk.Frame(self.display_container, bg=self.colors['pure_white'])
            display_frame.pack(fill=tk.BOTH, expand=True)
            display_frame.columnconfigure(0, weight=1)
            display_frame.rowconfigure(0, weight=1)
            
            # Notebook pour les onglets (repris du code original)
            self.app.notebook = ttk.Notebook(display_frame)
            self.app.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Onglet image principale
            self.app.image_frame = ttk.Frame(self.app.notebook)
            self.app.notebook.add(self.app.image_frame, text="🖼️ Image Analysis")
            
            # Canvas avec scrollbars
            canvas_frame = ttk.Frame(self.app.image_frame)
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            self.app.canvas = tk.Canvas(canvas_frame, bg="white", relief=tk.SUNKEN, bd=2)
            scrollbar_v = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.app.canvas.yview)
            scrollbar_h = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.app.canvas.xview)
            self.app.canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
            
            self.app.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
            scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))
            
            canvas_frame.columnconfigure(0, weight=1)
            canvas_frame.rowconfigure(0, weight=1)
            
            # Onglet résultats
            self.app.results_frame = ttk.Frame(self.app.notebook)
            self.app.notebook.add(self.app.results_frame, text="📋 Medical Results")
            
            results_container = ttk.Frame(self.app.results_frame)
            results_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            self.app.results_text = tk.Text(results_container, wrap=tk.WORD, 
                                           font=("Consolas", 10), relief=tk.SUNKEN, bd=2)
            results_scrollbar = ttk.Scrollbar(results_container, orient="vertical", 
                                            command=self.app.results_text.yview)
            self.app.results_text.configure(yscrollcommand=results_scrollbar.set)
            
            self.app.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            results_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            
            results_container.columnconfigure(0, weight=1)
            results_container.rowconfigure(0, weight=1)
            
            # Onglet historique patient
            self.app.history_frame = ttk.Frame(self.app.notebook)
            self.app.notebook.add(self.app.history_frame, text="👤 Patient History")
            
            history_container = ttk.Frame(self.app.history_frame)
            history_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            self.app.history_text = tk.Text(history_container, wrap=tk.WORD, 
                                           font=("Consolas", 9), relief=tk.SUNKEN, bd=2)
            history_scrollbar = ttk.Scrollbar(history_container, orient="vertical", 
                                            command=self.app.history_text.yview)
            self.app.history_text.configure(yscrollcommand=history_scrollbar.set)
            
            self.app.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            history_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            
            history_container.columnconfigure(0, weight=1)
            history_container.rowconfigure(0, weight=1)
            
        except Exception as e:
            logger.error(f"Error creating enhanced display area: {e}")

    def create_interactive_image_card_fixed(self):
        """Carte de chargement d'image avec interactions avancées - VERSION CORRIGÉE"""
        card_frame = self.create_glass_card("📸 Medical Image Upload", "", 
                                          self.colors['gradient_medical'], 'medium')
        
        # Trouver le content frame et le personnaliser
        for widget in card_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == self.colors['white']:
                # Nettoyer le contenu existant
                for child in widget.winfo_children():
                    child.destroy()
                
                # Zone de drop avec style moderne
                drop_zone = tk.Frame(widget, bg=self.colors['light_gray'], relief='flat',
                                   bd=2, height=80)
                drop_zone.pack(fill=tk.X, pady=(0, 10))
                drop_zone.pack_propagate(False)
                
                # Texte de la drop zone
                drop_text = tk.Label(drop_zone, text="📁 Drop image here or click to browse",
                                   font=self.fonts['body'], bg=self.colors['light_gray'],
                                   fg=self.colors['text_secondary'])
                drop_text.pack(expand=True)
                
                # Bouton moderne
                modern_btn = tk.Button(widget, text="🔍 Select Medical Image",
                                     font=self.fonts['label'],
                                     bg=self.colors['primary_blue'], fg='white',
                                     borderwidth=0, relief='flat', cursor='hand2',
                                     command=self.app.load_image, pady=12)
                modern_btn.pack(fill=tk.X, pady=(0, 10))
                
                # Info label modernisé
                self.app.image_info_label = tk.Label(widget, text="No image loaded",
                                                   font=self.fonts['caption'],
                                                   bg=self.colors['white'], 
                                                   fg=self.colors['text_tertiary'])
                self.app.image_info_label.pack(anchor=tk.W)
                
                # Effets hover sur le bouton
                self.add_button_animations(modern_btn)
                break
            
    def create_ai_analysis_card_fixed(self):
        """Carte d'analyse AI avec animations - VERSION CORRIGÉE"""
        card_frame = self.create_glass_card("🤖 Gemma 3n Analysis", "", 
                                          self.colors['gradient_ai'], 'medium')
        
        # Personnaliser le contenu
        for widget in card_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == self.colors['white']:
                for child in widget.winfo_children():
                    child.destroy()
                
                # Status de Gemma avec animation
                gemma_status = tk.Label(widget, text="🧠 Gemma 3n: Loading...",
                                      font=self.fonts['body'], bg=self.colors['white'],
                                      fg=self.colors['warning'])
                gemma_status.pack(anchor=tk.W, pady=(0, 10))
                
                # Bouton d'analyse ultra-moderne
                self.app.analyze_button = tk.Button(widget, text="🔬 Start AI Analysis",
                                                  font=self.fonts['label_large'],
                                                  bg=self.colors['success'], fg='white',
                                                  borderwidth=0, relief='flat', cursor='hand2',
                                                  command=self.app.analyze_image,
                                                  state='disabled', pady=16)
                self.app.analyze_button.pack(fill=tk.X, pady=(0, 10))
                
                # Progress mini
                mini_progress = ttk.Progressbar(widget, mode='indeterminate', length=200)
                mini_progress.pack(fill=tk.X, pady=(0, 5))
                
                # Métrique temps réel
                time_label = tk.Label(widget, text="Ready for analysis",
                                    font=self.fonts['caption'], bg=self.colors['white'],
                                    fg=self.colors['text_tertiary'])
                time_label.pack(anchor=tk.W)
                
                self.add_button_animations(self.app.analyze_button)
                break
            
    def create_smart_system_card_fixed(self):
        """Carte système intelligente avec métriques live - VERSION CORRIGÉE"""
        card_frame = self.create_glass_card("⚡ System Intelligence", "", 
                                          self.colors['gradient_primary'], 'large')
        
        # Contenu intelligent
        for widget in card_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == self.colors['white']:
                for child in widget.winfo_children():
                    child.destroy()
                
                # Grid pour les modules
                modules_grid = tk.Frame(widget, bg=self.colors['white'])
                modules_grid.pack(fill=tk.BOTH, expand=True)
                
                # Créer les status modules modernes
                self.create_modern_module_status_fixed(modules_grid)
                break
            
    def create_modern_module_status_fixed(self, parent):
        """Status des modules avec design moderne - VERSION CORRIGÉE"""
        self.app.module_status = {}
        
        modules = [
            ('gemma', '🧠 Gemma 3n', 'Initializing...'),
            ('eye_detector', '👁️ Eye Detection', 'Waiting...'),
            ('face_handler', '👤 Face Tracking', 'Waiting...'),
            ('visualizer', '🎨 Visualization', 'Waiting...')
        ]
        
        for i, (key, name, status) in enumerate(modules):
            # Container pour chaque module
            module_container = tk.Frame(parent, bg=self.colors['light_gray'], relief='flat')
            module_container.pack(fill=tk.X, pady=3, padx=5)
            
            # Status dot avec animation
            status_frame = tk.Frame(module_container, bg=self.colors['light_gray'])
            status_frame.pack(side=tk.LEFT, padx=10, pady=8)
            
            status_dot = tk.Label(status_frame, text="●", font=('Arial', 12),
                                bg=self.colors['light_gray'], fg=self.colors['warning'])
            status_dot.pack()
            
            # Texte du module
            text_frame = tk.Frame(module_container, bg=self.colors['light_gray'])
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=8)
            
            module_name = tk.Label(text_frame, text=name, font=self.fonts['label'],
                                 bg=self.colors['light_gray'], fg=self.colors['text_primary'])
            module_name.pack(anchor=tk.W)
            
            module_status = tk.Label(text_frame, text=status, font=self.fonts['caption'],
                                   bg=self.colors['light_gray'], fg=self.colors['text_secondary'])
            module_status.pack(anchor=tk.W)
            
            # Stocker pour updates - STRUCTURE COMPATIBLE
            self.app.module_status[key] = module_status  # Compatibilité avec le code existant
            
            # Stocker aussi la version complète pour l'interface moderne
            if not hasattr(self.app, 'module_status_enhanced'):
                self.app.module_status_enhanced = {}
            
            self.app.module_status_enhanced[key] = {
                'dot': status_dot,
                'name': module_name,
                'status': module_status,
                'container': module_container
            }
            
            # Animation de pulse pour les dots
            self.animate_status_dot(status_dot)
    
    def create_enhanced_progress_card_fixed(self):
        """Carte de progression avec visualisations avancées - VERSION CORRIGÉE"""
        card_frame = self.create_glass_card("📊 Analysis Progress", "", 
                                          self.colors['gradient_medical'], 'medium')
        
        # Trouver le content frame
        content_frame = None
        for widget in card_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == self.colors['white']:
                content_frame = widget
                break
            
        if content_frame:
            # Nettoyer le contenu existant
            for child in content_frame.winfo_children():
                child.destroy()
            
            # Barre de progression moderne
            self.app.progress = ttk.Progressbar(content_frame, mode='determinate')
            self.app.progress.pack(fill=tk.X, pady=(0, 10))
            
            # Label de progression
            self.app.progress_label = tk.Label(content_frame, text="Ready for analysis",
                                              font=self.fonts['caption'],
                                              bg=self.colors['white'],
                                              fg=self.colors['text_secondary'])
            self.app.progress_label.pack(anchor=tk.W)
    
    def create_modern_settings_card_fixed(self):
        """Carte de paramètres moderne - VERSION CORRIGÉE"""
        card_frame = self.create_glass_card("⚙️ Analysis Settings", "", 
                                          self.colors['gradient_ai'], 'large')
        
        for widget in card_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == self.colors['white']:
                for child in widget.winfo_children():
                    child.destroy()
                
                # Seuil de confiance
                conf_frame = tk.Frame(widget, bg=self.colors['white'])
                conf_frame.pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(conf_frame, text="Confidence Threshold:",
                        font=self.fonts['label'], bg=self.colors['white'],
                        fg=self.colors['text_primary']).pack(anchor=tk.W)
                
                self.app.confidence_var = tk.DoubleVar(value=0.5)
                confidence_scale = ttk.Scale(conf_frame, from_=0.1, to=0.9,
                                           variable=self.app.confidence_var,
                                           orient=tk.HORIZONTAL)
                confidence_scale.pack(fill=tk.X, pady=2)
                
                # Options avec checkboxes modernes
                self.app.face_tracking_var = tk.BooleanVar(value=True)
                face_cb = tk.Checkbutton(widget, text="🔍 Enable Face Tracking",
                                       variable=self.app.face_tracking_var,
                                       font=self.fonts['body'], bg=self.colors['white'],
                                       fg=self.colors['text_primary'])
                face_cb.pack(anchor=tk.W, pady=2)
                
                self.app.enhanced_detection_var = tk.BooleanVar(value=True)
                enhanced_cb = tk.Checkbutton(widget, text="🚀 Enhanced Detection",
                                           variable=self.app.enhanced_detection_var,
                                           font=self.fonts['body'], bg=self.colors['white'],
                                           fg=self.colors['text_primary'])
                enhanced_cb.pack(anchor=tk.W, pady=2)
                
                # Métriques de session
                self.app.metrics_label = tk.Label(widget, text="No analysis yet",
                                                 font=self.fonts['caption'],
                                                 bg=self.colors['white'],
                                                 fg=self.colors['text_tertiary'])
                self.app.metrics_label.pack(anchor=tk.W, pady=(10, 0))
                
                break
            
    def create_micro_interactions_card_fixed(self):
        """Carte avec micro-interactions pour les actions - VERSION CORRIGÉE"""
        card_frame = self.create_glass_card("💾 Smart Actions", "", 
                                          self.colors['gradient_primary'], 'large')
        
        for widget in card_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == self.colors['white']:
                for child in widget.winfo_children():
                    child.destroy()
                
                # Boutons d'action avec effets
                actions = [
                    ("📊 Export Results", self.app.export_results),
                    ("🏥 Medical Report", self.app.generate_medical_report),
                    ("🧠 AI Recommendations", self.app.generate_recommendations),
                    ("👤 Patient Summary", self.app.show_face_tracking_summary),
                    ("⚙️ System Info", self.app.show_system_info)
                ]
                
                for text, command in actions:
                    btn = tk.Button(widget, text=text, command=command,
                                  font=self.fonts['label'], bg=self.colors['primary_blue'],
                                  fg='white', borderwidth=0, relief='flat',
                                  cursor='hand2', pady=8)
                    btn.pack(fill=tk.X, pady=2)
                    self.add_button_animations(btn)
                
                break
                        