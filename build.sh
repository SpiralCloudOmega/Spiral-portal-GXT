#!/bin/bash

# SPGX Build Script
# Builds the Spiral Portal GXT application

echo "Building Spiral Portal GXT (SPGX)..."

# Clean previous build
echo "Cleaning previous build..."
mvn clean

# Compile the GWT application
echo "Compiling GWT application..."
mvn compile gwt:compile

# Package the application
echo "Packaging application..."
mvn package

echo "Build completed! WAR file created in target/ directory"
echo "To run the application:"
echo "  mvn jetty:run"
echo "Then open http://localhost:8080/spiral-portal in your browser"