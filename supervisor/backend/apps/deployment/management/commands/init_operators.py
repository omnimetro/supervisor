# -*- coding: utf-8 -*-
"""
Management command pour initialiser les operateurs telecom
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.deployment.models import Operator


class Command(BaseCommand):
    help = 'Initialise les operateurs telecom (Orange, Moov)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Initialisation des operateurs telecom...'))

        try:
            with transaction.atomic():
                # Donnees des operateurs
                operators_data = [
                    {
                        'code': 'ORA',
                        'nom': 'Orange CI',
                        'couleur': '#FF7900',  # Orange officiel
                        'contact_nom': 'Service Technique Orange',
                        'contact_email': 'technique@orange.ci',
                        'contact_telephone': '+225 07 08 09 10 11',
                        'is_active': True
                    },
                    {
                        'code': 'MOV',
                        'nom': 'Moov Africa',
                        'couleur': '#00A9E0',  # Bleu Moov
                        'contact_nom': 'Service Technique Moov',
                        'contact_email': 'technique@moov.ci',
                        'contact_telephone': '+225 05 04 03 02 01',
                        'is_active': True
                    }
                ]

                operators_created = 0
                operators_updated = 0

                for operator_data in operators_data:
                    operator, created = Operator.objects.update_or_create(
                        code=operator_data['code'],
                        defaults={
                            'nom': operator_data['nom'],
                            'couleur': operator_data['couleur'],
                            'contact_nom': operator_data['contact_nom'],
                            'contact_email': operator_data['contact_email'],
                            'contact_telephone': operator_data['contact_telephone'],
                            'is_active': operator_data['is_active']
                        }
                    )
                    if created:
                        operators_created += 1
                        self.stdout.write(self.style.SUCCESS(f'  Operateur cree: {operator.nom}'))
                    else:
                        operators_updated += 1
                        self.stdout.write(f'  Operateur mis a jour: {operator.nom}')

                # Recapitulatif
                self.stdout.write('\n' + '='*60)
                self.stdout.write(self.style.SUCCESS('INITIALISATION TERMINEE AVEC SUCCES'))
                self.stdout.write('='*60)
                self.stdout.write(f'\nOperateurs : {Operator.objects.count()} total')
                self.stdout.write(f'  - {operators_created} crees')
                self.stdout.write(f'  - {operators_updated} mis a jour')
                self.stdout.write('\n' + '='*60)

                # Liste des operateurs
                self.stdout.write('\nOperateurs actifs:')
                for operator in Operator.objects.filter(is_active=True):
                    self.stdout.write(f'  [{operator.code}] {operator.nom} - {operator.couleur}')

                self.stdout.write('\n')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\nErreur lors de l\'initialisation: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
            raise
