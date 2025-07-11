# Stage 1: Build the React application
FROM node:20-alpine AS build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the application for production
# The VITE_API_BASE_URL will be an empty string, so API calls will be relative (e.g., /api/v1/agents)
# This is ideal for when Nginx proxies the requests.
RUN npm run build


# Stage 2: Serve the built application with Nginx
FROM nginx:1.25-alpine

# Copy the built files from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy our custom Nginx configuration file into the container
# This line is now active and essential
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]