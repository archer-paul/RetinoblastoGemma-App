"""
Module d'animations avancées pour RetinoblastoGemma v6
Effets visuels pour créer l'impact "wahou"
"""
import tkinter as tk
import math
import time
import threading
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

class AdvancedAnimations:
    """Gestionnaire d'animations avancées"""
    
    def __init__(self, root):
        self.root = root
        self.running_animations = []
        self.animation_speed = 60  # FPS
        
    def create_particle_system(self, canvas, x, y, color='#4285f4', count=20):
        """Crée un système de particules pour les succès"""
        particles = []
        
        for _ in range(count):
            particle = {
                'x': x,
                'y': y,
                'vx': (math.random() - 0.5) * 4,
                'vy': (math.random() - 0.5) * 4,
                'life': 1.0,
                'size': math.random() * 3 + 1
            }
            particles.append(particle)
        
        def animate_particles():
            for particle in particles[:]:
                # Update position
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += 0.1  # Gravity
                particle['life'] -= 0.02
                
                if particle['life'] <= 0:
                    particles.remove(particle)
                else:
                    # Draw particle
                    alpha = int(particle['life'] * 255)
                    size = particle['size'] * particle['life']
                    
                    canvas.create_oval(
                        particle['x'] - size, particle['y'] - size,
                        particle['x'] + size, particle['y'] + size,
                        fill=color, outline='', tags='particle'
                    )
            
            # Continue animation
            if particles:
                self.root.after(16, animate_particles)  # ~60 FPS
        
        animate_particles()
    
    def morphing_progress_bar(self, progress_widget, target_value, duration=1000):
        """Barre de progression avec morphing fluide"""
        start_value = progress_widget['value']
        start_time = time.time()
        
        def update_progress():
            elapsed = (time.time() - start_time) * 1000
            if elapsed < duration:
                # Easing function (ease-out)
                progress = elapsed / duration
                eased_progress = 1 - (1 - progress) ** 3
                
                current_value = start_value + (target_value - start_value) * eased_progress
                progress_widget['value'] = current_value
                
                self.root.after(16, update_progress)
            else:
                progress_widget['value'] = target_value
        
        update_progress()
    
    def breathing_animation(self, widget, color1, color2, duration=2000):
        """Animation de respiration pour les éléments d'attente"""
        start_time = time.time()
        
        def breathe():
            elapsed = (time.time() - start_time) * 1000
            cycle_position = (elapsed % duration) / duration
            
            # Fonction sinusoïdale pour respiration naturelle
            alpha = (math.sin(cycle_position * 2 * math.pi) + 1) / 2
            
            # Interpolation des couleurs
            r1, g1, b1 = self.hex_to_rgb(color1)
            r2, g2, b2 = self.hex_to_rgb(color2)
            
            r = int(r1 + (r2 - r1) * alpha)
            g = int(g1 + (g2 - g1) * alpha)
            b = int(b1 + (b2 - b1) * alpha)
            
            new_color = f'#{r:02x}{g:02x}{b:02x}'
            
            try:
                widget.config(bg=new_color)
                self.root.after(50, breathe)
            except tk.TclError:
                # Widget destroyed
                pass
        
        breathe()
    
    def typewriter_effect(self, text_widget, text, delay=50):
        """Effet machine à écrire pour le texte"""
        text_widget.delete(1.0, tk.END)
        
        def type_char(index=0):
            if index < len(text):
                text_widget.insert(tk.END, text[index])
                text_widget.see(tk.END)
                self.root.after(delay, lambda: type_char(index + 1))
        
        type_char()
    
    def slide_in_animation(self, widget, direction='left', duration=500):
        """Animation de glissement d'entrée"""
        start_x = widget.winfo_x()
        start_y = widget.winfo_y()
        
        # Position de départ selon la direction
        if direction == 'left':
            start_offset_x = -widget.winfo_width()
            start_offset_y = 0
        elif direction == 'right':
            start_offset_x = widget.winfo_width()
            start_offset_y = 0
        elif direction == 'top':
            start_offset_x = 0
            start_offset_y = -widget.winfo_height()
        else:  # bottom
            start_offset_x = 0
            start_offset_y = widget.winfo_height()
        
        widget.place(x=start_x + start_offset_x, y=start_y + start_offset_y)
        
        start_time = time.time()
        
        def animate():
            elapsed = (time.time() - start_time) * 1000
            if elapsed < duration:
                progress = elapsed / duration
                # Easing ease-out
                eased_progress = 1 - (1 - progress) ** 3
                
                current_x = start_x + start_offset_x * (1 - eased_progress)
                current_y = start_y + start_offset_y * (1 - eased_progress)
                
                widget.place(x=current_x, y=current_y)
                self.root.after(16, animate)
            else:
                widget.place(x=start_x, y=start_y)
        
        animate()
    
    def pulse_animation(self, widget, scale_factor=1.1, duration=600):
        """Animation de pulse pour attirer l'attention"""
        original_font = widget.cget('font')
        if isinstance(original_font, str):
            # Parse font string
            font_parts = original_font.split()
            family = font_parts[0] if font_parts else 'Arial'
            size = int(font_parts[1]) if len(font_parts) > 1 else 12
            weight = font_parts[2] if len(font_parts) > 2 else 'normal'
        else:
            family, size, weight = original_font
        
        start_time = time.time()
        original_size = size
        
        def pulse():
            elapsed = (time.time() - start_time) * 1000
            if elapsed < duration:
                # Fonction sinusoïdale pour pulse naturel
                cycle_position = (elapsed / duration) * 2 * math.pi
                scale = 1 + (scale_factor - 1) * (math.sin(cycle_position) + 1) / 2
                
                new_size = int(original_size * scale)
                new_font = (family, new_size, weight)
                
                try:
                    widget.config(font=new_font)
                    self.root.after(16, pulse)
                except tk.TclError:
                    pass
            else:
                widget.config(font=original_font)
        
        pulse()
    
    def loading_dots_animation(self, label_widget, base_text="Loading"):
        """Animation de points de chargement"""
        dots_count = 0
        
        def animate_dots():
            nonlocal dots_count
            dots = "." * (dots_count % 4)
            spaces = " " * (3 - len(dots))
            
            try:
                label_widget.config(text=f"{base_text}{dots}{spaces}")
                dots_count += 1
                self.root.after(400, animate_dots)
            except tk.TclError:
                pass
        
        animate_dots()
    
    def gradient_shift_animation(self, canvas, colors, duration=3000):
        """Animation de décalage de gradient"""
        start_time = time.time()
        
        def shift_gradient():
            elapsed = (time.time() - start_time) * 1000
            cycle_position = (elapsed % duration) / duration
            
            # Rotation des couleurs
            color_count = len(colors)
            for i in range(canvas.winfo_height()):
                # Calcul de l'index de couleur avec décalage
                color_index = ((i / canvas.winfo_height()) + cycle_position) % 1
                color_index *= (color_count - 1)
                
                base_index = int(color_index)
                next_index = (base_index + 1) % color_count
                blend_factor = color_index - base_index
                
                # Interpolation entre les couleurs
                color1 = colors[base_index]
                color2 = colors[next_index]
                
                r1, g1, b1 = self.hex_to_rgb(color1)
                r2, g2, b2 = self.hex_to_rgb(color2)
                
                r = int(r1 + (r2 - r1) * blend_factor)
                g = int(g1 + (g2 - g1) * blend_factor)
                b = int(b1 + (b2 - b1) * blend_factor)
                
                color = f'#{r:02x}{g:02x}{b:02x}'
                canvas.create_line(0, i, canvas.winfo_width(), i, fill=color, tags='gradient')
            
            self.root.after(50, shift_gradient)
        
        shift_gradient()
    
    def success_celebration_animation(self, parent_widget):
        """Animation de célébration pour succès"""
        # Créer un overlay temporaire
        overlay = tk.Frame(parent_widget, bg='white')
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Canvas pour les effets
        canvas = tk.Canvas(overlay, bg='white', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Icône de succès centrale
        center_x = canvas.winfo_reqwidth() // 2
        center_y = canvas.winfo_reqheight() // 2
        
        success_icon = canvas.create_text(center_x, center_y, text="✅", 
                                        font=('Arial', 48), fill='#34a853')
        
        # Animation d'apparition avec scale
        start_time = time.time()
        
        def animate_success():
            elapsed = (time.time() - start_time) * 1000
            
            if elapsed < 500:  # Scale up
                scale = elapsed / 500
                size = int(48 * scale)
                canvas.itemconfig(success_icon, font=('Arial', size))
                
                self.root.after(16, animate_success)
            elif elapsed < 2000:  # Hold
                # Système de particules
                if elapsed == 500:  # Premier frame de hold
                    self.create_particle_system(canvas, center_x, center_y, '#34a853', 30)
                
                self.root.after(16, animate_success)
            else:  # Fade out
                alpha = max(0, 1 - (elapsed - 2000) / 500)
                if alpha > 0:
                    # Simuler fade avec couleur
                    gray_value = int(255 * (1 - alpha))
                    fade_color = f'#{gray_value:02x}{gray_value:02x}{gray_value:02x}'
                    overlay.config(bg=fade_color)
                    self.root.after(16, animate_success)
                else:
                    overlay.destroy()
        
        self.root.after(100, animate_success)  # Délai pour initialisation
    
    def hex_to_rgb(self, hex_color):
        """Convertit hex en RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_glass_effect(self, widget, blur_radius=10):
        """Crée un effet de verre/glassmorphism"""
        try:
            # Simuler glassmorphism avec transparence et flou
            original_bg = widget.cget('bg')
            
            # Créer un effet de flou simulé avec des couleurs légères
            glass_color = self.blend_colors(original_bg, '#ffffff', 0.3)
            widget.config(bg=glass_color)
            
            # Border pour effet glassmorphism
            widget.config(highlightbackground='#ffffff', highlightthickness=1)
            
        except Exception as e:
            print(f"Glass effect error: {e}")
    
    def blend_colors(self, color1, color2, factor):
        """Mélange deux couleurs"""
        try:
            r1, g1, b1 = self.hex_to_rgb(color1)
            r2, g2, b2 = self.hex_to_rgb(color2)
            
            r = int(r1 + (r2 - r1) * factor)
            g = int(g1 + (g2 - g1) * factor)
            b = int(b1 + (b2 - b1) * factor)
            
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return color1

class MicroInteractions:
    """Gestionnaire de micro-interactions"""
    
    def __init__(self, root):
        self.root = root
        
    def add_hover_scale(self, widget, scale_factor=1.05):
        """Ajoute un effet de scale au hover"""
        def on_enter(e):
            # Simuler scale avec padding
            current_padx = widget.cget('padx') or 0
            current_pady = widget.cget('pady') or 0
            
            new_padx = int(current_padx * scale_factor)
            new_pady = int(current_pady * scale_factor)
            
            widget.config(padx=new_padx, pady=new_pady)
        
        def on_leave(e):
            # Restaurer padding original
            widget.config(padx=0, pady=0)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def add_ripple_effect(self, widget, color='#4285f4'):
        """Ajoute un effet de ripple au clic"""
        def on_click(e):
            # Créer un overlay temporaire pour le ripple
            overlay = tk.Frame(widget, bg=color)
            overlay.place(x=e.x-10, y=e.y-10, width=20, height=20)
            
            # Animer l'expansion
            def expand_ripple(size=20):
                if size < 100:
                    overlay.place(x=e.x-size//2, y=e.y-size//2, 
                                width=size, height=size)
                    self.root.after(20, lambda: expand_ripple(size + 10))
                else:
                    overlay.destroy()
            
            expand_ripple()
        
        widget.bind("<Button-1>", on_click)
    
    def add_magnetic_hover(self, widget, strength=5):
        """Ajoute un effet magnétique au cursor"""
        def on_motion(e):
            # Calculer l'offset vers le cursor
            widget_center_x = widget.winfo_width() // 2
            widget_center_y = widget.winfo_height() // 2
            
            offset_x = (e.x - widget_center_x) // strength
            offset_y = (e.y - widget_center_y) // strength
            
            # Appliquer l'offset (simulé avec padding asymétrique)
            widget.config(padx=(max(0, -offset_x), max(0, offset_x)),
                         pady=(max(0, -offset_y), max(0, offset_y)))
        
        def on_leave(e):
            widget.config(padx=0, pady=0)
        
        widget.bind("<Motion>", on_motion)
        widget.bind("<Leave>", on_leave)

# Export des classes principales
__all__ = ['AdvancedAnimations', 'MicroInteractions']