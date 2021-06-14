# Flask app for XML conversion

## How it works

The app provides one endpoint `/export` which accepts `annotation_id` as a parameter in path (e.g. `/export/6422949`). In order to access this endpoint the user has to provide username and password (via BasicAuth).

If the user provides valid credentials (internally stored in ENV variables `APP_USERNAME` and `APP_PASSWORD`) and `annotation_id` the applcation internally logs in, using another set of credentials (internally stored in ENV variables `ROSSUM_USERNAME` and `ROSSUM_PASSWORD`), into the Rossum Elis API (https://api.elis.rossum.ai/v1/) where it tries to retrieve annotation for the document with the specified id.

If such a document exists (currently only ids `6439416` and `6422949` exist) the XML representation of the annotation is downloaded and then converted into a different XML format.

The conversion is implemented using a `template.xml` file which specifies the structure of the output document. The values are obtained from the downloaded document where the location of the source value is defined by the `from` attribute in the `template.xml` file. For elements that contain a list of elements as their children, the attribute `item` is used to define the corresponding source elements.

Finally, the converted xml is submitted in base64-encoded form to the https://my-little-endpoint.ok/rossum endpoint along with the `annotation_id`. If the request is successful, the original endpoint (`/export/<annotation_id>`) returns `{ "success": true }`, otherwise it returns `{ "success": false }`.

## How to run

1. Clone the repository.
```
git clone https://github.com/igor-erziak/flask-xml-conversion
cd flask-xml-conversion
```

2. Build the docker image
```
docker build --tag xml-conversion .
```

3. Run the image with port `5000` redirected to localhost.
```
docker run --publish 5000:5000 flask-xml-conversion
```

4. Access the application at http://127.0.0.1:5000/

## How to test

To run the provided test, (re)build the image to the test stage:

1. Build the docker image using the `--target test` option which will cause the container to execute `pytest` as the command (`CMD`) instead of running the flask app itself.
```
docker build -t xml-conversion-test --target test .
```

2. Run the tests
```
docker run xml-conversion-test
```