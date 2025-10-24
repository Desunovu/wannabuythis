import alembic.config


def run_migrations():
    alembic_args = [
        '--raiseerr',
        'upgrade',
        'head',
    ]

    alembic.config.main(argv=alembic_args)
