"""
Commande de gestion Django pour initialiser les spécialités techniques.

Cette commande crée les spécialités de base pour les techniciens AIV.
Elle est idempotente et peut être exécutée plusieurs fois sans problème.

Usage:
    python manage.py init_specialites
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.deployment.models import Specialite


class Command(BaseCommand):
    """Commande pour initialiser les spécialités techniques."""

    help = 'Initialise les spécialités techniques pour les techniciens'

    # Définition des spécialités par défaut avec leur ordre et couleur
    SPECIALITES_DATA = [
        {
            'code': 'GC',
            'nom': 'Génie Civil',
            'description': 'Travaux de génie civil : tranchées, chambres, fourreaux',
            'couleur': '#8B4513',  # Marron
            'ordre': 1
        },
        {
            'code': 'RESEAU',
            'nom': 'Travaux de réseau',
            'description': 'Installation de câbles, pose aérienne et souterraine',
            'couleur': '#4169E1',  # Bleu royal
            'ordre': 2
        },
        {
            'code': 'FO',
            'nom': 'Fibre Optique',
            'description': 'Installation et déploiement de fibre optique',
            'couleur': '#FF8C00',  # Orange
            'ordre': 3
        },
        {
            'code': 'SOUDURE',
            'nom': 'Soudure FO',
            'description': 'Soudure et raccordement de fibres optiques',
            'couleur': '#DC143C',  # Rouge cramoisi
            'ordre': 4
        },
        {
            'code': 'MESURE',
            'nom': 'Mesures et tests',
            'description': 'Tests de réflectométrie, mesures de perte, validation réseau',
            'couleur': '#9370DB',  # Violet moyen
            'ordre': 5
        },
        {
            'code': 'POLY',
            'nom': 'Polyvalent',
            'description': 'Technicien polyvalent capable d\'intervenir sur plusieurs domaines',
            'couleur': '#32CD32',  # Vert citron
            'ordre': 6
        },
    ]

    def handle(self, *args, **options):
        """Exécute la commande d'initialisation."""
        self.stdout.write(self.style.MIGRATE_HEADING('Initialisation des spécialités techniques...'))

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for specialite_data in self.SPECIALITES_DATA:
                specialite, created = Specialite.objects.update_or_create(
                    code=specialite_data['code'],
                    defaults={
                        'nom': specialite_data['nom'],
                        'description': specialite_data['description'],
                        'couleur': specialite_data['couleur'],
                        'ordre': specialite_data['ordre'],
                        'is_active': True
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  ✓ Créé : {specialite.code} - {specialite.nom}'
                        )
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ⚠ Mis à jour : {specialite.code} - {specialite.nom}'
                        )
                    )

        # Affichage du résumé
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Initialisation terminée : '
                f'{created_count} créé(es), {updated_count} mis(es) à jour'
            )
        )
        self.stdout.write(
            self.style.MIGRATE_LABEL(
                f'Total de spécialités actives : {Specialite.objects.filter(is_active=True).count()}'
            )
        )
