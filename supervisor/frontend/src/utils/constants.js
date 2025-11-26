/**
 * Constantes de Configuration SUPERVISOR V2.0
 * Centralise toutes les constantes de l'application
 */

// ============================================
// Configuration de l'API
// ============================================

/**
 * URL de base de l'API Django Backend
 * En production : remplacer par l'URL du serveur déployé
 */
export const API_BASE_URL = process.env.DEV
  ? 'http://localhost:8000/api'
  : process.env.API_URL || 'http://localhost:8000/api'

/**
 * Timeout par défaut pour les requêtes HTTP (en millisecondes)
 * 30 secondes pour les opérations standard
 */
export const API_TIMEOUT = 30000

/**
 * Endpoints de l'API Backend
 */
export const API_ENDPOINTS = {
  // Authentification
  AUTH: {
    LOGIN: '/token/',
    REFRESH: '/token/refresh/',
    LOGOUT: '/auth/logout/',
    REGISTER: '/auth/register/',
    PROFILE: '/auth/profile/',
    CHANGE_PASSWORD: '/auth/change-password/'
  },

  // Gestion des Chantiers (Déploiement)
  DEPLOYMENT: {
    // Opérateurs et BOQ
    OPERATORS: '/deployment/operators/',
    BOQ_CATEGORIES: '/deployment/boq-categories/',
    BOQ_ITEMS: '/deployment/boq-items/',
    TASK_DEFINITIONS: '/deployment/task-definitions/',

    // Ressources humaines
    SUBCONTRACTORS: '/deployment/subcontractors/',
    TECHNICIANS: '/deployment/technicians/',

    // Projets et plannings
    PROJECTS: '/deployment/projects/',
    PROJECT_PLANNINGS: '/deployment/project-plannings/',
    TASK_PLANNINGS: '/deployment/task-plannings/',

    // Suivi terrain
    DAILY_REPORTS: '/deployment/daily-reports/',
    CARTOGRAPHY_POINTS: '/deployment/cartography-points/',

    // Livraison et corrections
    DELIVERY_PHASES: '/deployment/delivery-phases/',
    CORRECTIONS: '/deployment/corrections/'
  },

  // Opérations B2B
  B2B: {
    TEAMS: '/b2b/teams/',
    STUDIES: '/b2b/studies/',
    CONNECTIONS: '/b2b/connections/',
    MAINTENANCES: '/b2b/maintenances/',
    INTERVENTIONS: '/b2b/interventions/'
  },

  // Gestion des Stocks
  INVENTORY: {
    MATERIALS: '/inventory/materials/',
    STOCK_MOVEMENTS: '/inventory/movements/',
    ALLOCATIONS: '/inventory/allocations/',
    RETURNS: '/inventory/returns/',
    REPORTS: '/inventory/reports/'
  },

  // Gestion des Dépenses
  EXPENSES: {
    LIST: '/expenses/',
    CATEGORIES: '/expenses/categories/',
    REPORTS: '/expenses/reports/',
    APPROVAL: '/expenses/approval/'
  },

  // Cartographie
  MAPPING: {
    LOCATIONS: '/mapping/locations/',
    INFRASTRUCTURE: '/mapping/infrastructure/',
    VEHICLES: '/mapping/vehicles/',
    GPS_TRACKING: '/mapping/gps-tracking/'
  },

  // Reporting
  REPORTING: {
    DAILY: '/reporting/daily/',
    RFC: '/reporting/rfc/',
    EXCEL: '/reporting/excel/',
    POWERPOINT: '/reporting/powerpoint/'
  },

  // Utilisateurs et Permissions
  USERS: {
    LIST: '/users/',
    ROLES: '/users/roles/',
    PERMISSIONS: '/users/permissions/',
    ACTIVITY_LOG: '/users/activity-log/'
  }
}

// ============================================
// Clés de Stockage Local (LocalStorage)
// ============================================

export const STORAGE_KEYS = {
  // Authentification
  AUTH_TOKEN: 'auth_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user',
  USER_ROLE: 'user_role',
  USER_PERMISSIONS: 'user_permissions',

  // Préférences Utilisateur
  THEME: 'theme', // 'light' ou 'dark'
  LANGUAGE: 'language', // 'fr' par défaut
  SIDEBAR_COLLAPSED: 'sidebar_collapsed',
  TABLE_PREFERENCES: 'table_preferences',

  // Cache et Données Hors Ligne
  OFFLINE_QUEUE: 'offline_queue',
  CACHED_DATA: 'cached_data',
  LAST_SYNC: 'last_sync'
}

// ============================================
// Limites et Contraintes de l'Application
// ============================================

/**
 * Taille maximale des fichiers uploadés (en octets)
 */
export const FILE_UPLOAD_LIMITS = {
  MAX_SIZE: 10 * 1024 * 1024, // 10 MB
  MAX_SIZE_IMAGE: 5 * 1024 * 1024, // 5 MB pour les images
  MAX_SIZE_DOCUMENT: 20 * 1024 * 1024, // 20 MB pour les documents (PDF, Excel)
  ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'image/webp'],
  ALLOWED_DOCUMENT_TYPES: [
    'application/pdf',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  ]
}

/**
 * Configuration de la pagination
 */
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
  MAX_PAGE_SIZE: 100
}

/**
 * Durées de validité (en millisecondes)
 */
