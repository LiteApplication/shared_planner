
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
            save: 'Save',
            cancel: 'Cancel',
            menu: 'Menu',
            select_date: 'Select week',

            date: 'Date',
            time: 'Time',

            reservation: {
                booked: 'Booked',
                booked_by_you: 'Booked by you',
                edit_title: 'Edit reservation',
                edit_description: 'Please select a new time range for your reservation and click "Save"',
                add_title: 'Add reservation',
                add_description: 'Please select a time range for your reservation and click "Save"',
                start_time: 'Start time',
                end_time: 'End time',
                delete: 'Delete',
                confirm_delete: 'Are you sure you want to delete this reservation?\nThe admins will be notified to try and find a replacement.\nIf you do not want to delete it, click "Cancel"',
            },
            shops: {
                description: "Open from {from} to {until}. {volunteers} volunteers needed.\n{description}",
                book: "Book",
            }
        },
        day: {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday',
        },
        error: {
            title: 'Error',
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
                not_loaded: 'Something went wrong while loading the shop',
            },
            reservation: {
                overlap: 'Too many reservations overlap',
                not_found: 'Reservation not found',
                cant_cancel: 'Not allowed to cancel this reservation',
                cant_update: 'Not allowed to update this reservation',
                cancel_validated: 'Cannot cancel a validated reservation',
                outside_open: 'The reservation must be within the shop\'s opening hours',

                end_before_start: 'The end time must be after the start time',
                too_short: 'The time range must be at least {min_time} minutes',
                too_long: 'The time range must be at most {max_time} minutes',
                not_open_day: 'The shop is not open on this day',
                not_open_time: 'The shop is not open at this time',

                unknown: 'An unknown error happened while trying to book this time range.',

            },
            user: {
                not_found: 'User not found',
                email_not_same: 'Cannot change email',
                cant_set_self_admin: 'Cannot change own admin status',
            }
        },
        menu: {
            my_reservations: "My reservations",
            create_reservation: "Book a time",
            admin: {
                title: 'Admin',
                shops: 'Shops',
                users: 'Users',
                reservations: 'Reservations'
            }

        },
        date_locale: 'en-GB',
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
            save: 'Sauvegarder',
            cancel: 'Annuler',
            reservation: {
                booked: 'Réservé',
                booked_by_you: 'Réservé par vous',
                edit_title: 'Modifier la réservation',
                edit_description: 'Veuillez sélectionner une nouvelle plage horaire pour votre réservation et cliquer sur "Sauvegarder"',
                start_time: 'Heure de début',
                end_time: 'Heure de fin',

            },
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
            title: 'Erreur',
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
        },
        date_locale: 'fr-FR',
    }
}

const languages: { [key: string]: string } = {
    en: 'English',
    fr: 'Français',
}

export { messages as default, languages }