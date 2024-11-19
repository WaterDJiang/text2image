#!/bin/bash
echo "Installing frontend dependencies..."
cd frontend
npm install
npm run build
cd .. 