export const EXPIRATION = {
  TOKEN_REFRESH_THRESHOLD: 5 * 60 * 1000, // 5 minutes avant expiration
  CACHE_DURATION: 15 * 60 * 1000, // 15 minutes
  SESSION_TIMEOUT: 2 * 60 * 60 * 1000 // 2 heures
}

// ============================================
// Statuts et États
// ============================================

/**
 * Statuts des tâches de chantier
 */
export const TASK_STATUS = {
  PENDING: 'pending',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
  ON_HOLD: 'on_hold'
}

/**
 * Statuts des interventions B2B
 */
export const INTERVENTION_STATUS = {
  STUDY_REQUESTED: 'study_requested',
  STUDY_IN_PROGRESS: 'study_in_progress',
  STUDY_COMPLETED: 'study_completed',
  CONNECTION_SCHEDULED: 'connection_scheduled',
  CONNECTION_IN_PROGRESS: 'connection_in_progress',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled'
}

/**
 * Types de mouvements de stock
 */
export const STOCK_MOVEMENT_TYPES = {
  ACQUISITION: 'acquisition',
  ALLOCATION: 'allocation',
  RETURN: 'return',
  RECOVERY: 'recovery',
  UNAVAILABLE: 'unavailable',
  ADJUSTMENT: 'adjustment'
}

/**
 * Statuts des dépenses
 */
export const EXPENSE_STATUS = {
  DRAFT: 'draft',
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  PAID: 'paid'
}

/**
 * Rôles utilisateurs
 */
export const USER_ROLES = {
  SUPER_ADMIN: 'super_admin',
  ADMIN: 'admin',
  COORDINATOR: 'coordinator',
  SUPERVISOR: 'supervisor',
  STOCK_MANAGER: 'stock_manager',
  TECHNICIAN: 'technician',
  VIEWER: 'viewer'
}

// ============================================
// Configuration Google Maps
// ============================================

export const GOOGLE_MAPS = {
  API_KEY: process.env.GOOGLE_MAPS_API_KEY || '',
  DEFAULT_CENTER: {
    lat: 5.3599517, // Abidjan, Côte d'Ivoire
    lng: -4.0082563
  },
  DEFAULT_ZOOM: 12,
  MAP_STYLES: {
    ROADMAP: 'roadmap',
    SATELLITE: 'satellite',
    HYBRID: 'hybrid',
    TERRAIN: 'terrain'
  }
}

// ============================================
// Configuration des Notifications
// ============================================

export const NOTIFICATION_CONFIG = {
  DEFAULT_DURATION: 5000, // 5 secondes
  SUCCESS_DURATION: 3000,
  ERROR_DURATION: 8000,
  WARNING_DURATION: 6000,
  POSITION: 'top-right'
}

// ============================================
// Formats de Date et Heure
// ============================================

export const DATE_FORMATS = {
  DISPLAY: 'DD/MM/YYYY', // Format d'affichage
  DISPLAY_LONG: 'DD MMMM YYYY', // Format long
  DISPLAY_WITH_TIME: 'DD/MM/YYYY HH:mm',
  API: 'YYYY-MM-DD', // Format pour l'API
  API_WITH_TIME: 'YYYY-MM-DD HH:mm:ss',
  TIME_ONLY: 'HH:mm'
}

// ============================================
// Configuration du Mode Hors Ligne
// ============================================

export const OFFLINE_CONFIG = {
  ENABLED: true,
  SYNC_INTERVAL: 5 * 60 * 1000, // 5 minutes
  MAX_QUEUE_SIZE: 100,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 2000 // 2 secondes
}

// ============================================
// Regex de Validation
// ============================================

export const VALIDATION_PATTERNS = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE_CI: /^((\+225|00225)?[0-9]{10})$/, // Format téléphone Côte d'Ivoire
  PHONE_INTERNATIONAL: /^\+?[1-9]\d{1,14}$/,
  COORDINATES: /^-?([1-8]?[0-9]\.{1}\d+|90\.{1}0+)$/,
  PASSWORD_STRONG: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
}

// ============================================
// Messages d'Erreur Standards
// ============================================

export const ERROR_MESSAGES = {
  NETWORK: 'Erreur de connexion. Vérifiez votre connexion internet.',
  UNAUTHORIZED: 'Session expirée. Veuillez vous reconnecter.',
  FORBIDDEN: 'Vous n\'avez pas les permissions nécessaires.',
  NOT_FOUND: 'Ressource non trouvée.',
  SERVER_ERROR: 'Erreur serveur. Veuillez réessayer plus tard.',
  VALIDATION_ERROR: 'Erreur de validation. Vérifiez les données saisies.',
  FILE_TOO_LARGE: 'Le fichier est trop volumineux.',
  INVALID_FILE_TYPE: 'Type de fichier non autorisé.'
}

// ============================================
// Export par défaut (objet complet)
// ============================================

export default {
  API_BASE_URL,
  API_TIMEOUT,
  API_ENDPOINTS,
  STORAGE_KEYS,
  FILE_UPLOAD_LIMITS,
  PAGINATION,
  EXPIRATION,
  TASK_STATUS,
  INTERVENTION_STATUS,
  STOCK_MOVEMENT_TYPES,
  EXPENSE_STATUS,
  USER_ROLES,
  GOOGLE_MAPS,
  NOTIFICATION_CONFIG,
  DATE_FORMATS,
  OFFLINE_CONFIG,
  VALIDATION_PATTERNS,
  ERROR_MESSAGES
}
