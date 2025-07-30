"""
Visualization V2 - Module de visualisation modulaire pour RetinoblastoGemma
Gère l'affichage des résultats avec support pour images complètes et croppées
Optimisé pour le hackathon Google Gemma
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Union, Tuple
import json

logger = logging.getLogger(__name__)

class VisualizationV2:
    """Gestionnaire de visualisation avec support pour images complètes et croppées"""
    
    def __init__(self):
        # Configuration des couleurs - thème médical moderne
        self.colors = {
            'safe': (46, 204, 113),      # Vert pour résultats normaux
            'warning': (241, 196, 15),    # Jaune pour surveillance
            'danger': (231, 76, 60),      # Rouge pour urgence
            'critical': (192, 57, 43),    # Rouge foncé pour critique
            'info': (52, 152, 219),       # Bleu pour information
            'background': (236, 240, 241), # Gris clair
            'text_dark': (44, 62, 80),    # Texte sombre
            'text_light': (255, 255, 255), # Texte clair
            'accent': (155, 89, 182)      # Violet pour accents
        }
        
        # Symboles d'alerte
        self.symbols = {
            'safe': '✅',
            'warning': '⚠️',
            'danger': '🚨',
            'critical': '🔴',
            'info': 'ℹ️',
            'medical': '🏥',
            'eye': '👁️'
        }
        
        # Configuration des polices
        self.fonts = self._initialize_fonts()
        
        # Modes de visualisation
        self.visualization_modes = {
            'full_image': 'Image complète avec annotations',
            'cropped_focus': 'Focus sur régions croppées',
            'mixed_view': 'Vue mixte adaptative'
        }
        
        logger.info("✅ VisualizationV2 initialized")
    
    def _initialize_fonts(self):
        """Initialise les polices avec fallbacks robustes"""
        fonts = {}
        
        # Tailles de police
        sizes = {
            'title': 24,
            'subtitle': 18,
            'normal': 14,
            'small': 11,
            'tiny': 9
        }
        
        # Essayer différentes polices système
        font_candidates = [
            "arial.ttf", "Arial.ttf", "arial.ttc",
            "calibri.ttf", "Calibri.ttf",
            "segoeui.ttf", "tahoma.ttf",
            "DejaVuSans.ttf", "liberation-sans.ttf"
        ]
        
        for size_name, size in sizes.items():
            fonts[size_name] = None
            
            # Essayer de charger une police système
            for font_name in font_candidates:
                try:
                    fonts[size_name] = ImageFont.truetype(font_name, size)
                    break
                except (OSError, IOError):
                    continue
            
            # Fallback vers police par défaut
            if fonts[size_name] is None:
                try:
                    fonts[size_name] = ImageFont.load_default()
                except:
                    fonts[size_name] = None
        
        logger.info("Fonts initialized with fallbacks")
        return fonts
    
    def create_annotated_image(
        self, 
        image_path: str, 
        detection_results: Dict, 
        analysis_results: Dict, 
        face_tracking_results: Optional[Dict] = None
    ) -> Optional[Image.Image]:
        """
        Crée une image annotée avec les résultats d'analyse
        Gère automatiquement les images complètes et croppées
        """
        try:
            # Charger l'image originale
            original_image = Image.open(image_path).convert('RGB')
            
            # Déterminer le mode de visualisation optimal
            viz_mode = self._determine_visualization_mode(
                original_image, detection_results
            )
            
            logger.info(f"Using visualization mode: {viz_mode}")
            
            # Créer l'image annotée selon le mode
            if viz_mode == 'full_image':
                annotated_image = self._create_full_image_annotation(
                    original_image, detection_results, analysis_results, face_tracking_results
                )
            elif viz_mode == 'cropped_focus':
                annotated_image = self._create_cropped_focus_annotation(
                    original_image, detection_results, analysis_results
                )
            else:  # mixed_view
                annotated_image = self._create_mixed_view_annotation(
                    original_image, detection_results, analysis_results, face_tracking_results
                )
            
            return annotated_image
            
        except Exception as e:
            logger.error(f"Error creating annotated image: {e}")
            return None
    
    def _determine_visualization_mode(self, image: Image.Image, detection_results: Dict) -> str:
        """Détermine le mode de visualisation optimal"""
        try:
            w, h = image.size
            aspect_ratio = w / h
            
            # Mode basé sur les résultats de détection
            detection_mode = detection_results.get('method', '')
            total_regions = detection_results.get('total_regions', 0)
            
            # Si détection sur image croppée
            if 'cropped' in detection_mode or aspect_ratio > 2.5:
                return 'cropped_focus'
            
            # Si détection sur visage complet avec régions
            elif 'full_face' in detection_mode and total_regions > 0:
                return 'full_image'
            
            # Mode mixte par défaut
            else:
                return 'mixed_view'
                
        except Exception as e:
            logger.error(f"Error determining visualization mode: {e}")
            return 'mixed_view'
    
    def _create_full_image_annotation(
        self, 
        image: Image.Image, 
        detection_results: Dict, 
        analysis_results: Dict, 
        face_tracking_results: Optional[Dict]
    ) -> Image.Image:
        """Crée une annotation pour image complète avec visages détectés"""
        try:
            # Créer une copie de l'image pour annotation
            annotated = image.copy()
            draw = ImageDraw.Draw(annotated)
            
            # Ajouter le titre global
            self._draw_main_header(draw, annotated.size, "RETINOBLASTOMA ANALYSIS - FULL IMAGE")
            
            # Annoter chaque région détectée
            regions = detection_results.get('regions', [])
            results = analysis_results.get('results', [])
            
            for i, region in enumerate(regions):
                # Trouver le résultat d'analyse correspondant
                result = self._find_matching_result(region, results, i)
                
                if result:
                    self._draw_eye_region_annotation(
                        draw, region, result, annotated.size
                    )
            
            # Ajouter les informations de tracking facial
            if face_tracking_results:
                self._draw_face_tracking_info(
                    draw, annotated.size, face_tracking_results
                )
            
            # Ajouter le résumé global
            self._draw_analysis_summary(
                draw, annotated.size, analysis_results, 'bottom'
            )
            
            # Ajouter metadata
            self._draw_metadata_footer(draw, annotated.size, analysis_results)
            
            return annotated
            
        except Exception as e:
            logger.error(f"Error in full image annotation: {e}")
            return image
    
    def _create_cropped_focus_annotation(
        self, 
        image: Image.Image, 
        detection_results: Dict, 
        analysis_results: Dict
    ) -> Image.Image:
        """Crée une annotation pour images croppées (focus sur yeux)"""
        try:
            # Pour images croppées, créer une vue avec layout optimisé
            w, h = image.size
            
            # Créer une image étendue pour annotations
            extended_height = h + 200  # Espace pour annotations
            extended_image = Image.new('RGB', (w, extended_height), self.colors['background'])
            
            # Coller l'image originale
            extended_image.paste(image, (0, 100))
            draw = ImageDraw.Draw(extended_image)
            
            # Titre spécialisé pour vue croppée
            self._draw_main_header(draw, extended_image.size, "RETINOBLASTOMA ANALYSIS - EYE FOCUS")
            
            # Analyser les régions (souvent l'image entière ou moitiés)
            regions = detection_results.get('regions', [])
            results = analysis_results.get('results', [])
            
            if len(regions) == 1:
                # Une seule région (œil unique)
                self._draw_single_eye_analysis(
                    draw, extended_image.size, regions[0], 
                    results[0] if results else None
                )
            elif len(regions) == 2:
                # Deux régions (yeux gauche/droit)
                self._draw_dual_eye_analysis(
                    draw, extended_image.size, regions, results
                )
            else:
                # Multiple régions - layout adaptatif
                self._draw_multiple_regions_analysis(
                    draw, extended_image.size, regions, results
                )
            
            # Résumé en bas
            self._draw_analysis_summary(
                draw, extended_image.size, analysis_results, 'bottom'
            )
            
            return extended_image
            
        except Exception as e:
            logger.error(f"Error in cropped focus annotation: {e}")
            return image
    
    def _create_mixed_view_annotation(
        self, 
        image: Image.Image, 
        detection_results: Dict, 
        analysis_results: Dict, 
        face_tracking_results: Optional[Dict]
    ) -> Image.Image:
        """Crée une annotation en mode mixte (adaptatif)"""
        try:
            # Commencer par l'annotation complète
            annotated = self._create_full_image_annotation(
                image, detection_results, analysis_results, face_tracking_results
            )
            
            # Ajouter des éléments spécialisés selon le contexte
            draw = ImageDraw.Draw(annotated)
            
            # Indicateur de mode mixte
            mode_indicator = "🔄 ADAPTIVE MODE"
            self._draw_text_with_background(
                draw, (10, annotated.size[1] - 40), mode_indicator,
                self.colors['info'], self.colors['text_light'], self.fonts['small']
            )
            
            return annotated
            
        except Exception as e:
            logger.error(f"Error in mixed view annotation: {e}")
            return image
    
    def _draw_main_header(self, draw: ImageDraw.Draw, image_size: Tuple[int, int], title: str):
        """Dessine l'en-tête principal"""
        try:
            w, h = image_size
            
            # Fond pour l'en-tête
            header_height = 80
            draw.rectangle([0, 0, w, header_height], fill=self.colors['accent'])
            
            # Titre principal
            title_font = self.fonts.get('title') or self.fonts.get('normal')
            self._draw_text_centered(
                draw, (w // 2, 25), title, 
                self.colors['text_light'], title_font
            )
            
            # Sous-titre avec info hackathon
            subtitle = "🏆 Google Gemma Hackathon - 100% Local AI"
            subtitle_font = self.fonts.get('small') or self.fonts.get('normal')
            self._draw_text_centered(
                draw, (w // 2, 50), subtitle,
                self.colors['text_light'], subtitle_font
            )
            
        except Exception as e:
            logger.error(f"Error drawing main header: {e}")
    
    def _draw_eye_region_annotation(
        self, 
        draw: ImageDraw.Draw, 
        region: Dict, 
        result: Dict, 
        image_size: Tuple[int, int]
    ):
        """Dessine l'annotation pour une région oculaire avec cadres colorés"""
        try:
            bbox = region.get('bbox')
            if not bbox:
                return
            
            x, y, w, h = bbox
            
            # Déterminer la couleur et le style selon les résultats
            style = self._get_annotation_style(result)
            
            # === CADRE PRINCIPAL AUTOUR DE L'ŒIL ===
            # Rectangle principal avec épaisseur variable
            rect_coords = (x, y, x + w, y + h)
            
            # Dessiner rectangle principal
            draw.rectangle(rect_coords, outline=style['color'], width=style['width'])
            
            # Effet de surbrillance pour les cas critiques
            if style['width'] >= 5:
                # Rectangle intérieur pour effet 3D
                margin = 2
                inner_coords = (x + margin, y + margin, x + w - margin, y + h - margin)
                draw.rectangle(inner_coords, outline=style['color'], width=2)
                
                # Points de corner pour attirer l'attention
                corner_size = 10
                corners = [
                    (x, y, x + corner_size, y + corner_size),  # Top-left
                    (x + w - corner_size, y, x + w, y + corner_size),  # Top-right
                    (x, y + h - corner_size, x + corner_size, y + h),  # Bottom-left
                    (x + w - corner_size, y + h - corner_size, x + w, y + h)  # Bottom-right
                ]
                
                for corner in corners:
                    draw.rectangle(corner, fill=style['color'])
            
            # === LABELS INFORMATIFS ===
            region_type = region.get('type', 'unknown')
            confidence = result.get('confidence', 0) if result else 0
            detected = result.get('leukocoria_detected', False) if result else False
            
            # Position des labels (éviter les chevauchements)
            label_x = x
            label_y = y - 80 if y > 90 else y + h + 10
            
            # Label principal avec symbole et type d'œil
            main_symbol = style['symbol']
            eye_type_display = region_type.replace('_face_', ' ').replace('_', ' ').upper()
            main_text = f"{main_symbol} {eye_type_display}"
            
            self._draw_text_with_background(
                draw, (label_x, label_y), main_text,
                style['color'], self.colors['text_light'], 
                self.fonts.get('normal')
            )
            
            # Label de statut (DÉTECTÉ/NORMAL)
            status_text = "⚠️ LEUKOCORIA DETECTED" if detected else "✅ NORMAL"
            status_color = self.colors['critical'] if detected else self.colors['safe']
            
            self._draw_text_with_background(
                draw, (label_x, label_y + 25), status_text,
                status_color, self.colors['text_light'],
                self.fonts.get('small')
            )
            
            # Label de confiance avec couleur adaptée
            conf_text = f"Confidence: {confidence:.1f}%"
            conf_color = style['color'] if detected else self.colors['info']
            
            self._draw_text_with_background(
                draw, (label_x, label_y + 45), conf_text,
                self.colors['background'], conf_color,
                self.fonts.get('small')
            )
            
            # Indicateur d'urgence pour les cas critiques
            if result and result.get('urgency') == 'immediate':
                urgency_text = "🚨 IMMEDIATE CONSULTATION"
                self._draw_text_with_background(
                    draw, (label_x, label_y + 65), urgency_text,
                    self.colors['critical'], self.colors['text_light'],
                    self.fonts.get('small')
                )
            
        except Exception as e:
            logger.error(f"Error drawing eye region annotation: {e}")
    
    def _create_full_image_annotation(
        self, 
        image: Image.Image, 
        detection_results: Dict, 
        analysis_results: Dict, 
        face_tracking_results: Optional[Dict]
    ) -> Image.Image:
        """Crée une annotation pour image complète avec visages ET yeux détectés"""
        try:
            # Créer une copie de l'image pour annotation
            annotated = image.copy()
            draw = ImageDraw.Draw(annotated)
            
            # Ajouter le titre global
            self._draw_main_header(draw, annotated.size, "RETINOBLASTOMA ANALYSIS - FULL IMAGE")
            
            # === DESSINER LES CADRES DE VISAGE D'ABORD ===
            faces_detected = detection_results.get('faces_detected', 0)
            if faces_detected > 0:
                # Estimer les positions de visage à partir des régions oculaires
                self._draw_estimated_face_frames(draw, detection_results, annotated.size)
            
            # === ANNOTER CHAQUE RÉGION OCULAIRE ===
            regions = detection_results.get('regions', [])
            results = analysis_results.get('results', [])
            
            for i, region in enumerate(regions):
                # Trouver le résultat d'analyse correspondant
                result = self._find_matching_result(region, results, i)
                
                if result:
                    self._draw_eye_region_annotation(
                        draw, region, result, annotated.size
                    )
            
            # Ajouter les informations de tracking facial
            if face_tracking_results:
                self._draw_face_tracking_info(
                    draw, annotated.size, face_tracking_results
                )
            
            # Ajouter le résumé global
            self._draw_analysis_summary(
                draw, annotated.size, analysis_results, 'bottom'
            )
            
            # Ajouter metadata
            self._draw_metadata_footer(draw, annotated.size, analysis_results)
            
            return annotated
            
        except Exception as e:
            logger.error(f"Error in full image annotation: {e}")
            return image
    
    def _draw_estimated_face_frames(self, draw: ImageDraw.Draw, detection_results: Dict, image_size: Tuple[int, int]):
        """Dessine des cadres de visage estimés à partir des régions oculaires"""
        try:
            regions = detection_results.get('regions', [])
            if len(regions) < 1:
                return
            
            # Grouper les yeux par visage (gauche/droit)
            face_groups = self._group_eyes_by_face(regions)
            
            for face_idx, eye_group in enumerate(face_groups):
                if len(eye_group) >= 1:
                    # Calculer la boîte englobante du visage
                    face_bbox = self._estimate_face_bbox_from_eyes(eye_group)
                    
                    if face_bbox:
                        x, y, w, h = face_bbox
                        
                        # Cadre de visage en bleu
                        face_color = self.colors['info']
                        draw.rectangle([x, y, x + w, y + h], outline=face_color, width=3)
                        
                        # Label du visage
                        face_label = f"👤 FACE {face_idx + 1}"
                        label_y = y - 30 if y > 35 else y + h + 5
                        
                        self._draw_text_with_background(
                            draw, (x, label_y), face_label,
                            face_color, self.colors['text_light'],
                            self.fonts.get('normal')
                        )
            
        except Exception as e:
            logger.error(f"Error drawing face frames: {e}")
    
    def _group_eyes_by_face(self, regions: List[Dict]) -> List[List[Dict]]:
        """Groupe les yeux par visage"""
        try:
            # Simple groupement par proximité verticale
            regions_with_y = []
            for region in regions:
                bbox = region.get('bbox')
                if bbox:
                    _, y, _, _ = bbox
                    regions_with_y.append((y, region))
            
            # Trier par position Y
            regions_with_y.sort(key=lambda x: x[0])
            
            # Grouper par proximité (seuil de 100 pixels)
            groups = []
            current_group = []
            last_y = None
            
            for y, region in regions_with_y:
                if last_y is None or abs(y - last_y) < 100:
                    current_group.append(region)
                else:
                    if current_group:
                        groups.append(current_group)
                    current_group = [region]
                last_y = y
            
            if current_group:
                groups.append(current_group)
            
            return groups
            
        except Exception as e:
            logger.error(f"Error grouping eyes by face: {e}")
            return []
    
    def _estimate_face_bbox_from_eyes(self, eye_regions: List[Dict]) -> Optional[Tuple[int, int, int, int]]:
        """Estime la boîte englobante du visage à partir des yeux"""
        try:
            if not eye_regions:
                return None
            
            # Trouver les limites des yeux
            min_x, min_y = float('inf'), float('inf')
            max_x, max_y = 0, 0
            
            for region in eye_regions:
                bbox = region.get('bbox')
                if bbox:
                    x, y, w, h = bbox
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x + w)
                    max_y = max(max_y, y + h)
            
            if min_x == float('inf'):
                return None
            
            # Étendre pour couvrir le visage entier
            eye_width = max_x - min_x
            eye_height = max_y - min_y
            
            # Estimation du visage: environ 2.5x la largeur des yeux, 4x la hauteur
            face_width = max(eye_width * 2.5, eye_width + 100)
            face_height = max(eye_height * 4, eye_height + 150)
            
            # Centrer autour des yeux
            center_x = (min_x + max_x) // 2
            center_y = (min_y + max_y) // 2
            
            face_x = int(center_x - face_width // 2)
            face_y = int(center_y - face_height // 3)  # Yeux dans le tiers supérieur
            
            return (face_x, face_y, int(face_width), int(face_height))
            
        except Exception as e:
            logger.error(f"Error estimating face bbox: {e}")
            return None
    
    def _get_annotation_style(self, result: Dict) -> Dict:
        """Détermine le style d'annotation basé sur les résultats"""
        if not result:
            return {
                'color': self.colors['info'],
                'width': 2,
                'symbol': self.symbols['info']
            }
        
        detected = result.get('leukocoria_detected', False)
        risk_level = result.get('risk_level', 'low')
        urgency = result.get('urgency', 'routine')
        confidence = result.get('confidence', 0)
        
        if not detected:
            return {
                'color': self.colors['safe'],
                'width': 3,
                'symbol': self.symbols['safe']
            }
        
        # Détection positive - gradation selon sévérité
        if urgency == 'immediate' or risk_level == 'high':
            return {
                'color': self.colors['critical'],
                'width': 6,
                'symbol': self.symbols['critical']
            }
        elif urgency == 'urgent' or (risk_level == 'medium' and confidence > 70):
            return {
                'color': self.colors['danger'],
                'width': 5,
                'symbol': self.symbols['danger']
            }
        else:
            return {
                'color': self.colors['warning'],
                'width': 4,
                'symbol': self.symbols['warning']
            }
    
    def _draw_enhanced_rectangle(self, draw: ImageDraw.Draw, coords: Tuple[int, int, int, int], style: Dict):
        """Dessine un rectangle avec style amélioré"""
        try:
            x1, y1, x2, y2 = coords
            color = style['color']
            width = style['width']
            
            # Rectangle principal
            draw.rectangle([x1, y1, x2, y2], outline=color, width=width)
            
            # Effet de profondeur si largeur > 3
            if width > 3:
                # Rectangle intérieur plus fin
                margin = 2
                draw.rectangle([x1 + margin, y1 + margin, x2 - margin, y2 - margin], 
                              outline=color, width=1)
                
                # Coins renforcés pour effet visuel
                corner_size = 8
                corner_coords = [
                    (x1, y1, x1 + corner_size, y1 + corner_size),  # Top-left
                    (x2 - corner_size, y1, x2, y1 + corner_size),  # Top-right
                    (x1, y2 - corner_size, x1 + corner_size, y2),  # Bottom-left
                    (x2 - corner_size, y2 - corner_size, x2, y2)   # Bottom-right
                ]
                
                for corner in corner_coords:
                    draw.rectangle(corner, outline=color, width=2)
            
        except Exception as e:
            logger.error(f"Error drawing enhanced rectangle: {e}")
    
    def _draw_single_eye_analysis(self, draw: ImageDraw.Draw, image_size: Tuple[int, int], region: Dict, result: Dict):
        """Dessine l'analyse pour un œil unique (mode croppé)"""
        try:
            w, h = image_size
            
            # Zone d'information à droite ou en bas
            info_x = w - 300 if w > 400 else 10
            info_y = 120
            
            # Titre de l'analyse
            eye_type = region.get('type', 'eye').upper()
            title = f"🔍 {eye_type} ANALYSIS"
            
            self._draw_text_with_background(
                draw, (info_x, info_y), title,
                self.colors['accent'], self.colors['text_light'],
                self.fonts.get('subtitle')
            )
            
            if result:
                # Résultats détaillés
                details = [
                    f"Detection: {'✅ POSITIVE' if result.get('leukocoria_detected') else '❌ NEGATIVE'}",
                    f"Confidence: {result.get('confidence', 0):.1f}%",
                    f"Risk Level: {result.get('risk_level', 'unknown').upper()}",
                    f"Urgency: {result.get('urgency', 'routine').upper()}"
                ]
                
                for i, detail in enumerate(details):
                    detail_y = info_y + 40 + (i * 20)
                    color = self.colors['danger'] if 'POSITIVE' in detail else self.colors['text_dark']
                    
                    draw.text((info_x, detail_y), detail, fill=color, 
                             font=self.fonts.get('small'))
            
        except Exception as e:
            logger.error(f"Error drawing single eye analysis: {e}")
    
    def _draw_dual_eye_modern_analysis(self, draw: ImageDraw.Draw, image_size: Tuple[int, int], 
                                     regions: List[Dict], results: List[Dict], start_y: int):
        """Analyse moderne pour DEUX yeux (optimisé dataset) - TOUJOURS 2 yeux"""
        try:
            w, h = image_size

            # Deux cartes côte à côte pour les deux yeux
            card_width = (w - 150) // 2  # Espace pour 2 cartes + marges
            card_height = 140
            card_spacing = 25

            left_card_x = 50
            right_card_x = left_card_x + card_width + card_spacing
            card_y = start_y

            # Titre général
            title = "👁️ DUAL EYE ANALYSIS - DATASET MODE"
            title_font = self.fonts.get('subtitle') or self.fonts.get('normal')
            self._draw_text_centered(
                draw, (w // 2, start_y - 30), title,
                self.colors['primary'], title_font
            )

            # Traiter chaque œil
            eye_positions = [
                (left_card_x, "LEFT EYE", "👁️‍🗨️"),
                (right_card_x, "RIGHT EYE", "👁️")
            ]

            for i, (card_x, eye_label, eye_icon) in enumerate(eye_positions):
                if i < len(regions) and i < len(results):
                    region = regions[i]
                    result = results[i]

                    # Carte moderne pour cet œil
                    self._draw_modern_card(
                        draw, 
                        (card_x, card_y, card_x + card_width, card_y + card_height),
                        self.colors['card_bg']
                    )

                    # En-tête de l'œil
                    draw.text((card_x + 15, card_y + 10), f"{eye_icon} {eye_label}", 
                             fill=self.colors['primary'], font=self.fonts.get('normal'))

                    if result:
                        detected = result.get('leukocoria_detected', False)
                        confidence = result.get('confidence', 0)

                        # GROS STATUT VISUEL
                        status_y = card_y + 40
                        if detected:
                            status_text = "🚨 DETECTED"
                            status_color = self.colors['danger']
                            # Fond d'alerte
                            draw.rectangle([card_x + 10, status_y - 5, card_x + card_width - 10, status_y + 25], 
                                         fill=(255, 235, 235))
                        else:
                            status_text = "✅ NORMAL"
                            status_color = self.colors['safe']
                            # Fond normal
                            draw.rectangle([card_x + 10, status_y - 5, card_x + card_width - 10, status_y + 25], 
                                         fill=(235, 255, 235))

                        # Texte du statut
                        status_font = self.fonts.get('normal') or self.fonts.get('small')
                        self._draw_text_centered(
                            draw, (card_x + card_width // 2, status_y + 5), status_text,
                            status_color, status_font
                        )

                        # Barre de confiance compacte
                        conf_y = card_y + 75
                        bar_x = card_x + 15
                        bar_width = card_width - 30
                        bar_height = 6

                        # Fond barre
                        draw.rectangle([bar_x, conf_y, bar_x + bar_width, conf_y + bar_height], 
                                      fill=(220, 220, 220))

                        # Barre de confiance
                        conf_width = int((confidence / 100) * bar_width)
                        conf_color = status_color
                        draw.rectangle([bar_x, conf_y, bar_x + conf_width, conf_y + bar_height], 
                                      fill=conf_color)

                        # Texte confiance
                        conf_text = f"{confidence:.0f}%"
                        self._draw_text_centered(
                            draw, (card_x + card_width // 2, conf_y + 15), conf_text,
                            self.colors['text_dark'], self.fonts.get('small')
                        )

                        # Risk level en bas
                        risk_level = result.get('risk_level', 'unknown')
                        urgency = result.get('urgency', 'routine')

                        if urgency == 'immediate':
                            risk_display = "🔴 HIGH RISK"
                            risk_color = self.colors['danger']
                        elif urgency in ['urgent', 'soon']:
                            risk_display = "🟡 MONITOR"
                            risk_color = self.colors['warning']
                        else:
                            risk_display = "🟢 LOW RISK"
                            risk_color = self.colors['safe']

                        self._draw_text_centered(
                            draw, (card_x + card_width // 2, card_y + 110), risk_display,
                            risk_color, self.fonts.get('small')
                        )

            # Résumé global sous les deux cartes
            summary_y = card_y + card_height + 20
            self._draw_dataset_summary(draw, w, summary_y, regions, results)

        except Exception as e:
            logger.error(f"Error drawing dual eye modern analysis: {e}")

    def _draw_dataset_summary(self, draw: ImageDraw.Draw, width: int, start_y: int, 
                             regions: List[Dict], results: List[Dict]):
        """Résumé global optimisé pour dataset 2 yeux"""
        try:
            # Compter les détections
            total_eyes = len(results)
            positive_eyes = sum(1 for r in results if r.get('leukocoria_detected', False))
            
            # Couleur du résumé
            if positive_eyes >= 2:
                summary_color = self.colors['danger']
                summary_text = f"🚨 BILATERAL LEUKOCORIA - {positive_eyes}/2 EYES AFFECTED"
                priority = "EMERGENCY CONSULTATION REQUIRED"
            elif positive_eyes == 1:
                summary_color = self.colors['warning'] 
                summary_text = f"⚠️ UNILATERAL LEUKOCORIA - {positive_eyes}/2 EYES AFFECTED"
                priority = "URGENT MEDICAL EVALUATION NEEDED"
            else:
                summary_color = self.colors['safe']
                summary_text = f"✅ NO LEUKOCORIA DETECTED - {total_eyes}/2 EYES NORMAL"
                priority = "CONTINUE ROUTINE MONITORING"
            
            # Fond du résumé
            summary_height = 60
            draw.rectangle([30, start_y, width - 30, start_y + summary_height], 
                          fill=summary_color)
            
            # Texte principal
            self._draw_text_centered(
                draw, (width // 2, start_y + 15), summary_text,
                self.colors['text_light'], self.fonts.get('normal')
            )
            
            # Priorité
            self._draw_text_centered(
                draw, (width // 2, start_y + 35), priority,
                self.colors['text_light'], self.fonts.get('small')
            )
            
        except Exception as e:
            logger.error(f"Error drawing dataset summary: {e}")
    
    def _draw_multiple_regions_analysis(self, draw: ImageDraw.Draw, image_size: Tuple[int, int], regions: List[Dict], results: List[Dict]):
        """Dessine l'analyse pour multiples régions"""
        try:
            w, h = image_size
            
            # Résumé compact pour multiples régions
            summary_y = h - 120
            
            draw.rectangle([10, summary_y, w - 10, h - 20],
                          outline=self.colors['accent'], width=2)
            
            # Titre
            title = f"📊 MULTIPLE REGIONS ANALYSIS ({len(regions)} regions)"
            draw.text((20, summary_y + 10), title,
                     fill=self.colors['accent'], font=self.fonts.get('normal'))
            
            # Statistiques rapides
            positive_count = sum(1 for r in results if r and r.get('leukocoria_detected', False))
            avg_confidence = np.mean([r.get('confidence', 0) for r in results if r]) if results else 0
            
            stats = [
                f"Positive detections: {positive_count}/{len(regions)}",
                f"Average confidence: {avg_confidence:.1f}%"
            ]
            
            for i, stat in enumerate(stats):
                draw.text((20, summary_y + 35 + (i * 15)), stat,
                         fill=self.colors['text_dark'], font=self.fonts.get('small'))
            
        except Exception as e:
            logger.error(f"Error drawing multiple regions analysis: {e}")
    
    def _draw_face_tracking_info(self, draw: ImageDraw.Draw, image_size: Tuple[int, int], face_tracking_results: Dict):
        """Dessine les informations de tracking facial"""
        try:
            w, h = image_size
            
            # Position en haut à droite
            info_x = w - 250
            info_y = 90
            
            # Données de tracking
            tracked_faces = face_tracking_results.get('tracked_faces', 0)
            new_faces = face_tracking_results.get('new_faces', 0)
            recognized_faces = face_tracking_results.get('recognized_faces', 0)
            
            # Titre de section
            title = "👤 FACE TRACKING"
            self._draw_text_with_background(
                draw, (info_x, info_y), title,
                self.colors['info'], self.colors['text_light'],
                self.fonts.get('small')
            )
            
            # Informations détaillées
            tracking_info = [
                f"Total faces: {tracked_faces}",
                f"New: {new_faces}",
                f"Recognized: {recognized_faces}"
            ]
            
            for i, info in enumerate(tracking_info):
                draw.text((info_x, info_y + 25 + (i * 15)), info,
                         fill=self.colors['text_dark'], font=self.fonts.get('tiny'))
            
            # Boosts de confiance si disponibles
            confidence_boosts = face_tracking_results.get('confidence_boosts', {})
            if confidence_boosts:
                boost_text = f"🔄 {len(confidence_boosts)} confidence boost(s)"
                draw.text((info_x, info_y + 80), boost_text,
                         fill=self.colors['accent'], font=self.fonts.get('tiny'))
            
        except Exception as e:
            logger.error(f"Error drawing face tracking info: {e}")
    
    def _draw_analysis_summary(self, draw: ImageDraw.Draw, image_size: Tuple[int, int], analysis_results: Dict, position: str = 'bottom'):
        """Dessine le résumé global de l'analyse"""
        try:
            w, h = image_size
            
            # Position selon paramètre
            if position == 'bottom':
                summary_y = h - 60
            else:
                summary_y = 100
            
            # Données du résumé
            results = analysis_results.get('results', [])
            total_analyzed = len(results)
            positive_count = sum(1 for r in results if r.get('leukocoria_detected', False))
            method = analysis_results.get('method', 'unknown')
            processing_time = analysis_results.get('processing_time', 0)
            
            # Déterminer le statut global
            if positive_count > 0:
                status_text = f"🚨 {positive_count} POSITIVE DETECTION(S) - MEDICAL CONSULTATION REQUIRED"
                status_color = self.colors['critical']
                bg_color = self.colors['danger']
            else:
                status_text = f"✅ NO CONCERNING FINDINGS - CONTINUE MONITORING"
                status_color = self.colors['text_light']
                bg_color = self.colors['safe']
            
            # Fond pour le résumé
            summary_height = 50
            draw.rectangle([0, summary_y, w, summary_y + summary_height], fill=bg_color)
            
            # Texte principal
            self._draw_text_centered(
                draw, (w // 2, summary_y + 15), status_text,
                status_color, self.fonts.get('normal')
            )
            
            # Informations techniques en petit
            tech_info = f"Analysis: {method} | Time: {processing_time:.1f}s | Regions: {total_analyzed}"
            self._draw_text_centered(
                draw, (w // 2, summary_y + 35), tech_info,
                status_color, self.fonts.get('tiny')
            )
            
        except Exception as e:
            logger.error(f"Error drawing analysis summary: {e}")
    
    def _draw_metadata_footer(self, draw: ImageDraw.Draw, image_size: Tuple[int, int], analysis_results: Dict):
        """Dessine les métadonnées en pied de page"""
        try:
            w, h = image_size
            
            # Timestamp et informations système
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            footer_text = f"Generated: {timestamp} | RetinoblastoGemma v6 | 🏆 Google Gemma Hackathon"
            
            # Position en bas
            footer_y = h - 15
            
            draw.text((10, footer_y), footer_text,
                     fill=self.colors['text_dark'], font=self.fonts.get('tiny'))
            
        except Exception as e:
            logger.error(f"Error drawing metadata footer: {e}")
    
    def _find_matching_result(self, region: Dict, results: List[Dict], index: int) -> Optional[Dict]:
        """Trouve le résultat d'analyse correspondant à une région"""
        try:
            # Essayer de matcher par region_id
            region_id = region.get('id')
            for result in results:
                if result.get('region_id') == index or result.get('region_id') == region_id:
                    return result
            
            # Fallback: prendre par index si disponible
            if index < len(results):
                return results[index]
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding matching result: {e}")
            return None
    
    def _get_method_display(self, method: str) -> str:
        """Convertit la méthode d'analyse en affichage lisible"""
        method_displays = {
            'multimodal_vision': '🤖 Gemma Vision',
            'text_with_cv_features': '🧠 Gemma + CV',
            'computer_vision_fallback': '👁️ Computer Vision',
            'cv_fallback': '⚙️ Basic CV',
            'fallback': '🔧 Fallback',
            'gemma3n_local': '🚀 Gemma 3n Local',
            'unknown': '❓ Unknown'
        }
        
        return method_displays.get(method, f"📊 {method}")
    
    def _draw_text_with_background(
        self, 
        draw: ImageDraw.Draw, 
        position: Tuple[int, int], 
        text: str,
        bg_color: Tuple[int, int, int], 
        text_color: Tuple[int, int, int], 
        font
    ):
        """Dessine du texte avec fond coloré"""
        try:
            if not font:
                return
            
            x, y = position
            
            # Calculer la taille du texte
            bbox = self._get_text_bbox(draw, text, font)
            
            if bbox:
                text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
                padding = 4
                
                # Dessiner le fond
                draw.rectangle([
                    x - padding, y - padding,
                    x + text_width + padding, y + text_height + padding
                ], fill=bg_color)
            
            # Dessiner le texte
            draw.text(position, text, fill=text_color, font=font)
            
        except Exception as e:
            logger.error(f"Error drawing text with background: {e}")
    
    def _draw_text_centered(
        self, 
        draw: ImageDraw.Draw, 
        position: Tuple[int, int], 
        text: str,
        text_color: Tuple[int, int, int], 
        font
    ):
        """Dessine du texte centré"""
        try:
            if not font:
                return
            
            x, y = position
            
            # Calculer la largeur du texte pour centrage
            bbox = self._get_text_bbox(draw, text, font)
            
            if bbox:
                text_width = bbox[2] - bbox[0]
                centered_x = x - (text_width // 2)
            else:
                # Estimation approximative
                centered_x = x - (len(text) * 4)
            
            draw.text((centered_x, y), text, fill=text_color, font=font)
            
        except Exception as e:
            logger.error(f"Error drawing centered text: {e}")
    
    def _get_text_bbox(self, draw: ImageDraw.Draw, text: str, font) -> Optional[Tuple[int, int, int, int]]:
        """Obtient la bounding box du texte avec gestion des versions Pillow"""
        try:
            # Méthode moderne (Pillow 8.0+)
            if hasattr(draw, 'textbbox'):
                return draw.textbbox((0, 0), text, font=font)
            
            # Méthode héritée (Pillow < 8.0)
            elif hasattr(draw, 'textsize'):
                width, height = draw.textsize(text, font=font)
                return (0, 0, width, height)
            
            # Estimation de fallback
            else:
                estimated_width = len(text) * 8
                estimated_height = 16
                return (0, 0, estimated_width, estimated_height)
                
        except Exception as e:
            logger.error(f"Error getting text bbox: {e}")
            return None
    
    def create_medical_report_image(
        self, 
        analysis_results: Dict, 
        detection_results: Dict,
        face_tracking_results: Optional[Dict] = None,
        person_summary: Optional[Dict] = None
    ) -> Optional[Image.Image]:
        """Crée un rapport médical visuel complet"""
        try:
            # Dimensions du rapport
            report_width = 800
            report_height = 1000
            
            # Créer l'image de base
            report_image = Image.new('RGB', (report_width, report_height), self.colors['background'])
            draw = ImageDraw.Draw(report_image)
            
            # En-tête du rapport
            self._draw_report_header(draw, report_width)
            
            # Section informations patient
            current_y = 120
            if person_summary:
                current_y = self._draw_patient_info_section(draw, report_width, current_y, person_summary)
            
            # Section résultats d'analyse
            current_y = self._draw_analysis_results_section(draw, report_width, current_y, analysis_results)
            
            # Section détection technique
            current_y = self._draw_technical_details_section(draw, report_width, current_y, detection_results)
            
            # Section recommandations
            current_y = self._draw_recommendations_section(draw, report_width, current_y, analysis_results)
            
            # Pied de page
            self._draw_report_footer(draw, report_width, report_height)
            
            return report_image
            
        except Exception as e:
            logger.error(f"Error creating medical report image: {e}")
            return None
    
    def _draw_report_header(self, draw: ImageDraw.Draw, width: int):
        """Dessine l'en-tête du rapport médical"""
        try:
            # Fond de l'en-tête
            header_height = 100
            draw.rectangle([0, 0, width, header_height], fill=self.colors['accent'])
            
            # Titre principal
            title = "🏥 RETINOBLASTOMA SCREENING REPORT"
            self._draw_text_centered(
                draw, (width // 2, 20), title,
                self.colors['text_light'], self.fonts.get('title')
            )
            
            # Sous-titre
            subtitle = "AI-Powered Early Detection System | Gemma 3n Multimodal Analysis"
            self._draw_text_centered(
                draw, (width // 2, 50), subtitle,
                self.colors['text_light'], self.fonts.get('small')
            )
            
            # Ligne de séparation
            draw.line([50, 80, width - 50, 80], fill=self.colors['text_light'], width=2)
            
        except Exception as e:
            logger.error(f"Error drawing report header: {e}")
    
    def _draw_patient_info_section(self, draw: ImageDraw.Draw, width: int, start_y: int, person_summary: Dict) -> int:
        """Dessine la section d'informations patient"""
        try:
            section_height = 100
            
            # Titre de section
            section_title = "👤 PATIENT INFORMATION"
            draw.text((30, start_y), section_title, 
                     fill=self.colors['accent'], font=self.fonts.get('subtitle'))
            
            # Informations patient
            info_y = start_y + 30
            patient_info = [
                f"Patient ID: {person_summary.get('face_id', 'Unknown')}",
                f"First Analysis: {person_summary.get('first_seen', 'Unknown')[:10]}",
                f"Total Analyses: {person_summary.get('total_analyses', 0)}",
                f"Positive Findings: {person_summary.get('positive_analyses', 0)}"
            ]
            
            for i, info in enumerate(patient_info):
                x = 50 + (i % 2) * 300
                y = info_y + (i // 2) * 20
                draw.text((x, y), info, fill=self.colors['text_dark'], font=self.fonts.get('small'))
            
            return start_y + section_height
            
        except Exception as e:
            logger.error(f"Error drawing patient info section: {e}")
            return start_y + 50
    
    def _draw_analysis_results_section(self, draw: ImageDraw.Draw, width: int, start_y: int, analysis_results: Dict) -> int:
        """Dessine la section des résultats d'analyse"""
        try:
            # Titre de section
            section_title = "🔬 ANALYSIS RESULTS"
            draw.text((30, start_y), section_title, 
                     fill=self.colors['accent'], font=self.fonts.get('subtitle'))
            
            results = analysis_results.get('results', [])
            section_height = 60 + (len(results) * 60)
            
            # Résumé global
            total_regions = len(results)
            positive_count = sum(1 for r in results if r.get('leukocoria_detected', False))
            
            summary_y = start_y + 30
            
            # Statut global avec couleur
            if positive_count > 0:
                status_text = f"🚨 POSITIVE FINDINGS: {positive_count}/{total_regions} regions"
                status_color = self.colors['danger']
            else:
                status_text = f"✅ NO CONCERNING FINDINGS: {total_regions} regions analyzed"
                status_color = self.colors['safe']
            
            draw.text((50, summary_y), status_text, fill=status_color, font=self.fonts.get('normal'))
            
            # Détails par région
            details_y = summary_y + 40
            for i, result in enumerate(results):
                region_y = details_y + (i * 60)
                
                # Encadré pour chaque région
                box_height = 50
                box_color = self.colors['danger'] if result.get('leukocoria_detected') else self.colors['safe']
                
                draw.rectangle([50, region_y, width - 50, region_y + box_height], 
                              outline=box_color, width=2)
                
                # Informations de la région
                region_type = result.get('region_type', f'Region {i+1}')
                confidence = result.get('confidence', 0)
                risk_level = result.get('risk_level', 'unknown')
                
                region_text = f"Region: {region_type.upper()}"
                draw.text((60, region_y + 10), region_text, 
                         fill=self.colors['text_dark'], font=self.fonts.get('small'))
                
                conf_text = f"Confidence: {confidence:.1f}%"
                draw.text((60, region_y + 30), conf_text, 
                         fill=self.colors['text_dark'], font=self.fonts.get('small'))
                
                risk_text = f"Risk: {risk_level.upper()}"
                risk_color = self.colors['danger'] if risk_level == 'high' else self.colors['text_dark']
                draw.text((250, region_y + 10), risk_text, 
                         fill=risk_color, font=self.fonts.get('small'))
                
                status_text = "DETECTED" if result.get('leukocoria_detected') else "NORMAL"
                status_color = self.colors['danger'] if result.get('leukocoria_detected') else self.colors['safe']
                draw.text((250, region_y + 30), status_text, 
                         fill=status_color, font=self.fonts.get('small'))
            
            return start_y + section_height
            
        except Exception as e:
            logger.error(f"Error drawing analysis results section: {e}")
            return start_y + 100
    
    def _draw_technical_details_section(self, draw: ImageDraw.Draw, width: int, start_y: int, detection_results: Dict) -> int:
        """Dessine la section des détails techniques"""
        try:
            section_height = 120
            
            # Titre de section
            section_title = "⚙️ TECHNICAL DETAILS"
            draw.text((30, start_y), section_title, 
                     fill=self.colors['accent'], font=self.fonts.get('subtitle'))
            
            # Détails techniques
            tech_y = start_y + 30
            
            method = detection_results.get('method', 'unknown')
            total_regions = detection_results.get('total_regions', 0)
            faces_detected = detection_results.get('faces_detected', 0)
            
            tech_details = [
                f"Detection Method: {method}",
                f"Regions Analyzed: {total_regions}",
                f"Faces Detected: {faces_detected}",
                f"AI Model: Gemma 3n Multimodal (Local)",
                f"Processing: 100% Offline",
                f"Privacy: Complete - No data transmitted"
            ]
            
            for i, detail in enumerate(tech_details):
                x = 50 + (i % 2) * 300
                y = tech_y + (i // 2) * 20
                draw.text((x, y), detail, fill=self.colors['text_dark'], font=self.fonts.get('small'))
            
            return start_y + section_height
            
        except Exception as e:
            logger.error(f"Error drawing technical details section: {e}")
            return start_y + 80
    
    def _draw_recommendations_section(self, draw: ImageDraw.Draw, width: int, start_y: int, analysis_results: Dict) -> int:
        """Dessine la section des recommandations"""
        try:
            section_height = 200
            
            # Titre de section
            section_title = "📋 MEDICAL RECOMMENDATIONS"
            draw.text((30, start_y), section_title, 
                     fill=self.colors['accent'], font=self.fonts.get('subtitle'))
            
            results = analysis_results.get('results', [])
            positive_count = sum(1 for r in results if r.get('leukocoria_detected', False))
            
            rec_y = start_y + 40
            
            if positive_count > 0:
                # Recommandations pour détections positives
                urgent_text = "🚨 IMMEDIATE ACTION REQUIRED"
                draw.text((50, rec_y), urgent_text, 
                         fill=self.colors['critical'], font=self.fonts.get('normal'))
                
                recommendations = [
                    "1. ⏰ Contact pediatric ophthalmologist IMMEDIATELY",
                    "2. 📋 Bring this report and original images to appointment", 
                    "3. 🚫 Do NOT delay seeking professional medical evaluation",
                    "4. 📞 Emergency: Call your healthcare provider if urgent",
                    "",
                    "⚠️ Retinoblastoma requires immediate professional attention.",
                    "Early detection and treatment can save sight and life."
                ]
                
                rec_color = self.colors['danger']
            else:
                # Recommandations pour résultats normaux
                normal_text = "✅ ROUTINE MONITORING RECOMMENDED"
                draw.text((50, rec_y), normal_text, 
                         fill=self.colors['safe'], font=self.fonts.get('normal'))
                
                recommendations = [
                    "1. 📅 Continue regular pediatric eye examinations",
                    "2. 📸 Take monthly photos under good lighting conditions",
                    "3. 👀 Watch for any changes in pupil appearance",
                    "4. 🔄 Repeat AI screening if concerns arise",
                    "",
                    "💡 Regular monitoring is key to early detection.",
                    "Consult pediatric ophthalmologist if any concerns."
                ]
                
                rec_color = self.colors['text_dark']
            
            # Afficher les recommandations
            for i, rec in enumerate(recommendations):
                y = rec_y + 30 + (i * 20)
                font_to_use = self.fonts.get('small') if rec else self.fonts.get('tiny')
                color = rec_color if rec else self.colors['text_dark']
                
                if rec:  # Ne pas afficher les lignes vides
                    draw.text((50, y), rec, fill=color, font=font_to_use)
            
            return start_y + section_height
            
        except Exception as e:
            logger.error(f"Error drawing recommendations section: {e}")
            return start_y + 150
    
    def _draw_report_footer(self, draw: ImageDraw.Draw, width: int, height: int):
        """Dessine le pied de page du rapport"""
        try:
            footer_height = 80
            footer_y = height - footer_height
            
            # Fond du pied de page
            draw.rectangle([0, footer_y, width, height], fill=self.colors['accent'])
            
            # Disclaimer médical
            disclaimer = "⚠️ IMPORTANT: This AI analysis is a screening tool only."
            disclaimer2 = "NOT a medical diagnosis. Professional evaluation required."
            
            self._draw_text_centered(
                draw, (width // 2, footer_y + 15), disclaimer,
                self.colors['text_light'], self.fonts.get('small')
            )
            
            self._draw_text_centered(
                draw, (width // 2, footer_y + 35), disclaimer2,
                self.colors['text_light'], self.fonts.get('small')
            )
            
            # Informations système
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            system_info = f"Generated: {timestamp} | RetinoblastoGemma v6 | 🏆 Google Gemma Hackathon"
            
            self._draw_text_centered(
                draw, (width // 2, footer_y + 60), system_info,
                self.colors['text_light'], self.fonts.get('tiny')
            )
            
        except Exception as e:
            logger.error(f"Error drawing report footer: {e}")
    
    def save_annotated_image(self, image: Image.Image, filename_prefix: str = "analysis") -> Optional[str]:
        """Sauvegarde une image annotée"""
        try:
            from config.settings import RESULTS_DIR
            
            # Créer le dossier de résultats
            results_dir = Path(RESULTS_DIR)
            results_dir.mkdir(parents=True, exist_ok=True)
            
            # Nom de fichier avec timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.jpg"
            filepath = results_dir / filename
            
            # Sauvegarder avec qualité optimale
            image.save(filepath, 'JPEG', quality=95, optimize=True)
            
            logger.info(f"Annotated image saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error saving annotated image: {e}")
            return None
    
    def create_comparison_view(self, image_paths: List[str], analysis_results_list: List[Dict]) -> Optional[Image.Image]:
        """Crée une vue comparative de plusieurs analyses"""
        try:
            if not image_paths or len(image_paths) != len(analysis_results_list):
                logger.error("Mismatch between image paths and analysis results")
                return None
            
            # Charger et redimensionner les images
            images = []
            max_width = 0
            total_height = 150  # Espace pour header
            
            for img_path in image_paths:
                img = Image.open(img_path).convert('RGB')
                
                # Redimensionner si nécessaire
                if img.width > 600:
                    ratio = 600 / img.width
                    new_size = (600, int(img.height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                images.append(img)
                max_width = max(max_width, img.width)
                total_height += img.height + 100  # Espace pour annotations
            
            # Créer l'image composite
            composite_width = max_width + 100
            composite_height = total_height + 100
            
            composite = Image.new('RGB', (composite_width, composite_height), self.colors['background'])
            draw = ImageDraw.Draw(composite)
            
            # En-tête de comparaison
            title = f"📊 COMPARATIVE ANALYSIS - {len(images)} IMAGES"
            self._draw_text_centered(
                draw, (composite_width // 2, 30), title,
                self.colors['accent'], self.fonts.get('title')
            )
            
            # Ajouter chaque analyse
            current_y = 100
            for i, (img, analysis_results) in enumerate(zip(images, analysis_results_list)):
                # Annoter l'image
                annotated_img = self._add_quick_annotations(img, analysis_results)
                
                # Ajouter à l'image composite
                composite.paste(annotated_img, (50, current_y))
                
                # Résumé à côté
                summary_x = img.width + 80
                positive_count = sum(1 for r in analysis_results.get('results', []) 
                                   if r.get('leukocoria_detected', False))
                
                summary_text = f"Analysis {i+1}:"
                draw.text((summary_x, current_y + 20), summary_text,
                         fill=self.colors['accent'], font=self.fonts.get('normal'))
                
                result_text = f"{positive_count} positive detection(s)"
                result_color = self.colors['danger'] if positive_count > 0 else self.colors['safe']
                draw.text((summary_x, current_y + 45), result_text,
                         fill=result_color, font=self.fonts.get('small'))
                
                current_y += img.height + 100
            
            return composite
            
        except Exception as e:
            logger.error(f"Error creating comparison view: {e}")
            return None
    
    def _add_quick_annotations(self, image: Image.Image, analysis_results: Dict) -> Image.Image:
        """Ajoute des annotations rapides à une image"""
        try:
            annotated = image.copy()
            draw = ImageDraw.Draw(annotated)
            
            results = analysis_results.get('results', [])
            positive_count = sum(1 for r in results if r.get('leukocoria_detected', False))
            
            # Overlay simple avec résultat
            overlay_height = 40
            if positive_count > 0:
                draw.rectangle([0, 0, image.width, overlay_height], fill=self.colors['danger'])
                status_text = f"🚨 {positive_count} POSITIVE"
                text_color = self.colors['text_light']
            else:
                draw.rectangle([0, 0, image.width, overlay_height], fill=self.colors['safe'])
                status_text = "✅ NORMAL"
                text_color = self.colors['text_light']
            
            self._draw_text_centered(
                draw, (image.width // 2, 15), status_text,
                text_color, self.fonts.get('normal')
            )
            
            return annotated
            
        except Exception as e:
            logger.error(f"Error adding quick annotations: {e}")
            return image
    
    def cleanup(self):
        """Nettoie les ressources du visualiseur"""
        try:
            # Rien de spécial à nettoyer pour ce module
            logger.info("VisualizationV2 cleaned up")
        except Exception as e:
            logger.error(f"Error during visualization cleanup: {e}")
    
    def __del__(self):
        """Nettoyage automatique"""
        self.cleanup()