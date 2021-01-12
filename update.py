import click


@click.command()
@click.option('--token', required=True,)
@click.option('--issue', required=True,)
def main(token, issue):

    # Testing GitHub actions (:
    print(f"The given GitHub Token is '{token}'")
    print(f"Issue defails: {issue}")


if __name__ == '__main__':
    main()
