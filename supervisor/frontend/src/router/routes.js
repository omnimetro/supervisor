const routes = [
  // ============================================
  // Routes d'authentification (publiques)
  // ============================================
  {
    path: '/auth',
    component: () => import('layouts/AuthLayout.vue'),
    meta: { requiresAuth: false },
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import('pages/auth/LoginPage.vue'),
        meta: { requiresAuth: false }
      },
      // Routes futures
      // {
      //   path: 'register',
      //   name: 'register',
      //   component: () => import('pages/auth/RegisterPage.vue'),
      //   meta: { requiresAuth: false }
      // },
      // {
      //   path: 'forgot-password',
      //   name: 'forgot-password',
      //   component: () => import('pages/auth/ForgotPasswordPage.vue'),
      //   meta: { requiresAuth: false }
      // }
    ]
  },

  // Alias pour /login → /auth/login
  {
    path: '/login',
    redirect: '/auth/login',
    meta: { requiresAuth: false }
  },

  // ============================================
  // Routes protégées (nécessitent authentification)
  // ============================================
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'home',
        redirect: '/dashboard'
      },
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('pages/DashboardPage.vue'),
        meta: {
          title: 'Tableau de Bord',
          icon: 'dashboard'
        }
      },
      {
        path: 'profile',
        name: 'profile',
        component: () => import('pages/ProfilePage.vue'),
        meta: {
          title: 'Mon Profil',
          icon: 'person'
        }
      },

      // ============================================
      // Routes futures (à décommenter progressivement)
      // ============================================

      // Gestion des Utilisateurs
      // {
      //   path: 'users',
      //   name: 'users',
      //   component: () => import('pages/users/UsersPage.vue'),
      //   meta: {
      //     title: 'Utilisateurs',
      //     icon: 'people',
      //     roles: ['SUPERADMIN', 'ADMIN']
      //   }
      // },

      // Gestion des Chantiers (Deployment)
      {
        path: 'deployment',
        children: [
          // Opérateurs - Test
          {
            path: 'operators-test',
            name: 'operators-test',
            component: () => import('pages/deployment/OperatorsTestPage.vue'),
            meta: {
              title: 'Opérateurs (Test)',
              icon: 'bug_report'
            }
          },

          // Opérateurs
          {
            path: 'operators',
            name: 'operators',
            component: () => import('pages/deployment/OperatorsPage.vue'),
            meta: {
              title: 'Opérateurs',
              icon: 'business',
              roles: ['SUPERADMIN', 'ADMIN']
            }
          },

          // Sous-traitants
          {
            path: 'subcontractors',
            name: 'subcontractors',
            component: () => import('pages/deployment/SubcontractorsPage.vue'),
            meta: {
              title: 'Sous-traitants',
              icon: 'engineering'
            }
          },

          // Spécialités
          {
            path: 'specialites',
            name: 'specialites',
            component: () => import('pages/deployment/SpecialitesPage.vue'),
            meta: {
              title: 'Spécialités',
              icon: 'school',
              roles: ['SUPERADMIN', 'ADMIN']
            }
          },

          // Techniciens
          {
            path: 'technicians',
            name: 'technicians',
            component: () => import('pages/deployment/TechniciansPage.vue'),
            meta: {
              title: 'Techniciens',
              icon: 'people'
            }
          },

          // Projets - Liste
          {
            path: 'projects',
            name: 'projects',
            component: () => import('pages/deployment/ProjectsPage.vue'),
            meta: {
              title: 'Projets',
              icon: 'construction'
            }
          },

          // Projets - Détail
          {
            path: 'projects/:id',
            name: 'project-detail',
            component: () => import('pages/deployment/ProjectDetailPage.vue'),
            meta: {
              title: 'Détail Projet',
              hideInMenu: true
            }
          },

          // Catégories BOQ
          {
            path: 'boq-categories',
            name: 'boq-categories',
            component: () => import('pages/deployment/BOQCategoriesPage.vue'),
            meta: {
              title: 'Catégories BOQ',
              icon: 'category'
            }
          },

          // Définitions de tâches
          {
            path: 'task-definitions',
            name: 'task-definitions',
            component: () => import('pages/deployment/TaskDefinitionsPage.vue'),
            meta: {
              title: 'Définitions de tâches',
              icon: 'assignment'
            }
          },

          // Types de Documents
          {
            path: 'type-documents',
            name: 'type-documents',
            component: () => import('pages/deployment/TypeDocumentsPage.vue'),
            meta: {
              title: 'Types de Documents',
              icon: 'description',
              roles: ['SUPERADMIN', 'ADMIN']
            }
          },

          // Documents de Projet
          {
            path: 'project-documents',
            name: 'project-documents',
            component: () => import('pages/deployment/ProjectDocumentsPage.vue'),
            meta: {
              title: 'Documents de Projet',
              icon: 'folder'
            }
          }

          // Routes futures (à créer)
          // {
          //   path: 'boq-items',
          //   name: 'boq-items',
          //   component: () => import('pages/deployment/BOQItemsPage.vue'),
          //   meta: { title: 'Articles BOQ', icon: 'list_alt' }
          // },
          // {
          //   path: 'daily-reports',
          //   name: 'daily-reports',
          //   component: () => import('pages/deployment/DailyReportsPage.vue'),
          //   meta: { title: 'Rapports journaliers', icon: 'assignment_turned_in' }
          // }
        ]
      },

      // Gestion B2B
      // {
      //   path: 'b2b',
      //   children: [
      //     {
      //       path: '',
      //       name: 'b2b',
      //       component: () => import('pages/b2b/InterventionsPage.vue'),
      //       meta: { title: 'B2B', icon: 'business_center' }
      //     }
      //   ]
      // },

      // Gestion des Stocks
      // {
      //   path: 'inventory',
      //   children: [
      //     {
      //       path: '',
      //       name: 'inventory',
      //       component: () => import('pages/inventory/InventoryPage.vue'),
      //       meta: { title: 'Stocks', icon: 'inventory' }
      //     }
      //   ]
      // },

      // Gestion des Dépenses
      // {
      //   path: 'expenses',
      //   children: [
      //     {
      //       path: '',
      //       name: 'expenses',
      //       component: () => import('pages/expenses/ExpensesPage.vue'),
      //       meta: { title: 'Dépenses', icon: 'payments' }
      //     }
      //   ]
      // },

      // Cartographie
      // {
      //   path: 'mapping',
      //   children: [
      //     {
      //       path: '',
      //       name: 'mapping',
      //       component: () => import('pages/mapping/MapPage.vue'),
      //       meta: { title: 'Cartographie', icon: 'map' }
      //     }
      //   ]
      // }
    ]
  },

  // ============================================
  // Page 404 (toujours en dernier)
  // ============================================
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
    meta: { requiresAuth: false }
  }
]

export default routes
