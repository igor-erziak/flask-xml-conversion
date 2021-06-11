# Flask app for XML conversion

## What the app does?

The app provides one endpoint `/export` which accepts `annotation_id` as a parameter in path (e.g. `/export/6422949`). In order to access this endpoint the usere has to provide username and password (via BasicAuth).

If the user provides valid credentials (internally stored in ENV variables `APP_USERNAME` and `APP_PASSWORD`) and `annotation_id` the applcation internally logs in using another set of credentials (internally stored in ENV variables `ROSSUM_USERNAME` and `ROSSUM_PASSWORD`) into the Rossum Elis API (https://api.elis.rossum.ai/v1/) where it tries to retrieve annotation for a document with the specified id.

If such a document exists (currently only ids `6439416` and `6422949` exist) the XML representation of the annotation is downloaded and then converted into a different XML format.

The conversion is implemented using a `template.xml` file which specifies the structure of the output document. The values are obtained from the downloaded document where the location of the source value is defined by the `from` attribute in the `template.xml` file. For elements that contain a list of elements as their children, the attribute `item` is used to define the corresponding source elements.

Finally, the converted xml is submitted in base64-encoded form to the https://my-little-endpoint.ok/rossum endpoint along with the `annotation_id`. If the request is successful, the original endpoint (`/export/<annotation_id>`) returns `{ "success": true }`, otherwise it returns `{ "success": false }`.
