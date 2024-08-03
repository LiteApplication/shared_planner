const messages = {
    en: {
        message: {
            hello_world: 'hello world',
            login: 'Login',
            register: 'Register',
            email: 'Email',
            password: 'Password',
            full_name: 'Full Name',
            group: 'Group',
            logout: 'Logout',
            to_register: "Don't have an account? Register",
            to_login: 'Already have an account?',
            shop_open: 'Open',
        },
        day: {
            0: 'Sunday',
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
        },
        error: {
            unknown: 'Something went wrong, please try again later',
            fields: 'Please fill all fields',
            token: {
                invalid: 'Invalid token',
                expired: 'Token expired',
            },
            admin: {
                required: 'Admin role required',
            },
            auth: {
                user_not_found: 'User not found',
                invalid_password: 'Invalid credentials',
                email_exists: 'Email already exists',
                password_too_short: 'Password too short',
                full_name_too_short: 'Full name too short',
                email_invalid: 'Invalid email',
            },
            shop: {
                not_found: 'Shop not found',
                invalid_week: 'Invalid week number',
                negative_time_range: 'Time range must be longer than 0',
                time_range_overlap: 'Time range overlaps an existing time range',
                time_range_not_found: 'Time range not found',
                id_mismatch: 'Shop id mismatch',
            },
            reservation: {
                overlap: 'Too many reservations overlap',
                not_found: 'Reservation not found',
                cant_cancel: 'Not allowed to cancel this reservation',
                cancel_validated: 'Cannot cancel a validated reservation',
            },
            user: {
                not_found: 'User not found',
                email_not_same: 'Cannot change email',
                cant_set_self_admin: 'Cannot change own admin status',
            }
        }
    },
    fr: {
        message: {
            hello_world: 'Bonjour le monde',
            login: 'Connexion',
            register: 'S\'inscrire',
            email: 'Email',
            password: 'Mot de passe',
            full_name: 'Nom complet',
            group: 'Groupe',
            logout: 'Déconnexion',
            to_register: 'Vous n\'avez pas de compte? Inscrivez-vous',
            to_login: 'Vous avez déjà un compte?',
            shop_open: 'Ouvert',
        },
        day: {
            0: 'Lundi',
            1: 'Mardi',
            2: 'Mercredi',
            3: 'Jeudi',
            4: 'Vendredi',
            5: 'Samedi',
            6: 'Dimanche',
        },
        error: {
            unknown: 'Une erreur est survenue, veuillez réessayer plus tard',
            fields: 'Veuillez remplir tous les champs',
            token: {
                invalid: 'Jeton invalide',
                expired: 'Jeton expiré',
            },
            admin: {
                required: 'Rôle d\'administrateur requis',
            },
            auth: {
                user_not_found: 'Utilisateur non trouvé, vérifiez votre email',
                invalid_password: 'Identifiants invalides, vérifiez votre mot de passe',
                email_exists: 'L\'email existe déjà dans la base de données',
                password_too_short: 'Mot de passe trop court',
                full_name_too_short: 'Nom complet trop court',
                email_invalid: 'Email invalide, vérifiez votre email',
            },
            shop: {
                not_found: 'Boutique introuvable',
                invalid_week: 'Numéro de semaine invalide',
                negative_time_range: 'La plage horaire doit être supérieure à 0',
                time_range_overlap: 'La plage horaire se chevauche avec une plage horaire existante',
                time_range_not_found: 'Plage horaire introuvable',
                id_mismatch: 'Id de boutique non conforme',
            },
            reservation: {
                overlap: 'Trop de réservations se chevauchent',
                not_found: 'Réservation introuvable',
                cant_cancel: 'Non autorisé à annuler cette réservation',
                cancel_validated: 'Impossible d\'annuler une réservation validée',
            },
            user: {
                not_found: 'Utilisateur non trouvé',
                email_not_same: 'Impossible de changer l\'email',
                cant_set_self_admin: 'Impossible de changer votre propre statut d\'administrateur',
            }
        }
    }
}


export default messages;