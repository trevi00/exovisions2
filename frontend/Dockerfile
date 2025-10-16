# Dockerfile for Expo + React Native Web Frontend
FROM node:18-alpine

WORKDIR /app

# Install expo-cli globally
RUN npm install -g expo-cli

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Set environment variable for web platform
ENV EXPO_DEVTOOLS_LISTEN_ADDRESS=0.0.0.0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# Start Expo web server
CMD ["npx", "expo", "start", "--web", "--port", "3000"]
