"use strict";
exports.__esModule = true;
require("dotenv").config();
var fs = require("fs");
var AWS = require("aws-sdk");
var chokidar_1 = require("chokidar");

// Update these values with your own
var region = process.env.AWS_REGION;
var bucketName = process.env.S3_BUCKET_NAME;
var s3ObjectName = process.env.S3_FILE_PATH; // Name of the file in S3

// Create an S3 instance

var s3 = new AWS.S3();

// Directory to watch for changes
var directoryToWatch = process.env.DIRECTORY_TO_WATCH; // Replace with your directory path
var watcher = chokidar_1.watch(directoryToWatch, {
  ignored: /(^|[\/\\])\../,
  persistent: true,
});

console.log("Watching directory: ".concat(directoryToWatch));

// Upload function
var uploadFileToS3 = function (filePath) {
  fs.readFile(filePath, function (err, data) {
    if (err) {
      console.error("Error reading local file:", err);
      return;
    }
    // Upload the file to S3

    s3.putObject(
      {
        Bucket: bucketName,
        Key: s3ObjectName,
        Body: data,
      },
      function (uploadErr, uploadData) {
        if (uploadErr) {
          console.error("Error uploading to S3:", uploadErr);
          return;
        }
        console.log("File uploaded successfully:", uploadData);
      }
    );
  });
};
watcher
  .on("add", function (path) {
    console.log("File added: ".concat(path));
    uploadFileToS3(path);
  })
  .on("change", function (path) {
    console.log("File changed: ".concat(path));
    uploadFileToS3(path);
  })
  .on("unlink", function (path) {
    console.log("File removed: ".concat(path));
    // You can add your custom logic here for when a file is removed
  });
// Handle errors
watcher.on("error", function (error) {
  console.error("Error: ".concat(error));
});
// Handle the Ctrl+C event to gracefully exit
process.on("SIGINT", function () {
  console.log("Stopping the watcher...");
  watcher.close().then(function () {
    console.log("Watcher stopped.");
    process.exit(0);
  });
});
