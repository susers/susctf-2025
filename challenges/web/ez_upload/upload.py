#!/usr/bin/python3

import cgi
import cgitb

UPLOAD_DIR = "/usr/local/apache2/htdocs/static/"


def main():
    cgitb.enable()

    print("Content-Type: text/html")
    print()

    form = cgi.FieldStorage()

    if "file" in form:
        fileitem = form["file"]
        if fileitem.filename:
            filename = fileitem.filename
            filepath = UPLOAD_DIR + filename

            with open(filepath, "wb") as f:
                f.write(fileitem.file.read())
            print("<h1>Uploaded successfully!</h1>")
            print(
                f"<p>Access the content here: <a href='/static/{filename}'>{filepath}</a></p>"
            )
        else:
            print("""
<meta http-equiv="refresh" content="5; url=/" >
<h1>No file was uploaded</h1>
            """)
    else:
        raise ValueError("Invalid data")


if __name__ == "__main__":
    main()
