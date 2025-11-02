FROM node:18-alpine
WORKDIR /app

# Install runtime dependencies
COPY package.json ./
RUN npm install --production

# Copy app source
COPY . .

EXPOSE 3000
ENV NODE_ENV=production

# Use a non-root user for better security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup || true
USER appuser

CMD ["node", "server.js"]