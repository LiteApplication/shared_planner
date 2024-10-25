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
            to_register: 'Don\'t have an account? Register',
            to_login: 'Already have an account?',
            save: 'Save',
            cancel: 'Cancel',
            menu: 'Menu',
            select_date: 'Select a week',
            success: 'Success',
            empty_list: 'Nothing to show here ... yet',
            google_maps: "Google Maps",

            date: 'Date',
            time: 'Time',

            reservation: {
                new_reservation_explanation: 'Click the button below to show the available shops, then click the \'Book\' button to create a reservation in the shop of your choice.',
                new_reservation_button: 'Click here to see the shops and book a time',
                booked: 'Booked',
                booked_by_you: 'Booked by you',
                edit_title: 'Edit reservation',
                edit_description: 'Please select a new time range for your reservation and click \'Save\'',
                add_title: 'Add reservation',
                add_description: 'Please select a time range for your reservation and click \'Save\'',
                date: 'Date',
                start_time: 'Start time',
                end_time: 'End time',
                user: 'User',
                delete: 'Delete',
                confirm_delete: 'Are you sure you want to delete this reservation?\nThe admins will be notified to try and find a replacement.\nIf you do not want to delete it, click \'Cancel\'',
            },
            shops: {
                description: 'Open from <br/><b>{from}</b> to <br/><b>{until}</b>.<br><i>{volunteers} volunteers needed.</i><br/>{description}',
                description_plain: 'Open from {from} to {until}. {volunteers} volunteers needed.\n{description}',
                open: 'Shop open',
                book: 'Book',
                week_format: '\'Week \'WW\', \'yy',
                select: 'Please select a shop',
            },
        },
        admin: {
            unauthorized: 'You are not authorized to view this page',
            admin_column: 'Admin',
            confirm_delete_selected_users: 'Are you sure you want to delete the selected users ? This action cannot be undone. Their reservations will be deleted as well.',
            user_deleted: 'The user(s) have been deleted successfully.',
            shop: {
                informations: 'Shop informations',
                create: 'Create shop',
                delete: 'Delete shop',
                name: 'Shop name',
                description: 'Description',
                location: 'Location',
                volunteers: 'Volunteers',
                maps: 'Google Maps link',
                min_time: 'Minimum reservation time',
                max_time: 'Maximum reservation time',
                start_date: 'Start date',
                end_date: 'End date',

                created: 'The shop has been created successfully.',
                updated: 'The shop has been updated successfully.',
                deleted: 'The shop has been deleted successfully.',
                delete_confirm: 'Are you sure you want to delete this shop? All reservations will be deleted as well.',

                open_ranges: 'Open ranges',
                or_add: 'Add an open range',
                or_added: 'The open range has been added successfully.',
                or_title: 'Open ranges',
                or_day: 'Day',
                or_start: 'Start time',
                or_end: 'End time',
                or_deleted: 'The open range has been deleted successfully.'
            },
            settings: {
                saved_description: "{key} has been saved successfully.",
                saved_title: "Setting saved",
                key: "Setting",
                value: "Value",

                title: {
                    email_confirm_reservation: "Send emails to confirm reservations",
                    email_notification_before: "Time before email reminder",
                    base_domain: "Server domain name",
                    notif_login: "Send notifications on login",
                    notif_reservation_created: "Notify user on new reservation",
                    notif_admin_reservation_created: "Notify admin on new reservation",
                    notif_admin_reservation_cancel: "Notify admin on reservation cancel",

                },
                description: {
                    email_confirm_reservation: "When enabled, an email will be sent immediately after a reservation is made.",
                    email_notification_before: "Send an email reminder to the user this many hours before their reservation.<br>Set this to -1 to disable email reminders.",
                    base_domain: "The domain name of the server. This is used to generate links in emails<br>Be sure to include the protocol (http/https).<br>Do not include a trailing slash. Example: <i>https://reservations.magev.fr</i>.<br><b>Do not modify this setting unless you know what you are doing.</b>",
                    notif_login: "When enabled, users will receive a notification when they log into the site.",
                    notif_reservation_created: "When enabled, users will receive a notification each time they create a new reservation.",
                    notif_admin_reservation_created: "When enabled, admins will receive a notification when someone creates a new reservation",
                    notif_admin_reservation_cancel: "When enabled, admins will receive a notification when someone deletes their reservation",

                }

            },
            reservations: {
                title: 'Reservations',
                select_user: 'Select a user',
                no_user_selected: '(Keep the same user)',
                filter_no_user_found: 'No users found',
                select_shop: 'Select a shop',
                filter_no_shop_found: 'No shops found',
                no_reservations: 'No reservations found',
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
            server: 'Something went wrong on the server. ',
            token: {
                invalid: 'Invalid token',
                expired: 'Token expired',
            },
            admin: {
                required: 'Admin role required',
                setting_not_found: 'This setting cannot be found'
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
                no_id: 'No shop id provided',
                unknown: 'An unknown error happened while trying to get the shop data.',
            },
            reservation: {
                overlap: 'Too many reservations overlap',
                not_found: 'Reservation not found',
                cant_cancel: 'Not allowed to cancel this reservation',
                cant_update: 'Not allowed to update this reservation',
                cancel_validated: 'Cannot cancel a validated reservation',
                outside_open: 'The reservation must be within the shop\'s opening hours',
                past_time: 'Cannot book a time in the past',
                before_open: 'Cannot book a time before the shop opens',
                after_close: 'Cannot book a time after the shop closes',

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
                already_exists: 'User already exists',
                unknown: 'An unknown error happened while trying to get the user data.',
            },
            notification: {
                unknown: 'An unknown error happened while trying to get the notifications.',
                not_found: 'Notification not found',
                not_allowed: 'Not allowed to access this notification',

            }
        },
        menu: {
            my_reservations: 'My future reservations',
            create_reservation: 'Book a time',
            admin: {
                title: 'Admin',
                shops: 'Shops',
                users: 'Users',
                reservations: 'Reservations',
                settings: 'Server settings'
            }

        },
        notification: {
            delete: 'Delete',
            mark_as_read: 'Mark as read',
            mark_as_unread: 'Mark as unread',
            mark_all_as_read: 'Mark all as read',

            login: {
                title: "New login",
                body: "You have logged in successfully",
            },
            loading: {
                title: "Loading",
                body: "Loading data ...",
                access: "Please wait"
            },
            test: {
                title: "Test notification {test}",
                body: "This is a test notification",
                access: "Open test"

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
            to_register: 'Vous n\'avez pas de compte ? Inscrivez-vous',
            to_login: 'Vous avez déjà un compte ?',
            save: 'Sauvegarder',
            cancel: 'Annuler',
            menu: 'Menu',
            select_date: 'Sélectionnez une semaine',
            success: 'Succès',
            empty_list: 'Rien à afficher pour le moment ...',
            google_maps: 'Google Maps',

            date: 'Date',
            time: 'Heure',

            reservation: {
                new_reservation_explanation: 'Cliquez sur le bouton ci-dessous pour afficher les boutiques disponibles, puis cliquez sur le bouton \'Réserver\' pour créer une réservation dans la boutique de votre choix.',
                new_reservation_button: 'Cliquez ici pour voir les boutiques et réserver un créneau',
                booked: 'Réservé',
                booked_by_you: 'Réservé par vous',
                edit_title: 'Modifier la réservation',
                edit_description: 'Veuillez sélectionner une nouvelle plage horaire pour votre réservation puis cliquez sur \'Sauvegarder\'',
                add_title: 'Ajouter une réservation',
                add_description: 'Veuillez sélectionner une plage horaire pour votre réservation puis cliquez sur \'Sauvegarder\'',
                date: 'Date',
                start_time: 'Heure de début',
                end_time: 'Heure de fin',
                user: 'Utilisateur',
                delete: 'Supprimer',
                confirm_delete: 'Êtes-vous sûr de vouloir supprimer cette réservation ?\nLes administrateurs seront informés pour tenter de trouver un remplaçant.\nSi vous ne souhaitez pas supprimer, cliquez sur \'Annuler\'',
            },
            shops: {
                description: 'Ouvert de <br/><b>{from}</b> à <br/><b>{until}</b>.<br><i>{volunteers} bénévoles nécessaires.</i><br/>{description}',
                description_plain: 'Ouvert de {from} à {until}. {volunteers} bénévoles nécessaires.\n{description}',
                open: 'Boutique ouverte',
                book: 'Réserver',
                week_format: '\'Semaine \'WW\', \'yy',
                select: 'Veuillez sélectionner une boutique',
            },
        },
        admin: {
            unauthorized: 'Vous n\'êtes pas autorisé à voir cette page',
            admin_column: 'Admin',
            confirm_delete_selected_users: 'Êtes-vous sûr de vouloir supprimer les utilisateurs sélectionnés ? Cette action est irréversible. Leurs réservations seront également supprimées.',
            user_deleted: 'Les utilisateurs ont été supprimés avec succès.',
            shop: {
                informations: 'Informations sur la boutique',
                create: 'Créer une boutique',
                delete: 'Supprimer la boutique',
                name: 'Nom de la boutique',
                description: 'Description',
                location: 'Emplacement',
                volunteers: 'Bénévoles',
                maps: 'Lien Google Maps',
                min_time: 'Temps de réservation minimum',
                max_time: 'Temps de réservation maximum',
                start_date: 'Date de début',
                end_date: 'Date de fin',

                created: 'La boutique a été créée avec succès.',
                updated: 'La boutique a été mise à jour avec succès.',
                deleted: 'La boutique a été supprimée avec succès.',
                delete_confirm: 'Êtes-vous sûr de vouloir supprimer cette boutique ? Toutes les réservations seront supprimées.',

                open_ranges: 'Plages horaires',
                or_add: 'Ajouter une plage horaire',
                or_added: 'La plage horaire a été ajoutée avec succès.',
                or_title: 'Plages horaires',
                or_day: 'Jour',
                or_start: 'Heure de début',
                or_end: 'Heure de fin',
                or_deleted: 'La plage horaire a été supprimée avec succès.'
            },
            settings: {
                saved_description: "{key} a été sauvegardé avec succès.",
                saved_title: "Paramètre sauvegardé",
                key: "Paramètre",
                value: "Valeur",

                title: {
                    email_confirm_reservation: "Envoyer des emails pour confirmer les réservations",
                    email_notification_before: "Temps avant le rappel par email",
                    base_domain: "Nom de domaine du serveur",
                },
                description: {
                    email_confirm_reservation: "Lorsque cette option est activée, un email est envoyé immédiatement après la création d'une réservation.",
                    email_notification_before: "Envoyer un rappel par email cet intervalle d'heures avant la réservation.<br>Définir à -1 pour désactiver les rappels par email.",
                    base_domain: "Le nom de domaine du serveur. Utilisé pour générer les liens dans les emails.<br>Incluez le protocole (http/https).<br>Ne pas inclure de barre oblique à la fin. Exemple : <i>https://reservations.magev.fr</i>.<br><b>Ne modifiez pas ce paramètre à moins de savoir ce que vous faites.</b>",
                }
            },
            reservations: {
                title: 'Réservations',
                select_user: 'Sélectionnez un utilisateur',
                no_user_selected: '(Garder le même utilisateur)',
                filter_no_user_found: 'Aucun utilisateur trouvé',
                select_shop: 'Sélectionnez une boutique',
                filter_no_shop_found: 'Aucune boutique trouvée',
                no_reservations: 'Aucune réservation trouvée',
            }
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
            server: 'Une erreur est survenue sur le serveur. ',
            token: {
                invalid: 'Jeton invalide',
                expired: 'Jeton expiré',
            },
            admin: {
                required: 'Rôle d\'administrateur requis',
                setting_not_found: 'Ce paramètre est introuvable',
            },
            auth: {
                user_not_found: 'Utilisateur non trouvé',
                invalid_password: 'Identifiants invalides',
                email_exists: 'L\'email existe déjà',
                password_too_short: 'Mot de passe trop court',
                full_name_too_short: 'Nom complet trop court',
                email_invalid: 'Email invalide',
            },
            shop: {
                not_found: 'Boutique introuvable',
                invalid_week: 'Numéro de semaine invalide',
                negative_time_range: 'La plage horaire doit être supérieure à 0',
                time_range_overlap: 'La plage horaire se chevauche avec une plage horaire existante',
                time_range_not_found: 'Plage horaire introuvable',
                id_mismatch: 'Id de boutique non conforme',
                not_loaded: 'Une erreur est survenue lors du chargement de la boutique',
                no_id: 'Aucun id de boutique fourni',
                unknown: 'Une erreur inconnue est survenue lors de la récupération des données de la boutique.',
            },
            reservation: {
                overlap: 'Trop de réservations se chevauchent',
                not_found: 'Réservation introuvable',
                cant_cancel: 'Non autorisé à annuler cette réservation',
                cant_update: 'Non autorisé à mettre à jour cette réservation',
                cancel_validated: 'Impossible d\'annuler une réservation validée',
                outside_open: 'La réservation doit être dans les horaires d\'ouverture de la boutique',
                past_time: 'Impossible de réserver un créneau dans le passé',
                before_open: 'Impossible de réserver un créneau avant l\'ouverture de la boutique',
                after_close: 'Impossible de réserver un créneau après la fermeture de la boutique',

                end_before_start: 'L\'heure de fin doit être après l\'heure de début',
                too_short: 'La plage horaire doit être d\'au moins {min_time} minutes',
                too_long: 'La plage horaire doit être au maximum de {max_time} minutes',
                not_open_day: 'La boutique n\'est pas ouverte ce jour-là',
                not_open_time: 'La boutique n\'est pas ouverte à cette heure',

                unknown: 'Une erreur inconnue est survenue lors de la réservation de cette plage horaire.',
            },
            user: {
                not_found: 'Utilisateur non trouvé',
                email_not_same: 'Impossible de changer l\'email',
                cant_set_self_admin: 'Impossible de modifier votre propre statut d\'administrateur',
                already_exists: 'L\'utilisateur existe déjà',
                unknown: 'Une erreur inconnue est survenue lors de la récupération des données de l\'utilisateur.',
            },
            notification: {
                unknown: 'Une erreur inconnue est survenue lors de la récupération des notifications.',
                not_found: 'Notification introuvable',
                not_allowed: 'Accès non autorisé à cette notification',
            }
        },
        menu: {
            my_reservations: 'Mes futures réservations',
            create_reservation: 'Réserver un créneau',
            admin: {
                title: 'Admin',
                shops: 'Boutiques',
                users: 'Utilisateurs',
                reservations: 'Réservations',
                settings: 'Paramètres du serveur',
            },
        },
        notification: {
            delete: 'Supprimer',
            mark_as_read: 'Marquer comme lu',
            mark_as_unread: 'Marquer comme non lu',
            mark_all_as_read: 'Tout marquer comme lu',

            login: {
                title: "Nouvelle connexion",
                body: "Vous vous êtes connecté avec succès",
            },
            loading: {
                title: "Chargement",
                body: "Chargement des données ...",
                access: "Veuillez patienter"
            },
            test: {
                title: "Notification de test {test}",
                body: "Ceci est une notification de test",
                access: "Ouvrir le test",
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