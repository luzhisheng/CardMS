from application import app
import www


def main():
    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'], debug=app.config['SERVER_DEBUG'])


if __name__ == '__main__':
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()
