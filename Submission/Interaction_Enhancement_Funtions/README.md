# OE Frontend

This is the frontend React application for the OE project.

This project was bootstrapped with [Create React App](https://github.com/facebookincubator/create-react-app).

Information on how to perform common tasks can be found [here](https://github.com/facebookincubator/create-react-app/blob/master/packages/react-scripts/template/README.md).

## Table of Contents

- [Installation](#installation)
- [Running the application](#running-the-application)
- [Running tests](#running-tests)
- [Build and deploy](#build-and-deploy)
- [Architecture](#architecture)

## Installation

Necessary dependencies are included in package.json. Simply run `npm install` from the project's root directory to install the necessary dependencies.
- In production, run `npm install --production` to exclude dev dependencies.

## Running the application

After installing the necessary dependencies, simply run `npm start` to start the application on localhost:3000.

## Running tests

Tests can be run by running `npm test`. An overview of test coverage follows:

- App.js
  - smoke test (render)
  - functions (login/logout [to eventually move to helpers.js])
- Search.js
  - smoke test (render)
  - functions/events
- SearchForms (in /forms/search)
  - smoke test (render)
  - events

Tests that still need to be written include:
- Upload.js
- UploadForms (in /forms/upload)
- Navigation.js
- Dashboard.js

## Build and deploy

Simply run `npm run build` to generate a /build directory with an optimized version of the application.

Just serve this directory on a webserver and your application should be accessible.

## Architecture

The application's components interact as depicted in the following diagram.

Reference-style:
![Preliminary architecture of the frontend application][architecture]

[architecture]: PreliminaryArchitecture.PNG "Preliminary architecture diagram"
