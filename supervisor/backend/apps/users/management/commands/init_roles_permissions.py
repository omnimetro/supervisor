# -*- coding: utf-8 -*-
"""
Management command pour initialiser les roles, permissions et modules du systeme SUPERVISOR
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.users.models import Role, Module, Permission


class Command(BaseCommand):
    help = 'Initialise les roles, modules et permissions du systeme SUPERVISOR'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Initialisation des roles, modules et permissions...'))

        try:
            with transaction.atomic():
                # ============================================
                # 1. CREATION DES MODULES
                # ============================================
                self.stdout.write('\n1. Creation des modules...')
                modules_data = [
                    {
                        'code': 'deployment',
                        'nom': 'Gestion des Chantiers',
                        'description': 'Module de gestion des chantiers de deploiement fibre optique',
                        'ordre': 1
                    },
                    {
                        'code': 'b2b',
                        'nom': 'Gestion B2B',
                        'description': 'Module de gestion des raccordements et maintenances B2B',
                        'ordre': 2
                    },
                    {
                        'code': 'inventory',
                        'nom': 'Gestion des Stocks',
                        'description': 'Module de gestion des stocks de materiels et consommables',
                        'ordre': 3
                    },
                    {
                        'code': 'expenses',
                        'nom': 'Gestion des Depenses',
                        'description': 'Module de suivi des depenses et facturation',
                        'ordre': 4
                    },
                    {
                        'code': 'mapping',
                        'nom': 'Cartographie',
                        'description': 'Module de cartographie et tracking GPS',
                        'ordre': 5
                    },
                    {
                        'code': 'users',
                        'nom': 'Gestion des Utilisateurs',
                        'description': 'Module de gestion des utilisateurs et permissions',
                        'ordre': 6
                    }
                ]

                modules_created = 0
                modules_updated = 0
                modules = {}

                for module_data in modules_data:
                    module, created = Module.objects.update_or_create(
                        code=module_data['code'],
                        defaults={
                            'nom': module_data['nom'],
                            'description': module_data['description'],
                            'ordre': module_data['ordre']
                        }
                    )
                    modules[module_data['code']] = module
                    if created:
                        modules_created += 1
                        self.stdout.write(self.style.SUCCESS(f'  Module cree: {module.nom}'))
                    else:
                        modules_updated += 1
                        self.stdout.write(f'  Module mis a jour: {module.nom}')

                self.stdout.write(self.style.SUCCESS(
                    f'\n  Total: {modules_created} crees, {modules_updated} mis a jour'
                ))

                # ============================================
                # 2. CREATION DES PERMISSIONS PAR MODULE
                # ============================================
                self.stdout.write('\n2. Creation des permissions...')

                # Actions disponibles par module
                permissions_data = []

                # Actions standards pour chaque module
                actions_standards = [
                    ('view', 'Voir'),
                    ('create', 'Creer'),
                    ('edit', 'Modifier'),
                    ('delete', 'Supprimer'),
                    ('approve', 'Approuver'),
                    ('export', 'Exporter')
                ]

                # Generer toutes les permissions
                for module_code, module in modules.items():
                    for action_code, action_nom in actions_standards:
                        permissions_data.append({
                            'code': f'{module_code}.{action_code}',
                            'nom': f'{action_nom} - {module.nom}',
                            'description': f'Permission de {action_nom.lower()} dans le module {module.nom}',
                            'module': module,
                            'is_active': True
                        })

                permissions_created = 0
                permissions_updated = 0
                permissions = {}

                for perm_data in permissions_data:
                    perm, created = Permission.objects.update_or_create(
                        code=perm_data['code'],
                        defaults={
                            'nom': perm_data['nom'],
                            'description': perm_data['description'],
                            'module': perm_data['module'],
                            'is_active': perm_data['is_active']
                        }
                    )
                    permissions[perm_data['code']] = perm
                    if created:
                        permissions_created += 1
                    else:
                        permissions_updated += 1

                self.stdout.write(self.style.SUCCESS(
                    f'  Total: {permissions_created} permissions creees, {permissions_updated} mises a jour'
                ))

                # ============================================
                # 3. CREATION DES ROLES
                # ============================================
                self.stdout.write('\n3. Creation des roles...')
                roles_data = [
                    {
                        'code': 'superadmin',
                        'nom': 'Super Administrateur',
                        'description': 'Acces complet au systeme, gestion de tous les modules et utilisateurs'
                    },
                    {
                        'code': 'admin',
                        'nom': 'Administrateur',
                        'description': 'Gestion au niveau des modules, configuration avancee'
                    },
                    {
                        'code': 'coordinator',
                        'nom': 'Coordonnateur',
                        'description': 'Supervision multi-chantiers et equipes'
                    },
                    {
                        'code': 'supervisor',
                        'nom': 'Superviseur',
                        'description': 'Gestion au niveau chantier/equipe'
                    },
                    {
                        'code': 'stockmanager',
                        'nom': 'Gestionnaire de Stock',
                        'description': 'Controle des inventaires et mouvements de stock'
                    },
                    {
                        'code': 'technician',
                        'nom': 'Technicien',
                        'description': 'Execution des taches terrain et reporting'
                    },
                    {
                        'code': 'viewer',
                        'nom': 'Visualisateur',
                        'description': 'Acces en lecture seule'
                    }
                ]

                roles_created = 0
                roles_updated = 0
                roles = {}

                for role_data in roles_data:
                    role, created = Role.objects.update_or_create(
                        code=role_data['code'],
                        defaults={
                            'nom': role_data['nom'],
                            'description': role_data['description']
                        }
                    )
                    roles[role_data['code']] = role
                    if created:
                        roles_created += 1
                        self.stdout.write(self.style.SUCCESS(f'  Role cree: {role.nom}'))
                    else:
                        roles_updated += 1
                        self.stdout.write(f'  Role mis a jour: {role.nom}')

                self.stdout.write(self.style.SUCCESS(
                    f'\n  Total: {roles_created} crees, {roles_updated} mis a jour'
                ))

                # ============================================
                # 4. ASSIGNATION DES PERMISSIONS AUX ROLES
                # ============================================
                self.stdout.write('\n4. Assignation des permissions aux roles...')

                # Matrice de permissions : {role_code: [permission_codes]}
                role_permissions = {
                    'superadmin': [  # Acces total
                        'deployment.view', 'deployment.create', 'deployment.edit', 'deployment.delete', 'deployment.approve', 'deployment.export',
                        'b2b.view', 'b2b.create', 'b2b.edit', 'b2b.delete', 'b2b.approve', 'b2b.export',
                        'inventory.view', 'inventory.create', 'inventory.edit', 'inventory.delete', 'inventory.approve', 'inventory.export',
                        'expenses.view', 'expenses.create', 'expenses.edit', 'expenses.delete', 'expenses.approve', 'expenses.export',
                        'mapping.view', 'mapping.create', 'mapping.edit', 'mapping.delete', 'mapping.approve', 'mapping.export',
                        'users.view', 'users.create', 'users.edit', 'users.delete', 'users.approve', 'users.export'
                    ],
                    'admin': [  # Acces quasi-total sauf suppression utilisateurs
                        'deployment.view', 'deployment.create', 'deployment.edit', 'deployment.delete', 'deployment.approve', 'deployment.export',
                        'b2b.view', 'b2b.create', 'b2b.edit', 'b2b.delete', 'b2b.approve', 'b2b.export',
                        'inventory.view', 'inventory.create', 'inventory.edit', 'inventory.delete', 'inventory.approve', 'inventory.export',
                        'expenses.view', 'expenses.create', 'expenses.edit', 'expenses.delete', 'expenses.approve', 'expenses.export',
                        'mapping.view', 'mapping.create', 'mapping.edit', 'mapping.delete', 'mapping.approve', 'mapping.export',
                        'users.view', 'users.create', 'users.edit', 'users.export'
                    ],
                    'coordinator': [  # Supervision multi-chantiers
                        'deployment.view', 'deployment.create', 'deployment.edit', 'deployment.approve', 'deployment.export',
                        'b2b.view', 'b2b.create', 'b2b.edit', 'b2b.approve', 'b2b.export',
                        'inventory.view', 'inventory.export',
                        'expenses.view', 'expenses.approve', 'expenses.export',
                        'mapping.view', 'mapping.export',
                        'users.view'
                    ],
                    'supervisor': [  # Gestion chantier/equipe
                        'deployment.view', 'deployment.create', 'deployment.edit', 'deployment.export',
                        'b2b.view', 'b2b.create', 'b2b.edit', 'b2b.export',
                        'inventory.view', 'inventory.create', 'inventory.edit',
                        'expenses.view', 'expenses.create', 'expenses.edit',
                        'mapping.view',
                        'users.view'
                    ],
                    'stockmanager': [  # Gestion stocks uniquement
                        'deployment.view',
                        'b2b.view',
                        'inventory.view', 'inventory.create', 'inventory.edit', 'inventory.delete', 'inventory.export',
                        'expenses.view',
                        'mapping.view'
                    ],
                    'technician': [  # Execution taches terrain
                        'deployment.view', 'deployment.edit',
                        'b2b.view', 'b2b.edit',
                        'inventory.view',
                        'expenses.view', 'expenses.create',
                        'mapping.view'
                    ],
                    'viewer': [  # Lecture seule
                        'deployment.view',
                        'b2b.view',
                        'inventory.view',
                        'expenses.view',
                        'mapping.view',
                        'users.view'
                    ]
                }

                for role_code, perm_codes in role_permissions.items():
                    role = roles[role_code]
                    self.stdout.write(f'\n  Configuration du role: {role.nom}')

                    # Recuperer toutes les permissions pour ce role
                    role_perms = []
                    for perm_code in perm_codes:
                        if perm_code in permissions:
                            role_perms.append(permissions[perm_code])

                    # Assigner toutes les permissions au role
                    role.permissions.set(role_perms)
                    self.stdout.write(f'    {len(role_perms)} permissions assignees')

                # ============================================
                # RECAPITULATIF
                # ============================================
                self.stdout.write('\n' + '='*60)
                self.stdout.write(self.style.SUCCESS('INITIALISATION TERMINEE AVEC SUCCES'))
                self.stdout.write('='*60)
                self.stdout.write(f'\nModules       : {Module.objects.count()} total')
                self.stdout.write(f'Roles         : {Role.objects.count()} total')
                self.stdout.write(f'Permissions   : {Permission.objects.count()} total')
                self.stdout.write('\n' + '='*60)

                # Affichage du resume par role
                self.stdout.write('\nResume des permissions par role:')
                for role in Role.objects.all().order_by('code'):
                    perms_count = role.permissions.count()
                    self.stdout.write(
                        f'  {role.nom:<25} : {perms_count:>3} permissions'
                    )

                self.stdout.write('\n' + '='*60 + '\n')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\nErreur lors de l\'initialisation: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
            raise
