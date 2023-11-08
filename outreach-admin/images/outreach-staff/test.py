from flask import Flask, Response
import csv
from io import StringIO

app = Flask(__name__)

# Sample data
log = [(1, 'John', 'Doe'), (2, 'Jane', 'Smith')]

@app.route('/download_csv')
def download_csv():
    def generate():
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=['ID', 'First Name', 'Last Name'])

        # Write the header once
        writer.writeheader()

        # Write each row including the header
        for row in log:
            # Repeat the header row for each data row
            writer.writerow({'ID': 'ID', 'First Name': 'First Name', 'Last Name': 'Last Name'})
            writer.writerow({'ID': row[0], 'First Name': row[1], 'Last Name': row[2]})

        output.seek(0)
        yield from output

    response = Response(generate(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    return response

if __name__ == '__main__':
    app.run()
