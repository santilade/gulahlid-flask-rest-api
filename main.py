from app.__init__ import create_app

app = create_app()

# Execute only if the file is been run not if it's imported:
if __name__ == '__main__':
    app.run(debug=True)
