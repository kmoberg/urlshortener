import boto3
import os
import random
import time
from decimal import Decimal
from urllib.parse import urlparse

from botocore.exceptions import ClientError
from flask import Flask, render_template, request, flash, redirect, url_for
from hashids import Hashids

# Hello Flask
app = Flask(__name__)

# Set a secret key - this must be unique! Get it from the Environment Variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

hashids = Hashids(min_length=4, salt="ljsdflkjsdlktj4woi35uoi2345u4lo")

dynamodb = boto3.resource('dynamodb', endpoint_url=os.getenv('ENDPOINT_URL'))
table = dynamodb.Table('urls')


def get_hostname(url, uri_type='both'):
    """Get the host name from the url"""
    parsed_uri = urlparse(url)
    if uri_type == 'both':
        return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    elif uri_type == 'netloc_only':
        return '{uri.netloc}'.format(uri=parsed_uri)


@app.route('/', methods=('GET', 'POST'))
def index():

    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('A URL is required')
            return redirect((url_for('index')))

        # Verify that the string is lowercase!
        url = url.lower()

        # Some super simple spellchecking
        # First define a base URL
        httpString = "http://"
        wordlist = ["htp://", "ttp://", "http:/"]

        # Check for some super simple spelling mistakes
        if any(word in url for word in wordlist):
            url = url[6:]
            url = httpString + url

        # Check if no HTTP has been entered at all
        elif httpString not in url:
            url = httpString + url

        # Fallback to verify that it is correct
        else:
            url = get_hostname(url)

        # Generate and encode a random integer to be used that hashid can use to generate the short URL
        hashid = hashids.encode(random.randint(0, 1200) * random.randint(5000, 10000))
        short_url = request.host_url + hashid

        # When the URL was generated, rounded, because Pythons timestamp is silly and gives milliseconds too.
        timestamp = str(round(time.time()))

        # Insert it into the database
        response = table.put_item(
            Item={
                'short_url': hashid,
                'full_url': url,
                'clicks': 0,
                'created': timestamp
            }
        )

        # Debugging
        flash("Time: " + timestamp)
        flash("Request ID: " + str(response['ResponseMetadata']['RequestId']))
        flash("Short URL: " + short_url)

        return render_template('url/index.html', short_url=response)
    return render_template('url/index.html')


@app.route('/<url>')
def url_redirect(url):

    # Check if a URL is set
    if url:

        # Try catch block to check if the URL actually exist
        try:
            response = table.get_item(Key={
                'short_url': url
            })

            # Update the click counter for the URL using the built in atomic counter
            update_click = table.update_item(
                Key={
                    'short_url': url
                },
                UpdateExpression="set clicks = clicks + :val",
                ExpressionAttributeValues={
                    ':val': Decimal(1)
                },
                ReturnValues="UPDATED_NEW"
            )

            # Return and redirect the user
            return redirect(response['Item']['full_url'])

        # Check for errors spouted by AWS
        except ClientError as e:
            flash(e.response['Error']['Message'], "info")
            return redirect(url_for('index'))

        # If nothing is found - return the normal index page
        else:
            return redirect(url_for('index'))

    # Kinda useless, but even so.
    else:
        flash('This URL was not found')
        return redirect(url_for('index'))


@app.route('/stats')
def stats():

    # Run a scan on the full table
    response = table.scan()
    data = response['Items']

    # Since DynamoDB won't return items larger than 1KB, paginate the results
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    # Get the length of the list - how many URLs have been generated?
    items = len(data)

    return render_template('url/stats.html', urls=data, items=items, base_url=request.host_url)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

