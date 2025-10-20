from flask import Flask, request, render_template, send_file
import pdfkit
import io

app = Flask(__name__)

options = {"disable-javascript": ""}


@app.route("/", methods=["GET"])
def index():
    default_html = "<html><h2>Hello PDF</h2><p>This is sample text that will be converted to PDF.</p></html>"
    return render_template("index.html", default_html=default_html)


@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    html_content = request.form.get("html_content", "")

    pdf = pdfkit.from_string(html_content, False)

    return send_file(
        io.BytesIO(pdf),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="generated.pdf",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
